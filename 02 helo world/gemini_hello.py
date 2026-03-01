from google import genai

client = genai.Client(
    api_key="AIzaSyBCkv4Sv9Ev2fPo0ABzkS2EyrOsGuPClDU"
)

response = client.models.generate_content(
    model="gemini-3-flash-preview", content="explain how ai work in few words"
)