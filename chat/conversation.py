from chat.message import Message
from file_manager.conv_file_manag import ConversationFileManager
from collections import deque

class Conversation():
    def __init__(self, system_message_content: str, file_manager: ConversationFileManager, reset: bool=False, max_history_length: int=5):
        
        self.system_message = Message(role="system",content=system_message_content)
        
        self.max_history_length = max_history_length
        self.file_manager = file_manager
        self.messages = deque() # messages only
        
        if reset:
            self.file_manager.reset_file()
        else:
            messages = self.file_manager.load_object_list(context_len=self.max_history_length)
            for message in messages:
                self.messages.append(message)

    def __call__(self):
        res = self.messages.copy()
        res.appendleft(self.system_message())
        return list(res)
    
    def add_message(self, message: Message):
        self.messages.append(message())
        if len(self.messages) > self.max_history_length:
            self.messages.popleft()
        self.file_manager.save_object(message)

    def __str__(self):
        return "\n".join([str(message) for message in self.messages])