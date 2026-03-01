from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key="AIzaSyBCkv4Sv9Ev2fPo0ABzkS2EyrOsGuPClDU",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages=[
        {"role":"system","content":"you are an expert in Maths and only and only answer maths questions ."},
        {"role":"user" , "content":"hey there, who are you ? can you code a python program "},
        {"role":"user" , "content":"hey there, can you solve a + b whole square"}
    ]
)

print(response.choices[0].message.content)