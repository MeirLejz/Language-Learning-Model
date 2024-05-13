from chat.message import Message
from file_manager.file_manag import FileManager

import json

class ConversationFileManager(FileManager):

    def __init__(self, file_path: str):
        super().__init__(file_path)

    def save_object(self, message: Message) -> None:   
        """Save a message object to the file."""  
        with open(self.file_path, mode='a') as file:
            json.dump(message(), file) # message.__call__() returns a dictionary
            file.write('\n')
    
    def load_object_list(self, context_len: int = 5) -> list[dict]: 
        """Load only recent history from conversation file.
        Goal is to save tokens when calling API"""   
        messages = []
        
        with open(self.file_path, mode='r') as file:
            lines = file.readlines()
            last_lines = lines[-context_len:]
            for line in last_lines:
                messages.append(json.loads(line.strip("\n")))

        return messages
    
    def reset_file(self) -> list:
        with open(self.file_path, 'w') as f:
            f.write("")
        return []