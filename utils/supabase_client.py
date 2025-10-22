"""
Supabase 클라이언트 초기화 및 관리
싱글톤 패턴으로 구현
"""

import os
from typing import Optional
from supabase import create_client, Client
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 싱글톤 인스턴스
_supabase_client: Optional[Client] = None


def get_supabase_client() -> Client:
    """
    Supabase 클라이언트 인스턴스 반환 (싱글톤 패턴)
    
    첫 호출 시에만 클라이언트를 생성하고, 이후에는 동일한 인스턴스를 반환합니다.
    
    Returns:
        Client: Supabase 클라이언트 객체
        
    Raises:
        ValueError: SUPABASE_URL 또는 SUPABASE_KEY가 설정되지 않은 경우
        Exception: Supabase 클라이언트 생성 실패 시
    
    Example:
        >>> client = get_supabase_client()
        >>> response = client.table('users').select("*").execute()
    """
    global _supabase_client
    
    if _supabase_client is None:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        
        # 환경변수 검증
        if not url or not key:
            raise ValueError(
                "Supabase URL 또는 KEY가 설정되지 않았습니다.\n"
                ".env 파일을 확인하세요:\n"
                "  SUPABASE_URL=your_supabase_url\n"
                "  SUPABASE_KEY=your_supabase_key"
            )
        
        try:
            _supabase_client = create_client(url, key)
        except Exception as e:
            raise Exception(f"Supabase 클라이언트 생성 실패: {str(e)}")
    
    return _supabase_client


def reset_supabase_client():
    """
    Supabase 클라이언트 인스턴스 초기화
    
    테스트나 재연결이 필요한 경우 사용합니다.
    """
    global _supabase_client
    _supabase_client = None

