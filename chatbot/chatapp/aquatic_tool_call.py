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
            "name": "get_weather",
            "description": """
                This function provides information about current and forecasted weather conditions which could affect 
                outdoor activities such as fishing. Users can inquire about the weather to determine if conditions 
                are favorable for fishing. This includes questions about temperature, wind speed, precipitation, and 
                any other weather-related factors that might influence fishing success or safety. 
                Example queries could be "What’s the weather like today?" or "Is today a good day for fishing?" 
            """,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "fishing_technique",
            "description": """
                This function offers guidance on various fishing techniques, including methods and tips for catching 
                different types of fish. It provides information on sustainable fishing practices that minimize 
                environmental impact, suggestions for fishing gear and bait, and techniques suited for different water 
                bodies and fish species. Users might ask, "What is the best technique for fishing bass?" or 
                "How can I fish sustainably?"
            """,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "greeting",
            "description": """
                This function is responsible for handling interactions that involve greetings or social pleasantries. 
                It caters to initiating, maintaining, or ending a conversation with polite exchanges. The function is 
                specifically not designed to handle any information-heavy inquiries—its sole purpose is to facilitate 
                social interaction, such as "Hello," "How are you?", or "Goodbye."
            """,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "iucn_status",
            "description": """
                This function provides information about the conservation status of various fish species as determined 
                by the International Union for Conservation of Nature (IUCN). It can inform users about which fish are 
                endangered, threatened, or safe to catch according to current environmental assessments and conservation 
                guidelines. Users can ask, "What is the IUCN status of Atlantic Cod?" or "Is it sustainable to fish 
                Bluefin Tuna?"
            """,
        },
    },
]

def aquatic_tool(user_message):
    messages = [{"role": "user", "content": user_message}]
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
        tool_choice="required"
    )
    function_name = completion.choices[0].message.tool_calls[0].function.name
    return function_name
