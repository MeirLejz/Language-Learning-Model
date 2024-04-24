from chat.encoder import Encoder
from chat.word import Word

class Vocabulary:
    def __init__(self, encoder: Encoder, words: list[Word]=[]):
        self.encoder = encoder
        self.words = words

    def add_word(self, word: Word) -> None:
        self.words.append(word)

    def to_logit_bias_format(self) -> dict:
        return {str(word.encode()[0]): word.bias for word in self.words}   

