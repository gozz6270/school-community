"""
재사용 가능한 Streamlit 다이얼로그/팝업 함수들
Streamlit 1.30+ @st.dialog 데코레이터 사용
"""

import streamlit as st


@st.dialog("✅ 성공")
def show_success(message: str, redirect_page: str = None):
    """
    성공 메시지 팝업 (초록색)
    
    Args:
        message: 표시할 성공 메시지
        redirect_page: 확인 버튼 클릭 시 이동할 페이지 (선택사항)
        
    Example:
        >>> show_success("회원가입이 완료되었습니다!", "pages/1_login.py")
    """
    st.success(message)
    if st.button("확인", use_container_width=True):
        if redirect_page:
            st.switch_page(redirect_page)
        else:
            st.rerun()


@st.dialog("❌ 오류")
def show_error(message: str):
    """
    에러 메시지 팝업 (빨간색)
    
    Args:
        message: 표시할 에러 메시지
        
    Example:
        >>> show_error("이메일 형식이 올바르지 않습니다.")
    """
    st.error(message)
    if st.button("확인", use_container_width=True):
        st.rerun()


@st.dialog("ℹ️ 안내")
def show_info(message: str):
    """
    정보 메시지 팝업 (파란색)
    
    Args:
        message: 표시할 정보 메시지
        
    Example:
        >>> show_info("현재 베타 버전입니다.")
    """
    st.info(message)
    if st.button("확인", use_container_width=True):
        st.rerun()


@st.dialog("⚠️ 경고")
def show_warning(message: str):
    """
    경고 메시지 팝업 (노란색)
    
    Args:
        message: 표시할 경고 메시지
        
    Example:
        >>> show_warning("비밀번호가 곧 만료됩니다.")
    """
    st.warning(message)
    if st.button("확인", use_container_width=True):
        st.rerun()


def confirm_dialog(message: str, title: str = "확인") -> bool:
    """
    확인/취소 선택 팝업
    
    Args:
        message: 표시할 메시지
        title: 다이얼로그 제목 (기본값: "확인")
    
    Returns:
        bool: 확인 클릭 시 True, 취소 클릭 시 False
        
    Example:
        >>> if confirm_dialog("정말 삭제하시겠습니까?", "삭제 확인"):
        ...     delete_item()
        ...     show_success("삭제되었습니다!")
    
    Note:
        이 함수는 @st.dialog 데코레이터를 직접 사용하지 않고,
        session_state를 통해 동작합니다.
    """
    # 다이얼로그 상태 초기화
    if "confirm_dialog_open" not in st.session_state:
        st.session_state.confirm_dialog_open = False
    if "confirm_dialog_result" not in st.session_state:
        st.session_state.confirm_dialog_result = None
    
    # 다이얼로그 열기
    st.session_state.confirm_dialog_open = True
    st.session_state.confirm_dialog_message = message
    st.session_state.confirm_dialog_title = title
    
    return st.session_state.confirm_dialog_result


@st.dialog("확인")
def _confirm_dialog_content():
    """
    confirm_dialog의 실제 내용을 렌더링하는 내부 함수
    """
    message = st.session_state.get("confirm_dialog_message", "")
    
    st.write(message)
    st.write("")  # 공백
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("확인", use_container_width=True):
            st.session_state.confirm_dialog_result = True
            st.session_state.confirm_dialog_open = False
            st.rerun()
    
    with col2:
        if st.button("취소", use_container_width=True):
            st.session_state.confirm_dialog_result = False
            st.session_state.confirm_dialog_open = False
            st.rerun()


@st.dialog("🗑️ 삭제 확인")
def delete_confirm_dialog(item_name: str):
    """
    삭제 확인 다이얼로그
    
    Args:
        item_name: 삭제할 항목 이름
        
    Example:
        >>> delete_confirm_dialog("게시글")
    """
    st.warning(f"**'{item_name}'**을(를) 정말 삭제하시겠습니까?")
    st.caption("⚠️ 이 작업은 되돌릴 수 없습니다.")
    st.write("")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("삭제", use_container_width=True):
            st.session_state.delete_confirmed = True
            st.rerun()
    
    with col2:
        if st.button("취소", use_container_width=True):
            st.session_state.delete_confirmed = False
            st.rerun()


@st.dialog("알림")
def alert_dialog(message: str, title: str = "알림"):
    """
    확인 버튼만 있는 알림 팝업
    
    Args:
        message: 표시할 메시지
        title: 다이얼로그 제목 (기본값: "알림")
        
    Example:
        >>> # 회원가입 완료 알림
        >>> alert_dialog("회원가입이 완료되었습니다!", "가입 완료")
        >>> 
        >>> # 에러 알림
        >>> alert_dialog("최대 5개의 학교만 추가할 수 있습니다.", "추가 불가")
    
    Note:
        다이얼로그 상단의 제목은 "알림"으로 고정되며,
        커스텀 title은 메시지 위에 표시됩니다.
    """
    # title이 기본값이 아니면 큰 제목으로 표시
    if title != "알림":
        st.markdown(f"### {title}")
        st.write("")  # 공백
    
    st.write(message)
    st.write("")  # 공백
    
    if st.button("확인", use_container_width=True):
        st.rerun()

