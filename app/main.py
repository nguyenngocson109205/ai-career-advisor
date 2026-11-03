from fastapi import FastAPI
from pydantic import BaseModel, Field
import pymupdf
from fastapi import UploadFile, File, HTTPException

from app.services.jd_analyzer import analyze_jd
app = FastAPI(title="Mini Tool Calling Agent")
    
""" 
Analyze Job Description
path: /analyze-jd
method: post
body{
    jd_text: str
    user_skills: list[str]
}
"""

class AnalyzeJDRequest(BaseModel):
    jd_text: str = Field(min_length=1)
    user_skills: list[str]

@app.post("/analyze-jd")
def analyze_job_description(request: AnalyzeJDRequest):
    return analyze_jd(
        jd_text=request.jd_text,
        user_skills=request.user_skills
    )
    
""" 
Upload Job Description
path: /upload-jd
method: post
body{
    file: UploadFile
}
"""
@app.post("/upload-jd")
async def upload_jd(file: UploadFile = File(...)):
    # 1. kiểm tra lại loại file 
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            
        )