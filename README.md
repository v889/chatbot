# 💬 Ask Chatbot (Streamlit + LangChain + Grok)

This is a Streamlit-based chatbot that uses LangChain with Grok's LLaMA 3 model to carry on intelligent conversations. It supports multiple chat sessions, renaming, and session management.

---

## 🚀 Features

- Multi-session chat with history
- Rename chat sessions
- Search through chats
- Uses LangChain + Grok API (LLaMA3)

---

## 📦 Requirements

Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in your project root:

```env
grok_api_key=your_actual_Grok_api_key_here
```

---

## 🏁 Run the App

Once dependencies are installed and `.env` is set:

```bash
streamlit run chatgpt.py


## 📁 Project Structure

```
.
├── chatgpt.py           # Main application
├── requirements.txt
├── .env                     # Your Grok API key
└── README.md

