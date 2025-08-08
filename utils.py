import requests
import tempfile
import fitz  # PyMuPDF
import faiss
import numpy as np
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def download_pdf(url):
    response = requests.get(url)
    response.raise_for_status()
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    temp_file.write(response.content)
    temp_file.close()
    return temp_file.name

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def chunk_text(text, chunk_size=500):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def embed_text(text_list):
    embeddings = []
    for chunk in text_list:
        resp = client.embeddings.create(model="text-embedding-3-small", input=chunk)
        embeddings.append(resp.data[0].embedding)
    return np.array(embeddings).astype("float32")

def process_pdf_and_create_faiss(url):
    pdf_path = download_pdf(url)
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text)
    embeddings = embed_text(chunks)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index, chunks

def get_relevant_chunks(index, texts, query, top_k=3):
    query_vec = embed_text([query])
    D, I = index.search(query_vec, top_k)
    return " ".join([texts[i] for i in I[0]])
