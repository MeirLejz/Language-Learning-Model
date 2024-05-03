from file_manager.vocab_file_manag import VocabularyFileManager
from file_manager.conv_file_manag import ConversationFileManager

from chat.conversation import Conversation
from chat.message import Message

from topics.topic import Topic

from api.openaiAPI import OpenaiAPIWrapper

from vocabulary.vocabulary import Vocabulary

import argparse as ap, os, pdb, json

# TODO: implement video frames addition to audio transcription for improved topic summary

MAX_TOKENS = 50
MAX_TOKENS_DESCRIPTION = 200
VOCABULARY_PATH = "output/vocabulary.txt"
CONVERSATION_PATH = "output/messages.txt"
SYSTEM_PROMPT_PATH = "prompts/system_prompt.txt"
TOPIC_PROMPT_PATH = "prompts/topic_prompt.txt"
TOPIC_SUMMARY_PATH = "prompts/topic_summary.txt"


def main():
    
    parser = ap.ArgumentParser(description="Tsabar")
    parser.add_argument("-m", "--model", type=str, default="gpt-3.5-turbo")
    parser.add_argument("-r", "--reset", action="store_true")
    parser.add_argument("-t", "--topic", type=str, default=None)
    args = vars(parser.parse_args())

    system_prompt = open(SYSTEM_PROMPT_PATH, "r").read()
    topic_prompt = open(TOPIC_PROMPT_PATH, "r").read()
    
    openAPI = OpenaiAPIWrapper(model=args['model'])
    vocab_file_manager = VocabularyFileManager(file_path=VOCABULARY_PATH)
    conv_file_manager = ConversationFileManager(file_path=CONVERSATION_PATH)
    vocabulary = Vocabulary(file_manager=vocab_file_manager, reset=args['reset'])

    if args['topic'] is not None:
        
        print("[INFO] Topic provided.")
        topic = Topic(video_path=args['topic'], topic_summary_path=TOPIC_SUMMARY_PATH, summary_length=MAX_TOKENS_DESCRIPTION)
        topic_summary, keywords = topic.handle_topic()
        vocabulary.add_words(words=keywords)
        system_prompt += topic_prompt + topic_summary

    conversation = Conversation(system_message_content=system_prompt, 
                                file_manager=conv_file_manager, 
                                reset=args['reset'], 
                                max_history_length=5)

    while True:
        
        user_input = input("You: ")

        if user_input == "exit":
            break

        conversation.add_message(Message(role="user", content=user_input))
        
        message_content = openAPI.stream_chat_completion(model=args['model'], messages=conversation(), max_tokens=MAX_TOKENS, logit_bias=vocabulary())
        
        vocabulary.add_word(message_content)

        conversation.add_message(Message(role="assistant", content=message_content))
        
if __name__ == "__main__":
    main()