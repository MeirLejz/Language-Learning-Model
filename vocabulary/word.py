from api.encoder import Encoder

class Word:
    def __init__(self, text: str, logit_bias: float = 5.0, encoder: Encoder = Encoder()):
        self.text = text
        self.bias = logit_bias
        self.encoder = encoder

    def encode(self):
        return self.encoder.encode(self.text)
    
    def decode(self, text: str):
        return self.encoder.decode(text)
