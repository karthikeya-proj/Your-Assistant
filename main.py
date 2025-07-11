import os
import pdfplumber
import fitz  # PyMuPDF (still needed for OCR fallback)
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from modules.ollama_qa import create_query_engine, ask_query
from pdf2image import convert_from_path
import pytesseract
from PIL import Image

# ---------------- FastAPI Setup ----------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "data/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------------- Request Model ----------------
class QueryRequest(BaseModel):
    question: str
    filename: str
    model: str

@app.get("/")
def root():
    return {"message": "Backend is running."}

# ---------------- Text Extraction ----------------

# First try: Extract using pdfplumber (text-based PDF)
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
    return text.strip()

# Fallback: OCR using Tesseract if no text found
def extract_text_with_ocr(pdf_path):
    images = convert_from_path(pdf_path)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img, lang="eng") + "\n"
    return text.strip()

def get_clean_text(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    if not text:
        print("⚠️ No text found with pdfplumber. Falling back to OCR...")
        text = extract_text_with_ocr(pdf_path)
    return text

# ---------------- Upload Endpoint ----------------
@app.post("/upload/")
async def upload_file(file: UploadFile):
    if not file.filename.lower().endswith(".pdf"):
        return JSONResponse(content={"error": "Only PDF files allowed."}, status_code=400)

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    txt_path = os.path.join(UPLOAD_DIR, file.filename.replace(".pdf", ".txt"))

    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    if os.path.exists(txt_path):
        return {"message": f"{file.filename} already converted."}

    text = get_clean_text(file_path)
    if not text:
        return JSONResponse(content={"error": "❌ Unable to extract text from the PDF."}, status_code=400)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)

    return {"message": f"{file.filename} uploaded and converted successfully."}

# ---------------- Query Endpoint ----------------
@app.post("/query/")
async def query_doc(req: QueryRequest):
    try:
        engine = create_query_engine(req.filename, req.model)
        response = ask_query(engine, req.question)
        return {"answer": response.response}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
