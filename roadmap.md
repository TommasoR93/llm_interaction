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

# Day 5 — Parsing & Validation
Parse JSON response in code
Add error handling (try/except)
Handle invalid outputs

Note The best practice is to use the SDK exceptions as your primary error-handling mechanism, not manually check HTTP status codes.

from openai import (
    APIError,
    AuthenticationError,
    RateLimitError,
    BadRequestError,
    APITimeoutError,
)

except AuthenticationError:
    # API key problem (401)
    print("Check your API key")

except RateLimitError:
    # Too many requests (429)
    print("Slow down or retry later")

except BadRequestError:
    # Invalid request (400)
    print("Fix the request parameters")

except APITimeoutError:
    # Network timeout
    print("Request timed out")

except APIError as e:
    # Catch-all OpenAI API errors
    print(f"OpenAI API error: {e}")

In general:
2. You can handle different errors differently

A production application usually treats errors differently:

Error	            Action
AuthenticationError	Stop, fix configuration
BadRequestError	    Log and fix code/input
RateLimitError	    Retry with backoff
APITimeoutError	    Retry
APIConnectionError	Retry
InternalServerError	Retry
APIError	        Log unexpected failures

# Day 6 — Context & Memory
Build chat history list
Send full message history to API
Observe token growth
Implement message trimming
Add basic summarization of old messages

-- this list is describing the basic architecture of a conversational AI system with memory management.
A chat model is stateless. It does not remember previous API calls automatically.
You need to maintain the conversation history yourself.
So you need to append the user input therefore Now the history contains the context. Then Every message you keep increases the input size for tokens consumptions because every call sends the entire context. You can't send unlimited history because 
models have context limits
cost increases
latency increases
so you can implement message trimming meaning to Keep only the last N messages and you can also add basic summarization of old messages. Note that Trimming removes information Instead of deleting old messages, summarize them.

Note here: 
Every model has a context window. Companies don't keep every message forever, Instead they periodically summarize. 
The summary is another API call and you need to use another prompt i.e. summary_system.md rather than conversation_system.md.
Example of a very modular architecture:
instructions/
    conversation.md
    summary.md
Then:
chat.py
    response = conversation()
memory.py

    summary = summarize()
logger.py
    save_json()

When do you summarize? There are no fixed rules however a good example is:
if token_count(messages) > 50000:
    summarize()

What OpenAI recommends (general architecture):
Developer Prompt
        │
        ▼
Conversation History
        │
        ▼
Running Summary
        │
        ▼
Latest 5-10 exchanges
        │
        ▼
Current User Message

 # Day 7 — Mini Project #1
💬 “CLI AI Assistant”
Chat interface in terminal
Maintains conversation memory
Uses system prompt personality
Outputs structured response option
Handles basic errors

# Retry limit logic with tenacity
from openai import OpenAI
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
    retry_if_exception_type,
    before_sleep_log,
)
import openai
import logging

client = OpenAI()
logger = logging.getLogger(__name__)

@retry(
    stop=stop_after_attempt(5),
    wait=wait_random_exponential(
        multiplier=1,
        max=60
    ),
    retry=retry_if_exception_type(
        (
            openai.RateLimitError,
            openai.APITimeoutError,
            openai.APIConnectionError,
        )
    ),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    reraise=True,
)
def generate_response(prompt: str):
    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt,
        timeout=30,
    )
    return response.output_text

 This configuration is close to what you typically see in production:
5 attempts
random exponential backoff
60s max wait
retry only transient OpenAI failures
log retries
raise the real error after exhaustion

Tenacity parameter / Example value / Purpose

stop / stop_after_attempt(5) / Defines the maximum number of attempts before giving up. Here: 5 total attempts (initial request + retries).

wait / wait_random_exponential(multiplier=1, max=60) / Controls the delay between retries using exponential backoff with randomness. The wait time increases after each failure while adding jitter to avoid multiple clients retrying at the same time.

max (inside wait_random_exponential) / 60 seconds / Caps the maximum retry wait time. Even if the exponential delay grows, Tenacity will never wait more than 60 seconds between attempts.

multiplier (inside wait_random_exponential) / 1 / Controls the base scale of the exponential delay. A higher value increases the initial and subsequent wait durations.

retry / retry_if_exception_type(...) / Defines which failures should trigger a retry. In the OpenAI example, only transient errors are retried (RateLimitError, APITimeoutError, APIConnectionError).

before_sleep / before_sleep_log(logger, logging.WARNING) / Logs information before each retry, including the exception and the next retry delay. Useful for monitoring and debugging.

reraise / True / After all retry attempts fail, raises the original OpenAI exception instead of wrapping it inside a Tenacity RetryError.