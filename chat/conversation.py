from chat.message import Message
from chat.recorder import Recorder

class Conversation():
    def __init__(self, system_message_content: str, recorder: Recorder, max_history_length: int=5):
        
        self.system_message = Message(role="system",content=system_message_content)
        self.history = [self.system_message()]
        self.max_history_length = max_history_length
        self.recorder = recorder

    def add_message(self, message: Message):
        self.history.append(message())
        self.recorder.save_message(message)
        if len(self.history) > self.max_history_length:
            self.history.pop(1)

    def __str__(self):
        return "\n".join([str(message) for message in self.history])