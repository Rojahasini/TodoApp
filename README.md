```markdown
# 📝 Roja's TODO App

A smart, AI-powered task management application built with **Python**, **Streamlit**, and **Google Gemini**. 
This app combines a modern, responsive UI with advanced AI capabilities to help you organize, prioritize, and track your daily tasks efficiently.

## ✨ Features

### 🎨 Modern UI & Theming
* **Dual Theme Support:** Seamless toggle between a clean **Light Mode** (Slate/White) and a sleek **Dark Mode** (Deep Blue/Grey).
* **Responsive Design:** Optimized for various screen sizes with custom CSS styling.

### 📋 Task Management
* **Dashboard View:** Separate tabs for **Pending** (🕒) and **Achieved** (✅) tasks.
* **CRUD Operations:** Easily Add, Delete, and Mark tasks as Done.
* **Undo Functionality:** Accidentally marked a task as done? Move it back to pending with one click.
* **Smart Dates:** Tasks automatically sort by due dates.

### 🤖 AI Buddy (Powered by Google Gemini)
* **✨ AI Task Creation:** Describe your goal (e.g., "Plan a surprise party"), and the AI generates a structured list of tasks with due dates automatically.
* **🚀 AI Prioritization:** The AI analyzes your pending list and suggests the most urgent tasks to focus on first.
* **📅 Daily Summaries:** Get a friendly, motivational summary of your progress and remaining work.
* *(Powered by the fast and efficient `gemini-2.5-flash-lite` model)*.

---

## 📸 Screenshots

| Light Mode Dashboard | Dark Mode Dashboard |
|:---:|:---:|
| ![Light Mode](image_e2383b.png) | ![Dark Mode](image_e2385a.png) |

| AI Task Generator | AI Prioritization |
|:---:|:---:|
| ![AI Buddy](image_e24682.png) | ![Create Task](image_e251e3.png) |

*(Note: These images correspond to the files uploaded to your repository).*

---

## 🚀 Installation & Setup

Follow these steps to run the app locally on your machine.

### 1. Clone the Repository
```bash
git clone [https://github.com/Rojahasini/TodoApp.git](https://github.com/Rojahasini/TodoApp.git)
cd TodoApp

```

### 2. Create a Virtual Environment

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

Create a `.env` file in the root directory to store your Google Gemini API Key.

```bash
# .env file
GEMINI_API_KEY=your_actual_api_key_here

```

*(You can get a free key from Google AI Studio)*

### 5. Run the App

```bash
streamlit run app.py

```

The app will open in your default browser at `http://localhost:8501`.

---

## 📂 Project Structure

```
TodoApp/
├── app.py              # Main application UI & Logic
├── ai_utils.py         # Google Gemini AI integration logic
├── database.py         # SQLite database handling (CRUD)
├── requirements.txt    # Project dependencies
├── .env                # API Keys (Protected, not on GitHub)
├── .gitignore          # Security rules
└── README.md           # Documentation

```

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/)
* **Language:** Python
* **Database:** SQLite (Built-in)
* **AI Engine:** Google Gemini (using `google-generativeai` library)

## 🛡️ Security Note

This repository utilizes a `.gitignore` file to ensure sensitive information (like API keys and virtual environment folders) is **never** uploaded to the public repository.

## 🤝 Contributing

Contributions are welcome! Please fork the repository and create a pull request with your features or fixes.

---

**Developed by Roja Hasini**
