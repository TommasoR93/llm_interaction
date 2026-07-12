# Day 2 — Message Structure (Roles)
Understand system / user / assistant roles
Build 2 different system prompts
Test behavior differences
Log responses for comparison

Levels based on priorities are: System (instruction parameter is equivalent to that), developer, user, assistant (llm response)

#Identity -- purpose, communication style, goals
#Instructions -- guidance to the model how to generate the response you want
#Examples 
#Context

# Day 3 — Prompt Engineering Basics
Write clear instruction prompts
Add constraints (format, tone, length)
Build simple summarizer script
Test with 3 different inputs

There isn't a fixed list of constraints you must use. A useful way to think about constraints is by category:
| Category         | Example constraints                                                   |
| ---------------- | --------------------------------------------------------------------- |
| **Length**       | Under 100 words, exactly 5 bullets, 2 paragraphs, one sentence        |
| **Format**       | Markdown, JSON, table, numbered list                                  |
| **Tone**         | Neutral, professional, friendly, technical, persuasive                |
| **Audience**     | Explain for a beginner, executive summary, ELI5, senior engineer      |
| **Content**      | Mention only key facts, include dates, omit opinions, highlight risks |
| **Style**        | Active voice, simple language, no jargon, concise                     |
| **Language**     | English, Polish, British English, translate to Spanish                |
| **Restrictions** | Don't speculate, don't use emojis, don't quote directly               |

# Day 4 — Structured Output (JSON)
Force JSON output from model
Define fixed output structure
Test consistency across prompts
Save outputs to variables (not just print)
# Day 5 — Parsing & Validation
Parse JSON response in code
Add error handling (try/except)
Handle invalid outputs

Note:
If you're using Pydantic with Structured Outputs, then client.responses.parse() is the recommended method.
client.responses.create() if you use this when you want the model's raw output. You then have to parse the JSON yourself if you asked for JSON.
While client.responses.parse() Use this when you have a Pydantic model and want the SDK to:
send the schema to the model,
validate the response,
return a Pydantic object.
Then to convert a Pydantic object/model to JSON, use .model_dump_json() in Pydantic v2.
Then to convert a Pydantic object/model to Python dict, use .model_dump in Pydantic v2.
Also the LLM is deciding what content goes inside each field. Pydantic is not generating the values — it is only defining the structure and validating the output.