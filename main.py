from file_manager.vocab_file_manag import VocabularyFileManager
from file_manager.conv_file_manag import ConversationFileManager

from chat.conversation import Conversation
from chat.message import Message

from topics.topic import Topic

from api.openaiAPI import OpenaiAPIWrapper

from vocabulary.vocabulary import Vocabulary

import argparse as ap

# TODO: implement video frames addition to audio transcription for improved topic summary

MAX_TOKENS = 50
MAX_TOKENS_DESCRIPTION = 200

# output paths
VOCABULARY_PATH = "output/vocabulary.txt"
CONVERSATION_PATH = "output/messages.txt"
TOPIC_SUMMARY_PATH = "output/topic_summary.txt"
AUDIO_PATH = "output/audio.mp4"

# prompts paths
SYSTEM_PROMPT_PATH = "prompts/system_prompt.txt"
TOPIC_PROMPT_PATH = "prompts/topic_prompt.txt"


def main():
    
    # parsing arguments
    parser = ap.ArgumentParser(description="Tsabar")
    parser.add_argument("-m", "--model", type=str, default="gpt-3.5-turbo")
    parser.add_argument("-r", "--reset", action="store_true")
    parser.add_argument("-t", "--topic", type=str, default=None)
    args = vars(parser.parse_args())

    # loading system prompts
    system_prompt = open(SYSTEM_PROMPT_PATH, "r").read()
    
    # objects construction
    openAPI = OpenaiAPIWrapper(model=args['model'])
    vocab_file_manager = VocabularyFileManager(file_path=VOCABULARY_PATH)
    conv_file_manager = ConversationFileManager(file_path=CONVERSATION_PATH)
    vocabulary = Vocabulary(file_manager=vocab_file_manager, reset=args['reset'])

    # handling topic
    if args['topic'] is not None:
        print("[INFO] Topic provided.")
            
        topic = Topic(video_path=args['topic'], topic_summary_path=TOPIC_SUMMARY_PATH, audio_path=AUDIO_PATH, summary_length=MAX_TOKENS_DESCRIPTION)
        
        # return topic summary (includes vocabulary from transcript) 
        # and keywords as list
        topic_summary, keywords_str, keywords_list = topic.handle_topic() 

        vocabulary.add_words(words=keywords_list)
        
        topic_prompt = open(TOPIC_PROMPT_PATH, "r").read() # load topic prompt
    
        system_prompt += '\n' + topic_prompt + '\n' + topic_summary + '\n' + 'Try to use in the conversation the following keywords from the video: ' + keywords_str

    print(f'[DEBUG] system_prompt: {system_prompt}')

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
        
        print('[DEBUG] conversation: ', str(conversation))
        print('[DEBUG] vocabulary: ', vocabulary.to_readable_format())

if __name__ == "__main__":
    main()