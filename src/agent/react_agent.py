import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from agent.tools import search_medical_info

load_dotenv()

SYSTEM_PROMPT = """당신은 의료 정보 전문 AI 에이전트입니다.
의료 가이드라인 문서를 기반으로 정확한 정보를 제공합니다.

규칙:
1. 반드시 search_medical_info 도구로 검색 후 답변하세요.
2. 검색 결과가 없거나 "찾을 수 없습니다"로 나오면, 절대 추측하거나 지어내지 말고 "죄송합니다, 해당 정보를 문서에서 찾을 수 없습니다"라고 정직하게 답하세요.
3. 모든 답변 마지막에 "본 정보는 참고용이며 전문의 상담을 권장합니다." 문구를 추가하세요.
4. 응급 상황 감지 시 즉시 119 안내하세요.
5. 한국어로 답변하세요.
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