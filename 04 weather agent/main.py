from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def main():
    user_query = input(">")

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role":"user","content":user_query}
        ],
        max_tokens=1000  # <-- Add this line to cap the response length
    )

    print(f"🤖 : {response.choices[0].message.content}")

main()