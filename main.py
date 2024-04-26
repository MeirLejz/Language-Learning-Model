from chat.recorder import Recorder
from chat.conversation import Conversation
from chat.message import Message

from api.openaiAPI import OpenaiAPIWrapper

from vocabulary.vocabulary import Vocabulary

import argparse as ap

import pdb
# can have access to each word in answer through chunk.choices[0].delta.content, compare to existing vocabulary

def main():
    
    # argparse
    parser = ap.ArgumentParser(description="Speakit")
    parser.add_argument("-m", "--model", type=str, default="gpt-3.5-turbo")
    parser.add_argument("-r", "--reset", action="store_true")
    args = vars(parser.parse_args())

    model = "gpt-3.5-turbo"
    max_tokens = 30
    stream = True
    vocabulary_path = "output/vocabulary.txt"
    recorder_path = "output/messages.txt"
    system_prompt_path = "system_prompt.txt"
    system_prompt = open(system_prompt_path, "r").read()
    vocabulary = Vocabulary(file_path=vocabulary_path, reset=args['reset'])
    recorder = Recorder(file_path=recorder_path)
    conversation = Conversation(system_message_content=system_prompt, recorder=recorder, reset=args['reset'])
    openAPI = OpenaiAPIWrapper(conversation=conversation, vocabulary=vocabulary, model=model)

    while True:
        
        user_input = input("You: ")
        user_message = Message(role="user", content=user_input)
        conversation.add_message(user_message)
        openAPI.create_chat_completion(messages=conversation.history, stream=stream, max_tokens=max_tokens, logit_bias=vocabulary.to_logit_bias_format())
        if user_input == "exit":
            break

if __name__ == "__main__":
    main()