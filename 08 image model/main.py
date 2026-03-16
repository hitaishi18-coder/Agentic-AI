from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

response = client.chat.completions.create(
    model="meta-llama/llama-3.2-11b-vision-instruct",
    max_tokens=80,
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Generate a caption for this image"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://images.pexels.com/photos/18105/pexels-photo.jpg"
                    }
                }
            ]
        }
    ]
)

print(response.choices[0].message.content)