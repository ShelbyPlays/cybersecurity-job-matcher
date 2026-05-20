from docx2pdf import convert
import os


COVER_FOLDER = "cover_letters"
PDF_FOLDER = "pdf_cover_letters"

os.makedirs(PDF_FOLDER, exist_ok=True)


for filename in os.listdir(COVER_FOLDER):

    if filename.endswith(".docx"):

        docx_path = os.path.join(COVER_FOLDER, filename)

        pdf_name = filename.replace(".docx", ".pdf")

        pdf_path = os.path.join(PDF_FOLDER, pdf_name)

        convert(docx_path, pdf_path)

        print(f"Converted: {filename}")