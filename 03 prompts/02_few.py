# few shot prompting

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# The client automatically configures itself using the .env variables!
client = OpenAI() 

SYSTEM_PROMPT="""you should only ans the coding related questions. Do not answer anything else .' 
' your name is Alexa, if user ask something other than code just say sorry ! '

Rule:
- strictly follow the response in JSON Format

Output format:
{{
  "code" : "string" or Null,
  "isCodingQuestion" : boolean
}}


Example:
Q: can you explain a+b whole square ?
A: sorry , i can answer only coding related questions .

Q: can you explain a+b whole square ?
A: {{"code" : null, "isCodingQuestion": false }}


Q: write a code in python for adding two numbers 
A: def add(a,b):
    return a + b 


Q: write a code in python for adding two numbers 
A:  {{"code" : def add(a,b):
    return a + b  , "isCodingQuestion": false }}

"""

response = client.chat.completions.create(
    model="gpt-4.1-nano",
   messages=[
        {"role":"system","content": SYSTEM_PROMPT},
        # {"role":"user" , "content":"hey there, can you explain a + b whole square "},
        {"role":"user" , "content":"hey there, can you write a code to add a n numbers in js "},
        # {"role":"user" , "content":"hey there, tell me a joke "},
        # {"role":"user" , "content":" write a python code to translate word hello to hindi"}


    ]
)

print(response.choices[0].message.content)