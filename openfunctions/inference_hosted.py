import openai
from openai import OpenAI

client = OpenAI(api_key="EMPTY")
import json

# TODO: The 'openai.api_base' option isn't read in the client API. You will need to pass it when you instantiate the client, e.g. 'OpenAI(base_url="http://luigi.millennium.berkeley.edu:8000/v1")'
# openai.api_base = "http://luigi.millennium.berkeley.edu:8000/v1"

# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API
def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    weather_info = {
        "location": location,
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)

def run_conversation():
    # Step 1: send the conversation and available functions to GPT
    messages = [{"role": "user", "content": "What's the weather like in the two cities of Boston and San Francisco?"}]
    functions = [
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        }
    ]
    completion = client.chat.completions.create(model='gorilla-openfunctions-v2',
    messages=messages,
    functions=functions,
    function_call="auto")

    print("--------------------")
    print(f"Function call strings(s): {completion.choices[0].message.content}")
    print("--------------------")
    print(f"OpenAI compatible `function_call`: {completion.choices[0].message.function_call}")

run_conversation()
