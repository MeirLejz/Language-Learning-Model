from openai import OpenAI
import tiktoken

from chat.conversation import Conversation
from chat.message import Message
from vocabulary.vocabulary import Vocabulary

import numpy as np
import pdb
class OpenaiAPIWrapper():
    
    def __init__(self, conversation: Conversation, vocabulary: Vocabulary, model: str="gpt-3.5-turbo"):
        self.client = OpenAI()
        self.model = model
        self.encoding = tiktoken.encoding_for_model(self.model)
        self.conversation = conversation
        self.vocabulary = vocabulary
        
    def create_chat_completion(self, messages: list, stream: bool=True, max_tokens: int=50, logit_bias: dict=None) -> Message:
        
        message_content = ""

        stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            stream=stream,
            logit_bias=logit_bias
        )
        
        print("tsabar: ", end="")

        for chunk in stream:
            token_content = chunk.choices[0].delta.content
            if token_content is not None:
                print(token_content, end="")
                message_content += token_content
            else:
                print("\n")

        words = [word.strip("`!¡@#$%^&*()_+-=,./<>¿?;:[]|\"'") for word in message_content.split() if word.strip() not in "`!¡@#$%^&*()_+-=,./<>¿?;:[]|\"'"]

        if np.random.random() < 0.9:   
            self.vocabulary.add_word(max(words, key=len))
        else:
            self.vocabulary.add_word(np.random.choice(words))

        message = Message(role="assistant", content=message_content)
        self.conversation.add_message(message)
        
        return message