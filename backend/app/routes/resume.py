from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Query
from typing import Optional, List
import uuid
from datetime import datetime
import logging

from ..services.model_service import model_service
from ..services.database_service import db_service
from ..utils.text_processor import extract_text_from_pdf, extract_text_from_docx

# Setup logging
logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    userId: str = Form(...),
    # 🔥 UPDATED: Made job_description mandatory to ensure dynamic suggestions
    job_description: str = Form(...) 
):
    """
    AI Recommendation Engine
    Compares Resume text against a specific Job Description to provide 
    tailored optimization tips and match scores.
    """
    try:
        # 1. Validate File existence
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        file_ext = file.filename.lower().split('.')[-1]
        content = await file.read()
        
        # 2. Extract Text based on file type
        if file_ext == 'pdf':
            text = extract_text_from_pdf(content)
        elif file_ext == 'docx':
            text = extract_text_from_docx(content)
        else:
            raise HTTPException(status_code=400, detail="Please upload PDF or DOCX only.")

        # 3. Process via AI Model Service 
        # We pass the job_description here so the NLP model knows what to compare against
        analysis = model_service.analyze_resume(text, job_description)
        
        # 4. Build Response with unique dynamic data
        result = {
            "id": str(uuid.uuid4()),
            "userId": userId,
            "fileName": file.filename,
            "jobTarget": job_description[:100] + "...", # Store a snippet of the target role
            "uploadDate": datetime.utcnow().isoformat(),
            
            # These are now DYNAMIC based on the Job Description
            "recommendations": analysis.get("recommendations", []),
            "suggestions": analysis.get("suggestions", []),
            "technicalSkills": analysis.get("technical_skills", []),
            "overallScore": analysis.get("overall_score", 0),
            "predictedCategory": analysis.get("predicted_category", "General")
        }
        
        # 5. Save to MongoDB
        await db_service.save_analysis(result)
        
        logger.info(f"Dynamic Analysis completed for user: {userId} against role: {job_description[:30]}")
        return result

    except Exception as e:
        logger.error(f"Post Analysis Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.get("/analyses")
async def get_history(userId: str = Query(...)):
    try:
        history = await db_service.get_all_analyses(user_id=userId)
        return history if history else []
    except Exception as e:
        logger.error(f"Get History Error: {str(e)}")
        return []

@router.delete("/analysis/{analysis_id}")
async def delete_analysis(analysis_id: str, userId: str = Query(...)):
    success = await db_service.delete_analysis(analysis_id, userId)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to delete or unauthorized.")
    return {"status": "success", "message": "Analysis deleted."}