# 헬스케어 RAG 챗봇

의료 가이드라인 문서 기반 AI 챗봇

## 기술 스택
- LLM: Groq (llama-3.1-8b-instant)
- 임베딩: HuggingFace
- 벡터DB: FAISS
- UI: Streamlit

## 실행 방법
pip install -r requirements.txt
streamlit run src/ui/app.py