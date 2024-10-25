import os
from dotenv import dotenv_values
import google.generativeai as genai

# Load environment variables into a dictionary 
# MUST BE IN ROOT DIRECTORY 
# MUST BE IN ROOT DIRECTORY 
# MUST BE IN ROOT DIRECTORY 
# .env MUST NOT BE COMMITTED TO GIT
# .env MUST NOT BE COMMITTED TO GIT
# .env MUST NOT BE COMMITTED TO GIT

config = dotenv_values(".env")

# Configure the Gemini API
api_key = config.get("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")
genai.configure(api_key=api_key)

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-flash')
print(f"Using model: {model}")

# Function to generate content
def generate_content(prompt):
    response = model.generate_content(prompt)
    return response.text

# Example usage
prompt = "Define the word 'dope' in the style of a caveman."
result = generate_content(prompt)
print(result)
