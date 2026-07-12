from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
client = OpenAI()

instruction_path = Path(__file__).resolve().parents[1] / "instructions" / "system_instruction_day3.md"
log_path = Path(__file__).resolve().parents[1] / "log" / "day3_ex_log.txt"

with open(instruction_path, "r", encoding  = "utf-8") as f:
    instructions = f.read()

response = client.responses.create(
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
    ]
)

with open(log_path, "w", encoding  = "utf-8") as f:
    f.write(response.output_text)




