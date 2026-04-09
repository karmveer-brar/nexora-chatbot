from transformers import pipeline

# Load Hugging Face model once
generator = pipeline("text-generation", model="gpt2")

def get_rule_based_answer(user_input, rules):
    for keyword, response in rules.items():
        if keyword.lower() in user_input.lower():
            return response
    return None

def get_hf_answer(user_input):
    response = generator(user_input, max_length=100, num_return_sequences=1)
    return response[0]["generated_text"]
