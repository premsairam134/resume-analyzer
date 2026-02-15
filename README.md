# Smart Resume Analyzer & Job Recommendation System

An AI-powered web application designed to help students and job seekers optimize their resumes. This tool analyzes resumes, extracts skills using NLP, calculates a match score against job descriptions, and recommends suitable roles.

## 🚀 Features

- **Resume Parsing**: Automatically extracts text from PDF and DOCX files.
- **Skill Extraction**: Identifies technical skills (e.g., Python, SQL, Machine Learning) using NLP.
- **Resume Scoring**: Generates a score (0-100) based on skill matching, section completeness, and formatting.
- **Job Recommendations**: Suggests top job roles based on extracted skills and a pre-defined dataset.
- **Skill Gap Analysis**: Highlights missing skills for recommended roles.
- **Interactive Dashboard**: Modern, dark-mode UI with visual score gauges and feedback.
- **Chatbot Assistant**: Provides instant resume writing tips.
- **Export Data**: Download analysis reports in CSV format for further analysis (e.g., Power BI).

## 🛠 Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **NLP/AI**: spaCy, NLTK, Scikit-learn
- **Data Handling**: Pandas

## 📂 Project Structure

```
Resume Analyzer/
├── app.py                 # Main Flask application
├── resume_parser.py       # Module for parsing PDF/DOCX
├── skill_extractor.py     # NLP logic for skill extraction
├── scoring_model.py       # Logic for scoring resumes
├── job_recommender.py     # Job matching algorithm
├── requirements.txt       # Python dependencies
├── dataset/
│   └── jobs.csv           # Job roles and skills database
├── static/
│   ├── style.css          # CSS styles
│   └── script.js          # Frontend logic
└── templates/
    └── index.html         # Main dashboard template
```

## ⚙️ Setup & Installation

Follow these steps to run the project locally:

1.  **Clone or Download** this repository.
2.  **Open a terminal** in the project folder.
3.  **Create a Virtual Environment** (Optional but recommended):
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

4.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Download spaCy Language Model**:
    This is required for the NLP features to work correctly.
    ```bash
    python -m spacy download en_core_web_sm
    ```

6.  **Run the Application**:
    ```bash
    python app.py
    ```

7.  **Access the Dashboard**:
    Open your browser and verify the address (usually `http://127.0.0.1:5000/`).

## 📊 Dataset

The system uses `dataset/jobs.csv` containing job roles and required skills. You can edit this file to add more roles or update skills.

## 📝 Usage

1.  Click **"Choose File"** to upload your Resume (PDF or DOCX).
2.  Click **"Analyze Resume"**.
3.  View your **Score**, **Extracted Skills**, and **Recommended Jobs**.
4.  Check the **Improvement Suggestions** to see what's missing.
5.  Use the **Chatbot** (bottom right) for quick tips.
6.  Click **"Export Report"** to save your results.

---
**Note**: Ensure you have a valid internet connection for the first run to download the spaCy model.
