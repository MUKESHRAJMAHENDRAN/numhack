import requests
from openai import OpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from uuid import uuid4
import chromadb
from langchain_chroma import Chroma

from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")
weather_api = os.getenv("WEATHER_API")
client = OpenAI(api_key=api_key)


def agri_endangered(base64_image, user_message):
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
      model="gpt-4o",
      messages=[
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": f"{user_message} You are expert based on the user message you will identify the species based on IUCN status Give the farmer what to do...",
            },
            {
              "type": "image_url",
              "image_url": {
                "url":  f"{base64_image}"
              },
            },
          ],
        }
      ],
    )
    
    return response.choices[0].message.content

def agri_retreival(query, collection_name):
    persistent_client = chromadb.PersistentClient(path="numhack_db/")
    collection = persistent_client.get_or_create_collection(collection_name)
    # collection.add(ids=["1", "2", "3"], documents=["a", "b", "c"])
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=api_key)
    vector_store_from_client = Chroma(
        client=persistent_client,
        collection_name=collection_name,
        embedding_function=embeddings,)
    
    results = vector_store_from_client.similarity_search(
    query=query,
    k=2,
    )
    return results