from chat.recorder import Recorder
from chat.conversation import Conversation
from chat.message import Message
from api.openaiAPI import OpenaiAPIWrapper

# can have access to each word in answer through chunk.choices[0].delta.content, compare to existing vocabulary

def main():
    model = "gpt-3.5-turbo"
    max_tokens = 50
    stream = True
    # logit_bias={str(enc.encode("world")[0]): 5.0}

    recorder = Recorder('chat/messages.txt')
    conversation = Conversation(system_message_content="You are a bot", recorder=recorder)
    openAPI = OpenaiAPIWrapper(conversation=conversation, model=model)
    # openAPI.create_chat_completion(messages=messages, stream=stream, max_tokens=max_tokens)

    while True:
        user_input = input("You: ")
        user_message = Message(role="user", content=user_input)
        conversation.add_message(user_message)
        openAPI.create_chat_completion(messages=conversation.history, stream=stream, max_tokens=max_tokens)

        if user_input == "exit":
            break

if __name__ == "__main__":
    main()