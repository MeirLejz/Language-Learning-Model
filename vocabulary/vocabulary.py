from vocabulary.word import Word
from file_manager.vocab_file_manag import VocabularyFileManager

from unidecode import unidecode
import numpy as np

class Vocabulary:

    def __init__(self, file_manager: VocabularyFileManager, reset: bool=False):
        self.file_manager = file_manager
        self.words = self.file_manager.reset_file() if reset else self.file_manager.load_object_list()
        self.__stripStr = "`!¡@#$%^&*()_+-=,./<>¿?;:[]|\"'"

    def add_word(self, message_content: str) -> None:
        """Add a word to the vocabulary from a message content.

        Args:
            message_content (str): A string containing a message.
        """
        message_content_list = message_content.split()
        message_content_list = self.__strip_message(message_content_list)

        text = max(message_content_list, key=len) if np.random.random() < 0.9 else np.random.choice(message_content_list)
 
        text = self.__normalize_text(text)
        self.__create_word(text)

    def add_words(self, words: list[str]) -> None:
        """Add a list of words to the vocabulary.

        Args:
            words (list[str]): A list of words usually extracted from a conversation topic.
        """
        words = self.__strip_message(words) 
        texts = [self.__normalize_text(text) for text in words]
        for text in texts:
            self.__create_word(text)

    def __create_word(self, text: str) -> None:
        """Private method to create a word object and add it to the vocabulary.

        Args:
            text (str): The text part of the word object.
        """
        if text not in [word.text for word in self.words] and text != "" and text not in self.__stripStr:
            word = Word(text)
            self.words.append(word)
            self.file_manager.save_object(word)

    @staticmethod
    def __normalize_text(text: str) -> str:
        return unidecode(text.lower().strip())
    
    def __strip_message(self, word_list: list[str]) -> list[str]:
        return [word.strip(self.__stripStr) for word in word_list if word.strip() not in self.__stripStr]

    def __str__(self) -> str:
        return '\n'.join([(word.text + ' : ' + str(word.bias)) for word in self.words])

    def __call__(self) -> dict:
        return {str(word.encode()[0]): word.bias for word in self.words}   

