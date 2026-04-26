import streamlit as st
import json
from utils import get_rule_based_answer, get_hf_answer

# Load rules
with open("rules.json", "r") as f:
    RULES = json.load(f)

st.set_page_config(page_title="Nexora Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 Nexora Chatbot")
st.write("Your free, realistic Q&A assistant powered by hybrid AI logic.")

# Chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Ask me anything..."):
    st.session_state["messages"].append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Nexora is thinking..."):
        rule_answer = get_rule_based_answer(prompt, RULES)
        if rule_answer:
            answer = rule_answer
        else:
            answer = get_hf_answer(prompt)

    st.session_state["messages"].append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)