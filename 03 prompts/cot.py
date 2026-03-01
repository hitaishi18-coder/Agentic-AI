# chain of thought ---------- MANUAL


from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

# The client automatically configures itself using the .env variables!
client = OpenAI() 


SYSTEM_PROMOT="""

you are an expert AI Assistant in resolving user queries using chain of thought. 

you work on START, PLAN and OUTPUT steps 

you need to first PLAN what needs to be done . The PLAN can be multiple steps.

once you think enough PLAN has been done , finally you can give the OUTPUT

Rules :
- strictly follow the given JSON output format 
- only run one step at a time 
- the sequence of step is START (where user gives an input), PLAN(that can be multiple 
   times ) and finally the OUTPUT (which is going to be displayed to the user )

Output JSON Format :
{"step":"START" | "PLAN" | "OUTPUT" , "Content" : "string" }


Example :
START : can you solve 2 + 3 * 5 / 10
PLAN : {"step" : "PLAN":"content": " seems like user is interested in maths problem" }
PLAN : {"step" : "PLAN":"content": " looking at the problem , we should solve this using BODMAS method "}
PLAN : {"step" : "PLAN":"content": " yes , the BODMAS is correct thing to be done here" }
PLAN : {"step" : "PLAN":"content": " first, we must multiply 3 * 5 which is 15 " }
PLAN : {"step" : "PLAN":"content": " no the new equation is 2 + 15 /10 " }
PLAN : {"step" : "PLAN":"content": " we must perform divide that is 15/10 = 1.5 "}
PLAN : {"step" : "PLAN":"content": " now the equation is 2 + 1.5 " }
PLAN : {"step" : "PLAN":"content": " now finally lets perform the add" }
PLAN : {"step" : "PLAN":"content": " great, we have finally solved and left with the answer as 3.5"}
OUTPUT : {"step": "OUTPUT": " content" : "3.5" }

"""


response = client.chat.completions.create(
    model="gpt-4.1-nano",
    response_format={"type":"json_object"},
   messages=[
        {"role":"system","content": SYSTEM_PROMOT},
        # {"role":"user" , "content":"hey there, can you explain a + b whole square "},
        {"role":"user" , "content":"hey there, can you write a code to add a n numbers in js "},

        # manually keep adding messages to the history 
        {"role":"assistant","content": json.dumps(
            {"step":"START","Content":"The user wants a JavaScript code to add 'n' numbers."}
        )},

        {"role":"assistant","content": json.dumps(
           {"step": "PLAN", "Content": "I should create a JavaScript function that takes an array of numbers as input and returns their sum. This is a common way to add 'n' numbers."}
        )},

        {"role":"assistant","content": json.dumps(
            {"step": "PLAN", "Content": "The function can be named 'sumNumbers' and it will accept one parameter, an array of numbers. I will use the reduce() method in JavaScript to sum all elements of the array."}
        )},

        {"role":"assistant","content": json.dumps(
            {"step": "PLAN", "Content": "Here's what the code will look like: a function called 'sumNumbers' that takes an array 'nums' and returns the sum using 'nums.reduce()'."}
        )},
        
    ]
)

print(response.choices[0].message.content)