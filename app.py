import streamlit as st
import database
import datetime

# Configure the main page settings like title and icon
st.set_page_config(page_title="Roja's TODO App", page_icon="📝", layout="wide")

# Initialize the session state to keep track of the current page and theme
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

# Define the color palettes for light and dark mode
if st.session_state.theme == "light":
    # Colors for light mode
    BG_COLOR = "#F8FAFC"        
    CARD_BG = "#FFFFFF"         
    TEXT_COLOR = "#0F172A"      
    SUBTEXT_COLOR = "#64748B"   
    BORDER_COLOR = "#CBD5E1"    
    ACCENT_COLOR = "#2563EB"    
    
    # Specific overrides for buttons and inputs
    BTN_BG = "#FFFFFF"          
    BTN_TEXT = "#0F172A"        
    INPUT_BG = "#FFFFFF"
    
    SHADOW = "0 4px 6px -1px rgba(0, 0, 0, 0.1)"
    CARET_COLOR = "#0F172A"
else:
    # Colors for dark mode
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

# Apply custom CSS to make the app look better and fix some Streamlit quirks
st.markdown(f"""
<style>
    /* Set the main background color */
    .stApp {{
        background-color: {BG_COLOR};
        color: {TEXT_COLOR};
    }}

    /* Force all text elements to use our theme color */
    p, h1, h2, h3, h4, h5, h6, span, div, label {{
        color: {TEXT_COLOR};
    }}

    /* Style the cards that hold content */
    .card {{
        background-color: {CARD_BG};
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        border: 1px solid {BORDER_COLOR};
        box-shadow: {SHADOW};
    }}

    /* Style the top header bar */
    .header {{
        background-color: {CARD_BG};
        padding: 0.75rem 1.25rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        border: 1px solid {BORDER_COLOR};
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: {SHADOW};
    }}
    .app-title {{
        font-size: 1.25rem;
        font-weight: 700;
        color: {TEXT_COLOR};
    }}

    /* Override default button styles to match our theme */
    button, 
    div[data-testid="stPopover"] > button,
    div[data-testid="stForm"] button {{
        background-color: {BTN_BG} !important;
        color: {BTN_TEXT} !important;
        border: 1px solid {BORDER_COLOR} !important;
        box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05);
    }}
    
    /* Add hover effects to buttons */
    button:hover, 
    div[data-testid="stPopover"] > button:hover,
    div[data-testid="stForm"] button:hover {{
        border-color: {ACCENT_COLOR} !important;
        color: {ACCENT_COLOR} !important;
        background-color: {BG_COLOR} !important;
    }}

    /* Style input fields and text areas */
    .stTextInput input, 
    .stTextArea textarea, 
    .stDateInput input, 
    .stSelectbox div[data-baseweb="select"] > div {{
        background-color: {INPUT_BG} !important;
        color: {TEXT_COLOR} !important;
        border: 1px solid {BORDER_COLOR} !important;
        caret-color: {CARET_COLOR} !important;
    }}
    
    /* Ensure widget labels are visible */
    .stCheckbox label p, .stRadio label p, .stTextInput label p, .stDateInput label p {{
        color: {TEXT_COLOR} !important;
    }}

    /* Fix the popover background color so it isn't black */
    div[data-testid="stPopoverBody"] {{
        background-color: {CARD_BG} !important;
        border: 1px solid {BORDER_COLOR} !important;
        color: {TEXT_COLOR} !important;
    }}
    div[data-testid="stPopoverBody"] > div {{
        background-color: transparent !important;
    }}

    /* Fix the calendar contrast issues in Light Mode */
    div[data-baseweb="calendar"] {{
        background-color: {CARD_BG} !important;
        color: {TEXT_COLOR} !important;
        border: 1px solid {BORDER_COLOR} !important;
    }}
    
    /* Style the calendar header (Month/Year) */
    div[data-baseweb="calendar"] > div {{
        background-color: {CARD_BG} !important;
        color: {TEXT_COLOR} !important;
    }}
    
    /* Color the text inside the calendar */
    div[data-baseweb="calendar"] button,
    div[data-baseweb="calendar"] div {{
        color: {TEXT_COLOR} !important;
    }}

    /* Make day tiles transparent by default */
    div[data-baseweb="day"] {{
        color: {TEXT_COLOR} !important;
        background-color: transparent !important;
    }}
    
    /* Highlight the selected day */
    div[data-baseweb="day"][aria-selected="true"] {{
        background-color: {ACCENT_COLOR} !important;
        color: #ffffff !important;
    }}

    /* Fix dropdown menus so they match the theme */
    ul[data-baseweb="menu"] {{
        background-color: {CARD_BG} !important;
        color: {TEXT_COLOR} !important;
        border: 1px solid {BORDER_COLOR} !important;
    }}
    li[data-baseweb="option"] {{
        color: {TEXT_COLOR} !important;
    }}

</style>
""", unsafe_allow_html=True)

# Make sure the database exists before we try to use it
try:
    database.create_tables()
except:
    pass

# Create the top header bar with title and navigation buttons
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
    # Popover menu for AI settings
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

# Function to show the main dashboard
def show_dashboard():
    st.markdown("### 📊 Task Dashboard")
    st.markdown("---")

    pending_tab, achieved_tab = st.tabs(["🕒 Pending Tasks", "✅ Achieved Tasks"])

    # Show the pending tasks tab
    with pending_tab:
        tasks = database.get_tasks("pending")
        if not tasks:
            st.info("No pending tasks. You are all caught up! 🎉")
        else:
            for t in tasks:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                
                # Show title and description
                st.markdown(f"<div style='font-weight:600; font-size:1.1rem; margin-bottom:5px;'>{t[1]}</div>", unsafe_allow_html=True)
                if t[2]:
                    st.markdown(f"<div style='color:{SUBTEXT_COLOR}; font-size:0.9rem;'>{t[2]}</div>", unsafe_allow_html=True)
                
                # Show due date
                st.markdown(f"<div style='color:{SUBTEXT_COLOR}; font-size:0.85rem; margin-top:10px;'>📅 Due: {t[3]}</div>", unsafe_allow_html=True)
                
                st.write("") 

                # Buttons to complete or delete the task
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

    # Show the completed tasks tab
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

# Function to display the form for adding a new task
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

# Placeholder for the AI features page
def show_ai():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"### 🤖 {st.session_state.ai_mode}")
    st.write("AI functionality is currently in beta.")
    
    if st.button("← Back to Dashboard"):
        st.session_state.page = "Dashboard"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# Determine which page to show based on the current state
if st.session_state.page == "Dashboard":
    show_dashboard()
elif st.session_state.page == "Add Task":
    show_add_task()
elif st.session_state.page == "AI Buddy":
    show_ai()