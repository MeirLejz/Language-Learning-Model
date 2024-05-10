from chat.message import Message
from file_manager.conv_file_manag import ConversationFileManager
from collections import deque

class Conversation:
    def __init__(self, system_message_content: str, file_manager: ConversationFileManager, reset: bool=False, max_history_length: int=5):
        
        self.system_message = Message(role="system",content=system_message_content)
        
        self.__max_history_length = max_history_length
        self.__file_manager = file_manager
        self.__messages = deque() # messages only
        
        messages = self.__file_manager.reset_file() if reset else self.__file_manager.load_object_list(context_len=self.__max_history_length)
        if messages != []:
            for message in messages:
                self.__messages.append(message)
    
    def add_message(self, message: Message) -> None:
        """Add a message object to the conversation history.

        Args:
            message (Message): Message object to be added to the conversation history.
        """
        self.__messages.append(message())
        if len(self.__messages) > self.__max_history_length:
            self.__messages.popleft()
        self.__file_manager.save_object(message)

    def __call__(self) -> list:
        res = self.__messages.copy()
        res.appendleft(self.system_message())
        return list(res)
        
    def __str__(self) -> str:
        return "\n".join([str(message) for message in self.__messages])