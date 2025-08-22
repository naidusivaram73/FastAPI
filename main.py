# main.py
from fastapi import FastAPI
from routers.resumes import router as resumes_router
from db import db

app = FastAPI(title="Resume Builder API")

app.include_router(resumes_router)

@app.get("/")
async def root():
    return {"status": "ok", "msg": "Resume Builder API running"}
