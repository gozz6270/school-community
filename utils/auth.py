"""
인증 관련 함수
Supabase Auth 기반 로그인, 로그아웃, 세션 관리
Supabase 세션만으로 로그인 상태 관리
"""

import streamlit as st
from typing import Optional, Dict, Any
from utils.supabase_client import get_supabase_client


def is_logged_in() -> bool:
    """
    현재 로그인 상태 확인 (캐싱 + Supabase 세션 기반)
    
    Returns:
        bool: 로그인 여부 (True: 로그인됨, False: 비로그인)
    """
    # 먼저 캐시된 상태 확인
    cached_logged_in = st.session_state.get("cached_logged_in")
    if cached_logged_in is not None:
        print(f"DEBUG: 캐시된 로그인 상태 - {cached_logged_in}")
        return cached_logged_in
    
    try:
        supabase = get_supabase_client()
        session = supabase.auth.get_session()
        
        # 디버깅을 위한 로그
        print(f"DEBUG: 세션 확인 - session: {session}")
        if session:
            print(f"DEBUG: 세션 사용자 - user: {session.user}")
            if session.user:
                print(f"DEBUG: 사용자 이메일 - email: {session.user.email}")
        
        is_logged = session and session.user is not None
        print(f"DEBUG: 로그인 상태 - is_logged: {is_logged}")
        
        # 결과를 캐시에 저장
        st.session_state.cached_logged_in = is_logged
        
        return is_logged
    except Exception as e:
        print(f"DEBUG: 세션 확인 오류 - {str(e)}")
        # 오류 시 캐시된 상태가 있으면 사용
        return st.session_state.get("cached_logged_in", False)


def get_current_user() -> Optional[Dict[str, Any]]:
    """
    현재 로그인한 사용자 정보 반환 (Supabase 세션 기반)
    
    Returns:
        dict or None: 로그인된 경우 사용자 정보, 비로그인 시 None
    """
    try:
        supabase = get_supabase_client()
        session = supabase.auth.get_session()
        
        if not session or not session.user:
            return None
        
        # users 테이블에서 정보 조회
        user_email = session.user.email
        user_response = supabase.table("users").select("*").eq("email", user_email).execute()
        
        if user_response.data and len(user_response.data) > 0:
            return user_response.data[0]
        
        return None
    except Exception:
        return None


def login_user(email: str, password: str) -> tuple[bool, str]:
    """
    Supabase Auth 인증
    
    Args:
        email: 이메일 (로그인 ID로 사용)
        password: 비밀번호
    
    Returns:
        tuple: (성공 여부, 메시지)
            - (True, "로그인 성공"): 로그인 성공
            - (False, "에러 메시지"): 로그인 실패
    """
    try:
        supabase = get_supabase_client()
        
        # Supabase Auth 로그인
        auth_response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        if not auth_response.user:
            return False, "로그인 실패"
        
        # users 테이블에서 추가 정보 조회
        user_response = supabase.table("users").select("*").eq("email", email).execute()
        
        if not user_response.data or len(user_response.data) == 0:
            return False, "사용자 정보를 찾을 수 없습니다."
        
        # 로그인 성공 시 캐시 업데이트
        st.session_state.cached_logged_in = True
        print("DEBUG: 로그인 성공 - 캐시 업데이트됨")
        
        return True, "로그인 성공"
    
    except Exception as e:
        error_msg = str(e).lower()
        
        # 에러 메시지 분석
        if "invalid" in error_msg or "credentials" in error_msg:
            return False, "이메일 또는 비밀번호가 올바르지 않습니다."
        elif "email not confirmed" in error_msg:
            return False, "이메일 인증이 필요합니다."
        elif "network" in error_msg or "connection" in error_msg:
            return False, "네트워크 오류입니다. 다시 시도해주세요."
        else:
            return False, f"로그인 오류: {str(e)}"


# signup_user 함수는 회원가입 페이지에서 직접 처리하므로 제거


def logout_user():
    """
    Supabase Auth 로그아웃
    
    Supabase 세션을 종료하고 캐시를 초기화합니다.
    """
    try:
        supabase = get_supabase_client()
        supabase.auth.sign_out()
    except Exception:
        pass
    
    # 캐시 초기화
    st.session_state.cached_logged_in = False
    print("DEBUG: 로그아웃 - 캐시 초기화됨")


def require_login():
    """
    로그인이 필요한 페이지에서 사용 (Supabase 세션 기반)
    
    비로그인 상태인 경우 로그인 페이지로 리다이렉트합니다.
    """
    if not is_logged_in():
        st.warning("⚠️ 로그인이 필요한 페이지입니다.")
        st.info("로그인 페이지로 이동합니다...")
        st.switch_page("pages/1_login.py")

