from chat.message import Message
import os

class Recorder:
  def __init__(self, file_path):
    self.file_path = file_path
    # Check if the file already exists
    if os.path.exists(file_path):
        # If it exists, overwrite the file
        with open(file_path, mode='w'):
            pass

  def save_message(self, message: Message):
    with open(self.file_path, mode='a') as file:
      file.write(str(message()) + '\n')

  def load_messages(self):
    messages = []
    with open(self.file_path, mode='r') as file:
      for line in file:
        message = line.strip()
        messages.append(message)
    return messages
