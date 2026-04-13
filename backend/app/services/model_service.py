import os
import joblib
import re
import numpy as np
import logging
import random
from pathlib import Path
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)

# --- PATH CONFIGURATION ---
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent.parent 
MODEL_PATH = project_root / "backend" / "app" / "models" / "resume_ai_pro.pkl"

# --- LOAD MODEL ---
try:
    logger.info(f"Loading model from: {MODEL_PATH}")
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
    
    data = joblib.load(str(MODEL_PATH))
    model = data["model"]
    vectorizer = data["vectorizer"]
    logger.info("Model and Vectorizer loaded successfully!")
except Exception as e:
    logger.error(f"Failed to load model: {str(e)}")
    model = None
    vectorizer = None

# --- SKILL DATABASE ---
TECHNICAL_SKILLS = [
    "python", "java", "javascript", "typescript", "sql", "nosql", "mongodb", "postgresql",
    "machine learning", "deep learning", "nlp", "computer vision", "tensorflow", "pytorch",
    "react", "angular", "vue", "nextjs", "node", "express", "django", "flask", "fastapi",
    "docker", "kubernetes", "aws", "azure", "gcp", "git", "ci/cd", "jenkins",
    "html", "css", "tailwind", "sass", "bootstrap", "figma", "adobe xd",
    "rest api", "graphql", "microservices", "redis", "elasticsearch",
    "pandas", "numpy", "scikit-learn", "spark", "hadoop", "tableau", "power bi",
    "linux", "bash", "powershell", "agile", "scrum", "jira"
]

# --- JOB ROLE MAPPING ---
JOB_ROLES = {
    "python": {"title": "Backend Developer", "category": "Backend"},
    "javascript": {"title": "Frontend Engineer", "category": "Frontend"},
    "react": {"title": "React Developer", "category": "Frontend"},
    "machine learning": {"title": "ML Engineer", "category": "AI/ML"},
    "sql": {"title": "Data Analyst", "category": "Data"},
    "aws": {"title": "Cloud Architect", "category": "Cloud"},
    "docker": {"title": "DevOps Engineer", "category": "DevOps"},
    "node": {"title": "Node.js Developer", "category": "Backend"},
    "figma": {"title": "UI/UX Designer", "category": "Design"}
}

class ModelService:
    def __init__(self):
        self.model = model
        self.vectorizer = vectorizer

    def extract_skills(self, text: str) -> List[str]:
        """Extracts unique technical skills from text."""
        text_lower = text.lower()
        found = [skill for skill in TECHNICAL_SKILLS if skill in text_lower]
        return list(dict.fromkeys(found))

    def detect_seniority(self, text: str) -> str:
        """Detects experience level based on years mentioned in text."""
        text_lower = text.lower()
        years = re.findall(r'(\d+)\+?\s*(?:years|yrs)', text_lower)
        if years:
            max_years = max([int(y) for y in years])
            if max_years >= 7: return "Senior"
            if max_years >= 3: return "Mid-Level"
        return "Junior"

    def generate_dynamic_insights(self, resume_text: str, job_description: Optional[str]) -> List[str]:
        """🔥 DYNAMIC SUGGESTIONS: Compares JD against Resume."""
        suggestions = []
        resume_lower = resume_text.lower()
        
        if job_description:
            jd_lower = job_description.lower()
            missing = [s.title() for s in TECHNICAL_SKILLS if s in jd_lower and s not in resume_lower]
            
            if missing:
                for skill in missing[:3]:
                    suggestions.append(f"The job requires '{skill}'. Highlight your projects in this area to improve matching.")
            else:
                suggestions.append("Your skills align perfectly with the job's technical requirements!")
        
        suggestions.append("Quantify your impact using metrics (e.g., 'Optimized query performance by 40%').")
        suggestions.append("Ensure your professional summary addresses the specific goals of the target role.")
        
        return suggestions[:4]

    def generate_recommendations(self, skills_found: List[str], base_score: float, seniority: str) -> List[Dict[str, Any]]:
        """🔥 DYNAMIC ROLES: Generates roles based on found skills and seniority."""
        recs = []
        for skill in skills_found:
            if skill in JOB_ROLES:
                role = JOB_ROLES[skill]
                # Add Seniority to the title
                display_title = f"{seniority} {role['title']}" if seniority != "Junior" else role['title']
                match_val = min(98.0, base_score + random.uniform(-3, 6))
                recs.append({"title": display_title, "match": round(match_val, 1)})

        if not recs:
            recs = [
                {"title": f"{seniority} Software Engineer", "match": round(base_score, 1)},
                {"title": "Technical Analyst", "match": round(base_score - 4, 1)}
            ]
        
        unique_recs = []
        seen = set()
        for r in sorted(recs, key=lambda x: x['match'], reverse=True):
            if r['title'] not in seen:
                seen.add(r['title'])
                unique_recs.append(r)
                
        return unique_recs[:3]

    def analyze_resume(self, text: str, job_description: Optional[str] = None) -> Dict[str, Any]:
        """Main entry point for analysis."""
        try:
            found_skills = self.extract_skills(text)
            seniority = self.detect_seniority(text)
            
            # Dynamic Score
            base_score = 55.0
            if job_description:
                matches = len([s for s in found_skills if s in job_description.lower()])
                base_score = min(98.0, 55.0 + (matches * 7))

            return {
                "overall_score": round(base_score, 1),
                "suggestions": self.generate_dynamic_insights(text, job_description),
                "recommendations": self.generate_recommendations(found_skills, base_score, seniority),
                "technical_skills": [s.title() for s in found_skills],
                "predicted_category": f"{seniority} Engineer",
                "ats_score": round(base_score * 0.9, 1)
            }
        except Exception as e:
            logger.error(f"Analysis Error: {e}")
            return {"overall_score": 0, "suggestions": ["Error processing resume."]}

model_service = ModelService()