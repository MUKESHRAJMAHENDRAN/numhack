from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")
client = OpenAI(api_key=api_key)

tools = [
    {
        "type": "function",
        "function": {
            "name": "helper_agent",
            "description": """
                This agent is designed to handle a wide array of general inquiries. It provides explanations, definitions, and overviews on various topics. The helper_agent assists users by delivering immediate, concise, and accurate answers to their questions. Whether you need clarification on a concept, advice on a particular matter, or general information, the helper_agent is your go-to source for swift and straightforward responses.

                Example Question: 
                "What are the primary differences between renewable and non-renewable energy sources?"
            """,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "assesment_agent",
            "description": """
                The primary role of this agent is to generate assessment questions related to the given topic. It is designed to create questions that evaluate understanding and knowledge retention, such as multiple choice questions, short-answer questions, or problem-solving exercises that test comprehension. Whether for educational environments, self-assessment, or training programs, the assesment_agent ensures the questions are appropriately challenging and relevant to the material.

                Example Question: 
                "Explain the process of photosynthesis and provide an example of how it impacts other organisms in an ecosystem."
            """,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "researcher_agent",
            "description": """
                This agent specializes in creating comprehensive study plans for specific topics. It outlines structured learning paths designed to optimize knowledge acquisition and retention by breaking down complex subjects into manageable modules or lessons. The researcher_agent provides a detailed plan that includes recommended resources, key objectives, timelines, and evaluation checkpoints. It is ideal for learners looking to dive deep into a subject in a systematic and efficient manner, catering to diverse learning needs and paces.

                Example Question: 
                "Could you outline a study plan for mastering the basics of data science over a three-month period?"
            """,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "math_agent",
            "description": """
                Assistance need for solving solving math problem...
                Example Question: 
                    how can I solve 8x + 7 = -23,
                   
            """,
        },
    },
]

def education_tool(user_message):
    messages = [{"role": "user", "content": user_message}]
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
        tool_choice="required"
    )
    function_name = completion.choices[0].message.tool_calls[0].function.name
    return function_name
