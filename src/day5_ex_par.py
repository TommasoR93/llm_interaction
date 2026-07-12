from openai import OpenAI
from pydantic import BaseModel, ValidationError
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
client = OpenAI()

instruction_path = Path(__file__).resolve().parents[1] / "instructions" / "system_instruction_day3.md"
log_path = Path(__file__).resolve().parents[1] / "log" / "day5_ex_log.txt"

class Json_test(BaseModel):
    city: str
    history: str
    weather: str
    places: str
    university: str
    night_life: str

try:
    with open(instruction_path, "r", encoding  = "utf-8") as f:
        instructions = f.read()

    response = client.responses.parse(
    model="gpt-5.5",
    instructions=instructions,
    input = [
        {
        "role":"developer",
        "content" : """
You are part of the AI assistant which summarizes text.
Below the application specific rules:
- Assume the users are beginenr
- Assume the users can prompt in different languages
- Answer with maximum 50 tokens
"""
        },
        {
        "role":"user",
        "content" : """
Summarize the article below about Wroclaw in Poland:
Wroclaw is an old city located in the south west of Poland. It has been part over the centuries of Poland, Germany, Hungary and now, since almost 80 years, again in Poland.
It is a beautiful city with cold winters and warm summer. It has multiple places to visit like Rynek in the old city, Hala Stulecia, Sky Tower despite the city has been destroyes during the second world war.
There are multiple universities in place and most important one is the technology one which is attracting multiple young students for all oevr the world, and that's why the city is international and you can see the vibe.
In the city there is a rievr called Odra which is enabling beautiful spots in which the city has organized beach bars where you can take a drink with a good atmosphere.
Example summary text:
- Wroclaw is a beautiful polish city
- Cold winters and hot summers
- Many places to visit
- International given students from all around the world
- To do is to take a drink in a beach bar near Odra
"""
        }
    ],
    text_format=Json_test
)

    result = response.output_parsed
    if result is None:
        print("Invalid result from the LLM")
    
    json_output = result.model_dump_json(indent=2)
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(json_output)
    
    print("Success")

except ValidationError as e:
    print("Validation schema error from Pydantic")\

except ValueError as e:
    print("Not a proper value returned")

except Exception as e:
    print("Unexpected error returned")

