from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import requests

app = FastAPI()

# ClickScan config (replace with your real values)
CLICKSCAN_UPLOAD_URL = "https://clickscan.terralogic.com/client/api/v1/file/upload"
BEARER_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXlsb2FkIjp7ImlkIjoxLCJlbWFpbCI6InN1cGVyYWRtaW5AdGVycmFsb2dpYy5jb20iLCJ1c2VybmFtZSI6InN1cGVyYWRtaW4iLCJyb2xlcyI6WyJBRE1JTiIsIlNBIl19LCJpYXQiOjE3NTE5NzY3NTYsImV4cCI6MTc1MjAxOTk1Nn0.4p4rqoSHBjvpUDR5YmyzsPN2m956iNgitJRL6u8IZpc"
TENANT_ID = "5yr3IUvCNC"

@app.post("/upload_to_clickscan/")
async def upload_to_clickscan(
    folder_id: str = Form(...),
    destination: str = Form(...),
    order_no: str = Form(...),
    location: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        files = {
            "files[]": (file.filename, await file.read(), file.content_type)
        }
        data = {
            "folder_id": folder_id,
            "destination": destination,
            "order_no": order_no,
            "location": location
        }
        headers = {
            "Authorization": f"Bearer {BEARER_TOKEN}",
            "X-Tenant-ID": TENANT_ID
        }
        res = requests.post(CLICKSCAN_UPLOAD_URL, headers=headers, data=data, files=files)
        return JSONResponse(content=res.json(), status_code=res.status_code)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
