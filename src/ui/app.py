import streamlit as st
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from src.agent.react_agent import build_agent

st.set_page_config(page_title="헬스케어 RAG 챗봇", page_icon="🏥", layout="wide")

# --- 커스텀 스타일 ---
st.markdown("""
<style>
    .stChatMessage { border-radius: 12px; }
    div[data-testid="stChatMessageContent"] { font-size: 15px; }
    .example-btn button {
        width: 100%;
        text-align: left;
        white-space: normal;
    }
</style>
""", unsafe_allow_html=True)

EXAMPLE_QUESTIONS = [
    "당뇨병 진단 경험률 지역별로 어때?",
    "주관적 건강인지율이 가장 높은 지역이 어디야?",
    "흡연율 지역 간 격차는 어떻게 돼?",
    "지역사회건강조사는 어떻게 진행돼?",
]

with st.sidebar:
    st.title("🏥 헬스케어 RAG 챗봇")
    st.caption("지역건강통계 문서 기반 AI 챗봇")
    st.markdown("---")

    st.subheader("💡 예시 질문")
    for q in EXAMPLE_QUESTIONS:
        if st.button(q, key=f"ex_{q}", use_container_width=True):
            st.session_state.pending_question = q

    st.markdown("---")
    if st.button("🗑️ 대화 초기화", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.caption("⚠️ 본 챗봇의 답변은 참고용이며, 실제 의료 판단은 반드시 전문의와 상담하세요.")

st.title("💊 의료 정보 질문하기")
st.caption("질병관리청 「2025 지역건강통계 한눈에 보기」 문서를 기반으로 답변합니다.")


@st.cache_resource
def get_agent():
    return build_agent()


if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

# 기존 대화 표시
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 입력 처리 (사이드바 예시 질문 클릭 or 직접 입력)
user_input = st.chat_input("질문을 입력하세요 (예: 당뇨병 진단율 알려줘)")
if st.session_state.pending_question:
    user_input = st.session_state.pending_question
    st.session_state.pending_question = None

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("문서를 검색하고 답변을 준비하는 중..."):
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
                st.error("답변 생성 중 문제가 발생했어요. 질문을 조금 더 구체적으로 바꿔서 다시 시도해보세요.")
                with st.expander("자세한 오류 내용 (개발자용)"):
                    import traceback
                    st.code(traceback.format_exc())