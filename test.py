from openai import OpenAI

# curl https://api.openai.com/v1/chat/completions \
#   -H "Content-Type: application/json" \
#   -H "Authorization: Bearer" \
#   -d '{
#      "model": "gpt-3.5-turbo",
#      "messages": [{"role": "user", "content": "Say this is a test!"}],
#      "temperature": 0.7
#    }'

import os

import openai

# openai.api_key = os.getenv("keyhere")

# completion = openai.ChatCompletion.create



def chatBotRunner():

    messages = [
    {"role": "system", "content": "You are a kind helpful assistant."}, # type: ignore
    ]
    
    while True:
        message = input("User : ")
        if message:
            messages.append(
                {"role" : "user", "content" : message},
            )
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=messages
            )

        reply = chat.choices[0].message.content
        print(f"ChatGPT: {reply}")
        messages.append({"role": "assistant", "content": reply})


if __name__ == "__main__":

    chatBotRunner()
