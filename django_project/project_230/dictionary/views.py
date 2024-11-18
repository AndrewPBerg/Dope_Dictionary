from django.shortcuts import render
import requests
from django.http import JsonResponse
from dotenv import load_dotenv
import google.generativeai as genai
import os
from pathlib import Path
from django.core.exceptions import SuspiciousOperation
from requests.exceptions import ConnectionError

def home(request):
    return render(request, "home.html")

def get_definition_llm(style, word):
    # Get the directory containing the current file
    current_dir = Path(__file__).resolve().parent
    env_path = current_dir / '.env'
    
    # Load environment variables from .env file
    load_dotenv(env_path)
    
    # Get API key
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        return "Error: Google API key not configured. Please check your .env file."
    
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Initialize model and generate response
        gemini_model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
            Define the word '{word}' in the style of (a) {style}.
            
            The definition should be:
            1. Safe for work and appropriate
            2. Clear and understandable
            3. True to the style's characteristics
            4. Lighthearted and funny, but also informative
            """
        
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating definition: {str(e)}"

def get_definition_service(request): 
    if request.method == "GET":
        try:
            style = request.GET.get("style")
            word = request.GET.get("word")
            
            if not style or not word:
                return render(request, "home.html", {"definition": "Please provide both style and word"})
            
            # First try to get from Java service
            java_url_get = f"http://localhost:8080/dictionary/get?style={style}&word={word}"
            try:
                answer_java = requests.get(java_url_get, timeout=5)  # Add timeout
                answer_java.raise_for_status()  # Raise exception for bad status codes
                
                if answer_java.text != "Definition not found":
                    return render(request, "home.html", {"definition": answer_java.text})
                
                # If not found, get from LLM and store in Java service
                answer_llm = get_definition_llm(style, word)
                if "Error:" in answer_llm:  # Check for LLM errors
                    return render(request, "home.html", {"definition": answer_llm})
                    
                java_url_add = f"http://localhost:8080/dictionary/add?style={style}&word={word}&definition={answer_llm}"
                requests.post(java_url_add, timeout=5)
                return render(request, "home.html", {"definition": answer_llm})
                
            except requests.Timeout:
                return render(request, "home.html", {"definition": "Service timeout - please try again"})
            except requests.ConnectionError:
                return render(request, "home.html", {"definition": "Cannot connect to service - please try again later"})
            except requests.RequestException as e:
                return render(request, "home.html", {"definition": f"Service error: {str(e)}"})
                
        except Exception as e:
            return render(request, "home.html", {"definition": f"Unexpected error: {str(e)}"})
            
    return render(request, "home.html")