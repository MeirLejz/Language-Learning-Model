from openai import OpenAI

class OpenaiAPIWrapper():
    
    def __init__(self):
        self.client = OpenAI()
        
    def create_audio_transcription(self, 
                                   audio_file_path: str, 
                                   model: str="whisper-1", 
                                   response_format: str="text") -> str:
        """Encapsulation for audio transcription model (whisper) API call.

        Args:
            audio_file_path (str): path to audio file to be transcripted
            model (str, optional): Speech To Text (STT) model. Defaults to "whisper-1".
            response_format (str, optional): text or json. Defaults to "text".

        Returns:
            str: Transcription of the audio file
        """
        
        with open(audio_file_path, "rb") as file:
            transcription = self.client.audio.transcriptions.create(
                model=model,
                file=file,
                response_format=response_format
            )
        
        return transcription
    
    def create_chat_completion(self, 
                               model: str, 
                               messages: list, 
                               max_tokens: int=200, 
                               response_format: dict={ "type": "text" }) -> str:
        """Basic chat completion encapsulation without streaming. Made for outside conversation api calls.

        Args:
            model (str): chatGPT model
            messages (list): list of messages - recent history of the conversation
            max_tokens (int, optional): max nb of tokens for the output. Defaults to 200 for max nb of tokens of topic description.
            response_format (dict, optional): API response format, text or json. Defaults to { "type": "text" }.

        Returns:
            str: chat completion content
        """
        
        completion = self.client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            response_format=response_format
        )

        return completion.choices[0].message.content

    def stream_chat_completion(self, 
                               model: str, 
                               messages: list, 
                               max_tokens: int=50, 
                               logit_bias: dict=None) -> str:
        """Basic chat completion encapsulation with streaming. Made for conversation api calls

        Args:
            model (str): chatGPT model
            messages (list): list of messages - recent history of the conversation
            max_tokens (int, optional): Nb of tokens for the model's response. Defaults to 50.
            logit_bias (dict, optional): Probabilities for specific words (Words from Vocabulary). Defaults to None.

        Returns:
            str: full message content as a string
        """
        
        message_content = ""

        # API call
        stream = self.client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            stream=True,
            logit_bias=logit_bias
        )
        
        print("tsabar: ", end="")

        # streaming response
        for chunk in stream:
            token_content = chunk.choices[0].delta.content
            if token_content is not None:
                print(token_content, end="")
                message_content += token_content # create full message
            else:
                print("\n") # end message with new line

        return message_content
        