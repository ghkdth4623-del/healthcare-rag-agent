# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain.tools import tool
from ingestion.vectorstore import load_vectorstore

def clean_text(text: str, max_length: int = 800) -> str:
    import re
    text = re.sub(r'\s+', ' ', text).strip()
    if len(text) > max_length:
        text = text[:max_length] + "..."
    return text

@tool
def search_medical_info(query: str) -> str:
    """지역 건강 통계 문서에서 관련 정보를 검색합니다."""
    try:
        vectorstore = load_vectorstore()
        retriever = vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 5, "fetch_k": 10}
        )
        docs = retriever.invoke(query)
        if not docs:
            return "관련 정보를 찾을 수 없습니다."
        results = [clean_text(doc.page_content, max_length=1000) for doc in docs]
        return "\n\n".join(results)
    except Exception as e:
        return f"검색 오류: {e}"