"""
인증 관련 함수
Supabase Auth 기반 로그인, 로그아웃, 세션 관리
사용자별 세션 분리 및 보안 강화
"""

import streamlit as st
import uuid
import hashlib
from typing import Optional, Dict, Any
from utils.supabase_client import get_supabase_client, cleanup_session_clients


def init_session_state():
    """
    Streamlit session_state 초기화 및 Supabase 세션 복원
    
    각 사용자 세션마다 고유한 세션 ID를 생성하고, Supabase의 저장된 세션을 확인하여 자동 로그인합니다.
    (페이지 새로고침해도 로그인 유지!)
    
    Example:
        >>> init_session_state()
        >>> print(st.session_state.logged_in)  # True or False
    """
    # 고유한 세션 ID 생성 (브라우저별 세션 분리)
    if "session_id" not in st.session_state:
        # 브라우저 정보와 타임스탬프를 조합하여 고유 ID 생성
        browser_info = st.session_state.get("_browser_info", str(uuid.uuid4()))
        session_id = hashlib.md5(f"{browser_info}_{uuid.uuid4()}".encode()).hexdigest()[:16]
        st.session_state.session_id = session_id
    
    # 세션 시작 시간 기록 (타임아웃 체크용)
    if "session_start_time" not in st.session_state:
        import time
        st.session_state.session_start_time = time.time()
    
    # 기본 세션 상태 초기화
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    if "user" not in st.session_state:
        st.session_state.user = None
    
    if "access_token" not in st.session_state:
        st.session_state.access_token = None
    
    if "user_data" not in st.session_state:
        st.session_state.user_data = None
    
    # Supabase 세션 복원 시도 (새로고침 시 자동 로그인)
    try:
        supabase = get_supabase_client()
        session = supabase.auth.get_session()
        
        if session and session.user:
            # users 테이블에서 정보 조회 - 탈퇴한 사용자 체크
            user_email = session.user.email
            user_response = supabase.table("users").select("*").eq("email", user_email).execute()
            
            # users 테이블에 사용자가 없으면 (탈퇴한 경우) 로그아웃 처리
            if not user_response.data or len(user_response.data) == 0:
                supabase.auth.sign_out()
                st.session_state.logged_in = False
                st.session_state.user = None
                st.session_state.access_token = None
                st.session_state.user_data = None
            else:
                # Auth 세션 복원
                st.session_state.logged_in = True
                st.session_state.user = session.user
                st.session_state.access_token = session.access_token
                st.session_state.user_data = user_response.data[0]
    except Exception:
        # 세션 복원 실패 시 로그아웃 상태 유지
        pass


def is_logged_in() -> bool:
    """
    현재 로그인 상태 확인
    
    Returns:
        bool: 로그인 여부 (True: 로그인됨, False: 비로그인)
        
    Example:
        >>> if is_logged_in():
        ...     st.write("환영합니다!")
        ... else:
        ...     st.write("로그인이 필요합니다.")
    """
    init_session_state()
    
    # session_state 확인
    if not st.session_state.get("logged_in", False):
        return False
    
    # Supabase 세션 유효성 재확인
    try:
        supabase = get_supabase_client()
        session = supabase.auth.get_session()
        return session and session.user is not None
    except Exception:
        return False


