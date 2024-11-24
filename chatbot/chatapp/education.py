from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from uuid import uuid4
import chromadb
from langchain_chroma import Chroma
from dotenv import load_dotenv
import os
from openai import OpenAI
from tavily import TavilyClient
from langchain.adapters.openai import convert_openai_messages
from langchain_openai import ChatOpenAI

load_dotenv()
api_key = os.getenv("API_KEY")
weather_api = os.getenv("WEATHER_API")
tavily_api = os.getenv("TAVILY_API")
client = OpenAI(api_key=api_key)

def helper_agent(user_query):
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful Educational assistant."},
            {
            "role": "system",
            "content": f"""I am going to ask you a question and my question is {user_query}, which I would like you to answer"
            "based only on the provided context"
            "If there is not enough information in the user question ask for more information to answer the question,"
            "Dont say i dont know the answer make"
            "Break your answer up into nicely readable paragraphs".
            "Make the result in maximum 2 lies"
            """,
            }
        ]
    )
    result = completion.choices[0].message.content
    return result



def researcher_agent(query):
    client = TavilyClient(api_key=tavily_api)
    # Step 2. Executing the search query and getting the results
    content = client.search(query=query, search_depth="advanced")["results"]
    
    # Step 3. Setting up the OpenAI prompts
    prompt = [{
        "role": "system",
        "content":  f'You are an AI critical thinker research assistant. '\
                    f'Your sole purpose is to write well written, critically acclaimed,'\
                    f'objective and structured reports on given text.'
    }, {
        "role": "user",
        "content": f'Information: """{content}"""\n\n' \
                   f'Using the above information, answer the following'\
                   f'query: "{query}" in a detailed report --'\
                   f'Please use MLA format and markdown syntax.'
    }]
    
    # Step 4. Running OpenAI through Langchain
    lc_messages = convert_openai_messages(prompt)
    report = ChatOpenAI(model='gpt-4o',openai_api_key=api_key).invoke(lc_messages).content
    return report

def assesment_agent(user_query):
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful Educational assistant will answer based on user query."},
            {
                "role": "system",
                "content": (
                    f"User query for Assesment: {user_query},"
                    "I am going to ask you to create an assessment consisting of 100 marks with 20 questions, "
                    "including 15 multiple-choice questions (MCQs) and 2 theory questions. "
                    "The assessment should be structured as follows:\n\n"
                    "### Assessment Structure:\n"
                    "- **Total Questions**: 20\n"
                    "- **Total Marks**: 100\n"
                    "- **MCQs**: 15 questions, each worth 4 marks (15 x 4 = 60 marks)\n"
                    "- **Theory Questions**: 2 questions, each worth 15 marks (2 x 15 = 30 marks)\n"
                    "- **Remaining Questions**: 3 questions, 2 worth 3 marks and 1 worth 4 marks. (9 + 1 = 10 marks)\n\n"
                    "### Example Format:\n\n"
                    "#### Section A: Multiple Choice Questions (MCQs)\n"
                    "(Each question carries 4 marks)\n\n"
                    "1. Sample Question 1\n"
                    "   - a) Option 1\n"
                    "   - b) Option 2\n"
                    "   - c) Option 3\n"
                    "   - d) Option 4\n\n"
                    "(Continue with the rest...)\n\n"
                    "#### Section B: Theory Questions\n"
                    "(Each question carries 15 marks)\n\n"
                    "16. Sample Theory Question 1\n"
                    "17. Sample Theory Question 2\n\n"
                    "#### Section C: Additional Questions\n"
                    "(Distribute remaining 9-10 marks)\n\n"
                    "18. Sample question worth 3 marks\n"
                    "19. Sample question worth 3 marks\n"
                    "20. Sample question worth 4 marks\n"
                ),
            },
        ]
    )
    result = completion.choices[0].message.content
    return result