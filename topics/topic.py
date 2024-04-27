from IPython.display import display, Image, Audio

import cv2  # We're using OpenCV to read video, to install !pip install opencv-python
import base64, time, os, requests
from chat.message import Message


class Topic:
    def __init__(self, video_path: str):
        self.video_path = video_path
        self.base64Frames = self.read_video()



    def read_video(self) -> list:

        video = cv2.VideoCapture(self.video_path)
        base64Frames = []
        print("Reading video...")
        while video.isOpened():

            success, frame = video.read()
            if not success:
                break

            _, buffer = cv2.imencode(".jpg", frame)
            base64Frames.append(base64.b64encode(buffer).decode("utf-8"))

        video.release()
        print("Video read.")
        print(len(base64Frames), "frames read.")
        return base64Frames

    def api_input(self):
        message = [
            {
                "role": "user",
                "content": [
                    "Generate a description for this video",
                    *map(lambda x: {"image": x, "resize": 768}, self.base64Frames[0::50]),
                ],
            },
        ]
        return {
            "model": "gpt-4-vision-preview",
            "messages": message,
            "max_tokens": 200,
        }



