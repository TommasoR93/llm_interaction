from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
from pydantic import BaseModel, ValidationError

load_dotenv()
client = OpenAI()

system_instruction = Path(__file__).resolve().parents[1] / "instructions" / "mini_proj_assistant.md"
log_response = Path(__file__).resolve().parents[1] / "log" / "mini_proj_log.json"

class Summary(BaseModel):
    city: str
    season: str
    history: str
    food: str
    sport: str

class AssistantResponse(BaseModel):
    reply: str
    summary : str

messages = [
        {
            "role": "developer",
            "content": """
    You are part of the AI assistant which summarizes test.
    You can receive user prompt in different langauges.
    Answer with maximum 50 tokens.
    """
        }
]

messages.append(
        {
            "role": "user",
            "content": """
        Summarize the text below by organizing the information into categories:
    Seville is a vibrant city located in the south of Spain. The summers are extremely hot, with temperatures often reaching 38–42°C,
    while winters are generally mild, with temperatures between 8 and 16°C.
    The city is well known for its impressive landmarks, including the Seville Cathedral, the Royal Alcázar, and Plaza de España.
    Visitors also enjoy walking through the historic Santa Cruz district.
    Seville is famous for its traditional cuisine, where people can try dishes such as gazpacho, salmorejo,
    and tapas in countless local restaurants. In addition to its rich culture, flamenco music and dance play an important role in
    the city's identity. Football is the most popular sport, and the city is home to two well-known clubs that have a strong rivalry.
    """
        }
)

try: 
    with open(system_instruction, "r", encoding="utf-8") as f:
        system_prompt = f.read()

    response = client.responses.parse(
        model="gpt-5.5",
        instructions=system_prompt,
        input=messages,
        text_format=AssistantResponse
    )

    result = response.output_parsed

    if result is None:
        print("Invalid result from the LLM")
        
except Exception as e:
    print(f"Exception error: {e}")

# Building context

messages.append(
    {
    "role" : "assistant",
    "content" : result.reply
    }
)



