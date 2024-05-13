from api.encoder import Encoder
from dataclasses import dataclass

@dataclass
class Word:
    text: str
    bias: float = 5.0
    encoder: Encoder = Encoder()

    def encode(self):
        return self.encoder.encode(self.text)
    
    def decode(self, text: str):
        return self.encoder.decode(text)