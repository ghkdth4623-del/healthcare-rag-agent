import streamlit as st
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from src.agent.react_agent import build_agent

st.set_page_config(page_title="헬스케어 RAG 챗봇", page_icon="🏥", layout="wide")

with st.sidebar:
    st.title("🏥 헬스케어 RAG 챗봇")
    st.markdown("---")
    st.caption("의료 가이드라인 기반 AI 챗봇")
    if st.button("대화 초기화"):
        st.session_state.messages = []
        st.rerun()

st.title("💊 의료 정보 질문하기")
st.caption("의료 가이드라인 기반으로 답변합니다.")

@st.cache_resource
def get_agent():
    return build_agent()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("질문을 입력하세요"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("답변 생성 중..."):
            try:
                agent = get_agent()
                result = agent.invoke({
                    "messages": [("user", user_input)]
                })
                answer = result["messages"][-1].content
                st.markdown(answer)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })
            except Exception as e:
                import traceback
                st.error(f"오류: {str(e)}\n{traceback.format_exc()}")