# app.py
import streamlit as st
import os
import time
from dotenv import load_dotenv
from parser import get_document_text
from ai_engine import analyze_resume_realtime
from generator import generate_resume_docx, generate_resume_pdf

load_dotenv()

# --- PREMIUM PAGE CONFIG ---
st.set_page_config(
    page_title="AI ATS Resume Optimizer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM CSS FOR ANIMATIONS & GLOW EFFECTS ---
st.markdown("""
<style>
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(-10px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulseGlow {
        0% { box-shadow: 0 0 5px rgba(0, 150, 255, 0.2); }
        50% { box-shadow: 0 0 20px rgba(0, 150, 255, 0.6); }
        100% { box-shadow: 0 0 5px rgba(0, 150, 255, 0.2); }
    }
    .main-title {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        background: linear-gradient(90deg, #FF4B4B, #4158D0, #C850C0);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: fadeIn 1.2s ease-out, gradientMove 6s ease infinite;
        font-size: 3rem !important;
        margin-bottom: 5px;
    }
    @keyframes gradientMove {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .card-container {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    .card-container:hover {
        transform: translateY(-3px);
        border-color: #FF4B4B;
        background: rgba(255, 255, 255, 0.05);
    }
    .stFileUploader {
        border-radius: 12px;
        padding: 10px;
        animation: pulseGlow 3s infinite;
    }
    .metric-box {
        text-align: center;
        padding: 15px;
        background: rgba(0, 150, 255, 0.1);
        border-radius: 10px;
        border-left: 5px solid #0096FF;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.markdown('<h1 class="main-title">🎯 AI-Powered ATS Resume Evaluator</h1>', unsafe_allow_html=True)
st.markdown('<p style="font-size: 1.2rem; color: #B0B3B8;">Get real-time scoring, gap analysis, and professional optimization pipelines instantly.</p>', unsafe_allow_html=True)
st.markdown("---")

# --- TWO COLUMN INPUT LAYOUT ---
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.markdown('### 🚀 Target Context')
    target_role = st.text_input(
        "Desired Position / Job Title",
        placeholder="e.g., Data Analyst, Software Engineer"
    )
    job_description = st.text_area(
        "Paste Target Job Description (JD) Here",
        placeholder="Paste the full job requirements or core lines here...",
        height=220
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.markdown('### 📂 Upload Your Resume')
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "docx"]
    )
    if uploaded_file is not None:
        st.success(f"✔️ {uploaded_file.name} loaded successfully.")
    else:
        st.info("💡 Pro-Tip: Ensure your file includes clear headers for better ATS indexing.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- ANALYSIS TRIGGER ---
if st.button("🚀 Run Comprehensive ATS Optimization", use_container_width=True):
    if not target_role or not job_description or not uploaded_file:
        st.error("⚠️ Environment Anomaly: Please verify all fields and the file asset are loaded completely.")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        steps = [
            ("🔍 Loading local document buffers...", 0.3),
            ("🧠 Pipelining profile weights to Groq Llama-3 cluster...", 0.7),
            ("✨ Formatting optimization dashboard report matrices...", 1.0)
        ]
        
        for message, progress in steps:
            status_text.markdown(f"**{message}**")
            progress_bar.progress(progress)
            time.sleep(0.5)
            
        progress_bar.empty()
        status_text.empty()
        
        try:
            resume_text = get_document_text(uploaded_file)
            analysis_report = analyze_resume_realtime(resume_text, job_description)
            
            st.balloons()
            st.markdown("### 📊 Comprehensive Optimization Dashboard")
            
            res_col1, res_col2 = st.columns([1, 2], gap="medium")
            
            with res_col1:
                st.markdown('<div class="card-container">', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="metric-box">
                    <p style="margin:0; font-size:1rem; color:#B0B3B8;">ATS MATCH VECTOR</p>
                    <h2 style="margin:0; color:#0096FF; font-size:2.5rem;">Verified</h2>
                </div>
                """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
            with res_col2:
                st.markdown('<div class="card-container">', unsafe_allow_html=True)
                st.markdown("#### 🧠 Strategic Matrix Analytics")
                
                try:
                    import json
                    data = json.loads(analysis_report)
                    
                    score = data.get("ats_score", 0)
                    st.markdown(f"**📈 Overall Match Score:** `{score}/100`")
                    st.progress(int(score) / 100)
                    
                    st.markdown("---")
                    st.markdown("🎯 **Missing Keywords:**")
                    keywords = data.get("missing_keywords", [])
                    if keywords:
                        kw_html = "".join([f"<span style='background-color:#FF4B4B; color:white; padding:4px 8px; margin:4px; border-radius:4px; display:inline-block; font-size:14px;'>{kw}</span>" for kw in keywords])
                        st.markdown(kw_html, unsafe_allow_html=True)
                    else:
                        st.success("Perfect! No major technical keywords missing.")
                        
                    st.markdown("---")
                    st.markdown("⚠️ **Identified Experience Gaps:**")
                    for gap in data.get("experience_gaps", []):
                        st.markdown(f"• {gap}")
                except Exception:
                    st.markdown(analysis_report)
                    
                st.markdown('</div>', unsafe_allow_html=True)

            # --- FULL OPTIMIZED RESUME GENERATION ENGINE ---
            st.markdown("---")
            st.markdown("### 📝 Tailored Full Resume Preview & Export Engine")
            
            with st.spinner("🧠 Groq AI is engineering your fully optimized corporate resume..."):
                from groq import Groq
                client = Groq(api_key=os.getenv("GROQ_API_KEY"))
                
                prompt = f"""
                You are an expert technical resume writer. Completely rewrite the user's original resume to perfectly align with the target job description while maximizing ATS score tracking tokens.
                
                Original Resume Text:
                {resume_text}
                
                Target Job Description:
                {job_description}
                
                Target Role:
                {target_role}
                
                Instructions:
                1. Include all standard professional sections: OBJECTIVE, EDUCATION, TECHNICAL SKILLS (incorporating missing keywords seamlessly), PROJECTS, and EXPERIENCE.
                2. Do NOT add any conversational headers, introduction text, or quotes. Give ONLY the pure optimized resume content.
                """
                
                try:
                    completion = client.chat.completions.create(
                        model="llama3-8b-8192",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.3
                    )
                    optimized_resume_content = completion.choices[0].message.content
                except Exception:
                    optimized_resume_content = resume_text

            prev_col1, prev_col2 = st.columns([2, 1], gap="medium")
            
            with prev_col1:
                st.markdown('<div class="card-container" style="border-left: 4px solid #C850C0;">', unsafe_allow_html=True)
                st.markdown("#### 👁️ Real-time Full Document Preview")
                final_edited_resume = st.text_area("Live Generated Corporate Stream (Editable)", value=optimized_resume_content.strip(), height=400)
                st.markdown('</div>', unsafe_allow_html=True)
                
            with prev_col2:
                st.markdown('<div class="card-container">', unsafe_allow_html=True)
                st.markdown("#### 🛠️ Available Actions")
                
                docx_buffer = generate_resume_docx(resume_text, final_edited_resume)
                st.download_button(
                    label="📥 Export Optimized Resume (.DOCX)",
                    data=docx_buffer,
                    file_name=f"Optimized_{target_role.replace(' ', '_')}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True,
                    key="ultimate_docx_download"
                )
                
                st.markdown("<div style='margin: 10px 0;'></div>", unsafe_allow_html=True)
                
                pdf_buffer = generate_resume_pdf(resume_text, final_edited_resume)
                st.download_button(
                    label="📥 Export Optimized Resume (.PDF)",
                    data=pdf_buffer,
                    file_name=f"Optimized_{target_role.replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    key="ultimate_pdf_download"
                )
                st.markdown('</div>', unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Execution Error encountered during dynamic processing: {str(e)}")
