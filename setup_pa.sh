#!/bin/bash

echo "🚀 Starting PythonAnywhere setup for ResumeAnalyzer..."

# 1. Create Folder
mkdir -p ~/resume_analyzer
cp -r * ~/resume_analyzer/
cd ~/resume_analyzer

# 2. Create Virtual Environment
echo "📦 Creating virtual environment..."
python3.11 -m venv venv
source venv/bin/activate

# 3. Install Dependencies
echo "📥 Installing dependencies (this may take a few minutes)..."
pip install --upgrade pip
pip install -r requirements.txt

# 4. Download spaCy Model
echo "🧠 Downloading spaCy language model..."
python -m spacy download en_core_web_sm

echo "✅ Setup complete!"
echo "Now go to the 'Web' tab on PythonAnywhere and configure your app."
