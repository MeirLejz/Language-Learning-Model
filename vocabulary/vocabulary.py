from api.encoder import Encoder
from vocabulary.word import Word

class Vocabulary:
    def __init__(self, encoder: Encoder, words: list[Word]=[]):
        self.encoder = encoder
        self.words = words
        self.save("vocabulary.txt")

    def add_word(self, text: str, initial_bias: float=5.0) -> None:
        self.words.append(Word(text, initial_bias))
        with open("vocabulary.txt", "a") as f:
            f.write(text + ' : ' + str(initial_bias) + '\n')

    def save(self, path: str) -> None:
        with open(path, "w") as f:
            f.write(self.to_readable_format())

    def to_readable_format(self) -> list:
        return [(word.text + ' : ' + str(word.bias)) for word in self.words]

    def to_logit_bias_format(self) -> dict:
        return {str(word.encode()[0]): word.bias for word in self.words}   

