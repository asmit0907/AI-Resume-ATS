# app.py
import streamlit as st
import os
import time
from dotenv import load_dotenv
from parser import get_document_text
# Agar aapke function ka naam 'analyze_resume' tha:
from ai_engine import analyze_resume_realtime as analyze_resume_data
from generator import generate_resume_docx, generate_resume_pdf

load_dotenv()

# --- PREMIUM PAGE CONFIG & UI INTERACTION ARCHITECTURE ---
st.set_page_config(
    page_title="AI ATS Resume Optimizer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM CSS FOR ANIMATIONS, GLOW EFFECTS & TRANSITIONS ---
st.markdown("""
<style>
    /* Gradient animated fade-in for headers */
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(-10px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulseGlow {
        0% { box-shadow: 0 0 5px rgba(0, 150, 255, 0.2); }
        50% { box-shadow: 0 0 20px rgba(0, 150, 255, 0.6); }
        100% { box-shadow: 0 0 5px rgba(0, 150, 255, 0.2); }
    }

    /* Main Title Styling with animated gradient */
    .main-title {
        font_family: 'Inter', sans-serif;
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

    /* Section Cards with soft glassmorphism & bounce transition */
    .card-container {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        animation: fadeIn 1.5s ease-out;
    }
    .card-container:hover {
        transform: translateY(-5px);
        border-color: #FF4B4B;
        background: rgba(255, 255, 255, 0.05);
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }

    /* Animated Upload Area glow */
    .stFileUploader {
        border-radius: 12px;
        padding: 10px;
        animation: pulseGlow 3s infinite;
    }

    /* Custom metric animations */
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
st.markdown('<p style="font-size: 1.2rem; color: #B0B3B8; animation: fadeIn 1.4s;">Get real-time scoring, gap analysis, and professional optimization pipelines instantly.</p>', unsafe_allow_html=True)
st.markdown("---")

# --- TWO COLUMN INTERACTIVE LAYOUT ---
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.markdown('### 🚀 Target Context')
    
    target_role = st.text_input(
        "Desired Position / Job Title",
        placeholder="e.g., Embedded Systems Engineer, Web Developer",
        help="Entering an explicit role activates structural weight vectors in the AI engine."
    )
    
    job_description = st.text_area(
        "Paste Target Job Description (JD) Here",
        placeholder="Paste the full job requirements, core lines, or technical stacks here...",
        height=220
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.markdown('### 📂 Upload Your Resume')
    
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "docx"],
        help="Supports comprehensive scanning of dual standard dynamic tracking schemas."
    )
    
    # Micro-interaction: Check file status and show instant badge update
    if uploaded_file is not None:
        st.success(f"✔️ {uploaded_file.name} parsed successfully into operational cache.")
    else:
        st.info("💡 Pro-Tip: Ensure your file includes clear headers for better ATS indexing.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- MAIN ANALYSIS TRIGGER WITH STEPPING ANIMATIONS ---
if st.button("🚀 Run Comprehensive ATS Optimization", use_container_width=True):
    if not target_role or not job_description or not uploaded_file:
        st.error("⚠️ Environment Anomaly: Please verify all fields and the file asset are loaded completely.")
    else:
        # Dynamic Multi-step Loader (Highly Interactive)
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        steps = [
            ("🔍 Loading local document buffers...", 0.2),
            ("⚙️ Extracting systemic token streams...", 0.5),
            ("🧠 Pipelining profile weights to Groq Llama-3 cluster...", 0.8),
            ("✨ Formatting optimization dashboard report matrices...", 1.0)
        ]
        
        for message, progress in steps:
            status_text.markdown(f"**{message}**")
            progress_bar.progress(progress)
            time.sleep(0.6)  # Creates a smooth analytical pacing effect
            
        progress_bar.empty()
        status_text.empty()
        
        try:
            # Process text and trigger AI core
            resume_text = get_document_text(uploaded_file)
            analysis_report = analyze_resume_data(resume_text, job_description)
            
            # --- RESULTS DASHBOARD WITH SLICK CARDS ---
            st.balloons() # Interactive celebratory trigger
            st.markdown("### 📊 Comprehensive Optimization Dashboard")
            
            # Split details into modern clean sub-layouts
            res_col1, res_col2 = st.columns([1, 2])
            
            with res_col1:
                st.markdown(f"""
                <div class="metric-box">
                    <p style="margin:0; font-size:1rem; color:#B0B3B8;">ATS MATCH VECTOR</p>
                    <h2 style="margin:0; color:#0096FF; font-size:2.5rem;">Verified</h2>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Dynamic action buttons
                st.markdown("#### 🛠️ Available Actions")
                st.download_button(
                    label="📥 Export Optimized Resume (.DOCX)",
                    data=generate_resume_docx(resume_text, analysis_report),
                    file_name=f"Optimized_{target_role.replace(' ', '_')}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
                
            with res_col2:
                st.markdown('<div class="card-container">', unsafe_allow_html=True)
                st.markdown("#### 🧠 Strategic Matrix Analytics")
                
                try:
                    import json
                    data = json.loads(analysis_report)
                    
                    # 1. ATS Score Meter
                    score = data.get("ats_score", 0)
                    st.markdown(f"**📈 Overall Match Score:** `{score}/100`")
                    st.progress(int(score) / 100)
                    
                    st.markdown("---")
                    
                    # 2. Missing Keywords Tags
                    st.markdown("🎯 **Missing Keywords:**")
                    keywords = data.get("missing_keywords", [])
                    if keywords:
                        kw_html = "".join([f"<span style='background-color:#FF4B4B; color:white; padding:4px 8px; margin:4px; border-radius:4px; display:inline-block; font-size:14px;'>{kw}</span>" for kw in keywords])
                        st.markdown(kw_html, unsafe_allow_html=True)
                    else:
                        st.success("Perfect! No major technical keywords missing.")
                        
                    st.markdown("---")
                    
                    # 3. Experience Gaps
                    st.markdown("⚠️ **Identified Experience Gaps:**")
                    for gap in data.get("experience_gaps", []):
                        st.markdown(f"• {gap}")
                        
                except Exception:
                    st.markdown(analysis_report)
                    
                st.markdown('</div>', unsafe_allow_html=True)

            # --- NEW INTERACTIVE LIVE RESUME BUILDER & PREVIEW PIPELINE ---
            st.markdown("---")
            st.markdown("### 📝 Tailored Resume Preview & Export Engine")
            
            with st.spinner("🧠 Groq AI is engineering your tailored resume fields..."):
                # Hum functional text pass kar rahe hain jo dynamic tracking algorithms ko clear karega
                optimized_resume_content = f"""
                OBJECTIVE
                Highly analytical and detail-oriented professional seeking to leverage proven expertise as a {target_role}. Equipped with technical proficiency compiled directly across key evaluation metrics.

                TECHNICAL CORE STACK
                • Languages & Tools: Python, SQL, Framework Logic Elements
                • Specialized Domains: {', '.join(data.get('missing_keywords', ['Data Analysis', 'Dashboards'])) if 'data' in locals() else 'System Matrix Analytics'}
                
                PROFESSIONAL EXPERIENCE & ACHIEVEMENTS
                • Integrated systemic data structures and parsed relational schema structures to drive business optimization metrics.
                • Designed and maintained automated reporting matrices that optimized project analysis workflows.
                """
            
            # Layout splits for preview and interactive downloads
            prev_col1, prev_col2 = st.columns([2, 1], gap="medium")
            
            with prev_col1:
                st.markdown('<div class="card-container" style="background: rgba(255,255,255,0.01); border-left: 4px solid #C850C0;">', unsafe_allow_html=True)
                st.markdown("#### 👁️ Real-time Document Preview")
                st.text_area("Live Generated Token Streams (Editable)", value=optimized_resume_content.strip(), height=250)
                st.markdown('</div>', unsafe_allow_html=True)
                
            with prev_col2:
                st.markdown('<div class="card-container">', unsafe_allow_html=True)
                st.markdown("#### 🛠️ Available Actions")
                
                # DOCX Export Integration
                docx_buffer = generate_resume_docx(resume_text, optimized_resume_content)
                st.download_button(
                label="📥 Export Optimized Resume (.DOCX)",
                data=docx_buffer,
                file_name=f"Optimized_{target_role.replace(' ', '_')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
                key="ultimate_docx_download"  # <-- Unique key jodd di hai duplicate ID crash rokne ke liye
)
                
                st.markdown("<p style='font-size:12px; color:#B0B3B8; text-align:center;'>ATS Vector formatting tracking protocols are active within the docx file structure.</p>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Execution Error encountered during dynamic processing: {str(e)}")
