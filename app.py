import streamlit as st
import json
from utils import get_response

# -------------------------------------------------------
# Page Configuration
# -------------------------------------------------------
st.set_page_config(
    page_title="Nexora Chatbot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------
# Custom CSS — cleaner, more polished UI
# -------------------------------------------------------
st.markdown("""
    <style>
        /* Main background */
        .stApp { background-color: #0f1117; }

        /* Chat container spacing */
        .block-container { padding-top: 1rem; padding-bottom: 0rem; }

        /* Hide default Streamlit header */
        header { visibility: hidden; }

        /* Custom title styling */
        .nexora-title {
            font-size: 2rem;
            font-weight: 700;
            color: #FF6B6B;
            text-align: center;
            margin-bottom: 0.2rem;
        }
        .nexora-subtitle {
            font-size: 0.9rem;
            color: #888;
            text-align: center;
            margin-bottom: 1.5rem;
        }

        /* Sidebar styling */
        .sidebar-info {
            background: #1e1e2e;
            border-radius: 10px;
            padding: 12px;
            margin-bottom: 10px;
            font-size: 0.85rem;
            color: #ccc;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# Load Rules
# -------------------------------------------------------
@st.cache_data
def load_rules():
    with open("rules.json", "r") as f:
        return json.load(f)

RULES = load_rules()

# -------------------------------------------------------
# Sidebar
# -------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/color/96/bot.png", width=70)
    st.markdown("## 🤖 Nexora Chatbot")
    st.markdown("---")
    st.markdown("**About Nexora:**")
    st.markdown("""
    - 🧠 Hybrid AI (Rules + Flan-T5)
    - 💬 Conversational memory (last 3 turns)
    - ⚡ Fast rule-based responses
    - 🆓 100% free & open-source
    """)
    st.markdown("---")
    st.markdown("**Try asking:**")
    st.markdown("""
    - *What is machine learning?*
    - *What is Python?*
    - *Tell me a joke*
    - *What is Streamlit?*
    - *Who are you?*
    """)
    st.markdown("---")

    # Clear chat button
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state["messages"] = []
        st.session_state["chat_history"] = []
        st.rerun()

    st.markdown('<div class="sidebar-info">💡 Powered by Google Flan-T5 + Custom Rules</div>', unsafe_allow_html=True)

# -------------------------------------------------------
# Main Title
# -------------------------------------------------------
st.markdown('<div class="nexora-title">🤖 Nexora Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div class="nexora-subtitle">Your free, realistic AI-powered Q&A assistant</div>', unsafe_allow_html=True)

# -------------------------------------------------------
# Session State Initialization
# -------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# -------------------------------------------------------
# Display Chat History
# -------------------------------------------------------
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"], avatar="🧑" if msg["role"] == "user" else "🤖"):
        st.markdown(msg["content"])

# -------------------------------------------------------
# Welcome Message (shown only when chat is empty)
# -------------------------------------------------------
if len(st.session_state["messages"]) == 0:
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown("👋 Hi! I'm **Nexora**, your AI assistant. Ask me anything — about tech, programming, AI, or just have a chat!")

# -------------------------------------------------------
# User Input Handler
# -------------------------------------------------------
if prompt := st.chat_input("Ask me anything..."):

    # Display user message
    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)

    # Save user message
    st.session_state["messages"].append({"role": "user", "content": prompt})

    # Generate response with typing indicator
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Nexora is thinking..."):
            answer = get_response(
                user_input=prompt,
                rules=RULES,
                chat_history=st.session_state["chat_history"]
            )
        st.markdown(answer)

    # Save assistant message
    st.session_state["messages"].append({"role": "assistant", "content": answer})

    # Update memory (conversation history for AI context)
    st.session_state["chat_history"].append({
        "user": prompt,
        "bot": answer
    })

    # Keep only last 10 turns in memory to avoid bloat
    if len(st.session_state["chat_history"]) > 10:
        st.session_state["chat_history"] = st.session_state["chat_history"][-10:]
