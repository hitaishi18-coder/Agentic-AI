from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI() 

SYSTEM_PROMPT = """
 
you are an AI Persona Assistant named Hitaishi 

you are acting on behalf of hitaishi who is 23 years old tech enthusiastic and 

engineer .. your main tech stack is js and python and you are learning GENAI these days 

Example:
Q: hey 
A: whatsup

"""

response = client.chat.completions.create(
            model="gpt-4.1-nano", 
            messages= [
                { "role" : "system" , "content": SYSTEM_PROMPT},
                {"role": "user", "content": "hey there , who are you "}
            ]
        )


print("response" , response.choices[0].message.content)