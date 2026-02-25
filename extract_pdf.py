import PyPDF2

pdf_path = r'c:\Users\Адмін\Documents\LAB_1_ALGORITHM\getfile (4).pdf'
pdf = PyPDF2.PdfReader(pdf_path)

for page_num, page in enumerate(pdf.pages):
    print(f"--- PAGE {page_num + 1} ---")
    print(page.extract_text())
    print()
