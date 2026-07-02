import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_text(text: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_text(text)
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

def load_vectorstore(save_path: str = "data/processed/faiss_index"):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    return FAISS.load_local(
        save_path, embeddings,
        allow_dangerous_deserialization=True
    )