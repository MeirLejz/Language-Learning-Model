from vocabulary.word import Word
from unidecode import unidecode
import pdb

class Vocabulary:
    def __init__(self, file_path: str, reset: bool):
        
        self.vocabulary_path = file_path
        
        self.words = []
        with open(self.vocabulary_path, "w" if reset else "r") as f:
            if reset:
                f.write("")
            else:
                for line in f:
                    if line != "\n":
                        word, bias = line.split(":")
                        self.words.append(Word(text=word.strip(), logit_bias=int(bias)))

    def add_word(self, text: str, initial_bias: int=5) -> None:
        
        text = unidecode(text.lower().strip())

        if text not in [word.text for word in self.words] and text != "" and text not in "`!¡@#$%^&*()_+-=,./<>¿?;:[]|'":
            
            self.words.append(Word(text, initial_bias))

            with open(self.vocabulary_path, "a") as f:
                f.write("\n")
                f.write(text + ' : ' + str(initial_bias))

    def to_readable_format(self) -> str:
        return '\n'.join([(word.text + ' : ' + str(word.bias)) for word in self.words])

    def to_logit_bias_format(self) -> dict:
        return {str(word.encode()[0]): word.bias for word in self.words}   

