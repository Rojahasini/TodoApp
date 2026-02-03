import os
import google.generativeai as genai
from dotenv import load_dotenv
import json

# Grab the keys from my .env file
load_dotenv()

# Set up the Gemini API
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def get_gemini_response(prompt):
    """My wrapper function to handle the AI calls and catch errors."""
    if not api_key:
        return "Error: I couldn't find the API Key. Need to check .env."
        
    try:
        # Using the flash-lite model because it's fast and available
        model = genai.GenerativeModel('gemini-2.5-flash-lite') 
        response = model.generate_content(prompt)
        
        if not response.text:
            return "Error: AI gave me an empty response."
            
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def ai_create_tasks(user_input):
    # Ask AI to parse the natural language into a JSON list
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
    
    # Sometimes Gemini adds markdown backticks, so I'll strip them just in case
    clean_response = response.replace("```json", "").replace("```", "").strip()
    return clean_response

def ai_prioritize_tasks(tasks):
    # Logic to ask AI for prioritization advice
    prompt = f"""
    You are a productivity expert.
    Given these tasks, prioritize them by urgency and importance.
    Return a simple text explanation, not JSON.
    
    Tasks:
    {tasks}
    """
    return get_gemini_response(prompt)

def ai_daily_summary(tasks):
    # Logic to get a nice summary and quote
    prompt = f"""
    Create a friendly daily summary of these tasks.
    Include a motivational quote.
    
    Tasks:
    {tasks}
    """
    return get_gemini_response(prompt)