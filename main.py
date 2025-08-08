from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List
from utils import process_pdf_and_create_faiss, get_relevant_chunks
from model import generate_answer

app = FastAPI()

class HackRxRequest(BaseModel):
    documents: str
    questions: list[str]

@app.post("/api/v1/hackrx/run")
async def hackrx_run(payload: HackRxRequest):
    print("Documents:", payload.documents)
    print("Questios:", payload.questions)
    try:
        index, texts = process_pdf_and_create_faiss(payload.documents)
        answers = []
        for q in payload.questions:
            context = get_relevant_chunks(index, texts, q)
            ans = generate_answer(q, context)
            answers.append(ans)
        return {"answers": answers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
