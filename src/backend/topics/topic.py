from pytube import YouTube
import os, json
from api.openaiAPI import OpenaiAPIWrapper


class Topic:
    def __init__(self, 
                 video_path: str, 
                 topic_summary_path: str, 
                 audio_path: str,
                 summary_length: int, 
                 openaiAPI: OpenaiAPIWrapper=OpenaiAPIWrapper()):
        
        self.video_path = video_path
        self.topic_summary_path = topic_summary_path
        self.audio_path = audio_path
        self.summary_length = summary_length
        self.__openaiAPI = openaiAPI

    def handle_topic(self) -> tuple[str, str, list]:
        """Handle topic by downloading audio, creating audio transcription, generating video summary and keywords for vocabulary.

        Returns:
            tuple[str, str, list]: topic summary, keywords as a string and as a list of words
        """

        # 1. reset topic summary and audio file if they exist
        if os.path.exists(self.topic_summary_path):
            print("[INFO] A topic summary already exists, overwriting it.")
            with open(self.topic_summary_path, "w") as f:
                f.write("")

        if os.path.exists(self.audio_path):
            print("[INFO] An audio file already exists, deleting it.")
            os.remove(self.audio_path)
    
        # 2. download audio
        print("[INFO] Downloading audio...")
        self.__download_audio()
        print("[INFO] Audio downloaded.")
        
        # 3. create audio transcription
        print("[INFO] Creating audio transcription...")
        video_transcription = self.__openaiAPI.create_audio_transcription(audio_file_path=self.audio_path)
        print("[INFO] Audio transcription created.")
        
        # 4. create topic summary
        print("[INFO] Generating video summary...")
        topic_summary = self.__create_topic_summary(transcript=video_transcription)
        print("[INFO] Video summary generated.")

        # 5. create topic keywords
        print("[INFO] Generating video keywords...")
        keywords_list, keywords_str = self.__create_topic_keywords(transcript=video_transcription)
        print("[INFO] Video keywords generated.")

        return topic_summary, keywords_str, keywords_list 


    def __download_audio(self, output_path: str="output", filename: str="audio.mp4") -> None:
        yt = YouTube(self.video_path)
        audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
        audio_stream.download(output_path=output_path, filename=filename) 

    def __create_topic_summary(self, transcript: str) -> str:
        params_summary = self.__prepare_summary_request(transcription=transcript)
        summary = self.__openaiAPI.create_chat_completion(model="gpt-3.5-turbo", messages=params_summary['messages'], max_tokens=self.summary_length)
        with open(self.topic_summary_path, "w") as f:
            f.write(summary)  
        return summary
        
    def __create_topic_keywords(self, transcript: str, n_keywords: int=5) -> tuple[list[str], str]:
        params_keywords = self.__prepare_keyword_request(transcription=transcript, n_keywords=n_keywords)
        keywords = self.__openaiAPI.create_chat_completion(model="gpt-3.5-turbo-0125", messages=params_keywords['messages'], response_format=params_keywords['response_format'])
        
        data = json.loads(keywords)
        keywords_list = data["keywords"]
        keywords_str = ", ".join(keywords_list)
        
        return keywords_list, keywords_str    

    def __prepare_summary_request(self, transcription: str) -> dict:
        return {
            "messages": [
                {
                    "role": "user",
                    "content": "You are given a video transcript: " + transcription + ". Generate an abstractive summary of the video."
                }
            ]
        }
    
    def __prepare_keyword_request(self, transcription: str, n_keywords: int) -> dict:
        return {
            "response_format": { "type": "json_object" },
            "messages": [
                {
                    "role": "user",
                    "content": "You are given a video transcript: " + transcription + ". Isolate " + str(n_keywords) + " keywords from the video transcript, keywords that represent the important words to remember from the video. Return a json object listing the keywords. The json object is of the form {\"keywords\": [\"keyword1\", \"keyword2\", ...]}"
                }
            ]
        }