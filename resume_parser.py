import fitz  # PyMuPDF
import re
import json


PDF_PATH = r"path"


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)

    full_text = ""

    for page in doc:
        full_text += page.get_text()

    return full_text


def clean_text(text):
    text = re.sub(r'\n+', '\n', text)
    return text.strip()


def extract_sections(text):
    """
    Basic section parser.
    """

    section_titles = [
        "TECHNICAL SKILLS",
        "EDUCATION",
        "CERTIFICATIONS",
        "TECHNICAL PROJECTS",
        "RELATED EXPERIENCE",
        "ADDITIONAL EXPERIENCE"
    ]

    sections = {}

    current_section = "HEADER"
    sections[current_section] = []

    lines = text.split("\n")

    for line in lines:
        stripped = line.strip()

        if stripped in section_titles:
            current_section = stripped
            sections[current_section] = []
            continue

        sections[current_section].append(stripped)

    return sections


def save_sections(sections):
    with open("parsed_resume.json", "w", encoding="utf-8") as f:
        json.dump(sections, f, indent=4)


def main():
    print("Parsing resume...")

    text = extract_text_from_pdf(PDF_PATH)
    text = clean_text(text)

    sections = extract_sections(text)

    save_sections(sections)

    print("Resume parsing complete.")
    print("Created parsed_resume.json")

    print("\nDetected Sections:")
    for section in sections.keys():
        print(f"- {section}")


if __name__ == "__main__":
    main()
