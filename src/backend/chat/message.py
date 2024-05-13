from dataclasses import dataclass

@dataclass
class Message:
    role: str
    content: str

    def __str__(self):
        return f"{self.role}: {self.content}"

    def __call__(self):
        return {"role": self.role, "content": self.content}

    @classmethod
    def from_dict(cls, message_dict: dict):
        return cls(role=message_dict["role"], content=message_dict["content"])