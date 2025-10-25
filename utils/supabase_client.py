"""
Supabase 클라이언트 초기화 및 관리
각 사용자별 독립적인 클라이언트로 세션 분리
"""

import os
import streamlit as st
from typing import Optional
from supabase import create_client, Client
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()


def get_supabase_client() -> Client:
    """
    Supabase 클라이언트 인스턴스 반환 (사용자별 독립)
    
    각 사용자의 st.session_state에 클라이언트를 저장하여 세션 분리
    
    Returns:
        Client: Supabase 클라이언트 객체
        
    Raises:
        ValueError: SUPABASE_URL 또는 SUPABASE_KEY가 설정되지 않은 경우
        Exception: Supabase 클라이언트 생성 실패 시
    
    Example:
        >>> client = get_supabase_client()
        >>> response = client.table('users').select("*").execute()
    """
    # st.session_state에 클라이언트가 없으면 생성
    if 'supabase_client' not in st.session_state:
        # Streamlit Cloud의 secrets 또는 환경 변수에서 가져오기
        try:
            url = st.secrets["SUPABASE_URL"]
            key = st.secrets["SUPABASE_KEY"]
        except (KeyError, FileNotFoundError):
            # secrets가 없으면 환경 변수에서 가져오기
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_KEY")
        
        # 환경변수 검증
        if not url or not key:
            raise ValueError(
                "Supabase URL 또는 KEY가 설정되지 않았습니다.\n"
                "로컬: .env 파일을 확인하세요\n"
                "Streamlit Cloud: Secrets에서 SUPABASE_URL과 SUPABASE_KEY를 설정하세요"
            )
        
        try:
            # persistSession을 True로 설정하여 localStorage 사용
            # 각 브라우저가 독립적인 클라이언트를 가지므로 세션 분리는 유지됨
            from supabase.lib.client_options import ClientOptions
            
            options = ClientOptions(
                auto_refresh_token=True,
                persist_session=True  # localStorage 사용하여 페이지 이동 시에도 세션 유지
            )
            
            st.session_state.supabase_client = create_client(url, key, options)
        except Exception as e:
            raise Exception(f"Supabase 클라이언트 생성 실패: {str(e)}")
    
    return st.session_state.supabase_client


def reset_supabase_client():
    """
    Supabase 클라이언트 인스턴스 초기화
    
    현재 사용자의 클라이언트를 초기화합니다.
    """
    if 'supabase_client' in st.session_state:
        del st.session_state.supabase_client


def cleanup_session_clients():
    """
    현재 세션의 Supabase 클라이언트 정리
    
    로그아웃 시 호출하여 메모리 정리를 수행합니다.
    """
    if 'supabase_client' in st.session_state:
        del st.session_state.supabase_client

