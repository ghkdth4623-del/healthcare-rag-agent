# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from agent.tools import search_medical_info

load_dotenv()

SYSTEM_PROMPT = """You are a health statistics assistant. 
RULES:
1. Use search_medical_info tool first.
2. Answer in Korean ONLY.
3. If not found, say exactly: "해당 정보는 문서에서 찾을 수 없습니다."
4. Never use any other tools.
5. End with: "본 정보는 참고용이며 전문의 상담을 권장합니다."
"""

from langchain_core.messages import SystemMessage

def build_agent():
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.2
    )
    agent = create_react_agent(
        llm,
        [search_medical_info],
        prompt=SYSTEM_PROMPT,
    )
    return agent

if __name__ == "__main__":
    agent = build_agent()
    result = agent.invoke({
        "messages": [("user", "서울 고혈압 유병률 알려줘")]
    })
    print("\n=== 최종 답변 ===")
    print(result["messages"][-1].content)