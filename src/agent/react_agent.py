import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from langchain_groq import ChatGroq
# 이걸로 다시 바꾸기
from langgraph.prebuilt import create_react_agent
from agent.tools import search_medical_info

load_dotenv()

SYSTEM_PROMPT = """당신은 의료 통계 전문 AI 에이전트입니다.
반드시 search_medical_info 도구로 검색한 결과만 사용해서 답변하세요.

규칙:
1. 반드시 search_medical_info 도구로 검색 후 답변하세요.
2. 검색 결과에 없는 내용은 절대 답변하지 마세요.
3. 검색 결과에 없으면 "해당 정보는 보유한 문서에서 찾을 수 없습니다." 라고 답변하세요.
4. 수치는 검색 결과에서 찾은 것만 사용하고 절대 추측하지 마세요.
5. 모든 답변 마지막에 "본 정보는 참고용이며 전문의 상담을 권장합니다." 를 추가하세요.
6. 응급 상황 감지 시 즉시 119 안내하세요.
7. 한국어로 답변하세요.
"""

def build_agent():
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",   # llama-3.1-8b-instant 에서 변경
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.2
    )
    agent = create_react_agent(
        llm,
        [search_medical_info],
        prompt=SYSTEM_PROMPT
    )
    return agent

if __name__ == "__main__":
    agent = build_agent()
    result = agent.invoke({
        "messages": [("user", "고혈압 치료 방법 알려줘")]
    })
    print("\n=== 최종 답변 ===")
    print(result["messages"][-1].content)