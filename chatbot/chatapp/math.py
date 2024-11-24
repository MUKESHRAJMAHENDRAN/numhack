import json
from textwrap import dedent
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")
weather_api = os.getenv("WEATHER_API")
client = OpenAI(api_key=api_key)

MODEL = "gpt-4o"

math_tutor_prompt = '''
    You are a helpful math tutor. You will be provided with a math problem,
    and your goal will be to output a step by step solution, along with a final answer.
    For each step, just provide the output as an equation use the explanation field to detail the reasoning.
'''

def get_math_solution(question):
    response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {
            "role": "system", 
            "content": dedent(math_tutor_prompt)
        },
        {
            "role": "user", 
            "content": question
        }
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "math_reasoning",
            "schema": {
                "type": "object",
                "properties": {
                    "steps": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "explanation": {"type": "string"},
                                "output": {"type": "string"}
                            },
                            "required": ["explanation", "output"],
                            "additionalProperties": False
                        }
                    },
                    "final_answer": {"type": "string"}
                },
                "required": ["steps", "final_answer"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
    )
    result = response.choices[0].message.content
    return result

# Testing with an example question
# question = "how can I solve 8x + 7 = -23"

# result = get_math_solution(question) 

# print(result.content)

def get_math_steps(response):
    # Parse the JSON response
    result = json.loads(response)
    steps = result['steps']
    final_answer = result['final_answer']

    # Initialize a list to store the formatted output
    structured_output = []

    # Step-by-step explanation and output
    for i, step in enumerate(steps):
        step_text = f"Step {i+1}: {step['explanation']}\n{step['output']}\n"
        structured_output.append(step_text)

    # Add the final answer
    structured_output.append(f"Final answer:\n{final_answer}\n")

    return structured_output
