from openai import OpenAI

class OpenaiAPIWrapper():
    
    def __init__(self):
        self.client = OpenAI()
        
    def create_audio_transcription(self, audio_file_path: str, model: str="whisper-1", response_format: str="text") -> str:
        
        with open(audio_file_path, "rb") as file:
            transcription = self.client.audio.transcriptions.create(
                model=model,
                file=file,
                response_format=response_format
            )
        
        return transcription
    
    def create_chat_completion(self, model: str, messages: list, max_tokens: int=200) -> str:
        
        completion = self.client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens
        )

        return completion.choices[0].message.content

    def stream_chat_completion(self, model: str, messages: list, max_tokens: int=50, logit_bias: dict=None) -> tuple[list, str]:
        
        message_content = ""

        stream = self.client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            stream=True,
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

        return message_content
        