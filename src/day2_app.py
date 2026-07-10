from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()
instructions_path = Path(__file__).resolve().parents[1] / "instructions" / "system_instruction.md"
log_path = Path(__file__).resolve().parents[1] / "log" / "day2_ex_log.txt"

with open(instructions_path, "r", encoding="utf-8") as f:
    instructions = f.read()

response = client.responses.create(
    model="gpt-5.5",
    instructions=instructions,
    input=[
        {
            "role" : "developer",
            "content": """
You are part of the QES application.

#Applcation specific rules:
-Assume the user is a beginner level unless indicated otherwise.
-Provide Pythoin examples unless requeted differently.
"""
        },
        {
            "role":"user",
            "content": "Explain decorators with an example and consume max 20 tokens in your response."
        }
    ]
)

with open(log_path, "w", encoding="utf-8") as f:
    f.write (response.output_text)
 




