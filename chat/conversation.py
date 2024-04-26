from chat.message import Message
from chat.recorder import Recorder
from collections import deque

class Conversation():
    def __init__(self, system_message_content: str, recorder: Recorder, reset: bool=False, max_history_length: int=5):
        
        self.system_message = Message(role="system",content=system_message_content)
        
        self.max_history_length = max_history_length
        self.recorder = recorder
        if reset:
            self.history = [self.system_message()]
        else:
            self.history = self.recorder.load_messages()
            history = deque(self.history)
            history.appendleft(self.system_message())
            self.history = list(history)

    def add_message(self, message: Message):
        self.history.append(message())
        self.recorder.save_message(message)
        if len(self.history) > self.max_history_length:
            self.history.pop(1)

    def __str__(self):
        return "\n".join([str(message) for message in self.history])