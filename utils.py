import requests
import streamlit as st

HF_API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"

def get_rule_based_answer(user_input, rules):
    for keyword, response in rules.items():
        if keyword.lower() in user_input.lower():
            return response
    return None

def get_hf_answer(user_input):
    try:
        headers = {"Authorization": f"Bearer {st.secrets['HF_TOKEN']}"}
        payload = {"inputs": user_input}
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        result = response.json()
        if isinstance(result, list) and result:
            return result[0].get("generated_text", "I'm not sure about that!")
        return "I'm thinking... try asking me again!"
    except Exception as e:
        return f"Oops! Something went wrong: {str(e)}"