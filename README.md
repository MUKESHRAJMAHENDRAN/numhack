# **GenAI Application [Multifunctional Agent Framework Application for Fisherman, farmers, Education]**  
A versatile, AI-powered platform built with Django, HTML, CSS, JavaScript, LangChain, OpenAI, and ChromaDB. This application caters to users with occupations like *Fisherman, Farmer,* and *Education*, offering tailored AI solutions for weather analysis, sustainable practices, career planning, and learning support.  

## **Table of Contents**  
1. [Introduction](#introduction)  
2. [Features](#features)  
3. [Technical Stack](#technical-stack)  
4. [Functionality by Occupation](#functionality-by-occupation)  
   - [Fisherman](#fisherman)  
   - [Farmer](#farmer)  
   - [Education](#education)  
5. [Architecture](#architecture)  
6. [Future Enhancements](#future-enhancements)  
7. [Getting Started](#getting-started)  


## **1. Introduction**  
The **Multifunctional Agent Framework Application** provides a personalized experience for users based on their selected occupation.  
- Fishermen and farmers receive actionable insights based on weather data and AI analysis.  
- Students benefit from career planning, real-time study resources, assessment tools, and mathematics problem-solving assistance.  
- Built with AI frameworks, the application intelligently selects agents to perform specific tasks, ensuring optimal performance.  


## **2. Features**  
- **Multi-Agent Framework:** Selects the right agent for the right task using LangChain.  
- **Weather-Based Decision Making:** Real-time weather data integration using OpenWeather API.  
- **Sustainability Guidance:** Offers insights on sustainable fishing and farming practices using Retrieval-Augmented Generation (RAG).  
- **Image Analysis:** Determines animal/fish species and provides IUCN status for actionable insights.  
- **Career Assistance for Students:** Career planning, study material generation, and assessments using Tavily API and other tools.  
- **Step-by-Step Problem Solving:** Detailed explanations of mathematical problems.  
- **Scalable Design:** Easily adaptable to multiple languages and AI models like Llama or Gemini.  


## **3. Technical Stack**  
The application leverages the following technologies:  
### **Frontend:**  
- HTML, CSS, JavaScript for user interfaces.  

### **Backend:**  
- Django for handling backend logic and user interactions.  

### **AI Framework:**  
- LangChain for managing multi-agent workflows.  
- OpenAI (GPT-based models) for language processing.  
- ChromaDB for vector database integration.  

### **APIs:**  
- OpenWeather API for weather analysis.  
- Tavily API for real-time search-based study resources. 


## **4. Functionality by Occupation**  

### **Fisherman**  
- **Weather Insights:** Helps fishermen decide whether to go fishing by analyzing real-time weather data.  
- **Sustainable Practices:** Guides sustainable fishing practices using RAG (Retrieval-Augmented Generation).  
- **Species Identification:** Analyzes images of caught fish, identifies the species, and checks its IUCN conservation status.  

### **Farmer**  
- **Weather-Based Crop Planning:** Analyzes weather data to provide recommendations on crop planting.  
- **Sustainability Guidance:** Offers tips for sustainable farming using RAG.  
- **Image Analysis:** Identifies pests or animals in uploaded images to provide action recommendations.  

### **Education**  
- **Career Planning:** Assists students in selecting and exploring career paths.  
- **Study Material Generation:** Fetches and compiles real-time resources in markdown format using Tavily API.  
- **Assessments:** Generates subject-specific 100-mark assessment questions.  
- **Mathematics Assistance:** Solves and explains math problems step-by-step.  


## **5. Architecture**  
The application employs a modular architecture:  
1. **User Authentication:** Django handles user sign-up and login.  
2. **Occupation-Based Routing:** Each occupation triggers its specific agents.  
3. **Agent Execution:**  
   - Agents are implemented using LangChain, which orchestrates task-specific workflows.  
   - Calls APIs or tools as needed to complete tasks.  
4. **Data Management:**  
   - ChromaDB stores vector embeddings for RAG.  
   - APIs like OpenWeather and Tavily provide real-time data for decisions.  


## **6. Future Enhancements**  
- **Regional Language Support:** Extend the application to support multiple languages.  
- **Additional AI Models:** Incorporate models like Llama, Gemini, etc., for enhanced capabilities.  
- **Expanded Occupations:** Introduce new categories such as healthcare, legal assistance, or business planning.  
- **Improved Sustainability Insights:** Use more specialized APIs for ecological data.  


## **7. Getting Started**  
### **Prerequisites:**  
- Python 3.11.6  
- Django  
- OpenAI API Key  
- OpenWeather API Key  
- Tavily API Key  

### **Installation:**  
1. Clone the repository:  
   ```bash  
   git clone https://github.com/MUKESHRAJMAHENDRAN/numhack_2024.git  
   cd chatbot  
   ```  

2. Install dependencies:  
   ```bash  
   pip install -r requirements.txt  
   ```  

3. Set up environment variables:  
   - Add API keys in a `.env` file.  

4. Run the server:  
   ```bash  
   python manage.py runserver  
   ```  

5. Access the application:  
   - Open `http://localhost:8000` in your browser.  

