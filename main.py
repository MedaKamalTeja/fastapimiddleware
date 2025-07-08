from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import requests
import base64

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class UploadRequest(BaseModel):
    file_name: str
    file_base64: str
    folder_id: int
    destination: str

@app.post("/upload_to_clickscan")
def upload_to_clickscan(data: UploadRequest):
    decoded_file = base64.b64decode(data.file_base64)
    
    files = {
        "files[]": (data.file_name, decoded_file, "application/octet-stream")
    }

    form_data = {
        "folder_id": str(data.folder_id),
        "destination": data.destination,
        "order_no": "1",
        "location": "default"
    }

    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXlsb2FkIjp7ImlkIjoxLCJlbWFpbCI6InN1cGVyYWRtaW5AdGVycmFsb2dpYy5jb20iLCJ1c2VybmFtZSI6InN1cGVyYWRtaW4iLCJyb2xlcyI6WyJBRE1JTiIsIlNBIl19LCJpYXQiOjE3NTE5NzkxMTYsImV4cCI6MTc1MjAyMjMxNn0.RJLxhoq6G0iUQiUFingNZeAIb1qXJI2R6XcUYshQqBs",
        "X-Tenant-ID": "5yr3IUvCNC"
    }

    res = requests.post(
        "https://clickscan.terralogic.com/client/api/v1/file/upload",
        headers=headers,
        data=form_data,
        files=files
    )

    if res.status_code == 201:
        return {"message": "✅ File uploaded", "clickscan_response": res.json()}
    else:
        return {"message": "❌ Upload failed", "details": res.text}, res.status_code
