# app.py
import streamlit as st
import json
import os
import io
from dotenv import load_dotenv
from groq import Groq

# Import text extractor and document compilers from our custom modules
from parser import get_document_text
from generator import generate_resume_docx, generate_resume_pdf

# Load environment configurations (.env file)
load_dotenv()

# 1. Page Layout Configuration Setup
st.set_page_config(
    page_title="AI Resume ATS Optimizer", 
    layout="wide", 
    page_icon="📄"
)

st.title("📄 AI-Powered ATS Resume Evaluator")
st.subheader("Get real-time scoring, gap analysis, and tailored formatting updates.")

# 2. Front-End Input Panels (Two Column Core UI Setup)
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.header("🎯 Target Context")
    target_role = st.text_input(
        "Desired Position / Job Title", 
        placeholder="e.g., Data Analyst, Software Engineer"
    )
    job_description = st.text_area(
        "Paste Target Job Description (JD) Here", 
        height=300, 
        placeholder="Paste the full job requirements or core lines here..."
    )

with col2:
    st.header("📤 Upload Your Resume")
    uploaded_file = st.file_uploader(
        "Choose a file (PDF or DOCX)", 
        type=["pdf", "docx"]
    )
    
    extracted_text = ""
    if uploaded_file is not None:
        st.success(f"Successfully uploaded: '{uploaded_file.name}'")
        
        with st.spinner("Extracting text from document..."):
            extracted_text = get_document_text(uploaded_file)
            
        with st.expander("🔍 View Extracted Resume Text"):
            if extracted_text.startswith("Error") or extracted_text == "Unsupported file format.":
                st.error(extracted_text)
            else:
                st.text(extracted_text[:1000] + "\n... [Truncated for Preview] ...")

# 3. Main Action Trigger: Analyze Resume via Groq Engine
st.markdown("---")
if st.button("🚀 Analyze Resume Against Job Description", use_container_width=True):
    if not job_description or not extracted_text or not target_role:
        st.warning("Please fill out the Job Title, Job Description, and upload a Resume file before running the analysis.")
    else:
        with st.spinner("🔄 Running real-time ATS and System checks..."):
            from ai_engine import analyze_resume_realtime
            raw_response = analyze_resume_realtime(extracted_text, job_description)
            
            try:
                # Parse JSON output from Groq Engine
                analysis = json.loads(raw_response)
                
                # Save results to session state so they persist when generation buttons are triggered
                st.session_state['analysis_results'] = analysis
                st.success("✅ Analysis Complete!")
                
            except json.JSONDecodeError:
                st.error("Failed to parse clean metrics from the AI engine. Raw Engine Output below:")
                st.code(raw_response)

