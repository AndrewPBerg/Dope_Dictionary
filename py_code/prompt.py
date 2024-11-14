import os
import json
from dotenv import dotenv_values
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import Dict, Tuple

# Load environment variables
config = dotenv_values(".env")

# Configure Gemini
api_key = config.get("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")
genai.configure(api_key=api_key)

# Initialize models
gemini_model = genai.GenerativeModel('gemini-1.5-flash')
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

class StyleDefinitionRAG:
    def __init__(self):
        self.styles = self._load_styles()
        self.style_embeddings = self._create_style_embeddings()
        
    def _load_styles(self) -> Dict:
        with open('python_LLM/styles_db.json', 'r') as f:
            return json.load(f)
    
    def _create_style_embeddings(self):
        # Create embeddings for each style's characteristics
        style_texts = [
            ' '.join(style_data['characteristics']) 
            for style_data in self.styles.values()
        ]
        return embedding_model.encode(style_texts)
    
    def _validate_style(self, style: str) -> Tuple[bool, str]:
        if style.lower() in self.styles:
            return True, style.lower()
        
        # Find closest matching style using embeddings
        query_embedding = embedding_model.encode([style])
        similarities = np.dot(query_embedding, self.style_embeddings.T)[0]
        most_similar_idx = np.argmax(similarities)
        
        if similarities[most_similar_idx] > 0.7:  # Threshold for similarity
            return True, list(self.styles.keys())[most_similar_idx]
        return False, ""

    def generate_definition(self, word: str, style: str) -> str:
        # Validate style
        is_valid, matched_style = self._validate_style(style)
        if not is_valid:
            return f"Error: '{style}' is not a valid style. Please choose from: {', '.join(self.styles.keys())}"
        
        # Construct RAG prompt
        style_info = self.styles[matched_style]
        prompt = f"""
        Define the word '{word}' in the style of {matched_style}.
        
        Style characteristics:
        - {' '.join(style_info['characteristics'])}
        - Tone should be {style_info['tone']}
        
        The definition should be:
        1. Safe for work and appropriate
        2. Clear and understandable
        3. True to the style's characteristics
        """
        
        try:
            response = gemini_model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating definition: {str(e)}"

def handle_definition_request(api_data: Dict) -> str:
    """Handle incoming API requests for definitions"""
    word = api_data.get('word', '').strip()
    style = api_data.get('style', '').strip()
    
    if not word or not style:
        return "Error: Both 'word' and 'style' are required"
    
    rag = StyleDefinitionRAG()
    return rag.generate_definition(word, style)

# Example usage
if __name__ == "__main__":
    # Simulate API request
    api_request = {
        "word": "dope",
        "style": "caveman"
    }
    result = handle_definition_request(api_request)
    print(result)
