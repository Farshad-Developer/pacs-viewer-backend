
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import shutil
import os
import sqlite3
from datetime import datetime
from typing import List

app = FastAPI()

# اتصال به دیتابیس
conn = sqlite3.connect("pacs_files.db", check_same_thread=False)
cursor = conn.cursor()

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class FileInfo(BaseModel):
    id: int
    filename: str
    content_type: str
    upload_time: str

@app.post("/upload/", response_model=FileInfo)
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    upload_time = datetime.now().isoformat()
    cursor.execute("INSERT INTO files (filename, content_type, upload_time) VALUES (?, ?, ?)",
                   (file.filename, file.content_type, upload_time))
    conn.commit()
    file_id = cursor.lastrowid
    return {"id": file_id, "filename": file.filename, "content_type": file.content_type, "upload_time": upload_time}

@app.get("/files/", response_model=List[FileInfo])
def list_files():
    cursor.execute("SELECT * FROM files")
    rows = cursor.fetchall()
    return [{"id": row[0], "filename": row[1], "content_type": row[2], "upload_time": row[3]} for row in rows]

@app.get("/files/{file_id}")
def get_file(file_id: int):
    cursor.execute("SELECT filename FROM files WHERE id=?", (file_id,))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="File not found")
    file_path = os.path.join(UPLOAD_DIR, row[0])
    return FileResponse(path=file_path, filename=row[0])
