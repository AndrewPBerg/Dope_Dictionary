from django.shortcuts import render
import requests
from django.http import JsonResponse
from dotenv import dotenv_values
import google.generativeai as genai

# Create your views here.
def home(request):
    return render(request, "home.html")

def get_definition_llm(request):  # Changed to accept request parameter
    if request.method == "GET":
        style = request.GET.get("style")
        word = request.GET.get("word")
        
        # Load environment variables
        config = dotenv_values(".env")
        
        # Configure Gemini
        api_key = config.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
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
        try:
            response = gemini_model.generate_content(prompt)
            return render(request, "home.html", {"definition": response.text})
        except Exception as e:
            return render(request, "home.html", {"definition": f"Error generating definition: {str(e)}"})
    
    return render(request, "home.html")
# def get_definition_llm(style, word):
    
#     # Load environment variables
#     config = dotenv_values(".env") # API KEY is stored in untracked .env file
    
#     # Configure Gemini
#     api_key = config.get("GOOGLE_API_KEY")
#     if not api_key:
#         raise ValueError("GOOGLE_API_KEY not found in environment variables")
#     genai.configure(api_key=api_key)
    
#     # Initialize model
#     gemini_model = genai.GenerativeModel('gemini-1.5-flash')
    
#     # Define prompt
#     prompt = f"""
#     Define the word '{word}' in the style of (a) {style}.
    
#     The definition should be:
#     1. Safe for work and appropriate
#     2. Clear and understandable
#     3. True to the style's characteristics
#     4. Lighthearted and funny, but also informative
#     """
    
#     # Generate response
#     try:
#         response = gemini_model.generate_content(prompt)
#         return response.text
#     except Exception as e:
#         return f"Error generating definition: {str(e)}"

def get_definition_service(request): 
    #gets definition from Java microservice (hashmap database)
    #if not found, get_definition_llm
    #stores definition in Java microservice and displays to user
    
    if request.method == "GET":
        style = request.GET.get("style")
        word = request.GET.get("word")
        
        java_url_get = f"http://localhost:8080/dictionary/get?style={style}&word={word}"
        answer_java = requests.get(java_url_get)
        if answer_java.text != "Definition not found" and answer_java.status_code == 200:
            return render(request, "dictionary/home.html", {"definition": answer_java.text})
        else:
            answer_llm = get_definition_llm(style, word)
            java_url_add = f"http://localhost:8080/dictionary/add?style={style}&word={word}&definition={answer_llm}"
            requests.post(java_url_add)
            return render(request, "dictionary/home.html", {"definition": answer_llm})
    return render(request, "dictionary/home.html")

def main():
    word = "apple"
    style = "Shakespeare"

    config = dotenv_values(".env")
            
    # Configure Gemini
    api_key = config.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")
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
    try:
        response = gemini_model.generate_content(prompt)
        print(response.text)
    except Exception as e:
        print(f"Error generating definition: {str(e)}")


if __name__ == "__main__":
    main()