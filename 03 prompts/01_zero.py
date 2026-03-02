# zero shot prompting

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# The client automatically configures itself using the .env variables!
client = OpenAI() 

SYSTEM_PROMPT='you should only ans the coding related questions. Do not answer anything else .' \
' your name is Alexa, if user ask something other than code just say sorry ! '

response = client.chat.completions.create(
    model="gpt-4.1-nano",
   messages=[
        {"role":"system","content": SYSTEM_PROMPT},
        {"role":"user" , "content":"hey there, tell me a joke "},
        {"role":"user" , "content":" write a python code to translate word hello to hindi"}

    ]
)

print(response.choices[0].message.content)