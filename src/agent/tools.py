# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain.tools import tool
from ingestion.vectorstore import load_vectorstore

def clean_text(text: str, max_length: int = 300) -> str:
    import re
    text = re.sub(r'\s+', ' ', text).strip()
    if len(text) > max_length:
        text = text[:max_length] + "..."
    return text

@tool
def search_medical_info(query: str) -> str:
    """지역 건강 통계 문서에서 관련 정보를 검색합니다. 지역별 건강 통계, 유병률 등을 검색할 때 사용하세요."""
    try:
        vectorstore = load_vectorstore()
        retriever = vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 3, "fetch_k": 6}
        )
        docs = retriever.invoke(query)
        if not docs:
            return "관련 정보를 찾을 수 없습니다."
        results = [clean_text(doc.page_content) for doc in docs]
        return "\n\n".join(results)
    except Exception as e:
        return f"검색 오류: {e}"