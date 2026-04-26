import streamlit as st
import requests

def get_rule_based_answer(user_input, rules):
    user_input_lower = user_input.lower().strip()
    for keyword, response in rules.items():
        if keyword.lower().strip() == user_input_lower:
            return response
    return None

def get_claude_answer(user_input, chat_history=[]):
    try:
        api_key = st.secrets["GROQ_API_KEY"]
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        messages = [
            {
                "role": "system", 
                "content": "You are Nexora, a friendly, smart and helpful AI assistant. Give detailed, accurate and conversational answers like ChatGPT. Never say you cannot answer."
            }
        ]

        for msg in chat_history:
            if msg["role"] in ["user", "assistant"]:
                messages.append({
                    "role": msg["role"], 
                    "content": msg["content"]
                })

        messages.append({"role": "user", "content": user_input})

        payload = {
            "model": "llama3-70b-8192",
            "messages": messages,
            "max_tokens": 1024,
            "temperature": 0.7
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        result = response.json()
        
        # Debug: show full error if something goes wrong
        if "choices" not in result:
            error_msg = result.get("error", {}).get("message", str(result))
            return f"API Error: {error_msg}"
            
        return result["choices"][0]["message"]["content"]

    except requests.exceptions.Timeout:
        return "⏳ Request timed out. Please try again!"
    except Exception as e:
        return f"Oops! Something went wrong: {str(e)}"