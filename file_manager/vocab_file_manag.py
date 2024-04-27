from vocabulary.word import Word
from file_manager.file_manag import FileManager

class VocabularyFileManager(FileManager):

    def __init__(self, file_path: str):
        super().__init__(file_path)

    def save_object(self, word: Word) -> None:
        with open(self.file_path, mode='a') as file:
            file.write("\n")
            file.write(word.text + ' : ' + str(word.bias))

    def load_object_list(self) -> list[Word]:
        words = []
        with open(self.file_path, "r") as f:
            for line in f:
                if line != "\n":
                    word, bias = line.split(":")
                    words.append(Word(text=word.strip(), logit_bias=int(bias)))
        return words
    
    def reset_file(self) -> None:
        with open(self.file_path, "w") as f:
            f.write("")