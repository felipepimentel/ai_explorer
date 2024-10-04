from fastapi import FastAPI, File, UploadFile, Depends
from data_pipeline.core.search import DocumentSearch
from data_pipeline.auth.auth_manager import get_current_user, User
import uvicorn

app = FastAPI()

search_engine = DocumentSearch()

@app.post("/documents/")
async def add_document(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    content = await file.read()
    text = content.decode("utf-8")
    search_engine.add_documents([text])
    return {"filename": file.filename, "status": "added"}

@app.get("/search/")
async def search_documents(query: str, k: int = 3, current_user: User = Depends(get_current_user)):
    results = search_engine.search_documents(query, k)
    return {"query": query, "results": results}

@app.post("/documents/pdf/")
async def add_pdf(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    search_engine.add_pdf(file.file)
    return {"filename": file.filename, "status": "added"}

@app.post("/documents/image/")
async def add_image(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    search_engine.add_image(file.file)
    return {"filename": file.filename, "status": "added"}

@app.post("/documents/audio/")
async def add_audio(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    search_engine.add_audio(file.file)
    return {"filename": file.filename, "status": "added"}

def start_api():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    start_api()