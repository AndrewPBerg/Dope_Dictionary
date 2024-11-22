from django.shortcuts import render
import requests
from urllib.parse import quote, unquote
from django.http import JsonResponse
from dotenv import load_dotenv
import google.generativeai as genai
import os
from pathlib import Path
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request, "home.html")

def get_definition_llm(style, word):
    # Get the directory containing the current file
    current_dir = Path(__file__).resolve().parent
    env_path = current_dir / '.env'
    
    # Load environment variables from .env file
    load_dotenv(env_path)
    
    # Load Google API key from .env file 🔑
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        return "Error: Google API key not configured. Please check your .env file."
    
    try:
        # Configure Gemini 💡
        genai.configure(api_key=api_key)
        
        # Initialize model with gemini-1.5-flash for faster responses 🚀
        gemini_model = genai.GenerativeModel('gemini-1.5-flash')

        # Prompt the LLM for the definition 💬
        prompt = (
            f"Define '{word}' in {style} style. Make it:, Safe for Work, Clear, "
            f"Fun yet informative, end with a period, and 1 to 2 sentences."
        )

        # configure gemini model request parameters 📝
        response = gemini_model.generate_content(
            prompt,
            generation_config={
                'temperature': 0.5,  # Lower temperature for faster, more focused responses
                'top_p': 0.8,       # Reduce sampling space
                'top_k': 30,        # Limit token selection
                'max_output_tokens': 60  # Limit response length
            }
        )

        return response.text # Return the definition
    except Exception as e:
        return f"Error generating definition: {str(e)}"

@csrf_exempt
def get_definition_service(request): 
    if request.method == "GET":
        try:
            style = request.GET.get("style", "").strip()
            word = request.GET.get("word", "").strip()
            
            if not style or not word:
                return render(request, "home.html", {"definition": "Please provide both style and word"})
            
            # URL encode parameters to handle special characters 
            encoded_style = quote(style)
            encoded_word = quote(word)
            encoded_base_url = "http://localhost:8080/dictionary"
            
            try:
                # Try to get definition from Java service 📚
                response = requests.get(
                    f"{encoded_base_url}/get",
                    params={"style": encoded_style, "word": encoded_word},
                    timeout=5
                )
                response.raise_for_status()
                
                if response.text != "Definition not found":
                    # Decode the URL-encoded definition before rendering 🔍
                    decoded_definition = unquote(response.text)
                    return render(request, "home.html", {
                        "definition": decoded_definition,
                        "selected_style": style
                    })
                
                if style == "N/A": # Handle case where no style is selected ⚠️
                    return render(request, "home.html", {"definition": "Please select a style"})
                
                # If no definition is found, get from LLM 🤖
                answer_llm = get_definition_llm(style, word)

                # Handle LLM error
                if "Error:" in answer_llm:
                    return render(request, "home.html", {
                        "definition": answer_llm,
                        "selected_style": style
                    })
                
                # Store in Java HashTable micro-service 📚
                store_response = requests.post(
                    f"{encoded_base_url}/add",
                    params={
                        "style": encoded_style,
                        "word": encoded_word,
                        "definition": quote(answer_llm)
                    },
                    timeout=5
                )
                store_response.raise_for_status()
                
                # Render the definition on the home page 🎨
                return render(request, "home.html", {
                    "definition": answer_llm,
                    "selected_style": style
                })
                
            except requests.Timeout:
                return render(request, "home.html", {
                    "definition": "Service timeout - please try again",
                    "selected_style": style
                })
            except requests.ConnectionError:
                return render(request, "home.html", {
                    "definition": "Cannot connect to service - please try again later",
                    "selected_style": style
                })
            except requests.RequestException as e:
                return render(request, "home.html", {
                    "definition": f"Service error: {str(e)}",
                    "selected_style": style
                })
                
        except Exception as e:
            return render(request, "home.html", {
                "definition": f"Unexpected error: {str(e)}",
                "selected_style": style if 'style' in locals() else ""
            })
            
    return render(request, "home.html")

def main():
    current_dir = Path(__file__).resolve().parent
    env_path = current_dir / '.env'

    # Load environment variables from .env file
    load_dotenv(env_path)
    
    word = "pi"
    style = "Shakespeare"

    # Get API key
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        return "Error: Google API key not configured. Please check your .env file."

    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Initialize model with gemini-1.5-flash for faster responses
        # Flash model is optimized for speed while maintaining quality
        gemini_model = genai.GenerativeModel('gemini-1.5-flash')

        # Optimize prompt to be more concise while maintaining requirements
        prompt = (
            f"Define '{word}' in {style} style. "
            "Make it: 1) SFW 2) Clear 3) Style-authentic "
            "4) Fun yet informative 5) 1 to 2 sentences."
        )
        
        # Set generation config for faster responses
        response = gemini_model.generate_content(
            prompt,
            generation_config={
                'temperature': 0.5,  # Lower temperature for faster, more focused responses
                'top_p': 0.8,       # Reduce sampling space
                'top_k': 30,        # Limit token selection
                'max_output_tokens': 50  # Limit response length
            }
        )
        print(response.text)
    except Exception as e:
        print(f"Error generating definition: {str(e)}")
    
if __name__ == "__main__":
    main()