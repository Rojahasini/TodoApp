
# 📝 Roja's TODO App

A smart, AI-powered task management application built with **Python** and **Streamlit**. 
This app combines a modern, responsive UI with AI capabilities to help you organize, prioritize, and track your daily tasks efficiently.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31%2B-ff4b4b)
![Status](https://img.shields.io/badge/Status-Active-success)

## ✨ Features

### 🎨 Modern UI & Theming
* **Dual Theme Support:** Seamless toggle between a clean **Light Mode** (Slate/White) and a sleek **Dark Mode** (Deep Blue/Grey).
* **Responsive Design:** Optimized for various screen sizes with custom CSS styling.

### 📋 Task Management
* **Dashboard View:** Separate tabs for **Pending** (🕒) and **Achieved** (✅) tasks.
* **CRUD Operations:** Easily Add, Delete, and Mark tasks as Done.
* **Undo Functionality:** Accidentally marked a task as done? Move it back to pending with one click.
* **Calendar Integration:** Intuitive date picker for setting deadlines.

### 🤖 AI Buddy (Roja AI)
* **AI Task Creation:** Let AI suggest tasks based on your goals.
* **Prioritization:** AI analyzes your list to suggest what to tackle first.
* **Daily Summaries:** Get an AI-generated summary of your workload.
* *(Note: AI features require an API key setup).*

---

## 🚀 Installation & Setup

Follow these steps to run the app locally on your machine.

### 1. Clone the Repository
```bash
git clone [https://github.com/Rojahasini/TodoApp.git](https://github.com/Rojahasini/TodoApp.git)
cd TodoApp

```

### 2. Create a Virtual Environment (Optional but Recommended)

**Windows:**

```bash
python -m venv venv
.\venv\Scripts\activate

```

**Mac/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

### 4. Set up Environment Variables

Create a `.env` file in the root directory to store your API keys securely.

```bash
# .env file
OPENAI_API_KEY=your_api_key_here

```

### 5. Run the App

```bash
streamlit run app.py

```

The app will open in your default browser at `http://localhost:8501`.

---

## 📂 Project Structure

```
TodoApp/
├── app.py              # Main application entry point (UI & Logic)
├── database.py         # SQLite database handling (CRUD operations)
├── ai_utils.py         # AI logic and API connections
├── requirements.txt    # Project dependencies
├── .env                # API Keys (Not uploaded to GitHub)
├── .gitignore          # Files to ignore (e.g., venv, .env)
└── README.md           # Project documentation

```

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/)
* **Language:** Python
* **Database:** SQLite (Built-in)
* **AI Engine:** OpenAI API / Google Gemini (configurable)

## 🛡️ Security Note

This repository utilizes a `.gitignore` file to ensure sensitive information (like API keys and virtual environment folders) is **never** uploaded to the public repository.

## 🤝 Contributing

Contributions are welcome! Please fork the repository and create a pull request with your features or fixes.

---

**Developed by Roja Hasini**
