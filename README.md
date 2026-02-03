# NGK Todo Application

This project is a Todo application built using Python, SQLite, and Streamlit, developed as part of the NGK Internship technical assignment.

## Features
- Task creation, completion, and deletion
- Persistent storage using SQLite
- Clean Streamlit-based UI

## Generative AI Features
1. Natural language task creation
2. AI-based task prioritization
3. AI-generated daily productivity summary

## Architecture
- Streamlit frontend
- Python backend logic
- SQLite database
- OpenAI API for GenAI features

## How to Run
1. Install dependencies:
   pip install -r requirements.txt

2. Add OpenAI API key in `.env`:
   OPENAI_API_KEY=your_key_here

3. Run the app:
   streamlit run app.py

Note: The API key is not included in the source code as per instructions.
