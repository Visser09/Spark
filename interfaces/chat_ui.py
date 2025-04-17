import streamlit as st
import sys
import os
import json
from core.prompt_builder import build_prompt

# Add the root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from core.spark_brain import SparkBrain



# Initialize SparkBrain
if "spark" not in st.session_state:
    st.session_state["spark"] = SparkBrain()
spark = st.session_state["spark"]

# Memory bank directory
CHAT_HISTORY_DIR = "memory_bank"
os.makedirs(CHAT_HISTORY_DIR, exist_ok=True)

# Utility: Load chat history summaries
def load_chat_summaries():
    summaries = []
    for file in os.listdir(CHAT_HISTORY_DIR):
        if file.endswith(".json"):
            with open(os.path.join(CHAT_HISTORY_DIR, file), "r") as f:
                data = json.load(f)
                if isinstance(data, dict) and "history" in data and data["history"]:
                    last_entry = data["history"][-1]
                    summary = summarize_title(last_entry["user"] + " " + last_entry["spark"])
                    summaries.append((file.replace(".json", ""), summary))
    return summaries

# Utility: Summarize title for chat
def summarize_title(text):
    if "bee" in text.lower():
        return "🐝 Bee Adventures"
    elif "space" in text.lower():
        return "🚀 Space Exploration"
    elif "story" in text.lower():
        return "📖 Story Time"
    else:
        return "💡 Curiosity Chat"

# Streamlit UI setup
st.set_page_config(page_title="Spark - Curiosity Companion", page_icon="✨", layout="wide")

# Sidebar
with st.sidebar:
    st.title("✨ Spark Menu")
    if st.button("New Chat"):
        st.session_state["spark"] = SparkBrain()
        st.rerun()


    if st.button("Show Top Interests"):
        interests = spark.memory.top_interests()
        st.info(f"Top Interests: {', '.join(interests) if interests else 'No interests yet!'}")

    if st.button("Story Generator"):
        st.session_state["story_mode"] = True

    if st.button("Random Fun Fact"):
        from core.curiosity import pick_hook
        st.success(pick_hook())

    st.markdown("---")
    st.markdown("### 🗂️ Chat History")
    for file, summary in load_chat_summaries():
        if st.button(summary, key=file):
            # Load selected chat history
            spark.memory.path = os.path.join(CHAT_HISTORY_DIR, f"{file}.json")
            spark.memory.data = spark.memory._load()
            st.rerun()


st.title("✨ Spark - Curiosity Companion")

# Chat Interface
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

for msg in st.session_state["chat_history"]:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Spark:** {msg['content']}")



# Chat input section with form
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("What are you curious about today?", key="input_box")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    prompt = build_prompt(user_input, spark.memory)
    response = spark.model.generate(prompt)

    st.session_state["chat_history"].append({"role": "user", "content": user_input})
    st.session_state["chat_history"].append({"role": "spark", "content": response})
    spark.memory.update(user_input, response)

    st.rerun()

