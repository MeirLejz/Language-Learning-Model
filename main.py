from file_manager.vocab_file_manag import VocabularyFileManager
from file_manager.conv_file_manag import ConversationFileManager

from chat.conversation import Conversation
from chat.message import Message
from topics.topic import Topic

from api.openaiAPI import OpenaiAPIWrapper

from vocabulary.vocabulary import Vocabulary

import argparse as ap


def main():
    
    # argparse
    parser = ap.ArgumentParser(description="Speakit")
    parser.add_argument("-m", "--model", type=str, default="gpt-3.5-turbo")
    parser.add_argument("-r", "--reset", action="store_true")
    parser.add_argument("-t", "--topic", type=str, default=None)
    args = vars(parser.parse_args())

    chat_model = "gpt-3.5-turbo"
    topic_model = "gpt-4-vision-preview"

    vocabulary_path = "output/vocabulary.txt"
    recorder_path = "output/messages.txt"
    system_prompt_path = "prompts/system_prompt.txt"
    topic_prompt_path = "prompts/topic_prompt.txt"

    openAPI = OpenaiAPIWrapper()

    system_prompt = open(system_prompt_path, "r").read()

    if args['topic'] is not None:
        topic_prompt = open(topic_prompt_path, "r").read()
        topic = Topic(args['topic'])
        params = topic.api_input()
        description = openAPI.create_chat_completion(model=params["model"], messages=params["messages"], max_tokens=params["max_tokens"])
        system_prompt = system_prompt + description

    vocab_file_manager = VocabularyFileManager(file_path=vocabulary_path)
    conv_file_manager = ConversationFileManager(file_path=recorder_path)

    vocabulary = Vocabulary(file_manager=vocab_file_manager, 
                            reset=args['reset'])
    conversation = Conversation(system_message_content=system_prompt, 
                                file_manager=conv_file_manager, 
                                reset=args['reset'], 
                                max_history_length=5)


    while True:
        
        user_input = input("You: ")
        
        conversation.add_message(Message(role="user", content=user_input))
        
        message_content_list, message_content = openAPI.stream_chat_completion(messages=conversation.history, stream=stream, max_tokens=max_tokens, logit_bias=vocabulary.to_logit_bias_format())
        
        vocabulary.add_word(message_content_list)

        conversation.add_message(Message(role="assistant", content=message_content))
        
        if user_input == "exit":
            break

if __name__ == "__main__":
    main()