import streamlit as st
import database
import datetime

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(page_title="Roja's TODO App", page_icon="📝", layout="wide")

# ======================================================
# SESSION STATE
# ======================================================
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

# ======================================================
# 🎨 COLOR PALETTE
# ======================================================
if st.session_state.theme == "light":
    # Light Mode Colors (Clean White/Slate)
    BG_COLOR = "#F8FAFC"        # Slate-50
    CARD_BG = "#FFFFFF"         # White
    TEXT_COLOR = "#0F172A"      # Slate-900
    SUBTEXT_COLOR = "#64748B"   # Slate-500
    BORDER_COLOR = "#CBD5E1"    # Slate-300
    ACCENT_COLOR = "#2563EB"    # Blue-600
    
    # Buttons & Inputs (Force White)
    BTN_BG = "#FFFFFF"          
    BTN_TEXT = "#0F172A"        
    INPUT_BG = "#FFFFFF"
    
    SHADOW = "0 4px 6px -1px rgba(0, 0, 0, 0.1)"
    CARET_COLOR = "#0F172A"     # Dark Cursor
else:
    # Dark Mode Colors
    BG_COLOR = "#0F172A"        # Slate-900
    CARD_BG = "#1E293B"         # Slate-800
    TEXT_COLOR = "#F8FAFC"      # Slate-50
    SUBTEXT_COLOR = "#94A3B8"   # Slate-400
    BORDER_COLOR = "#334155"    # Slate-700
    ACCENT_COLOR = "#60A5FA"    # Blue-400
    
    BTN_BG = "#1E293B"          
    BTN_TEXT = "#F8FAFC"        
    INPUT_BG = "#334155"
    
    SHADOW = "0 4px 6px -1px rgba(0, 0, 0, 0.2)"
    CARET_COLOR = "#F8FAFC"     # White Cursor

