This small project aims to make the most of chatGPT capabilities as a conversation partner when learning a language.
The program takes as input a youtube video link, and you'll be able to have a conversation about the video.
The idea is that conversations for language learning are usually pretty boring and therefore not working although it is a great tool to practice a language.

The program handles the conversation like the OPENAI website, using only a recent history of the conversation as context for the model because pay is per token and because it would reach token number limit very fast.

Keywords from the youtube video as well as words from the conversation are saved in a "vocabulary" object and is then fed to the model as system prompt or as logit bias so that the model can help pratice specific words from the video and words used in the past in the conversation.
Key idea is that word repetion is a big part of the memorization process.  

Conversation and vocabulary can be reset using --reset flag.

Use case:

python main.py --topic https://www.youtube.com/watch?v=MikGVFFF5Rg&ab_channel=SpanishConversationswithOlgaandMiguel --reset