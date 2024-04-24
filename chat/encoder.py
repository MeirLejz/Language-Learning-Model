import tiktoken

class Encoder:
    def __init__(self, model: str="gpt-3.5-turbo"):
        self.model = model
        self.encoding = tiktoken.encoding_for_model(self.model)

    def encode(self, text: str):
        return self.encoding.encode(text)

    def decode(self, text: str):
        return self.encoding.decode(text)