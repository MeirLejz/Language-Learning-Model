from abc import ABC, abstractmethod
import os

class FileManager(ABC):

    def __init__(self, file_path: str):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            with open(file_path, 'w') as f:
                f.write('')

    @abstractmethod
    def save_object(self, obj) -> None:
        pass

    @abstractmethod
    def load_object_list(self) -> list:
        pass
    
    @abstractmethod
    def reset_file(self) -> None:
        pass

        
