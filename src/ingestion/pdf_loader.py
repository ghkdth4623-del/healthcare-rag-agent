import os
import pdfplumber

def load_pdf(file_path: str) -> str:
    text = ""
    with pdfplumber.open(file_path) as pdf:
        print(f"총 페이지 수: {len(pdf.pages)}")
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

            tables = page.extract_tables()
            for table in tables:
                if not table or len(table) < 2:
                    continue
                header = table[0]
                for row in table[1:]:
                    if not row:
                        continue
                    row_texts = []
                    for i, cell in enumerate(row):
                        if cell and i < len(header) and header[i]:
                            row_texts.append(f"{header[i]}:{cell}")
                    if row_texts:
                        text += " | ".join(row_texts) + "\n"

    print(f"추출된 텍스트 길이: {len(text)}자")
    return text

def load_all_pdfs(folder_path: str = "data/raw") -> str:
    full_text = ""
    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            print(f"처리 중: {file}")
            text = load_pdf(os.path.join(folder_path, file))
            full_text += text + "\n"
    return full_text

if __name__ == "__main__":
    text = load_all_pdfs()
    print(text[:500])