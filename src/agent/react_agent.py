# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from agent.tools import search_medical_info

load_dotenv()

SYSTEM_PROMPT = """당신은 지역 건강 통계 전문 AI 에이전트입니다.
반드시 search_medical_info 도구로 검색한 결과만 사용해서 답변하세요.

규칙:
1. 반드시 search_medical_info 도구로 검색 후 답변하세요.
2. 검색 결과에 없는 수치는 절대 만들어내지 마세요.
3. 특정 지역 개별 수치가 없으면 '해당 문서는 전국/권역별 통계만 포함하고 있어 특정 지역 수치는 제공할 수 없습니다.' 라고 답변하세요.
4. 검색 결과에 있는 내용만 답변하세요.
5. 모든 답변 마지막에 '본 정보는 참고용이며 전문의 상담을 권장합니다.' 를 추가하세요.
6. 응급 상황 감지 시 즉시 119 안내하세요.
7. 한국어로 답변하세요.
"""

from langchain_core.messages import SystemMessage

def build_agent():
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )
    agent = create_react_agent(
        llm,
        [search_medical_info],
    )
    return agent

if __name__ == "__main__":
    agent = build_agent()
    result = agent.invoke({
        "messages": [("user", "서울 고혈압 유병률 알려줘")]
    })
    print("\n=== 최종 답변 ===")
    print(result["messages"][-1].content)