from docx2pdf import convert
import os


DOCX_FILE = "tailored_resume.docx"

PDF_FOLDER = "pdf_resumes"

os.makedirs(PDF_FOLDER, exist_ok=True)

PDF_OUTPUT = os.path.join(
    PDF_FOLDER,
    "tailored_resume.pdf"
)


convert(DOCX_FILE, PDF_OUTPUT)

print("Resume PDF created.")
print(f"Saved to: {PDF_OUTPUT}")