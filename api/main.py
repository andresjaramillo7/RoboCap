from fastapi import FastAPI, UploadFile, File
from pathlib import Path
import time

app = FastAPI()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/caption")
async def caption(image: UploadFile = File(...)):
    contents = await image.read()
    print("[SERVER] got file:", image.filename, "bytes:", len(contents))

    filename = f"{int(time.time()*1000)}_{image.filename or 'photo.jpg'}"
    out_path = UPLOAD_DIR / filename
    out_path.write_bytes(contents)
    print("[SERVER] saved to:", out_path.resolve())

    return {"caption": "upload works (dummy caption)"}