# 🤖 Nexora Chatbot — Complete Upgrade Guide
### From Basic GPT-2 → Realistic AI with Flan-T5, Memory & Better UI

---

## 📋 Table of Contents
1. [What Changed & Why](#what-changed)
2. [Files Overview](#files-overview)
3. [Local Setup — Step by Step](#local-setup)
4. [Deploying to Streamlit Cloud](#streamlit-deploy)
5. [Streamlit Explained](#streamlit-explained)
6. [Testing Your Chatbot](#testing)
7. [Future Improvements](#future)

---

## 1. What Changed & Why {#what-changed}

| File | Old Version | New Version | Why It's Better |
|------|------------|-------------|-----------------|
| `utils.py` | GPT-2 (text completion) | Flan-T5 (instruction-following) | Direct, factual answers |
| `utils.py` | No memory | Last 3 turns context | Bot remembers conversation |
| `utils.py` | Exact keyword match | Exact + partial match | Catches more user inputs |
| `rules.json` | 3 rules | 55+ rules | Covers far more topics |
| `app.py` | Basic chat UI | Sidebar + memory + avatars | Professional look & feel |
| `requirements.txt` | transformers, torch | + sentencepiece | Required for Flan-T5 |

---

## 2. Files Overview {#files-overview}

```
Nexora-Chatbot/
├── app.py            ← Streamlit UI (main entry point)
├── utils.py          ← All AI logic (rules + Flan-T5 + memory)
├── rules.json        ← 55+ keyword → response mappings
└── requirements.txt  ← Python dependencies
```

### How They Work Together

```
User types message
       ↓
   app.py receives input
       ↓
   utils.get_response() is called
       ↓
   ┌─────────────────────────────┐
   │  1. Check rules.json first  │  ← Fast, deterministic
   │     (exact + partial match) │
   └────────────┬────────────────┘
                │ No match found
                ↓
   ┌─────────────────────────────┐
   │  2. Flan-T5 AI generation   │  ← Smart, contextual
   │     (with last 3 turns)     │
   └────────────┬────────────────┘
                │ Failed / empty
                ↓
   ┌─────────────────────────────┐
   │  3. Graceful fallback msg   │  ← Never crashes
   └─────────────────────────────┘
                ↓
   app.py displays response in chat
```

---

## 3. Local Setup — Step by Step {#local-setup}

### Step 1: Prerequisites
Make sure you have Python installed. Check with:
```bash
python --version
# Should show Python 3.8 or higher
```

If not installed, download from: https://python.org/downloads

---

### Step 2: Clone Your Repository
```bash
git clone https://github.com/karmveer-brar/Nexora-Chatbot.git
cd Nexora-Chatbot
```

---

### Step 3: Create a Virtual Environment (Recommended)

A virtual environment keeps your project dependencies isolated from other Python projects.

```bash
# Create virtual environment
python -m venv venv

# Activate it — Windows:
venv\Scripts\activate

# Activate it — Mac/Linux:
source venv/bin/activate

# You should now see (venv) in your terminal prompt
```

---

### Step 4: Replace Your Files

Copy the 4 new files into your project folder, replacing the old ones:
- `app.py`
- `utils.py`
- `rules.json`
- `requirements.txt`

---

### Step 5: Install Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- `streamlit` — the web UI framework
- `transformers` — Hugging Face model library
- `torch` — PyTorch (powers Flan-T5)
- `sentencepiece` — tokenizer required by Flan-T5

> ⚠️ First install takes 5–10 minutes. Flan-T5 model (~900MB) downloads automatically on first run.

---

### Step 6: Run the Chatbot
```bash
streamlit run app.py
```

Your browser will automatically open at: **http://localhost:8501**

---

### Step 7: First Run Notes
- The **first launch** will download Flan-T5 (~900MB). This happens only once — it gets cached.
- Subsequent launches are fast (model loads from cache in seconds).

---

## 4. Deploying to Streamlit Cloud {#streamlit-deploy}

Streamlit Cloud lets you host your app for FREE so anyone can use it via a URL (like your current app).

### Step 1: Push updated files to GitHub
```bash
# In your project folder (make sure virtual env is active)
git add app.py utils.py rules.json requirements.txt
git commit -m "Upgrade: Flan-T5, memory, 55+ rules, better UI"
git push origin main
```

### Step 2: Open Streamlit Cloud
Go to: https://share.streamlit.io

Log in with your GitHub account.

### Step 3: Deploy / Redeploy
- If your app is already deployed at your existing URL, click **"Reboot app"** or **"Redeploy"** — it will automatically pick up the new code from GitHub.
- If deploying fresh: click **"New app"** → select your repo → set main file as `app.py` → click **Deploy**.

### Step 4: Wait for Build
Streamlit Cloud will install your requirements and start the app. This takes 3–5 minutes on first deploy.

> ✅ Your live URL stays the same: https://nexora-chatbot-4znbiwnlbqru5nag4fz2wh.streamlit.app/

---

## 5. Streamlit Explained {#streamlit-explained}

Streamlit is what makes your chatbot look like a real web app without needing HTML, CSS, or JavaScript.

### Key Concepts You're Using

#### `st.chat_message(role)`
Displays a chat bubble. The `role` is either `"user"` or `"assistant"`.
```python
with st.chat_message("assistant", avatar="🤖"):
    st.markdown("Hello!")
```

#### `st.chat_input("placeholder")`
Renders the text input box at the bottom of the screen. Returns the user's text when they press Enter.
```python
if prompt := st.chat_input("Ask me anything..."):
    # prompt contains whatever the user typed
```

#### `st.session_state`
This is Streamlit's memory. Without it, every time the user types something, the entire page reruns and you'd lose the chat history.
```python
if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.session_state["messages"].append({"role": "user", "content": prompt})
```

#### `st.spinner("text")`
Shows a loading animation while your AI model is generating a response.
```python
with st.spinner("Nexora is thinking..."):
    answer = get_response(prompt, RULES, chat_history)
```

#### `@st.cache_data`
Prevents re-loading your `rules.json` file every single time a user sends a message.
```python
@st.cache_data
def load_rules():
    with open("rules.json", "r") as f:
        return json.load(f)
```

#### `st.sidebar`
Everything inside this block appears in the left panel.
```python
with st.sidebar:
    st.markdown("## About Nexora")
```

#### `st.rerun()`
Forces a page refresh (used when clearing chat history).
```python
if st.button("Clear Chat"):
    st.session_state["messages"] = []
    st.rerun()
```

---

## 6. Testing Your Chatbot {#testing}

After launching, test these inputs to verify everything works:

### Rule-based responses (should be instant):
| Input | Expected Response |
|-------|------------------|
| `hello` | Greeting message |
| `who are you` | Nexora identity |
| `what is python` | Python explanation |
| `what is streamlit` | Streamlit explanation |
| `tell me a joke` | Programmer joke 😄 |
| `what is the capital of india` | New Delhi |
| `thanks` | Welcome message |
| `bye` | Goodbye message |

### AI responses (Flan-T5, may take 2-4 seconds):
| Input | Expected |
|-------|----------|
| `Explain quantum physics` | Multi-sentence factual answer |
| `What is the speed of light?` | Scientific answer |
| `How does photosynthesis work?` | Biology explanation |

### Memory test:
1. Ask: `My name is Karmveer`
2. Then ask: `What is my name?`
3. The bot should reference the earlier context.

---

## 7. Future Improvements {#future}

### Easy (can do now):
- **Add more rules** — just edit `rules.json`, add more key-value pairs
- **Change the bot name/avatar** — edit the title in `app.py`
- **Add topics** — add a domain (cooking, sports, movies) by expanding rules

### Intermediate:
- **Switch to Flan-T5-Large** — replace `"google/flan-t5-base"` with `"google/flan-t5-large"` in `utils.py` for smarter answers (uses more RAM)
- **Add a feedback button** — let users upvote/downvote responses to improve quality
- **Typing speed effect** — use `st.write_stream()` to stream responses word by word

### Advanced:
- **Add RAG (Retrieval-Augmented Generation)** — connect a knowledge base (PDF, website) so the bot answers questions about YOUR specific content
- **Use LLaMA 2 or Mistral** — open-source models that give ChatGPT-level responses, free to run locally
- **Add voice input** — use `st.audio` + Whisper (OpenAI's free speech-to-text model)
- **User authentication** — different users get personalised memory

---

## 📞 Quick Reference Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py

# Push to GitHub (triggers Streamlit Cloud redeploy)
git add . && git commit -m "Update" && git push

# Deactivate virtual environment
deactivate
```

---

*Built with ❤️ by Karmveer Brar | Nexora Chatbot v2.0*