def login_user(email: str, password: str) -> tuple[bool, str]:
    """
    Supabase Auth 인증 + users 테이블 정보 조회
    
    Args:
        email: 이메일 (로그인 ID로 사용)
        password: 비밀번호
    
    Returns:
        tuple: (성공 여부, 메시지)
            - (True, "로그인 성공"): 로그인 성공
            - (False, "에러 메시지"): 로그인 실패
    
    Example:
        >>> success, msg = login_user("user@example.com", "password123")
        >>> if success:
        ...     st.success(msg)
        ... else:
        ...     st.error(msg)
    """
    try:
        supabase = get_supabase_client()
        
        # 1단계: Supabase Auth 로그인
        auth_response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        if not auth_response.user:
            return False, "로그인 실패"
        
        # 2단계: users 테이블에서 추가 정보 조회 (이메일로 조회)
        user_response = supabase.table("users").select("*").eq("email", email).execute()
        
        if not user_response.data or len(user_response.data) == 0:
            return False, "사용자 정보를 찾을 수 없습니다."
        
        user_data = user_response.data[0]
        
        # 3단계: session_state 업데이트 (Auth 정보 + DB 정보)
        st.session_state.logged_in = True
        st.session_state.user = auth_response.user
        st.session_state.access_token = auth_response.session.access_token
        st.session_state.user_data = user_data  # DB의 추가 정보 저장
        
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
    Supabase Auth 로그아웃 및 세션 정리
    
    Supabase 세션을 종료하고 session_state를 초기화하며, 세션별 클라이언트도 정리합니다.
    
    Example:
        >>> logout_user()
        >>> print(is_logged_in())  # False
    """
    try:
        supabase = get_supabase_client()
        supabase.auth.sign_out()
    except Exception:
        pass
    
    # session_state 초기화
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.access_token = None
    st.session_state.user_data = None
    
    # 세션별 Supabase 클라이언트 정리
    cleanup_session_clients()


def get_current_user() -> Optional[Dict[str, Any]]:
    """
    현재 로그인한 사용자 정보 반환 (Auth + users 테이블 정보)
    
    Returns:
        dict or None: 로그인된 경우 사용자 정보, 비로그인 시 None
            - id: DB users 테이블 ID
            - auth_user_id: Supabase Auth User ID (UUID)
            - user_id: 아이디
            - nickname: 닉네임
            - phone: 휴대폰
            - auth_email: 로그인용 이메일 (변경 불가)
            - contact_email: 연락용 이메일 (변경 가능)
            
    Example:
        >>> user = get_current_user()
        >>> if user:
        ...     st.write(f"환영합니다, {user['nickname']}님!")
        ...     st.write(f"연락처: {user['contact_email']}")
        ... else:
        ...     st.write("로그인이 필요합니다.")
    """
    if not is_logged_in():
        return None
    
    user_data = st.session_state.get("user_data")
    if not user_data:
        return None
    
    return user_data


def require_login():
    """
    로그인이 필요한 페이지에서 사용
    
    비로그인 상태인 경우 로그인 페이지로 리다이렉트합니다.
    페이지 상단에서 호출하여 로그인을 강제합니다.
    
    Example:
        >>> # 페이지 최상단에 추가
        >>> require_login()
        >>> st.write("로그인한 사용자만 볼 수 있는 내용")
    """
    if not is_logged_in():
        st.warning("⚠️ 로그인이 필요한 페이지입니다.")
        st.info("로그인 페이지로 이동합니다...")
        st.switch_page("pages/1_login.py")


def validate_session():
    """
    현재 세션의 유효성을 검증
    
    세션 하이재킹이나 세션 공유를 방지하기 위해 세션을 주기적으로 검증합니다.
    
    Returns:
        bool: 세션이 유효한 경우 True, 그렇지 않으면 False
    """
    if not is_logged_in():
        return False
    
    try:
        supabase = get_supabase_client()
        session = supabase.auth.get_session()
        
        # 세션이 존재하고 유효한지 확인
        if not session or not session.user:
            logout_user()
            return False
        
        # 사용자 정보가 일치하는지 확인
        current_user = get_current_user()
        if not current_user or current_user.get('email') != session.user.email:
            logout_user()
            return False
        
        return True
    except Exception:
        logout_user()
        return False


def check_session_timeout(timeout_hours: float = 24.0) -> bool:
    """
    세션 타임아웃 체크
    
    Args:
        timeout_hours: 타임아웃 시간 (시간 단위, 기본값: 24시간)
    
    Returns:
        bool: 세션이 유효한 경우 True, 타임아웃된 경우 False
    """
    if "session_start_time" not in st.session_state:
        return False
    
    import time
    current_time = time.time()
    session_duration = current_time - st.session_state.session_start_time
    timeout_seconds = timeout_hours * 3600
    
    if session_duration > timeout_seconds:
        logout_user()
        return False
    
    return True


def refresh_session():
    """
    세션 갱신 (활동 시간 업데이트)
    
    사용자가 활동할 때마다 호출하여 세션을 갱신합니다.
    """
    import time
    st.session_state.session_start_time = time.time()

