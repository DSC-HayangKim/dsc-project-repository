"""
실제 Agent 응답을 실시간으로 확인하는 스크립트

실행 방법:
    python tests/manual_agent_test.py
"""
import asyncio
from app.agent.core import process_message

async def test_simple_query():
    print("=" * 60)
    print("🤖 AI Agent 테스트 시작")
    print("=" * 60)
    
    query = "안녕? 테스트야"
    print(f"\n📝 질문: {query}\n")
    print("💬 AI 응답:\n")
    
    full_response = ""
    async for chunk in process_message(query, []):
        print(chunk, end="", flush=True)
        full_response += chunk
    
    print(f"\n\n✅ 응답 완료! (총 {len(full_response)}자)")
    print("=" * 60)

async def test_vector_search():
    print("\n" + "=" * 60)
    print("🔍 벡터 DB 검색 테스트")
    print("=" * 60)
    
    query = "항공기를 좀더 견고하면서도 가벼운 소재로 바꾸고 싶어 관련된 특허 없어?"
    print(f"\n📝 질문: {query}\n")
    print("💬 AI 응답:\n")
    
    full_response = ""
    async for chunk in process_message(query, []):
        print(chunk, end="", flush=True)
        full_response += chunk
    
    print(f"\n\n✅ 응답 완료! (총 {len(full_response)}자)")
    print("=" * 60)

async def test_with_history():
    print("\n" + "=" * 60)
    print("💭 대화 히스토리 테스트")
    print("=" * 60)
    
    history = [
        ("user", "안녕하세요"),
        ("assistant", "안녕하세요! 무엇을 도와드릴까요?"),
    ]
    
    print("\n📚 대화 히스토리:")
    for role, content in history:
        emoji = "👤" if role == "user" else "🤖"
        print(f"  {emoji} {role}: {content}")
    
    query = "항공 관련 특허를 찾고 있어요"
    print(f"\n📝 질문: {query}\n")
    print("💬 AI 응답:\n")
    
    full_response = ""
    async for chunk in process_message(query, history):
        print(chunk, end="", flush=True)
        full_response += chunk
    
    print(f"\n\n✅ 응답 완료! (총 {len(full_response)}자)")
    print("=" * 60)

async def main():
    print("\n" + "🚀 " * 20)
    print("Agent 실시간 응답 테스트 시작!")
    print("🚀 " * 20 + "\n")
    
    # 1. 간단한 질문
    await test_simple_query()
    
    # 2. 벡터 DB 검색
    await test_vector_search()
    
    # 3. 대화 히스토리 포함
    await test_with_history()
    
    print("\n" + "🎉 " * 20)
    print("모든 테스트 완료!")
    print("🎉 " * 20 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
