from django.shortcuts import render
import requests
from django.http import JsonResponse

# Create your views here.
def get_definition_llm(style, word):
    andrew = 
    #gets definition from Google Gemini API 
    #sends request to API endpoint with API KEY
    
    #GEMINI API CODE (ANDREW)

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