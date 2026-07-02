import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain.tools import tool
from ingestion.vectorstore import load_vectorstore

@tool
def search_medical_info(query: str) -> str:
    """의료 가이드라인에서 관련 정보를 검색합니다. 질병, 치료, 약물 등을 검색할 때 사용하세요."""
    try:
        vectorstore = load_vectorstore()
        retriever = vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 5, "fetch_k": 10}
        )
        docs = retriever.invoke(query)
        if not docs:
            return "관련 의료 정보를 찾을 수 없습니다."
        return "\n\n".join([doc.page_content for doc in docs])
    except Exception as e:
        return f"검색 오류: {e}"