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

def weather_alert(location):
    base_url = f"http://api.openweathermap.org/data/2.5/forecast?q="+location+"&appid="+weather_api
    response = requests.get(base_url)
    x = response.json()
    weather_extraction = []
    for weather_data in x['list']:
        date_wise_weather = {
        "date_key": {
            'date_time': weather_data['dt_txt'],
            'weather_condition': weather_data['weather'][0]['description'],
            'wind_speed': weather_data['wind']['speed'],
            'wind_gust': weather_data['wind']['gust'],
            'visibility': weather_data['visibility'],
            'temperature': weather_data['main']['temp'],
            'feels_like_temperature': weather_data['main']['feels_like'],
            'precipitation_probability': weather_data['pop']}
        }
        weather_extraction.append(date_wise_weather)
    return weather_extraction

def weather_analyzer(weather_extraction, occupation):
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpfulf Weather Expert Assistant."},
            {
                "role": "user",
                "content": f"""I am giving you the next three days data :{weather_extraction} 
                for with an span of 3hours you have to help me weather the {occupation} is good to
                go for [planting/fishing] or not Based on the occupation only you should response. Explain the result in three lines"""
            }
        ]
    )
    # print(completion.choices[0].message)
    return completion.choices[0].message.content


def endangered(base64_image, user_message):
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
      model="gpt-4o",
      messages=[
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": f"{user_message} You are expert based on the user message you will identify the aquatic species based on IUCN status Give the fishmen you fish or not",
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

def aquatic_retreival(query):
    persistent_client = chromadb.PersistentClient(path="numhack_db/")
    collection = persistent_client.get_or_create_collection("fishing_collection")
    # collection.add(ids=["1", "2", "3"], documents=["a", "b", "c"])
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=api_key)
    vector_store_from_client = Chroma(
        client=persistent_client,
        collection_name="fishing_collection",
        embedding_function=embeddings,)
    
    results = vector_store_from_client.similarity_search(
    query=query,
    k=2,
    )
    retreived_data = ""
    for res in results:
        retreived_data += res.page_content
    return retreived_data