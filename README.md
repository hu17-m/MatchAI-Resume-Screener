 MatchAI: AI-Based Resume Screening & Candidate Recommendation System

Developed during the AI/ML Engineering Internship at **Shamgar Software Solutions**.

MatchAI is a professional recruitment tool that uses Natural Language Processing (NLP) to analyze resumes against specific job descriptions. It provides candidates with a dynamic "Optimization Plan" and "Career Trajectories" based on their extracted skills and detected seniority level.



 🚀 Project Objective
To design and develop an AI/ML solution that analyzes resumes and job descriptions to score, rank, and recommend candidates using NLP and machine learning techniques.

 🛠️ Technical Architecture
- **Frontend**: Next.js 15+, Tailwind CSS, Lucide React.
- **Backend**: FastAPI (Python), Uvicorn.
- **AI/NLP Layer**: Scikit-learn, TF-IDF Vectorization, Cosine Similarity, Regex-based Seniority Detection.
- **Database**: MongoDB for secure, isolated user session and analysis storage.



✨ Key Features
- Dynamic Seniority Detection**: Extracts years of experience from resume text to categorize candidates as Junior, Mid-Level, or Senior.
- Role-Based Optimization Plan**: Compares the resume against a user-provided Job Description to identify specific missing keywords and provide tailored improvement tips.
- Intelligent Career Trajectories**: Recommends job roles (e.g., "Senior Python Developer") based on the intersection of found skills and detected seniority.
- ATS Scoring Engine**: Calculates an overall match percentage by analyzing technical skill density and formatting.
- Secure User Isolation**: Ensures that data remains private to the individual user session using unique MongoDB identifiers.



 📂 Project Structure

```text
Resume_AI_Project/
├── backend/                # FastAPI Backend
│   ├── app/
│   │   ├── models/         # Pre-trained ML models (.pkl)
│   │   ├── routes/         # API Endpoints (resume.py)
│   │   ├── services/       # Core Logic (model_service.py, database_service.py)
│   │   └── utils/          # Text Processing (PDF/DOCX parsers)
│   ├── main.py             # Entry point
│   └── requirements.txt    # Python dependencies
├── frontend/               # Next.js Frontend
│   ├── app/                
│   │   ├── dashboard/      # Dashboard & Upload Pages
│   │   ├── login/          # Auth Page
│   │   └── page.tsx        # Landing Page
│   ├── lib/                # API and Auth helpers
│   └── public/             # Static assets
└── screenshots/            # Project visual documentation

 📸 Project Screenshots

 1. Landing Page
*Professional "Cream & Glass" aesthetic presenting project objectives.*
![Landing Page](./screenshot/landing%203.png)

 2. Personalized Upload
*Features a dual-input system for the Resume and the Target Job Description.*
![Upload Page](./screenshot/personalised%20scan.png)

 3. Analysis Dashboard
*Dynamic ATS Scoring, customized Optimization Plans, and Skill-Mapped Recommendations.*
![Dashboard](./screenshot/user%20dashboard.png)

⚙️ Installation & Setup
Backend
Navigate to the /backend folder.

Install dependencies: pip install -r requirements.txt

Start the server: uvicorn app.main:app --reload

Frontend
Navigate to the /frontend folder.

Install dependencies: npm install

Run the development server: npm run dev

👨‍💻 Developer
Himanshu Gadekar AI/ML Engineer Intern @ Shamgar Software Solutions

LinkedIn

GitHub

© 2026 MatchAI Project • Intern Engagement Program