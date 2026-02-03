import streamlit as st
import database
import datetime
import ai_utils  # Importing your Gemini Brain
import json

# Configure the main page settings like title and icon
st.set_page_config(page_title="Roja's TODO App", page_icon="📝", layout="wide")

# Initialize session state to track the current page and settings
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"
if "ai_mode" not in st.session_state:
    st.session_state.ai_mode = "AI Task Creation"
if "ai_name" not in st.session_state:
    st.session_state.ai_name = "Roja AI"
if "theme" not in st.session_state:
    st.session_state.theme = "light"

def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

# Define color palettes for light and dark modes
if st.session_state.theme == "light":
    BG_COLOR = "#F8FAFC"        
    CARD_BG = "#FFFFFF"         
    TEXT_COLOR = "#0F172A"      
    SUBTEXT_COLOR = "#64748B"   
    BORDER_COLOR = "#CBD5E1"    
    ACCENT_COLOR = "#2563EB"    
    BTN_BG = "#FFFFFF"          
    BTN_TEXT = "#0F172A"        
    INPUT_BG = "#FFFFFF"
    SHADOW = "0 4px 6px -1px rgba(0, 0, 0, 0.1)"
    CARET_COLOR = "#0F172A"
else:
    BG_COLOR = "#0F172A"        
    CARD_BG = "#1E293B"         
    TEXT_COLOR = "#F8FAFC"      
    SUBTEXT_COLOR = "#94A3B8"   
    BORDER_COLOR = "#334155"    
    ACCENT_COLOR = "#60A5FA"    
    BTN_BG = "#1E293B"          
    BTN_TEXT = "#F8FAFC"        
    INPUT_BG = "#334155"
    SHADOW = "0 4px 6px -1px rgba(0, 0, 0, 0.2)"
    CARET_COLOR = "#F8FAFC"

# Apply custom CSS to style buttons, cards, and inputs
st.markdown(f"""
<style>
    .stApp {{ background-color: {BG_COLOR}; color: {TEXT_COLOR}; }}
    p, h1, h2, h3, h4, h5, h6, span, div, label {{ color: {TEXT_COLOR}; }}
    .card {{ background-color: {CARD_BG}; padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem; border: 1px solid {BORDER_COLOR}; box-shadow: {SHADOW}; }}
    .header {{ background-color: {CARD_BG}; padding: 0.75rem 1.25rem; border-radius: 12px; margin-bottom: 2rem; border: 1px solid {BORDER_COLOR}; display: flex; align-items: center; justify-content: space-between; box-shadow: {SHADOW}; }}
    .app-title {{ font-size: 1.25rem; font-weight: 700; color: {TEXT_COLOR}; }}
    
    /* Button Overrides */
    button, div[data-testid="stPopover"] > button, div[data-testid="stForm"] button {{ background-color: {BTN_BG} !important; color: {BTN_TEXT} !important; border: 1px solid {BORDER_COLOR} !important; box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05); }}
    button:hover, div[data-testid="stPopover"] > button:hover, div[data-testid="stForm"] button:hover {{ border-color: {ACCENT_COLOR} !important; color: {ACCENT_COLOR} !important; background-color: {BG_COLOR} !important; }}
    
    /* Inputs */
    .stTextInput input, .stTextArea textarea, .stDateInput input, .stSelectbox div[data-baseweb="select"] > div {{ background-color: {INPUT_BG} !important; color: {TEXT_COLOR} !important; border: 1px solid {BORDER_COLOR} !important; caret-color: {CARET_COLOR} !important; }}
    .stCheckbox label p, .stRadio label p, .stTextInput label p, .stDateInput label p {{ color: {TEXT_COLOR} !important; }}

    /* Popover & Calendar Fixes */
    div[data-testid="stPopoverBody"] {{ background-color: {CARD_BG} !important; border: 1px solid {BORDER_COLOR} !important; color: {TEXT_COLOR} !important; }}
    div[data-testid="stPopoverBody"] > div {{ background-color: transparent !important; }}
    div[data-baseweb="calendar"] {{ background-color: {CARD_BG} !important; color: {TEXT_COLOR} !important; border: 1px solid {BORDER_COLOR} !important; }}
    div[data-baseweb="calendar"] > div {{ background-color: {CARD_BG} !important; color: {TEXT_COLOR} !important; }}
    div[data-baseweb="calendar"] button, div[data-baseweb="calendar"] div {{ color: {TEXT_COLOR} !important; }}
    div[data-baseweb="day"] {{ color: {TEXT_COLOR} !important; background-color: transparent !important; }}
    div[data-baseweb="day"][aria-selected="true"] {{ background-color: {ACCENT_COLOR} !important; color: #ffffff !important; }}
    ul[data-baseweb="menu"] {{ background-color: {CARD_BG} !important; color: {TEXT_COLOR} !important; border: 1px solid {BORDER_COLOR} !important; }}
    li[data-baseweb="option"] {{ color: {TEXT_COLOR} !important; }}
</style>
""", unsafe_allow_html=True)

