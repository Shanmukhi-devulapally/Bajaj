# HackRx FAISS-based Webhook
This project implements a FastAPI webhook for the HackRx competition.

## 📂 Project Structure
```
hackrx_faiss_webhook/
├── main.py
├── utils.py
├── model.py
├── requirements.txt
├── .env
└── README.md
```

## ⚙️ Installation
```bash
pip install -r requirements.txt
```
Set your OpenAI API key in `.env`:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## 🚀 Running the Webhook
```bash
uvicorn main:app --reload
```
Runs at: `http://127.0.0.1:8000/api/v1/hackrx/run`

## 🌍 Using ngrok for Public URL
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
ngrok http 8000
```
Submit: `https://<ngrok_id>.ngrok-free.app/api/v1/hackrx/run`
