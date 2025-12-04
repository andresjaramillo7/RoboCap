from fastapi import FastAPI, UploadFile, File
from pathlib import Path
from src.data.load_data import Robocap
app = FastAPI()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/caption")
async def caption(image: UploadFile = File(...)):
    contents = await image.read()
    cap = Robocap(contents)
    
    return {"caption": cap}