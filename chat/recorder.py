from chat.message import Message
import os

class Recorder:
    def __init__(self, file_path):
      self.file_path = file_path
      
    def save_message(self, message: Message):
        with open(self.file_path, mode='a') as file:
            file.write(str(message()) + '\n')
    
    def load_messages(self):
        messages = []
        with open(self.file_path, mode='r') as file:
            lines = file.readlines()
            lines = lines[-5:]
            for line in lines:
                message = line.strip()
                messages.append(message)
        return messages
