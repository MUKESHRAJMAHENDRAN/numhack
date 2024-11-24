from openai import OpenAI
from dotenv import load_dotenv
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from uuid import uuid4
import chromadb
from langchain_chroma import Chroma
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
api_key = os.getenv("API_KEY")
weather_api = os.getenv("WEATHER_API")
client = OpenAI(api_key=api_key)


def data_refinement(user_query, retreived_data):
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
            "role": "system",
            "content": f"""I am going to ask you a question and my question is {user_query}, which I would like you to answer"
            "based only on the provided context {retreived_data}and the context is , and not any other information."
            "If there is not enough information in the context to answer the question,"
            "Dont say i dont know the answer make"
            "Break your answer up into nicely readable paragraphs".
            "Make the result in maximum 2 lies"
            """,
            }
        ]
    )
    result = completion.choices[0].message.content
    return result

def data_retreival(query, collection_name):
    persistent_client = chromadb.PersistentClient(path=r"C:\Users\Mukesh\Desktop\numhack_2024\data_ingestion_notebooks\numhack_db")
    collection = persistent_client.get_or_create_collection(collection_name)
    # collection.add(ids=["1", "2", "3"], documents=["a", "b", "c"])
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=api_key)
    vector_store_from_client = Chroma(
        client=persistent_client,
        collection_name=collection_name,
        embedding_function=embeddings,)
    
    results = vector_store_from_client.similarity_search(query=query,k=2)
    retreived_data = ""
    for res in results:
        retreived_data += res.page_content
    return retreived_data