import os
import google.generativeai as genai
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Configure the Google AI
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def get_gemini_response(prompt):
    """Helper function to talk to Gemini safely"""
    if not api_key:
        return "Error: API Key not found. Check your .env file."
        
    try:
        # --- UPDATED MODEL NAME HERE ---
        # We are using the model found in your specific list:
        model = genai.GenerativeModel('gemini-2.5-flash-lite') 
        response = model.generate_content(prompt)
        
        if not response.text:
            return "Error: Empty response from AI."
            
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def ai_create_tasks(user_input):
    prompt = f"""
    You are a task management assistant.
    Extract tasks from the user's input and return them as a JSON list.
    
    Rules:
    1. Return ONLY raw JSON. No Markdown formatting (no ```json or ```).
    2. Each item must have "title" (string) and "due_date" (string YYYY-MM-DD or null).
    3. If you cannot find tasks, return an empty list: []

    User Input: "{user_input}"
    """
    response = get_gemini_response(prompt)
    
    # Clean up response
    clean_response = response.replace("```json", "").replace("```", "").strip()
    return clean_response

def ai_prioritize_tasks(tasks):
    prompt = f"""
    You are a productivity expert.
    Given these tasks, prioritize them by urgency and importance.
    Return a simple text explanation, not JSON.
    
    Tasks:
    {tasks}
    """
    return get_gemini_response(prompt)

def ai_daily_summary(tasks):
    prompt = f"""
    Create a friendly daily summary of these tasks.
    Include a motivational quote.
    
    Tasks:
    {tasks}
    """
    return get_gemini_response(prompt)