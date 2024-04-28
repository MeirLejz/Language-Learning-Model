from pytube import YouTube
import os

class Topic:
    def __init__(self, video_path: str):
        self.video_path = video_path

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




