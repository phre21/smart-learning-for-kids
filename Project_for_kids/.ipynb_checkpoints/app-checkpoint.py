import streamlit as st
import os
import json
from datetime import datetime
import pandas as pd

# --- Configuration ---
st.set_page_config(page_title="📚 Smart Learning for Kids", page_icon="📖")
audio_dir = "audio"
PARENT_PASSWORD = "bdu2025"
users_file = "data/users.json"
progress_file = "data/progress.json"

# --- Load and Save Users ---
def load_users():
    if os.path.exists(users_file):
        try:
            with open(users_file, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_user(user):
    users = load_users()
    users.append(user)
    with open(users_file, "w") as f:
        json.dump(users, f, indent=4)

# --- Custom CSS for Styling ---
st.markdown("""
    <style>
        .big-font {
            font-size: 32px !important;
            font-weight: bold;
            color: #2E86C1;
            text-align: center;
        }

        .radio-button label {
            display: block;
            background-color: #f9e79f;
            color: #2e4053;
            padding: 15px 20px;
            margin: 10px 0;
            border-radius: 15px;
            font-size: 22px;
            font-weight: bold;
            cursor: pointer;
            border: 3px solid #f4d03f;
            transition: background-color 0.3s ease;
        }

        .radio-button label:hover {
            background-color: #f1c40f;
            color: white;
        }

        div.stButton > button {
            background-color: #2ECC71;
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 24px;
            font-weight: bold;
            border-radius: 40px;
            margin: 30px auto;
            display: block;
            transition: background-color 0.3s ease;
        }

        div.stButton > button:hover {
            background-color: #27AE60;
        }

        .register-button button {
            background-color: #27ae60;
            color: white;
            padding: 12px 24px;
            font-size: 20px;
            font-weight: bold;
            border-radius: 10px;
            margin-top: 10px;
            margin-bottom: 25px;
            border: none;
        }

        .register-button button:hover {
            background-color: #219150;
        }
    </style>
""", unsafe_allow_html=True)

# --- Header with Logos ---
col1, col2, col3 = st.columns([1, 6, 1])
with col1:
    if os.path.exists("mint_logo.jpg"):
        st.image("mint_logo.jpg", width=100, caption="MiNT")
    else:
        st.warning("⚠️ mint_logo.jpg not found")
with col2:
    st.markdown("<h1 class='big-font'>📚 Smart Learning Assistant for Kids</h1>", unsafe_allow_html=True)
with col3:
    if os.path.exists("bahir_dar.jpg"):
        st.image("bahir_dar.jpg", width=100, caption="BDU")
    else:
        st.warning("⚠️ bahir_dar.jpg not found")

# --- Top Buttons: Register Child & Parent Dashboard ---
if "show_register" not in st.session_state:
    st.session_state.show_register = False
if "show_parent_dashboard" not in st.session_state:
    st.session_state.show_parent_dashboard = False
if "parent_logged_in" not in st.session_state:
    st.session_state.parent_logged_in = False

cols = st.columns([1,1])
with cols[0]:
    if st.button("📝 Register New Child", key="register_btn"):
        st.session_state.show_register = not st.session_state.show_register
        if st.session_state.show_register:
            st.session_state.show_parent_dashboard = False
            st.session_state.parent_logged_in = False

with cols[1]:
    if st.button("👨‍👩‍👧 Parent Dashboard", key="parent_dashboard_btn"):
        st.session_state.show_parent_dashboard = not st.session_state.show_parent_dashboard
        if st.session_state.show_parent_dashboard:
            st.session_state.show_register = False

# --- Show Registration Form ---
if st.session_state.show_register:
    st.markdown("### 🧒 Child Registration Form")
    with st.form("register_form"):
        child_name = st.text_input("👶 Child Name")
        parent_name = st.text_input("👨 Parent or Guardian Name")
        password = st.text_input("🔐 Password", type="password")
        age_group = st.selectbox("🎂 Age Group", ["1-3", "4-5"])
        submitted = st.form_submit_button("Register")

        if submitted:
            if not child_name or not parent_name or not password:
                st.warning("⚠️ Please fill all fields.")
            else:
                new_user = {
                    "child_name": child_name,
                    "parent_name": parent_name,
                    "password": password,
                    "age_group": age_group,
                    "registered_at": str(datetime.now()),
                }
                save_user(new_user)
                st.success(f"✅ {child_name} has been registered successfully!")

# --- Show Parent Dashboard ---
if st.session_state.show_parent_dashboard:
    st.subheader("🔒 Parent Login")
    password = st.text_input("Enter Parent Password", type="password", key="parent_password")

    if password == PARENT_PASSWORD:
        st.success("✅ Login successful!")
        st.session_state.parent_logged_in = True
    elif password and password != PARENT_PASSWORD:
        st.error("❌ Incorrect password")

    if st.session_state.parent_logged_in:
        st.subheader("📊 Parent Dashboard")
        st.markdown("Track your child's learning progress.")

        # Example progress data for charts
        subjects = ["Numbering", "English", "Amharic"]
        progress_percentages = [80, 50, 30]  # Example data (% completed)

        progress_df = pd.DataFrame({
            "Subject": subjects,
            "Progress (%)": progress_percentages
        })

        st.markdown("### 📈 Progress by Subject")
        st.bar_chart(progress_df.set_index("Subject"))

        # Progress trend over 4 weeks
        weeks = ["Week 1", "Week 2", "Week 3", "Week 4"]
        progress_trends = {
            "Numbering": [20, 40, 60, 80],
            "English": [10, 20, 35, 50],
            "Amharic": [5, 15, 25, 30]
        }
        trends_df = pd.DataFrame(progress_trends, index=weeks)

        st.markdown("### 📊 Progress Trend Over Time")
        st.line_chart(trends_df)

# --- Mode Selection (hide if register or parent dashboard open) ---
if not (st.session_state.show_register or st.session_state.show_parent_dashboard):
    st.markdown("### 🎮 Choose How You Want to Learn")
    with st.container():
        st.markdown('<div class="radio-button">', unsafe_allow_html=True)
        mode = st.radio(
            "Select one:",
            ["🎧 Audio", "🎬 Video", "❓ Quiz"],
            key="learning_mode",
            index=0,
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Age & Subject Selection ---
    st.markdown("### 👶 Select Your Age Group")
    age = st.selectbox("", ["1-3", "4-5"])

    st.markdown("### 📘 Pick a Subject")
    subject = st.selectbox("", ["Numbering", "English", "Amharic"])

    if st.button("Start Learning!"):
        st.session_state.started = True
        st.session_state.submitted = False
        st.session_state.user_answer = None

# --- Lessons Data ---
lessons = {
    "1-3": {
        "Numbering": {
            "audio": os.path.join(audio_dir, "1-3_numbering.mp3"),
            "video": "https://www.youtube.com/embed/1H0Sk-5n5K8",
            "question": "What number comes after three?",
            "options": ["Four", "Five", "Two"],
            "answer": "Four"
        },
        "English": {
            "audio": os.path.join(audio_dir, "1-3_english_alphabet.mp3"),
            "video": "https://www.youtube.com/embed/D0Ajq682yrA",
            "question": "What letter comes after A?",
            "options": ["B", "C", "Z"],
            "answer": "B"
        },
        "Amharic": {
            "audio": os.path.join(audio_dir, "1-3_amharic_alphabet.mp3"),
            "video":  "https://www.youtube.com/embed/bsp3m7DX8JQ",
            "question": "ሀ በኋላ ምን ነው?",
            "options": ["ለ", "ሐ", "ሁ"],
            "answer": "ለ"
        }
    },
    "4-5": {
        "Numbering": {
            "audio": os.path.join(audio_dir, "4-5_numbering.mp3"),
            "video": "https://www.youtube.com/embed/2RQYoL_4Sp4",
            "question": "What number comes after ten?",
            "options": ["Eleven", "Nine", "Twenty"],
            "answer": "Eleven"
        },
        "English": {
            "audio": os.path.join(audio_dir, "4-5_english_words.mp3"),
            "video": "https://www.youtube.com/embed/D0Ajq682yrA",
            "question": "Which word starts with D?",
            "options": ["Apple", "Dog", "Fish"],
            "answer": "Dog"
        },
        "Amharic": {
            "audio": os.path.join(audio_dir, "4-5_amharic_words.mp3"),
            "video": "https://www.youtube.com/embed/GPlrz9Z0rU8",
            "question": "ከነሐሴ በኋላ ምን ነው?",
            "options": ["መስከረም", "ጷግሜ", "ሐምሌ"],
            "answer": "መስከረም"
        }
    }
}

# --- Learning Content ---
if st.session_state.get("started", False) and not (st.session_state.show_register or st.session_state.show_parent_dashboard):
    if age in lessons and subject in lessons[age]:
        lesson = lessons[age][subject]

        mode = st.session_state.get("learning_mode", "🎧 Audio")

        if mode == "🎧 Audio":
            st.subheader("🎧 Listen and Learn")
            if os.path.exists(lesson["audio"]):
                with open(lesson["audio"], "rb") as f:
                    st.audio(f.read(), format="audio/mp3")
            else:
                st.warning("🚫 Audio file not found.")

        elif mode == "🎬 Video":
            st.subheader("🎬 Watch a Video")
            st.video(lesson["video"])
            st.caption("👀 Watch carefully, then take the quiz!")

        elif mode == "❓ Quiz":
            st.subheader("❓ Quiz Time!")
            st.write("💬", lesson["question"])
            user_answer = st.radio("Choose one:", lesson["options"], key="quiz")

            if st.button("Submit Answer"):
                st.session_state.submitted = True
                st.session_state.user_answer = user_answer

            if st.session_state.submitted:
                if st.session_state.user_answer == lesson["answer"]:
                    st.success("✅ አዎ ትክክል ነው!")
                    if os.path.exists("audio/correct_amharic.mp3"):
                        with open("audio/correct_amharic.mp3", "rb") as f:
                            st.audio(f.read(), format="audio/mp3")
                else:
                    st.error("❌ ስህተት ነው፣ እባኮትን እንደገና ይሞክሩ።")
                    if os.path.exists("audio/wrong_amharic.mp3"):
                        with open("audio/wrong_amharic.mp3", "rb") as f:
                            st.audio(f.read(), format="audio/mp3")
    else:
        st.info("🚧 No content available yet for this selection.")

# --- Footer ---
st.markdown("---")
st.markdown("<center><small>Made with ❤️ by BDU Students for the Ministry of Innovation and Technology & Bahir Dar University</small></center>", unsafe_allow_html=True)
