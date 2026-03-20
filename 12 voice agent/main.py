from dotenv import load_dotenv
from openai import OpenAI
import speech_recognition as sr 


load_dotenv()

client = OpenAI()

def main():
    r = sr.Recognizer()   # speech to text 
    with sr.Microphone() as source:   # mic access 
        r.adjust_for_ambient_noise(source)    # noise cancellation 
        r.pause_threshold = 2


        print("speak something...")
        audio = r.listen(source)


        print("processing audio ... STT")
        stt = r.recognize_google(audio)


        print("you said:- ", stt)


        SYSTEM_PROMPT = f"""
                You're an expert voice agent. You are given the transcript of what
                user has said using voice.
                You need to output as if you are an voice agent and whatever you speak
                will be converted back to audio using AI and played back to user.
            """

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role":"system","content": SYSTEM_PROMPT},
                {"role":"user" , "content" : stt}
            ]
        )

        print("ai response", response.choices[0].message.content)

main()