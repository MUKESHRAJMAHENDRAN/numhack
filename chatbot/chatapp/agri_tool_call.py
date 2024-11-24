from openai import OpenAI
from dotenv import load_dotenv
import os
 
# Load environment variables from the .env file
load_dotenv()
api_key = os.getenv("API_KEY")
client = OpenAI(api_key=api_key)

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": """
                This function provides information about current and forecasted weather conditions that could affect 
                agricultural activities. Users can inquire about the weather to determine if conditions are favorable 
                for planting, harvesting, or other farming activities. This includes questions about temperature, wind 
                speed, precipitation, and any other weather-related factors that might influence farming success or 
                safety. Example queries could be "What’s the weather like today?" or "Is today a good day for planting?"
            """,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "agri_technique",
            "description": """
                This function offers guidance on various agricultural techniques, including methods and tips for 
                growing different types of crops. It provides information on sustainable farming practices that minimize 
                environmental impact, suggestions for farming equipment and methods, and techniques suited for different 
                soil types and climates. Users might ask, "What is the best technique for growing tomatoes?" or 
                "How can I farm sustainably?"
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
                This function provides information about the conservation status of various plant species as determined 
                by the International Union for Conservation of Nature (IUCN). It can inform users about which plants are 
                endangered, threatened, or safe to cultivate according to current environmental assessments and 
                conservation guidelines. Users can ask, "What is the IUCN status of the American Chestnut?" or "Is it 
                sustainable to cultivate the Baobab Tree? What is status of the animal? This animal looks new to me"
            """,
        },
    },
]

def agri_tool(user_message):
    messages = [{"role": "user", "content": user_message}]
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
        tool_choice="required"
    )
    function_name = completion.choices[0].message.tool_calls[0].function.name
    return function_name
