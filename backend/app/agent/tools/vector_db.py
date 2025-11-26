import os
from langchain.tools import tool
from supabase import create_client, Client
from app.core.embedding import get_embedding
from app.db import supabase

@tool
def get_patent_by_applicant_number(application_number: str) -> str:
    """
    출원번호로 특허 정보를 조회합니다.

    Args:
        application_number (str): 특허의 출원번호.

    Returns:
        str: 출원번호에 해당하는 특허 정보 (JSON 문자열).
    """

    print(f"[DEBUG] get_patent_by_applicant_number Agent Used by query : {application_number}")
    try:
        response = supabase.table("patents").select("*").eq("application_number", application_number).execute()
        if response.data:
            return str(response.data[0])
        else:
            return "해당 출원번호로 특허를 찾을 수 없습니다."
    except Exception as e:
        return f"특허 정보를 조회하는 중 오류가 발생했습니다: {e}"


@tool
def get_patent_by_id(id : str) -> str:
    """
    ID로 특허 정보를 조회합니다.

    Args:
        id (str): DataBase에 저장된 특허 PK _ID.
        
    Returns:
        str: 특허 정보.
    """

    print(f"[DEBUG] get_patent_by_id Agent Used by query : {id}")

    try:
        response = supabase.table("patents").select("*").eq("_id", id).execute()
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
            _id = doc.get("_id", "ID 불명")

            results.append(f"_id: {_id}\n제목: {title}\n(유사도: {similarity:.4f})\n내용: {summary[:300]}...\n출원인: {applicant}\n출원번호: {app_number}\n출원시기: {applicant_date}")
            
        return "\n\n".join(results)
        
    except Exception as e:
        return f"vector_db_search Error: {str(e)}"


@tool
def get_contact_info_by_applicant(applicant: str):
    """
    신청인 이름으로 연락 방법을 조회합니다.
    사용시 주의사항 : 
    1. 신청인 이름을 정확하게 입력해야 합니다.
    2. 신청인 이름은 기관, 학교 단위로 검색됩니다. 산학협력단 키워드를 넣지 마십시오.
    3. 신청인 이름은 alike로 검색됩니다.

    Args:
        applicant (str): 연락처를 조회할 신청인 이름(기관, 학교 단위로 검색하세요 alike로 검색됩니다).

    Returns:
        str: 신청인의 연락 방법(평문)
    """

    applicant = applicant.replace('산학협력단', '').strip()
    if applicant == '':
        return "검색 결과가 없습니다."
    

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