# ai_engine.py
import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def analyze_resume_realtime(extracted_text, job_description):
    """
    Connects to Groq Cloud API using Gemma 2 or Llama 3 to evaluate 
    the resume text against the target job profile parameters.
    """
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        return json.dumps({
            "ats_score": 0,
            "missing_keywords": ["API Key Missing"],
            "experience_gaps": ["Please check your .env configuration file."],
            "profile_suggestions": ["Ensure GROQ_API_KEY is written correctly in your .env file."]
        })
        
    try:
        # Initialize Groq Client
        client = Groq(api_key=api_key)
        
        prompt = f"""
        You are an advanced Applicant Tracking System (ATS) optimization engine. 
        Analyze the following resume text against the provided Job Description (JD).
        
        Resume Content:
        {extracted_text}
        
        Target Job Description:
        {job_description}
        
        Provide your response strictly in raw JSON format. Do not write any markdown code fences, backticks, or intro/outro text. The response must match this schema exactly:
        {{
            "ats_score": 85,
            "missing_keywords": ["Keyword1", "Keyword2"],
            "experience_gaps": ["Gap description 1", "Gap description 2"],
            "profile_suggestions": ["Suggestion 1", "Suggestion 2"]
        }}
        """
        
        # Calling Groq using Gemma-2-9b (highly accurate for technical scoring)
      # Calling Groq using the active stable production model
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # <-- UPDATED ENDPOINT
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            response_format={"type": "json_object"}  
        )
        
        return completion.choices[0].message.content
        
    except Exception as e:
        return json.dumps({
            "ats_score": 0,
            "missing_keywords": [f"Connection Error: {str(e)}"],
            "experience_gaps": [],
            "profile_suggestions": ["Verify your network or check your daily Groq tokens allotment."]
        })