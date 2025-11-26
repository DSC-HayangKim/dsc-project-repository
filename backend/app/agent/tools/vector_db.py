import os
from langchain.tools import tool
from supabase import create_client, Client
from app.core.embedding import get_embedding
from app.db import supabase

@tool
def get_patent_by_id(id : str) -> str:
    """
    ID로 특허 정보를 조회합니다.

    Args:
        id (str): DataBase에 저장된 특허 PK _ID.
        
    Returns:
        str: 특허 정보.
    """

    try:
        response = supabase.table("patents").select("*").eq("id", id).execute()
        if not response.data:
            return "검색 결과가 없습니다."

        return f"\n제목: {response.data[0]['invention_title']}\n내용: {response.data[0]['abstract_content']}\n"

    except Exception as e:
        return f"get_patent_by_id Error: {str(e)}"

@tool
def vector_db_search(query: str) -> str:
    """
    벡터 데이터베이스에서 관련 특허 정보를 검색합니다.
    사용자의 질문과 관련된 특허 문서를 찾아 반환합니다.
    
    Args:
        query (str): 검색할 질문 또는 키워드.
        
    Returns:
        str: 검색된 문서들의 요약 정보.
    """

    print(f"{query} 가 agent가 사용함. \n", flush=True)

    try:
        # 1. Query Embedding
        query_embedding = get_embedding(query)
        
        # 2. Supabase RPC Call
        # 'match_patents' function must be defined in Supabase
        params = {
            "query_embedding": query_embedding,
            "match_threshold": 0.5, # Adjust threshold as needed
            "match_count": 10
        }
        
        response = supabase.rpc("match_patents_all_info", params).execute()
        
        if not response.data:
            return "검색 결과가 없습니다."
            
        # 3. Format Results
        results = []
        for doc in response.data:
            title = doc.get("invention_title", "제목 없음")
            summary = doc.get("abstract_content")
            similarity = doc.get("similarity", 0)
            applicant = doc.get("applicant_name", "출원인 불명")
            app_number = doc.get("application_number", "출원번호 불명")
            applicant_date = doc.get("application_date", "출원시기 불명")

            results.append(f"[제목: {title}]\n(유사도: {similarity:.4f})\n내용: {summary[:300]}...\n출원인: {applicant}\n출원번호: {app_number}\n출원시기: {applicant_date}")
            
        return "\n\n".join(results)
        
    except Exception as e:
        return f"vector_db_search Error: {str(e)}"


@tool
def get_contact_info_by_applicant(applicant: str):
    """
    신청인 이름으로 연락 방법을 조회합니다.

    Args:
        applicant (str): 연락처를 조회할 신청인 이름.

    Returns:
        str: 신청인의 연락 방법(평문)
    """

    print(f"[DEBUG] get_contact_info_by_applicant Agent Used by query : {applicant}")
    try:
        response = supabase.table("contacts").select("applicant, contact").ilike("applicant", f"%{applicant}%").execute()
        if not response.data:
            return "검색 결과가 없습니다."

        contact_info = []
        for record in response.data:
            contact_info.append(f"신청인: {record['applicant']}, 연락처: {record['contact']}")
        return "\n".join(contact_info)

    except Exception as e:
        return f"get_contact_info_by_applicant Error: {str(e)}"