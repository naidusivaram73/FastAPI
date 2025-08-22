# routers/resumes.py
from fastapi import APIRouter, HTTPException, status
from typing import List
from bson.objectid import ObjectId
from starlette.responses import HTMLResponse

from db import db
from models import ResumeCreate, ResumeUpdate

router = APIRouter(prefix="/resumes", tags=["resumes"])
collection = db["resumes"]

# helper: convert mongo doc -> response dict
def doc_to_response(doc: dict) -> dict:
    doc["id"] = str(doc["_id"])
    doc.pop("_id", None)
    return doc

@router.on_event("startup")
async def ensure_indexes():
    # any useful indexes (example: email)
    await collection.create_index("email", background=True)

@router.post("/", status_code=201)
async def create_resume(payload: ResumeCreate):
    data = payload.dict()
    res = await collection.insert_one(data)
    new_doc = await collection.find_one({"_id": res.inserted_id})
    return doc_to_response(new_doc)

@router.get("/", response_model=List[dict])
async def list_resumes(skip: int = 0, limit: int = 20):
    cursor = collection.find().skip(skip).limit(limit)
    results = []
    async for doc in cursor:
        results.append(doc_to_response(doc))
    return results

@router.get("/{resume_id}")
async def get_resume(resume_id: str):
    if not ObjectId.is_valid(resume_id):
        raise HTTPException(status_code=400, detail="Invalid id")
    doc = await collection.find_one({"_id": ObjectId(resume_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Resume not found")
    return doc_to_response(doc)

@router.put("/{resume_id}")
async def update_resume(resume_id: str, payload: ResumeUpdate):
    if not ObjectId.is_valid(resume_id):
        raise HTTPException(status_code=400, detail="Invalid id")
    update_data = {k: v for k, v in payload.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")
    result = await collection.update_one({"_id": ObjectId(resume_id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Resume not found")
    doc = await collection.find_one({"_id": ObjectId(resume_id)})
    return doc_to_response(doc)

@router.delete("/{resume_id}", status_code=204)
async def delete_resume(resume_id: str):
    if not ObjectId.is_valid(resume_id):
        raise HTTPException(status_code=400, detail="Invalid id")
    result = await collection.delete_one({"_id": ObjectId(resume_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Resume not found")
    return {"status": "deleted"}

# Optional: simple HTML render of resume (template below)
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
env = Environment(
    loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "..", "templates")),
    autoescape=select_autoescape(["html", "xml"])
)

# @router.get("/{resume_id}/html", response_class=HTMLResponse)
# async def resume_html(resume_id: str):
#     if not ObjectId.is_valid(resume_id):
#         raise HTTPException(status_code=400, detail="Invalid id")
#     doc = await collection.find_one({"_id": ObjectId(resume_id)})
#     if not doc:
#         raise HTTPException(status_code=404, detail="Resume not found")
#     tpl = env.get_template("resume.html")
#     # convert ObjectId for template
#     doc["id"] = str(doc["_id"])
#     return tpl.render(resume=doc)
