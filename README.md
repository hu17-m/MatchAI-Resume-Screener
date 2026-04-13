# 🧠 MatchAI: Candidate Recommendation System
> An intelligent platform that aligns candidate resumes with specific job descriptions using AI.

MatchAI is an advanced recruitment engine that leverages Natural Language Processing (NLP) to bridge the gap between candidate resumes and specific job requirements. It doesn't just scan; it analyzes context, seniority, and skill gaps to provide actionable career intelligence and tailored optimization plans.

---

## 🌟 What makes it special?

* **Dynamic Seniority Detection:** Automatically identifies if a candidate is Junior, Mid-Level, or Senior based on experience patterns extracted from the resume.
* **Explainable Feedback:** It doesn't just give a score. It provides a Role-Based Optimization Plan, identifying exactly which keywords and skills are missing compared to the target job description.
* **Secure User Isolation:** Built with enterprise-grade privacy in mind, ensuring that data remains secure and isolated to individual user sessions using unique MongoDB identifiers.

---

## 🖥 System Overview & Visualizations

### Primary Interfaces
| The Landing Experience | Personalized AI Gateway |
| :---: | :---: |
| ![Landing Page](./screenshot/landing%201%20-%20Copy.png) | ![Upload Page](./screenshot/personalised%20scan.png) |

### Inference Capabilities
| Intelligence Dashboard & ATS Scoring |
| :---: |
| ![Dashboard](./screenshot/user%20dashboard.png) |

---

## 📂 Project Structure & File Paths

```text
Resume_AI_Project/
├── backend/                # FastAPI Backend
│   ├── app/
│   │   ├── models/         # Pre-trained ML models (.pkl)
│   │   ├── services/       # Core Logic (model_service.py, database_service.py)
│   │   ├── routes/         # API Endpoints (resume.py)
│   │   └── utils/          # Text Processing (PDF/DOCX parsers)
│   ├── main.py             # Server Entry Point
│   └── requirements.txt    # Python dependencies
├── frontend/               # Next.js Frontend
│   ├── app/                
│   │   ├── dashboard/      # Dashboard UI Components
│   │   ├── login/          # Authentication Gateway
│   │   └── page.tsx        # Landing Page UI
│   └── lib/                # API and Auth helpers
└── screenshot/             # Visual Assets Directory
    ├── landing 1 - Copy.png
    ├── personalised scan.png
    └── user dashboard.png
    🛠 Tech Stack & Architecture
Core Components
Frontend: Next.js 15+ (App Router), Tailwind CSS, Lucide-React.

Backend: FastAPI (Python), Uvicorn, RESTful Architecture.

Machine Learning: Scikit-Learn, NumPy, TF-IDF Vectorization.

Database: MongoDB (NoSQL).

🔬 Model Technical Analysis
Algorithm: NLP Skill Extraction & Cosine Similarity
We utilized a combination of TF-IDF vectorization and heuristic skill mapping for this recruitment use case:

Explainability: By directly comparing extracted resume tokens against job description requirements, we provide real-time feature gaps. Users see exactly which skills are needed to improve their match.

Seniority Parsing: Engineered regex pipelines accurately detect years of experience to dynamically adjust the recommended career trajectories.

Adaptive Scoring: Achieved a highly responsive ATS Scoring Engine that penalizes skill mismatches while rewarding high-density technical alignment.

🚀 Key Functionalities
Dual-Input Analysis: Switch seamlessly between general resume scoring and highly targeted role-based analysis by providing a specific job description.

Intelligent Career Trajectories: Recommends specific job roles (e.g., "Senior Python Developer") based on the intersection of found skills and detected seniority.

Optimization Plan: Generates customized, actionable bullet points to help candidates improve their formatting and content.

High-Speed Inference: FastAPI ensures rapid processing from document upload to fully visualized dashboard results.

📥 Installation & Usage
Clone the Repository

Bash
git clone [https://github.com/hu17-m/MatchAI-Resume-Screener.git](https://github.com/hu17-m/MatchAI-Resume-Screener.git)
Backend Setup

Bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
Frontend Setup

Bash
cd frontend
npm install
npm run dev
👨‍💻 Developed By
Himanshu Gadekar AI/ML Engineer Intern @ Shamgar Software Solutions

LinkedIn

GitHub Profile

🎯 Future Roadmap
[ ] Transformer Integration: Upgrading the core engine to BERT/RoBERTa for deeper semantic understanding of project descriptions.

[ ] Live API Connectors: Direct integration with LinkedIn APIs to pull live job descriptions for real-time matching.

[ ] Export Module: Generate annotated PDF reports for candidates to download their optimization plans.