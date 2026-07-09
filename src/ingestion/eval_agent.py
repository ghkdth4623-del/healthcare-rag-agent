"""
검증용 질문-정답 세트로 Agent 답변 정확도를 자동 체크하는 스크립트.

실행 방법 (프로젝트 루트에서):
    python src/ingestion/eval_agent.py
"""
import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.react_agent import build_agent

# 질문과, 답변에 반드시 포함되어야 하는 핵심 키워드(정답 근거) 목록
TEST_CASES = [
    {
        "question": "2025년 전국 현재흡연율 중앙값은?",
        "expected_keywords": ["17.9"],
    },
    {
        "question": "2025년 전국 월간음주율 중앙값은?",
        "expected_keywords": ["57.1"],
    },
    {
        "question": "2025년 전국 고위험음주율 중앙값은?",
        "expected_keywords": ["12.0"],
    },
    {
        "question": "2024년 현재흡연율 중앙값은?",
        "expected_keywords": ["18.9"],
    },
    {
        "question": "코로나 백신 부작용 알려줘",
        "expected_keywords": ["찾을 수 없", "모르", "제공할 수 없"],
    },
]


def run_eval():
    agent = build_agent()
    results = []

    for i, case in enumerate(TEST_CASES, 1):
        print(f"\n[{i}/{len(TEST_CASES)}] 질문: {case['question']}")
        time.sleep(1)  # TPM(분당 토큰) 제한 방지용 대기
        try:
            result = agent.invoke({
                "messages": [("user", case["question"])]
            })
            answer = result["messages"][-1].content
        except Exception as e:
            answer = f"[에러 발생] {e}"

        print(f"답변: {answer[:200]}{'...' if len(answer) > 200 else ''}")

        passed = any(kw in answer for kw in case["expected_keywords"])
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"결과: {status} (기대 키워드: {case['expected_keywords']})")

        results.append({
            "question": case["question"],
            "answer": answer,
            "passed": passed,
        })

    print("\n" + "=" * 50)
    print("최종 결과")
    print("=" * 50)
    passed_count = sum(1 for r in results if r["passed"])
    for r in results:
        mark = "✅" if r["passed"] else "❌"
        print(f"{mark} {r['question']}")
    print(f"\n총 {len(results)}개 중 {passed_count}개 통과 ({passed_count}/{len(results)})")


if __name__ == "__main__":
    run_eval()