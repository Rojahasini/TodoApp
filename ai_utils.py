import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ai_create_tasks(user_input):
    prompt = f"""
Convert the following sentence into a JSON list of tasks.
Each task must have:
- title
- due_date (YYYY-MM-DD if mentioned, else null)

Sentence:
{user_input}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


def ai_prioritize_tasks(tasks):
    prompt = f"""
Given the following tasks, prioritize them based on urgency and due date.
Explain briefly.

Tasks:
{tasks}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


def ai_daily_summary(tasks):
    prompt = f"""
Create a daily productivity summary based on the following tasks.
Include:
- Completed tasks
- Pending tasks
- Suggested focus for today

Tasks:
{tasks}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
