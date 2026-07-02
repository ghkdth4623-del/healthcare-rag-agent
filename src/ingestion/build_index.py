"""
data/raw 폴더의 모든 PDF를 읽어서
텍스트 추출 -> 청크 분할 -> FAISS 인덱스 생성/저장까지 한 번에 처리하는 스크립트.

실행 방법 (프로젝트 루트에서):
    python src/ingestion/build_index.py
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ingestion.pdf_loader import load_all_pdfs
from ingestion.vectorstore import split_text, save_vectorstore


def main():
    raw_folder = "data/raw"
    save_path = "data/processed/faiss_index"

    if not os.path.exists(raw_folder):
        print(f"[오류] '{raw_folder}' 폴더가 없습니다. PDF를 먼저 넣어주세요.")
        return

    pdf_files = [f for f in os.listdir(raw_folder) if f.endswith(".pdf")]
    if not pdf_files:
        print(f"[오류] '{raw_folder}' 폴더에 PDF 파일이 없습니다.")
        return

    print(f"발견된 PDF 파일: {len(pdf_files)}개")
    for f in pdf_files:
        print(f"  - {f}")

    print("\n[1/3] PDF 텍스트 추출 중...")
    full_text = load_all_pdfs(raw_folder)

    if not full_text.strip():
        print("[오류] PDF에서 텍스트를 추출하지 못했습니다. (스캔본/이미지 PDF일 수 있음)")
        return

    print("\n[2/3] 텍스트 청크 분할 중...")
    chunks = split_text(full_text)

    print("\n[3/3] 임베딩 및 FAISS 인덱스 생성 중... (다소 시간이 걸릴 수 있습니다)")
    save_vectorstore(chunks, save_path)

    print(f"\n완료! 인덱스가 '{save_path}'에 저장되었습니다.")
    print("이제 'streamlit run src/ui/app.py'로 챗봇을 실행해보세요.")


if __name__ == "__main__":
    main()