# 4. Display Evaluation Metrics & Analytics Dashboard
if 'analysis_results' in st.session_state:
    analysis = st.session_state['analysis_results']
    
    st.header("📊 Evaluation Dashboard")
    
    # Render Dynamic Metric Score Bar Tracker
    score = analysis.get("ats_score", 0)
    col_metric, col_progress = st.columns([1, 3])
    with col_metric:
        st.metric(label="Overall ATS Match Score", value=f"{score}%")
    with col_progress:
        st.markdown("<br>", unsafe_allow_html=True)
        st.progress(score / 100)
    
    st.markdown("---")
    
    # Render Strategic Structural Analysis Columns
    res_col1, res_col2 = st.columns(2, gap="medium")
    
    with res_col1:
        st.subheader("❌ Missing Keywords & Skills")
        keywords = analysis.get("missing_keywords", [])
        if keywords:
            for kw in keywords:
                st.markdown(f"• :red[{kw}]")
        else:
            st.write("No major missing keywords found!")
            
        st.subheader("⚠️ Detected Experience Gaps")
        gaps = analysis.get("experience_gaps", [])
        if gaps:
            for gap in gaps:
                st.markdown(f"• {gap}")
        else:
            st.write("No major domain experience gaps noticed.")

    with res_col2:
        st.subheader("💡 Tailored Optimization Suggestions")
        suggestions = analysis.get("profile_suggestions", [])
        if suggestions:
            for idx, sug in enumerate(suggestions, 1):
                st.info(f"**Action {idx}:** {sug}")
        else:
            st.write("Your layout and profiles match optimally with the target specifications!")
            
    st.markdown("---")
    
    # 5. Document Digital Preview & Dynamic Rewrite Generation Engine
    st.header("✨ AI Resume Generation Engine")
    st.write("Ready to fill those gaps? Click below to let the AI rewrite your profile text tailored to your target job parameters.")
    
    if st.button("🛠️ Generate Optimized Resume Text", use_container_width=True):
        with st.spinner("Rewriting content using real-time JD alignments..."):
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                st.error("Groq API Key missing from configuration pipeline.")
            else:
                try:
                    # Initialize the Groq core pipeline channel
                    ai_client = Groq(api_key=api_key)
                    
                    rewrite_prompt = f"""
                    Using this original resume: {extracted_text} 
                    targeting this role: {target_role} 
                    with this Job Description: {job_description}, 
                    
                    Rewrite a comprehensive, professional resume layout text. Optimize for missing keywords natively. 
                    Include:
                    1. Professional Summary / Objective statement
                    2. Key Core Competencies / Technical Skills list
                    3. Updated experience bullet points incorporating quantifiable metrics.
                    
                    Add clear Markdown headings for sections like SUMMARY, SKILLS, and EXPERIENCE.
                    Provide clean, ready-to-read layout text. Do not include introductory notes, markdown code fences (like ```), or chat commentary.
                    """
                    
                    # Using the active flagship Llama 3.3 model to avoid decommissioning errors
                 # Using the active versatile production Llama 3.3 model
                    completion = ai_client.chat.completions.create(
                        model="llama-3.3-70b-versatile",  # <-- UPDATED ENDPOINT
                        messages=[{"role": "user", "content": rewrite_prompt}],
                        temperature=0.3
                    )
                    
                    raw_draft = completion.choices[0].message.content
                    st.session_state['resume_draft'] = raw_draft
                    st.success("✨ Optimization complete! Preview generated below.")
                    
                except Exception as e:
                    st.error(f"Error connecting to optimization service: {e}")

    # If the tailored layout draft is built, handle preview rendering and download pipeline
    if 'resume_draft' in st.session_state:
        st.subheader("📋 Document Digital Preview")
        
        # Build an aesthetic physical white-page layout simulation using structural container tags
        preview_html = f"""
        <div style="background-color: white; color: #333333; padding: 30px; border: 1px solid #dddddd; border-radius: 5px; font-family: 'Helvetica', Arial, sans-serif; box-shadow: 1px 1px 10px rgba(0,0,0,0.05); max-height: 400px; overflow-y: auto;">
            <h1 style="text-align: center; margin-bottom: 0; color: #111111; font-size: 24px;">YOUR NAME</h1>
            <p style="text-align: center; font-size: 12px; color: #666666; margin-top: 5px;">Email: email@example.com | Phone: +123 456 7890 | Location: Jamshedpur, Jharkhand</p>
            <hr style="border: 0; border-top: 2px solid #333333; margin: 15px 0;">
            <div style="white-space: pre-wrap; font-size: 14px; line-height: 1.6; text-align: left;">{st.session_state['resume_draft']}</div>
        </div>
        """
        # Inject the live scrollable mock layout safely into the screen canvas
        st.markdown(preview_html, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.subheader("📥 Choose Your Download Format")
        dl_col1, dl_col2 = st.columns(2)
        
        with dl_col1:
            # Word Document Compiler Output Stream
            docx_buffer = generate_resume_docx(target_role, st.session_state['resume_draft'])
            st.download_button(
                label="📥 Download Tailored Resume (.DOCX)",
                data=docx_buffer,
                file_name=f"{target_role.replace(' ', '_')}_Optimized_Resume.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
            
        with dl_col2:
            # Native Python-HTML PDF Document Output Stream (Safe from Windows DLL errors)
            with st.spinner("Compiling PDF configuration assets..."):
                pdf_buffer = generate_resume_pdf(target_role, st.session_state['resume_draft'])
            st.download_button(
                label="📥 Download Tailored Resume (.PDF)",
                data=pdf_buffer,
                file_name=f"{target_role.replace(' ', '_')}_Optimized_Resume.pdf",
                mime="application/pdf",
                use_container_width=True
            )