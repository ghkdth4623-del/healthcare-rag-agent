import os
import pdfplumber

def load_pdf(file_path: str) -> str:
    """PDF에서 텍스트 추출"""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        print(f"총 페이지 수: {len(pdf.pages)}")
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    print(f"추출된 텍스트 길이: {len(text)}자")
    return text

def load_all_pdfs(folder_path: str = "data/raw") -> str:
    """폴더 안의 모든 PDF 불러오기"""
    full_text = ""
    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            print(f"처리 중: {file}")
            text = load_pdf(os.path.join(folder_path, file))
            full_text += text + "\n"
    return full_text

if __name__ == "__main__":
    text = load_all_pdfs()
    print(text[:300])