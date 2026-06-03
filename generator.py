# generator.py
import io
import markdown
from docx import Document
from docx.shared import Inches, Pt, RGBColor  # Clean direct import
from docx.enum.text import WD_ALIGN_PARAGRAPH
from xhtml2pdf import pisa

def generate_resume_docx(target_role, optimized_content):
    """
    Generates a beautifully structured, clean typographic layout for Word
    with 1-inch margins, bold uppercase headings, and crisp list bullet offsets.
    """
    doc = Document()
    
    # 1. Professional Page Architecture (Standard 1-Inch Margins)
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
        
    # 2. Executive Centered Contact Header
    p_name = doc.add_paragraph()
    p_name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_name = p_name.add_run("YOUR NAME")
    r_name.font.name = 'Arial'
    r_name.font.size = Pt(22)
    r_name.bold = True
    
    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_meta = p_meta.add_run("Email: email@example.com  |  Phone: +123 456 7890  |  Jamshedpur, Jharkhand")
    r_meta.font.name = 'Arial'
    r_meta.font.size = Pt(10.5)
    
    # FIXED: Direct assignment using our imported RGBColor class (No more NameError)
    r_meta.font.color.rgb = RGBColor(100, 100, 100)

    doc.add_paragraph("―" * 50).alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # 3. Dynamic Section Rendering
    lines = optimized_content.split('\n')
    for line in lines:
        clean_line = line.strip()
        if not clean_line:
            continue
            
        # Transform structural titles into clear, bold dividers
        if clean_line.startswith('###') or "SUMMARY" in clean_line.upper() or "SKILLS" in clean_line.upper() or "EXPERIENCE" in clean_line.upper() or "EDUCATION" in clean_line.upper():
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(4)
            r = p.add_run(clean_line.replace('#', '').replace('*', '').upper().strip())
            r.font.name = 'Arial'
            r.bold = True
            r.font.size = Pt(12)
            
        # Cleanly indent list bullet targets
        elif clean_line.startswith('•') or clean_line.startswith('*') or clean_line.startswith('-'):
            clean_bullet = clean_line.lstrip('•*-').strip()
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.space_after = Pt(3)
            r = p.add_run(clean_bullet)
            r.font.name = 'Arial'
            r.font.size = Pt(11)
        else:
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(4)
            r = p.add_run(clean_line)
            r.font.name = 'Arial'
            r.font.size = Pt(11)
                
    file_stream = io.BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)
    return file_stream


def generate_resume_pdf(target_role, optimized_content):
    """
    Transforms plain text into an exceptionally clean, modern 
    minimalist PDF template utilizing sharp lines and strict column tracking.
    """
    # Parse Markdown data to logical web elements natively
    body_html_content = markdown.markdown(optimized_content)
    
    # Professional Styling Shell Injection
    full_html_document = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            @page {{
                size: a4;
                margin: 20mm 18mm 20mm 18mm;
            }}
            body {{
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                color: #2c3e50;
                font-size: 10.5pt;
                line-height: 1.5;
            }}
            .header-container {{
                text-align: center;
                margin-bottom: 25px;
            }}
            h1 {{
                font-size: 24pt;
                font-weight: 700;
                letter-spacing: 0.5px;
                margin: 0 0 5px 0;
                color: #1a252f;
            }}
            .contact-info {{
                font-size: 10pt;
                color: #7f8c8d;
                word-spacing: 1px;
            }}
            h2, h3 {{
                color: #1a252f;
                font-size: 12pt;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.8px;
                margin-top: 20px;
                margin-bottom: 8px;
                border-bottom: 1.5px solid #2c3e50;
                padding-bottom: 2px;
            }}
            p {{
                margin-top: 4px;
                margin-bottom: 6px;
                text-align: justify;
            }}
            ul {{
                margin-top: 4px;
                margin-bottom: 6px;
                padding-left: 18px;
            }}
            li {{
                margin-bottom: 4px;
                text-align: justify;
            }}
            strong {{
                color: #111111;
            }}
        </style>
    </head>
    <body>
        <div class="header-container">
            <h1>YOUR NAME</h1>
            <div class="contact-info">
                Email: email@example.com &nbsp;&bull;&nbsp; Phone: +123 456 7890 &nbsp;&bull;&nbsp; Jamshedpur, Jharkhand
            </div>
        </div>
        
        <div class="content-body">
            {body_html_content}
        </div>
    </body>
    </html>
    """
    
    pdf_buffer = io.BytesIO()
    pisa.CreatePDF(src=full_html_document, dest=pdf_buffer)
    pdf_buffer.seek(0)
    return pdf_buffer