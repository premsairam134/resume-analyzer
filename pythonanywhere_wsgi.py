import sys
import os

# Set up paths
path = '/home/ResumeAnalyzer/resume_analyzer'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