# Make sure the database exists
try:
    database.create_tables()
except:
    pass

# Create the top navigation bar with title and buttons
st.markdown('<div class="header">', unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns([4, 1.2, 1.2, 2, 0.6])

with c1:
    st.markdown('<div class="app-title">📝 Roja\'s TODO App</div>', unsafe_allow_html=True)
with c2:
    if st.button("Dashboard", use_container_width=True):
        st.session_state.page = "Dashboard"
with c3:
    if st.button("Add Task", use_container_width=True):
        st.session_state.page = "Add Task"
with c4:
    with st.popover(f"🤖 {st.session_state.ai_name}", use_container_width=True):
        st.markdown("**AI Settings**")
        st.session_state.ai_name = st.text_input("Name", st.session_state.ai_name)
        st.radio("Features", ["AI Task Creation", "AI Prioritization", "AI Daily Summary"], key="ai_mode")
        if st.button("Do it with AI!", use_container_width=True):
            st.session_state.page = "AI Buddy"
            st.rerun()
with c5:
    icon = "🌙" if st.session_state.theme == "light" else "☀️"
    if st.button(icon, use_container_width=True):
        toggle_theme()
        st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# Function to display the main dashboard with task lists
def show_dashboard():
    st.markdown("### 📊 Task Dashboard")
    st.markdown("---")
    pending_tab, achieved_tab = st.tabs(["🕒 Pending Tasks", "✅ Achieved Tasks"])

    with pending_tab:
        tasks = database.get_tasks("pending")
        if not tasks:
            st.info("No pending tasks. You are all caught up! 🎉")
        else:
            for t in tasks:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown(f"<div style='font-weight:600; font-size:1.1rem; margin-bottom:5px;'>{t[1]}</div>", unsafe_allow_html=True)
                if t[2]: st.markdown(f"<div style='color:{SUBTEXT_COLOR}; font-size:0.9rem;'>{t[2]}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='color:{SUBTEXT_COLOR}; font-size:0.85rem; margin-top:10px;'>📅 Due: {t[3]}</div>", unsafe_allow_html=True)
                st.write("") 
                c_check, c_bin = st.columns([4, 0.5])
                with c_check:
                    if st.checkbox("Mark as Done", key=f"done_{t[0]}"):
                        database.update_task_status(t[0], "completed")
                        st.rerun()
                with c_bin:
                    if st.button("🗑️", key=f"del_{t[0]}"):
                        database.delete_task(t[0])
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True) 

    with achieved_tab:
        tasks = database.get_tasks("completed")
        if not tasks:
            st.info("No completed tasks yet.")
        else:
            for t in tasks:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown(f"<div style='font-weight:600; font-size:1.1rem; text-decoration: line-through; opacity: 0.6;'>✅ {t[1]}</div>", unsafe_allow_html=True)
                st.write("") 
                c_undo, c_del = st.columns([1, 4])
                with c_undo:
                    if st.button("↩️ Undo", key=f"undo_{t[0]}"):
                        database.update_task_status(t[0], "pending")
                        st.rerun()
                with c_del:
                    if st.button("🗑️", key=f"del2_{t[0]}"):
                        database.delete_task(t[0])
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

