import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_text(text: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=300
    )
    chunks = splitter.split_text(text)
    # None 값 제거
    chunks = [c for c in chunks if c and c.strip()]
    print(f"청크 수: {len(chunks)}개")
    return chunks

def save_vectorstore(chunks, save_path: str = "data/processed/faiss_index"):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    vectorstore = FAISS.from_texts(chunks, embeddings)
    os.makedirs(save_path, exist_ok=True)
    vectorstore.save_local(save_path)
    print(f"벡터 저장 완료: {save_path}")
    return vectorstore

_vectorstore_cache = None

def load_vectorstore(save_path: str = "data/processed/faiss_index"):
    global _vectorstore_cache
    if _vectorstore_cache is not None:
        return _vectorstore_cache
    
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    _vectorstore_cache = FAISS.load_local(
        save_path, embeddings,
        allow_dangerous_deserialization=True
    )
    return _vectorstore_cache

if __name__ == "__main__":
    from pdf_loader import load_all_pdfs
    text = load_all_pdfs()
    chunks = split_text(text)
    save_vectorstore(chunks)
    print("완료!")