# ======================================================
# 💅 CSS STYLING (FIXED CALENDAR HEADER & BUTTONS)
# ======================================================
st.markdown(f"""
<style>
    /* 1. Main App Background */
    .stApp {{
        background-color: {BG_COLOR};
        color: {TEXT_COLOR};
    }}

    /* 2. Global Text */
    p, h1, h2, h3, h4, h5, h6, span, div, label {{
        color: {TEXT_COLOR};
    }}

    /* 3. Card Container */
    .card {{
        background-color: {CARD_BG};
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        border: 1px solid {BORDER_COLOR};
        box-shadow: {SHADOW};
    }}

    /* 4. Header Container */
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

    /* 5. UNIVERSAL BUTTON FIX (Targets ALL buttons: Popover, Form, Regular) */
    button, 
    div[data-testid="stPopover"] > button,
    div[data-testid="stForm"] button {{
        background-color: {BTN_BG} !important;
        color: {BTN_TEXT} !important;
        border: 1px solid {BORDER_COLOR} !important;
        box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05);
    }}
    
    /* Hover Effects */
    button:hover, 
    div[data-testid="stPopover"] > button:hover,
    div[data-testid="stForm"] button:hover {{
        border-color: {ACCENT_COLOR} !important;
        color: {ACCENT_COLOR} !important;
        background-color: {BG_COLOR} !important;
    }}

    /* 6. INPUT FIELDS */
    .stTextInput input, 
    .stTextArea textarea, 
    .stDateInput input, 
    .stSelectbox div[data-baseweb="select"] > div {{
        background-color: {INPUT_BG} !important;
        color: {TEXT_COLOR} !important;
        border: 1px solid {BORDER_COLOR} !important;
        caret-color: {CARET_COLOR} !important;
    }}
    
    /* Widget Labels */
    .stCheckbox label p, .stRadio label p, .stTextInput label p, .stDateInput label p {{
        color: {TEXT_COLOR} !important;
    }}

    /* ============================================================ */
    /* 🛠️ SPECIFIC FIXES FOR CALENDAR & POPOVER 🛠️ */
    /* ============================================================ */

    /* A. POPOVER BODY (White Box) */
    div[data-testid="stPopoverBody"] {{
        background-color: {CARD_BG} !important;
        border: 1px solid {BORDER_COLOR} !important;
        color: {TEXT_COLOR} !important;
    }}
    div[data-testid="stPopoverBody"] > div {{
        background-color: transparent !important;
    }}

    /* B. CALENDAR HEADER FIX (The most important part!) */
    /* Forces the main calendar container to be the card color */
    div[data-baseweb="calendar"] {{
        background-color: {CARD_BG} !important;
        color: {TEXT_COLOR} !important;
        border: 1px solid {BORDER_COLOR} !important;
    }}
    
    /* Forces the Month/Year Header to be the card color (Fixes Black Header) */
    div[data-baseweb="calendar"] > div {{
        background-color: {CARD_BG} !important;
        color: {TEXT_COLOR} !important;
    }}
    
    /* Targets the text inside the header (Month Year, Arrows) */
    div[data-baseweb="calendar"] button,
    div[data-baseweb="calendar"] div {{
        color: {TEXT_COLOR} !important;
    }}

    /* Day Tiles (Standard) */
    div[data-baseweb="day"] {{
        color: {TEXT_COLOR} !important;
        background-color: transparent !important;
    }}
    
    /* Selected Day (Red/Blue Circle) */
    div[data-baseweb="day"][aria-selected="true"] {{
        background-color: {ACCENT_COLOR} !important;
        color: #ffffff !important;
    }}

    /* C. DROPDOWNS */
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

# ======================================================
# DB INIT
# ======================================================
try:
    database.create_tables()
except:
    pass

# ======================================================
# HEADER
# ======================================================
st.markdown('<div class="header">', unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns([4, 1.2, 1.2, 2, 0.6])

with c1:
    # UPDATED TITLE HERE
    st.markdown('<div class="app-title">📝 Roja\'s TODO App</div>', unsafe_allow_html=True)

with c2:
    if st.button("Dashboard", use_container_width=True):
        st.session_state.page = "Dashboard"

with c3:
    if st.button("Add Task", use_container_width=True):
        st.session_state.page = "Add Task"

with c4:
    # Popover Button (Now Fixed via CSS)
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

# ======================================================
# DASHBOARD
# ======================================================
def show_dashboard():
    st.markdown("### 📊 Task Dashboard")
    st.markdown("---")

    pending_tab, achieved_tab = st.tabs(["🕒 Pending Tasks", "✅ Achieved Tasks"])

    # -------- PENDING --------
    with pending_tab:
        tasks = database.get_tasks("pending")
        if not tasks:
            st.info("No pending tasks. You are all caught up! 🎉")
        else:
            for t in tasks:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                
                # Title
                st.markdown(f"<div style='font-weight:600; font-size:1.1rem; margin-bottom:5px;'>{t[1]}</div>", unsafe_allow_html=True)
                if t[2]:
                    st.markdown(f"<div style='color:{SUBTEXT_COLOR}; font-size:0.9rem;'>{t[2]}</div>", unsafe_allow_html=True)
                
                # Date
                st.markdown(f"<div style='color:{SUBTEXT_COLOR}; font-size:0.85rem; margin-top:10px;'>📅 Due: {t[3]}</div>", unsafe_allow_html=True)
                
                st.write("") 

                # Actions
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

    # -------- ACHIEVED --------
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

# ======================================================
# ADD TASK
# ======================================================
def show_add_task():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### ➕ Create New Task")
    
    with st.form("new_task"):
        title = st.text_input("Task Title", placeholder="e.g. Study for Interview")
        desc = st.text_area("Description", placeholder="Add details...")
        date = st.date_input("Due Date", datetime.date.today())
        
        # Submit Button (Now Fixed via CSS)
        if st.form_submit_button("Save Task", use_container_width=True):
            if title:
                database.add_task(title, desc, date.isoformat())
                st.success("Task Saved!")
                st.session_state.page = "Dashboard"
                st.rerun()
            else:
                st.warning("Please add a title.")
    st.markdown("</div>", unsafe_allow_html=True)

# ======================================================
# AI PAGE
# ======================================================
def show_ai():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"### 🤖 {st.session_state.ai_mode}")
    st.write("AI functionality is currently in beta.")
    
    if st.button("← Back to Dashboard"):
        st.session_state.page = "Dashboard"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ======================================================
# ROUTER
# ======================================================
if st.session_state.page == "Dashboard":
    show_dashboard()
elif st.session_state.page == "Add Task":
    show_add_task()
elif st.session_state.page == "AI Buddy":
    show_ai()