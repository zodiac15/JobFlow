import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    # This might happen during initial setup before user provides key.
    # We'll handle it gracefully in the functions.
    print("Warning: GEMINI_API_KEY not found in environment variables.")

def configure_gemini():
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)

def generate_content(prompt, model_name="gemini-2.5-flash"):
    """
    Generates content using Gemini API.
    """
    if not GEMINI_API_KEY:
         return {"error": "API Key is missing. Please configure GEMINI_API_KEY."}

    try:
        configure_gemini()
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return None

def generate_json_content(prompt, model_name="gemini-2.5-flash"):
    """
    Generates JSON content using Gemini API.
    Enforces JSON response format.
    """
    if not GEMINI_API_KEY:
         return {"error": "API Key is missing."}

    try:
        configure_gemini()
        model = genai.GenerativeModel(model_name, generation_config={"response_mime_type": "application/json"})
        response = model.generate_content(prompt)
        return json.loads(response.text)
    except json.JSONDecodeError:
         print("Failed to decode JSON from Gemini response")
         return None
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return None
