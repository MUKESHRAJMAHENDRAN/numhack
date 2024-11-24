from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import ChatMessage
from .forms import SignUpForm
from .aquatic import weather_alert, weather_analyzer, endangered
from .aquatic_tool_call import aquatic_tool
from .refinement import data_refinement, data_retreival
from .agri_tool_call import agri_tool
from .farms import agri_endangered
from .math import get_math_solution, get_math_steps
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
import json
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import re
from .education import helper_agent, researcher_agent, assesment_agent
from .education_tool_call import education_tool
from .history import get_last_two_messages

@login_required(login_url='login')
def home(request):
    # Renders the homes page after login
    return render(request, 'chatapp/index.html')

@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        # Ensure we're using appropriate methods to access the data
        message = request.POST.get('message')
        occupation = request.POST.get('occupation')
        location = request.POST.get('location')
        base64_image = request.POST.get('base64_image')
        # image = request.FILES.get('image')  # Use .get to avoid KeyError
        print("type---------", type(base64_image))
        # with open("m.txt", "w") as f:
        #     f.write(base64_image)
        # print(base64_image.keys())
        # image = base64_image.replace("data:image/jpeg;base64,", "")
        # Debugging output
        
        print("Received message:", message)
        print("Occupation:", occupation)
        print("Location:", location)
        # print("Image----------------:", image)
        # en_species = endangered(base64_image=f"{base64_image}", user_message=message)
        # print("eeeee", en_species)
        # return JsonResponse({'response': en_species})


        if occupation == "fisherman":
        
            # print("kkkeeeeee", en_species)
            tool_call  = aquatic_tool(message)
            if tool_call == "get_weather":
                weather_data = weather_alert(location)
                analyzed_data = weather_analyzer(weather_data, occupation)
                chat_message = ChatMessage(user_message=message, bot_response=analyzed_data)
                chat_message.save()
                return JsonResponse({'response': analyzed_data})
            elif tool_call == "fishing_technique":
                print("_____________________")
                db_path = r'C:\Users\Mukesh\Desktop\numhack_2024\chatbot\db.sqlite3'
                message_pairs = get_last_two_messages(db_path)
                for user_message, bot_response in message_pairs:
                    message += f"User Message: {user_message}, Bot Response: {bot_response}"
                ai_response = data_retreival(query=message, collection_name="fishing_collection")
                response = data_refinement(user_query=message, retreived_data=ai_response)
                chat_message = ChatMessage(user_message=message, bot_response=response)
                chat_message.save()
                return JsonResponse({'response': response})
            elif tool_call == "iucn_status":
                # print("peeeeeeeee", message)
                # print("zzzzzzzzkeeeeee", en_species)
                en_species = endangered(base64_image=f"{base64_image}", user_message=message)
                chat_message = ChatMessage(user_message=message, bot_response=en_species)
                chat_message.save()
                return JsonResponse({'response': en_species})
            else:
                return JsonResponse({'response': helper_agent(message)})
            
        if occupation == "farmer":
            tool_call  = agri_tool(message)
            if tool_call == "get_weather":
                weather_data = weather_alert(location)
                analyzed_data = weather_analyzer(weather_data, occupation)
                chat_message = ChatMessage(user_message=message, bot_response=analyzed_data)
                chat_message.save()
                return JsonResponse({'response': analyzed_data})
            elif tool_call == "agri_technique":
                print("___________________")
                db_path = r'C:\Users\Mukesh\Desktop\numhack_2024\chatbot\db.sqlite3'
                message_pairs = get_last_two_messages(db_path)
                for user_message, bot_response in message_pairs:
                    message += f"User Message: {user_message}, Bot Response: {bot_response}"
                ai_response = data_retreival(query=message, collection_name="agri_collection")
                response = data_refinement(user_query=message, retreived_data=ai_response)
                chat_message = ChatMessage(user_message=message, bot_response=response)
                chat_message.save()
                return JsonResponse({'response': response})
            elif tool_call == "iucn_status":
                # print("peeeeeeeee", message)
                # print("zzzzzzzzkeeeeee", en_species)
                en_species = agri_endangered(base64_image=f"{base64_image}", user_message=message)
                chat_message = ChatMessage(user_message=message, bot_response=en_species)
                chat_message.save()
                return JsonResponse({'response': en_species})
            else:
                return JsonResponse({'response': helper_agent(message)})
        if occupation == "education":
            tool_call  = education_tool(message)
            if tool_call == "researcher_agent":
                research = researcher_agent(message)
                chat_message = ChatMessage(user_message=message, bot_response=research)
                chat_message.save()
                return JsonResponse({'response': research})
            elif tool_call == "assesment_agent":
                asses = assesment_agent(message)
                chat_message = ChatMessage(user_message=message, bot_response=asses)
                chat_message.save()
                return JsonResponse({'response': asses})
            elif tool_call == "helper_agent":
                # db_path = r'C:\Users\Mukesh\Desktop\numhack_2024\chatbot\db.sqlite3'
                # message_pairs = get_last_two_messages(db_path)
                # for user_message, bot_response in message_pairs:
                #     message += f"User Message: {user_message}, Bot Response: {bot_response}"
                helper = helper_agent(message)
                chat_message = ChatMessage(user_message=message, bot_response=helper)
                chat_message.save()
                return JsonResponse({'response': helper})
            else:
                # db_path = r'C:\Users\Mukesh\Desktop\numhack_2024\chatbot\db.sqlite3'
                # message_pairs = get_last_two_messages(db_path)
                # for user_message, bot_response in message_pairs:
                #     message += f"User Message: {user_message}, Bot Response: {bot_response}"
                result = get_math_solution(message)
                ai_resp = get_math_steps(result)
                chat_message = ChatMessage(user_message=message, bot_response=ai_resp)
                chat_message.save()
                return JsonResponse({'response': ai_resp})
        
    return JsonResponse({'error': 'Invalid request'}, status=400)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')  # Redirect to a success page
    else:
        form = SignUpForm()

    return render(request, 'chatapp/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to a home page after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'chatapp/login.html', {'form': form})