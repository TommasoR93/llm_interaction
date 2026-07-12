# Version 5 — Combine with your original structured output

from openai import OpenAI
# from pydantic import BaseModel, ValidationError
from dotenv import load_dotenv
# from pathlib import Path

load_dotenv()
client = OpenAI()

messages = [
        {
        "role":"developer",
        "content" : """
You are part of the AI assistant which summarizes text.
Below the application specific rules:
- Assume the users are beginenr
- Assume the users can prompt in different languages
- Answer with maximum 50 tokens
"""
        }
]

#First user message
messages.append(
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
)

response = client.responses.create(
    model="gpt-5.5",
    input=messages
)

assistant_answer = response.output_text

#save assistant to history
messages.append(
    {
        "role" : "assistant",
        "content": "assistant_answer"
    }
)
print(response.output_text)
print("Input tokens:", response.usage.input_tokens)
print("Output tokens:", response.usage.output_tokens)
print("Total tokens:", response.usage.total_tokens)

# Second user message
messages.append(
    {
        "role": "user",
        "content": "What river flows through the city?"
    }
)


response = client.responses.create(
    model="gpt-5.5",
    input=messages
)


assistant_answer = response.output_text


messages.append(
    {
        "role": "assistant",
        "content": assistant_answer
    }
)

print(response.output_text)
print("Input tokens:", response.usage.input_tokens)
print("Output tokens:", response.usage.output_tokens)
print("Total tokens:", response.usage.total_tokens)

#The model has context because you sent it again.

# Note:
# Your original code:
# response = client.responses.parse(
#     model="gpt-5.5",
#     instructions=instructions,
#     input=[...],
#     text_format=Json_test
# )
# becomes:
# messages = [
#     {
#         "role": "developer",
#         "content": instructions
#     },
#     {
#         "role": "user",
#         "content": "Tell me about Wroclaw"
#     }
# ]


# response = client.responses.parse(
#     model="gpt-5.5",
#     input=messages,
#     text_format=Json_test
# )


# result = response.output_parsed


# messages.append(
#     {
#         "role": "assistant",
#         "content": result.model_dump_json()
#     }
# )
# Now you have:

# conversation memory ✅
# structured output ✅
# token monitoring ✅
# trimming strategy ✅
# summarization strategy ✅
# Version 1
# ---------
# messages list
#         |
#         v
# send history


# Version 2
# ---------
# messages list
#         |
#         v
# measure token growth


# Version 3
# ---------
# messages list
#         |
#         v
# remove old messages


# Version 4
# ---------
# messages list
#         |
#         v
# summarize old messages


# Version 5
# ---------
# messages list
#         |
#         v
# structured responses + memory