from pytube import YouTube
import os, json
from api.openaiAPI import OpenaiAPIWrapper


class Topic:
    def __init__(self, video_path: str, topic_summary_path: str, summary_length: int, openaiAPI: OpenaiAPIWrapper=OpenaiAPIWrapper()):
        self.video_path = video_path
        self.topic_summary_path = topic_summary_path
        self.summary_length = summary_length
        self.openaiAPI = openaiAPI

    def create_topic_summary(self, transcript: str) -> str:
        params_summary = self.prepare_summary_request(transcription=transcript)
        print("[INFO] Generating video summary...")
        summary = self.openaiAPI.create_chat_completion(model=self.openaiAPI.model, messages=params_summary['messages'], max_tokens=self.summary_length)
        print("[INFO] Video summary generated.")
        with open(self.topic_summary_path, "w") as f:
            f.write(summary)
        return summary
        
    def create_topic_keywords(self, transcript: str, n_keywords: int=5) -> str:
        params_keywords = self.prepare_keyword_request(transcription=transcript)
        keywords = self.openaiAPI.create_chat_completion(model="gpt-3.5-turbo-0125", messages=params_keywords['messages'], response_format=params_keywords['response_format'], n_keywords=n_keywords)
        data = json.loads(keywords)
        keywords_list = data["keywords"]
        keywords_str = ", ".join(keywords_list)
        return keywords_list, keywords_str

    def handle_topic(self) -> tuple[str, list]:
        if os.path.exists(self.topic_summary_path):
            print("[INFO] A topic summary already exists, using it.")
            with open(self.topic_summary_path, "r") as f:
                topic_summary = f.read()
            return topic_summary, []
        else:
            audio_path = self.download_audio()
            print("[INFO] Creating audio transcription...")
            video_transcription = self.openaiAPI.create_audio_transcription(audio_file_path=audio_path)
            topic_summary = self.create_topic_summary(transcript=video_transcription)
            keywords_list, keywords_str = self.create_topic_keywords(transcript=video_transcription)
            return topic_summary + keywords_str, keywords_list 

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

    #     self.base64Frames = self.read_video()

    # def read_video(self) -> list:

    #     video = cv2.VideoCapture(self.video_path)
    #     base64Frames = []
    #     print("Reading video...")
    #     while video.isOpened():

    #         success, frame = video.read()
    #         if not success:
    #             break

    #         _, buffer = cv2.imencode(".jpg", frame)
    #         base64Frames.append(base64.b64encode(buffer).decode("utf-8"))

    #     video.release()
    #     print("Video read.")
    #     print(len(base64Frames), "frames read.")
    #     return base64Frames

    # def api_input(self):
    #     return [
    #         {
    #             "role": "user",
    #             "content": [
    #                 "Generate a description for this video",
    #                 *map(lambda x: {"image": x, "resize": 768}, self.base64Frames[0::50]),
    #             ],
    #         },
    #     ]




