from vocabulary.word import Word
from file_manager.vocab_file_manag import VocabularyFileManager

from unidecode import unidecode

import numpy as np

class Vocabulary:

    def __init__(self, file_manager: VocabularyFileManager, reset: bool=False, initial_bias: int=5):
        
        self.file_manager = file_manager
        self.initial_bias = initial_bias
        self.words = []

        if reset:
            self.file_manager.reset_file()
        else:
            self.words = self.file_manager.load_object_list()

    def add_word(self, message_content: str) -> None:

        message_content_list = [word.strip("`!¡@#$%^&*()_+-=,./<>¿?;:[]|\"'") for word in message_content.split() if word.strip() not in "`!¡@#$%^&*()_+-=,./<>¿?;:[]|\"'"]

        if np.random.random() < 0.9:   
            text = max(message_content_list, key=len)
        else:
            text = np.random.choice(message_content_list)
 
        text = unidecode(text.lower().strip())

        if text not in [word.text for word in self.words] and text != "" and text not in "`!¡@#$%^&*()_+-=,./<>¿?;:[]|'":
            
            word = Word(text, self.initial_bias)
            self.words.append(word)
            self.file_manager.save_object(word)

    def add_words(self, words: list[str]) -> None:
        words = [word.strip("`!¡@#$%^&*()_+-=,./<>¿?;:[]|\"'") for word in words if word.strip() not in "`!¡@#$%^&*()_+-=,./<>¿?;:[]|\"'"]
        words = [unidecode(word.lower().strip()) for word in words]
        for word in words:
            if word not in [word.text for word in self.words] and word != "" and word not in "`!¡@#$%^&*()_+-=,./<>¿?;:[]|'":
                word = Word(word, self.initial_bias)
                self.words.append(word)
                self.file_manager.save_object(word)


    def to_readable_format(self) -> str:
        return '\n'.join([(word.text + ' : ' + str(word.bias)) for word in self.words])

    def __call__(self) -> dict:
        return {str(word.encode()[0]): word.bias for word in self.words}   

