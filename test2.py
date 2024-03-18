# import statements
from openai import OpenAI
from dotenv import load_dotenv
import os

# load env reader from import
load_dotenv()

# load api key from env file and send it to client for the request
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# create a couple ai things for testing that are using gpt-3.5-turbo
completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)

# print the results
print(completion.choices[0].message)