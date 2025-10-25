"""
인증 관련 함수
Streamlit session_state 기반 로그인 관리
브라우저별 독립적인 세션 보장
"""

import streamlit as st
from typing import Optional, Dict, Any
from utils.supabase_client import get_supabase_client


def init_auth():
    """
    세션 상태 초기화 및 Supabase 세션 복원
    """
    # 기본값 설정 (이미 있으면 건드리지 않음)
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'access_token' not in st.session_state:
        st.session_state.access_token = None
    if 'refresh_token' not in st.session_state:
        st.session_state.refresh_token = None
    if 'user_data' not in st.session_state:
        st.session_state.user_data = None
    
    # 로그인되어 있고 access_token이 있으면 Supabase 세션 복원
    if st.session_state.logged_in and st.session_state.access_token:
        try:
            supabase = get_supabase_client()
            # 저장된 세션을 Supabase 클라이언트에 수동으로 설정
            supabase.auth.set_session(
                st.session_state.access_token,
                st.session_state.refresh_token
            )
        except Exception as e:
            # 세션 복원 실패 시 로그아웃 처리
            import sys
            print(f"세션 복원 실패: {str(e)}", file=sys.stderr)
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.access_token = None
            st.session_state.refresh_token = None
            st.session_state.user_data = None


def login(email: str, password: str) -> bool:
    """
    로그인 처리
    
    Args:
        email: 이메일 (로그인 ID로 사용)
        password: 비밀번호
    
    Returns:
        bool: 로그인 성공 여부
    """
    try:
        supabase = get_supabase_client()
        
        # Supabase Auth 로그인
        auth_response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        if not auth_response.user:
            return False
        
        # users 테이블에서 추가 정보 조회
        user_response = supabase.table("users").select("*").eq("email", email).execute()
        
        if not user_response.data or len(user_response.data) == 0:
            return False
        
        user_data = user_response.data[0]
        
        # session_state에 로그인 정보 저장 (이 브라우저 세션에만 저장됨)
        st.session_state.logged_in = True
        st.session_state.user = auth_response.user
        st.session_state.access_token = auth_response.session.access_token
        st.session_state.refresh_token = auth_response.session.refresh_token
        st.session_state.user_data = user_data
        
        return True
    
    except Exception as e:
        import sys
        print(f"로그인 실패: {str(e)}", file=sys.stderr)
        return False


def logout():
    """
    로그아웃 처리
    """
    try:
        supabase = get_supabase_client()
        supabase.auth.sign_out()
    except Exception:
        pass
    
    # session_state 초기화 (이 브라우저 세션에만 적용)
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.access_token = None
    st.session_state.refresh_token = None
    st.session_state.user_data = None
    
    # Supabase 클라이언트도 삭제 (다음 로그인 시 새로 생성됨)
    if 'supabase_client' in st.session_state:
        del st.session_state.supabase_client


def require_login():
    """
    로그인이 필요한 페이지에서 사용
    """
    # 세션 상태 초기화 먼저
    init_auth()
    
    if not st.session_state.logged_in:
        st.warning("⚠️ 로그인이 필요한 페이지입니다.")
        st.info("로그인 페이지로 이동합니다...")
        st.switch_page("pages/1_login.py")
        st.stop()


def get_current_user() -> Optional[Dict[str, Any]]:
    """
    현재 로그인한 사용자 정보 반환
    """
    # 세션 상태 초기화 먼저
    init_auth()
    
    if not st.session_state.logged_in:
        return None
    
    return st.session_state.get('user_data')


# 기존 함수들과의 호환성을 위한 별칭
def is_logged_in() -> bool:
    """기존 코드와의 호환성을 위한 함수"""
    # 세션 상태 초기화 먼저
    init_auth()
    
    return st.session_state.get('logged_in', False)


def login_user(email: str, password: str) -> tuple[bool, str]:
    """기존 코드와의 호환성을 위한 함수"""
    success = login(email, password)
    if success:
        return True, "로그인 성공"
    else:
        return False, "이메일 또는 비밀번호가 올바르지 않습니다."


def logout_user():
    """기존 코드와의 호환성을 위한 함수"""
    logout()

