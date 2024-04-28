from file_manager.vocab_file_manag import VocabularyFileManager
from file_manager.conv_file_manag import ConversationFileManager

from chat.conversation import Conversation
from chat.message import Message

from topics.topic import Topic

from api.openaiAPI import OpenaiAPIWrapper

from vocabulary.vocabulary import Vocabulary

import argparse as ap
import os

# TODO: implement text to keywords model to add vocabulary from topic summary
# TODO: implement video frames addition to audio transcription for improved topic summary

MAX_TOKENS = 50
MAX_TOKENS_DESCRIPTION = 200
VOCABULARY_PATH = "output/vocabulary.txt"
CONVERSATION_PATH = "output/messages.txt"
SYSTEM_PROMPT_PATH = "prompts/system_prompt.txt"
TOPIC_PROMPT_PATH = "prompts/topic_prompt.txt"
TOPIC_SUMMARY_PATH = "prompts/topic_summary.txt"


def main():
    
    parser = ap.ArgumentParser(description="Speakit")
    parser.add_argument("-m", "--model", type=str, default="gpt-3.5-turbo")
    parser.add_argument("-r", "--reset", action="store_true")
    parser.add_argument("-t", "--topic", type=str, default=None)
    args = vars(parser.parse_args())

    openAPI = OpenaiAPIWrapper()
    vocab_file_manager = VocabularyFileManager(file_path=VOCABULARY_PATH)
    conv_file_manager = ConversationFileManager(file_path=CONVERSATION_PATH)
    vocabulary = Vocabulary(file_manager=vocab_file_manager, 
                            reset=args['reset'])
    
    system_prompt = open(SYSTEM_PROMPT_PATH, "r").read()

    if args['topic'] is not None:
        if os.path.exists(TOPIC_SUMMARY_PATH):
            print("[INFO] Topic summary already exists.")
            with open(TOPIC_SUMMARY_PATH, "r") as f:
                summary = f.read()
        else:
            topic_prompt = open(TOPIC_PROMPT_PATH, "r").read()
            topic = Topic(args['topic'])
            audio_path = topic.download_audio()
            print("[INFO] Creating audio transcription...")
            video_transcription = openAPI.create_audio_transcription(audio_file_path=audio_path)
            params = topic.prepare_summary_request(transcription=video_transcription)
            print("[INFO] Generating video summary...")
            summary = openAPI.create_chat_completion(model=args['model'], messages=params['messages'], max_tokens=MAX_TOKENS_DESCRIPTION)
            print("[INFO] Video summary generated.")
            with open(TOPIC_SUMMARY_PATH, "w") as f:
                f.write(summary)
        
        system_prompt += topic_prompt + summary
        print(f'System prompt: {system_prompt}')
        vocabulary.add_word(message_content=summary)

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