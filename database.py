import sqlite3
from datetime import datetime

DB_NAME = "tasks.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def create_tables():
    conn = get_connection()
    with open("schema.sql", "r") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

def add_task(title, description, due_date):
    conn = get_connection()
    conn.execute(
        "INSERT INTO tasks (title, description, due_date, status, created_at) VALUES (?, ?, ?, ?, ?)",
        (title, description, due_date, "pending", datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def get_tasks(status=None):
    conn = get_connection()
    cursor = conn.cursor()
    if status:
        cursor.execute("SELECT * FROM tasks WHERE status=?", (status,))
    else:
        cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def update_task_status(task_id, status):
    conn = get_connection()
    conn.execute("UPDATE tasks SET status=? WHERE id=?", (status, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = get_connection()
    conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
