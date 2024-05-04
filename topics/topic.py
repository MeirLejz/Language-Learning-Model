from pytube import YouTube
import os, json
from api.openaiAPI import OpenaiAPIWrapper


class Topic:
    def __init__(self, 
                 video_path: str, 
                 topic_summary_path: str, 
                 summary_length: int, 
                 openaiAPI: OpenaiAPIWrapper=OpenaiAPIWrapper()):
        
        self.video_path = video_path
        self.topic_summary_path = topic_summary_path
        self.summary_length = summary_length
        self.openaiAPI = openaiAPI

    def create_topic_summary(self, transcript: str) -> str:
        
        print("[INFO] Generating video summary...")
        
        params_summary = self.prepare_summary_request(transcription=transcript)
        summary = self.openaiAPI.create_chat_completion(model=self.openaiAPI.model, messages=params_summary['messages'], max_tokens=self.summary_length)
        
        with open(self.topic_summary_path, "w") as f:
            f.write(summary)
        
        print("[INFO] Video summary generated.")
        return summary
        
    def create_topic_keywords(self, transcript: str, n_keywords: int=5) -> str:
        
        print("[INFO] Generating video keywords...")

        params_keywords = self.prepare_keyword_request(transcription=transcript, n_keywords=n_keywords)
        keywords = self.openaiAPI.create_chat_completion(model="gpt-3.5-turbo-0125", messages=params_keywords['messages'], response_format=params_keywords['response_format'])
        
        data = json.loads(keywords)
        keywords_list = data["keywords"]
        keywords_str = ", ".join(keywords_list)
        
        print("[INFO] Video keywords generated.")
        return keywords_list, keywords_str

    def handle_topic(self) -> tuple[str, str, list]:

        if os.path.exists(self.topic_summary_path):

            print("[INFO] A topic summary already exists, overwriting it.")

            with open(self.topic_summary_path, "w") as f:
                f.write("")
    
        audio_path = self.download_audio()
        
        print("[INFO] Creating audio transcription...")
        video_transcription = self.openaiAPI.create_audio_transcription(audio_file_path=audio_path)
        print("[INFO] Audio transcription created.")
        
        topic_summary = self.create_topic_summary(transcript=video_transcription)
        
        keywords_list, keywords_str = self.create_topic_keywords(transcript=video_transcription)
        
        return topic_summary, keywords_str, keywords_list 


    def download_audio(self, output_path: str="output", filename: str="audio.mp4") -> None:
        
        print("[INFO] Downloading audio...")
        
        yt = YouTube(self.video_path)
        audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
        audio_stream.download(output_path=output_path, filename=filename) 
        
        print("[INFO] Audio downloaded.")
        
        return os.path.join(output_path, filename) 
    

    def prepare_summary_request(self, transcription: str) -> dict:
        
        return {
            "messages": [
                {
                    "role": "user",
                    "content": "You are given a video transcript: " + transcription + ". Generate an abstractive summary of the video."
                }
            ]
        }
    
    def prepare_keyword_request(self, transcription: str, n_keywords: int) -> dict:
        
        return {
            "response_format": { "type": "json_object" },
            "messages": [
                {
                    "role": "user",
                    "content": "You are given a video transcript: " + transcription + ". Isolate " + str(n_keywords) + " keywords from the video transcript, keywords that represent the important words to remember from the video. Return a json object listing the keywords."
                }
            ]
        }