import streamlit as st
import requests

def get_rule_based_answer(user_input, rules):
    for keyword, response in rules.items():
        if keyword.lower() in user_input.lower():
            return response
    return None

def get_claude_answer(user_input, chat_history=[]):
    try:
        headers = {
            "Authorization": f"Bearer {st.secrets['GROQ_API_KEY']}",
            "Content-Type": "application/json"
        }

        messages = [{"role": "system", "content": "You are Nexora, a friendly and intelligent AI assistant. Answer questions clearly, helpfully and conversationally."}]

        for msg in chat_history:
            messages.append({"role": msg["role"], "content": msg["content"]})

        messages.append({"role": "user", "content": user_input})

        payload = {
            "model": "llama3-70b-8192",
            "messages": messages,
            "max_tokens": 1024
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload
        )
        result = response.json()
        return result["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Oops! Something went wrong: {str(e)}"