# Function to display the add task form
def show_add_task():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### ➕ Create New Task")
    with st.form("new_task"):
        title = st.text_input("Task Title", placeholder="e.g. Study for Interview")
        desc = st.text_area("Description", placeholder="Add details...")
        date = st.date_input("Due Date", datetime.date.today())
        if st.form_submit_button("Save Task", use_container_width=True):
            if title:
                database.add_task(title, desc, date.isoformat())
                st.success("Task Saved!")
                st.session_state.page = "Dashboard"
                st.rerun()
            else:
                st.warning("Please add a title.")
    st.markdown("</div>", unsafe_allow_html=True)

# Function to handle AI features like task generation and prioritization
def show_ai():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"### 🤖 {st.session_state.ai_mode}")
    
    # Feature 1: AI Task Creation
    if st.session_state.ai_mode == "AI Task Creation":
        st.write("Describe what you need to do, and I'll create the tasks for you.")
        user_input = st.text_area("What's on your mind?", height=100, placeholder="e.g. Plan a surprise party for dad.")
        
        if st.button("✨ Generate Tasks", use_container_width=True):
            if user_input.strip():
                with st.spinner("Roja AI is thinking..."):
                    try:
                        # Call the Gemini Brain
                        raw_response = ai_utils.ai_create_tasks(user_input)
                        
                        # DEBUG: Check if AI sent an error message directly
                        if raw_response.startswith("Error:"):
                            st.error(raw_response)
                        else:
                            # Clean up the JSON (Gemini sometimes adds ```json markers)
                            clean_json = raw_response.replace("```json", "").replace("```", "").strip()
                            
                            # Parse JSON
                            new_tasks = json.loads(clean_json)
                            
                            # Save to Database
                            count = 0
                            for task in new_tasks:
                                d_date = task.get("due_date")
                                if not d_date:
                                    d_date = datetime.date.today().isoformat()
                                database.add_task(task["title"], "AI Generated", d_date)
                                count += 1
                            
                            st.success(f"Successfully created {count} tasks!")
                            st.balloons()
                            
                    except json.JSONDecodeError:
                        st.error("The AI response format was incorrect. Please try again.")
                        with st.expander("Debugging Info"):
                            st.code(raw_response)
                    except Exception as e:
                        st.error(f"System Error: {str(e)}")
            else:
                st.warning("Please enter some text first.")

    # Feature 2: Prioritization
    elif st.session_state.ai_mode == "AI Prioritization":
        st.write("I will analyze your pending tasks and suggest what to focus on.")
        tasks = database.get_tasks("pending")
        if not tasks:
            st.info("No tasks to prioritize.")
        else:
            task_list_str = "\n".join([f"- {t[1]} (Due: {t[3]})" for t in tasks])
            if st.button("🚀 Prioritize My Day", use_container_width=True):
                with st.spinner("Analyzing..."):
                    response = ai_utils.ai_prioritize_tasks(task_list_str)
                    st.markdown("### 💡 AI Suggestions")
                    st.info(response)

    # Feature 3: Daily Summary
    elif st.session_state.ai_mode == "AI Daily Summary":
        st.write("Get a summary of your progress.")
        pending = database.get_tasks("pending")
        completed = database.get_tasks("completed")
        
        all_tasks_str = "PENDING:\n" + "\n".join([f"- {t[1]}" for t in pending])
        all_tasks_str += "\n\nCOMPLETED:\n" + "\n".join([f"- {t[1]}" for t in completed])
        
        if st.button("📝 Generate Summary", use_container_width=True):
            with st.spinner("Summarizing..."):
                response = ai_utils.ai_daily_summary(all_tasks_str)
                st.markdown("### 📅 Daily Report")
                st.success(response)

    if st.button("← Back to Dashboard"):
        st.session_state.page = "Dashboard"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# Determine which page to show based on session state
if st.session_state.page == "Dashboard":
    show_dashboard()
elif st.session_state.page == "Add Task":
    show_add_task()
elif st.session_state.page == "AI Buddy":
    show_ai()