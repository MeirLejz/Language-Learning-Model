from openai import OpenAI
import tiktoken

from chat.conversation import Conversation
from chat.message import Message
from vocabulary.vocabulary import Vocabulary

class OpenaiAPIWrapper():
    
    def __init__(self, conversation: Conversation, vocabulary: Vocabulary, model: str="gpt-3.5-turbo"):
        self.client = OpenAI()
        self.model = model
        self.encoding = tiktoken.encoding_for_model(self.model)
        self.conversation = conversation
        self.vocabulary = vocabulary
        
    def create_chat_completion(self, messages: list, stream: bool=True, max_tokens: int=50, logit_bias: dict=None) -> Message:
        
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            stream=stream,
            logit_bias=logit_bias
        )
        
        content = ""
        print("tsabar: ", end="")
        for chunk in stream:
            token = chunk.choices[0].delta.content
            if token is not None:
                print(token, end="")
                content += token
                self.vocabulary.add_word(content)
            else:
                print("\n")

        message = Message(role="assistant", content=content)
        self.conversation.add_message(message)
        
        return message