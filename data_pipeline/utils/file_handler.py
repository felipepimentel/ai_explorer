import os
import pandas as pd
from PyPDF2 import PdfReader
from docx import Document
import asyncio
import aiofiles

async def read_text_file(file_path):
    async with aiofiles.open(file_path, 'r', encoding='utf-8') as file:
        return await file.read()

async def read_pdf_file(file_path):
    # PyPDF2 não suporta operações assíncronas, então usamos run_in_executor
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _read_pdf_file_sync, file_path)

def _read_pdf_file_sync(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

async def read_docx_file(file_path):
    # python-docx não suporta operações assíncronas, então usamos run_in_executor
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _read_docx_file_sync, file_path)

def _read_docx_file_sync(file_path):
    doc = Document(file_path)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])

async def read_csv_file(file_path):
    # pandas não suporta operações assíncronas, ent��o usamos run_in_executor
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _read_csv_file_sync, file_path)

def _read_csv_file_sync(file_path):
    return pd.read_csv(file_path).to_string()

async def read_file(file_path):
    _, ext = os.path.splitext(file_path)
    if ext == '.txt':
        return await read_text_file(file_path)
    elif ext == '.pdf':
        return await read_pdf_file(file_path)
    elif ext == '.docx':
        return await read_docx_file(file_path)
    elif ext == '.csv':
        return await read_csv_file(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

async def process_folder(folder_path):
    texts = []
    tasks = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            tasks.append(process_file(file_path))
    
    results = await asyncio.gather(*tasks)
    texts = [result for result in results if result is not None]
    return texts

async def process_file(file_path):
    try:
        text = await read_file(file_path)
        return {"file": file_path, "content": text}
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return None