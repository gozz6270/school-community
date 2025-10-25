"""
마이페이지
Figma 디자인: https://www.figma.com/design/HHDev1QHqPB31yP9lENPD9/%EC%BA%A0%ED%8D%BC%EC%8A%A4%EB%A7%81%ED%81%AC-%ED%99%94%EB%A9%B4-%EC%84%A4%EA%B3%84%EC%84%9C?node-id=4-803&m=dev
"""

import streamlit as st
import re
from utils.supabase_client import get_supabase_client
from utils.auth import require_login, get_current_user, logout, logout_user
from utils.styles import hide_sidebar
from utils.dialogs import show_error, show_success

# 페이지 설정 - centered로 변경 (홈 화면과 동일)
st.set_page_config(
    page_title="캠퍼스링크",
    page_icon="🏫",
    layout="centered"
)

# 사이드바 숨김
hide_sidebar()


def render_header():
    """헤더 렌더링 - 홈 화면과 동일"""
    user = get_current_user()
    nickname = user.get('nickname', '사용자') if user else '사용자'
    
    # 사용자의 관심 학교 개수 확인
    try:
        client = get_supabase_client()
        schools_response = client.table("user_schools").select("id").eq("user_id", user["id"]).execute()
        has_schools = len(schools_response.data) > 0 if schools_response.data else False
    except:
        has_schools = False
    
    # URL 쿼리 파라미터 확인
    query_params = st.query_params
    
    # 버튼 액션 처리
    if "action" in query_params:
        action = query_params["action"]
        
        if action == "logout":
            logout_user()
            st.query_params.clear()
            st.switch_page("pages/1_login.py")
            st.stop()
        elif action == "home":
            st.query_params.clear()
            st.switch_page("pages/3_home.py")
        elif action == "schools":
            st.query_params.clear()
            st.switch_page("pages/4_add_school.py")
        elif action == "mypage":
            st.query_params.clear()
            # 이미 마이페이지에 있으므로 새로고침
            st.rerun()
    
    # 헤더 스타일링 (홈 화면과 동일)
    st.markdown("""
    <style>
    /* 헤더와 툴바 완전히 숨기기 */
    .stAppHeader {
        display: none !important;
    }

    .stToolbar {
        display: none !important;
    }

    /* 툴바 관련 요소들 숨기기 */
    [data-testid="stToolbar"] {
        display: none !important;
    }

    [data-testid="stHeader"] {
        display: none !important;
    }

    [data-testid="stAppToolbar"] {
        display: none !important;
    }

    /* 개발자 도구 숨기기 */
    .stDeployButton {
        display: none !important;
    }

    .stAppDeployButton {
        display: none !important;
    }

    /* 메인 메뉴 숨기기 */
    .stMainMenu {
        display: none !important;
    }

    [data-testid="stMainMenu"] {
        display: none !important;
    }

    /* 최상단 여백 완전 제거 */
    .stApp {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }

    .stApp > div {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }

    .stApp > div:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }

    /* 모든 최상위 컨테이너 여백 제거 */
    .stVerticalBlock:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }

    .stElementContainer:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }

    [data-testid="stVerticalBlock"]:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }

    [data-testid="stElementContainer"]:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }

    /* Streamlit 최상단 gap 제거 */
    .st-emotion-cache-tn0cau {
        gap: 0rem !important;
    }

    /* 또는 전체 앱 컨테이너의 상단 패딩 제거 */
    .main {
        padding-top: 0 !important;
    }
    
    /* Streamlit 기본 패딩 - 상하만 제거, 좌우는 유지 */
    .main .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    
    /* 컬럼 gap 제거하여 input box 정렬 맞추기 */
    [data-testid="column"] {
        padding-left: 0 !important;
        padding-right: 0 !important;
    }
    
    /* 두 번째 컬럼(입력 필드)만 왼쪽 패딩 추가 */
    [data-testid="column"]:nth-child(2) {
        padding-left: 0.75rem !important;
    }
    
    /* 세 번째 컬럼(버튼)만 왼쪽 패딩 추가 */
    [data-testid="column"]:nth-child(3) {
        padding-left: 0.5rem !important;
    }

    /* 추가 패딩 제거 */
    .stApp > div {
        padding-top: 0rem !important;
    }

    /* 메인 컨테이너 패딩 제거 */
    .main .block-container > div {
        padding-top: 0rem !important;
    }

    /* 더 강력한 패딩 제거 - 상하만, 좌우는 유지 */
    .stMainBlockContainer {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    .stVerticalBlock {
        padding-top: 0rem !important;
    }

    .stElementContainer {
        padding-top: 0rem !important;
    }

    /* 모든 컨테이너 패딩 제거 - 상하만 */
    [data-testid="stMainBlockContainer"] {
        padding-top: 0rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    [data-testid="stVerticalBlock"] {
        padding-top: 0rem !important;
    }

    [data-testid="stElementContainer"] {
        padding-top: 0rem !important;
    }

    /* 헤더 전체 너비 */
    .header-full-width {
        width: 100vw;
        position: fixed;
        top: 0;
        left: 0;
        margin-top: 0rem;
        padding: 16px 0;
        background: white;
        border-bottom: 1px solid #e3e3e3;
        display: flex;
        justify-content: space-between;
        align-items: center;
        z-index: 1000;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .header-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 16px;
        width: 100%;
    }

    .left-section {
        display: flex;
        align-items: center;
        gap: 16px;
    }

    .logo-section {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .logo-icon {
        width: 35px;
        height: 35px;
        background-color: #e3e3e3;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
    }

    .logo-text {
        font-size: 19px;
        font-weight: bold;
        color: black;
    }

    .search-section {
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .search-input {
        width: 206px;
        height: 29px;
        border: 1px solid #929292;
        border-radius: 8px;
        padding: 0 12px;
        font-size: 14px;
    }
    
    /* 학교가 없을 때 검색 비활성화 */
    .search-input.disabled {
        background-color: #eeeeee;
        cursor: not-allowed;
        pointer-events: none;
    }
    
    /* 학교가 있을 때 검색 활성화 */
    .search-input.enabled {
        background-color: white;
        cursor: text;
        pointer-events: auto;
    }

    .search-button {
        width: 16px;
        height: 16px;
        background-color: transparent;
        border: none;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        font-size: 14px;
    }

    .right-section {
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .nickname {
        font-size: 12px;
        font-weight: bold;
        color: black;
        margin-right: 8px;
    }

    .header-buttons {
        display: flex;
        gap: 8px;
        align-items: center;
    }

    .header-button {
        width: 66px;
        height: 29px;
        border-radius: 6px;
        background-color: #e3e3e3;
        border: 1px solid #767676;
        font-size: 13px;
        color: #1e1e1e !important;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        text-decoration: none !important;
        font-weight: normal !important;
    }

    .header-button:hover {
        background-color: #d3d3d3;
        color: #1e1e1e !important;
        text-decoration: none !important;
    }

    .header-button:visited {
        color: #1e1e1e !important;
        text-decoration: none !important;
    }

    .header-button:link {
        color: #1e1e1e !important;
        text-decoration: none !important;
    }
    
    /* 스마트폰 화면에서 검색 영역과 닉네임 숨기기 */
    @media (max-width: 768px) {
        .search-section {
            display: none !important;
        }
        
        .nickname {
            display: none !important;
        }
        
        /* 로고와 버튼 간격 조정 */
        .left-section {
            gap: 8px;
        }
        
        .header-buttons {
            gap: 6px;
        }
        
        /* 버튼 크기 조정 */
        .header-button {
            width: 55px;
            height: 24px;
            font-size: 11px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # 헤더 HTML (홈 화면과 동일)
    search_class = "enabled" if has_schools else "disabled"
    search_disabled = "" if has_schools else "disabled"
    
    st.markdown(f"""
    <div class="header-full-width">
        <div class="header-content">
            <div class="left-section">
                <div class="logo-section">
                    <div class="logo-icon"></div>
                    <a href="?action=home" target="_self" class="logo-text" style="text-decoration: none; color: inherit; cursor: pointer;">캠퍼스링크</a>
                </div>
                <div class="search-section">
                    <input type="text" class="search-input {search_class}" placeholder="" {search_disabled}>
                    <div class="search-button" onclick="alert('검색 기능은 아직 준비 중입니다.');" style="cursor: pointer;">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <circle cx="11" cy="11" r="8" stroke="currentColor" stroke-width="2"/>
                            <path d="m21 21-4.35-4.35" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                        </svg>
                    </div>
                </div>
            </div>
            <div class="right-section">
                <div class="nickname">{nickname}님</div>
                <div class="header-buttons">
                    <a href="?action=logout" class="header-button" target="_self">로그아웃</a>
                    <a href="?action=schools" class="header-button" target="_self">관심학교</a>
                    <a href="?action=mypage" class="header-button" target="_self">내 정보</a>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def main() -> None:
    # 탈퇴 성공 시 로그인 페이지로 리다이렉트
    if "delete_success" in st.session_state and st.session_state.delete_success:
        st.session_state.delete_success = False
        st.switch_page("pages/1_login.py")
        st.stop()
    
    require_login()
    
    # 헤더 렌더링
    render_header()
    
    # 회원가입 화면 스타일 적용
    st.markdown("""
    <style>
    /* 본문 컨테이너 상단 여백 (헤더 높이만큼) */
    .content-wrapper {
        margin-top: 70px;
        padding: 20px 0;
    }
    
    /* 전체 컨테이너 */
    .main {
        background-color: white;
    }
    
    /* 메인 블록 컨테이너 상단 패딩 줄이기 */
    .stMainBlockContainer,
    [data-testid="stMainBlockContainer"],
    .block-container {
        padding-top: 3rem !important;
        padding-bottom: 3rem !important;
    }
    
    /* 제목 링크 아이콘 숨김 */
    h1 a {
        display: none !important;
    }
    
    /* 입력 필드 외부 컨테이너 */
    .stTextInput > div {
        position: relative !important;
        background: transparent !important;
        z-index: 1 !important;
    }
    
    /* data-baseweb="input" 컨테이너 - input box와 크기 맞춤 */
    .stTextInput div[data-baseweb="input"] {
        height: 50px !important;
        min-height: 50px !important;
        max-height: 50px !important;
        background: transparent !important;
        padding: 0 !important;
        position: relative !important;
        z-index: 2 !important;
        overflow: visible !important;
        border: none !important;
        box-shadow: none !important;
    }
    
    /* data-baseweb="base-input" 컨테이너 - input box와 크기 맞춤 */
    .stTextInput div[data-baseweb="base-input"] {
        height: 50px !important;
        min-height: 50px !important;
        max-height: 50px !important;
        background: transparent !important;
        padding: 0 !important;
        border: none !important;
        box-shadow: none !important;
        position: relative !important;
        z-index: 3 !important;
        overflow: visible !important;
    }
    
    /* 입력 필드 중간 컨테이너 */
    .stTextInput > div > div {
        background: transparent !important;
        padding: 0 !important;
        gap: 0 !important;
    }
    
    /* 입력 필드 스타일 */
    .stTextInput input {
        border: 1px solid #aaa9a9 !important;
        border-radius: 8px !important;
        height: 50px !important;
        min-height: 50px !important;
        max-height: 50px !important;
        font-size: 16px !important;
        padding: 0 16px !important;
        line-height: 50px !important;
        box-sizing: border-box !important;
        background-color: white !important;
        width: 100% !important;
        vertical-align: middle !important;
        position: relative !important;
        z-index: 10 !important;
    }
    
    /* 입력 필드 모든 상태에서 테두리 유지 */
    .stTextInput input:focus,
    .stTextInput input:active,
    .stTextInput input:focus-visible,
    .stTextInput input:focus-within {
        border: 1px solid #aaa9a9 !important;
        border-color: #aaa9a9 !important;
        outline: none !important;
        outline-width: 0 !important;
        outline-style: none !important;
        box-shadow: none !important;
    }
    
    /* 비밀번호 필드 특수 처리 */
    input[type="password"] {
        padding-right: 16px !important;
    }
    
    input[type="password"]:focus,
    input[type="password"]:active,
    input[type="password"]:focus-visible,
    input[type="password"]:focus-within {
        border: 1px solid #aaa9a9 !important;
        border-color: #aaa9a9 !important;
        outline: none !important;
        outline-width: 0 !important;
        outline-style: none !important;
        box-shadow: none !important;
    }
    
    /* Streamlit 기본 포커스 스타일 완전 제거 */
    .stTextInput div[data-baseweb="input"]:focus-within,
    .stTextInput div[data-baseweb="input"]:focus,
    .stTextInput div[data-baseweb="input"]:active,
    .stTextInput div[data-baseweb="base-input"]:focus-within,
    .stTextInput div[data-baseweb="base-input"]:focus,
    .stTextInput div[data-baseweb="base-input"]:active {
        border: none !important;
        border-color: transparent !important;
        box-shadow: none !important;
        outline: none !important;
    }
    
    /* 모든 Press Enter to apply 메시지 완전히 숨김 */
    .stTextInput [data-testid="InputInstructions"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        height: 0 !important;
        width: 0 !important;
        position: absolute !important;
    }
    
    .stTextInput div[data-testid="stMarkdownContainer"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* 비밀번호 보기 아이콘 완전히 제거 */
    .stTextInput button,
    .stTextInput button[kind="icon"],
    .stTextInput [data-testid="StyledLinkIconContainer"],
    .stTextInput svg {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        height: 0 !important;
        position: absolute !important;
        opacity: 0 !important;
    }
    
    /* 라벨 스타일 (collapsed 상태에서 완전히 숨김) */
    .stTextInput > label {
        display: none !important;
    }
    
    /* 중복 확인 버튼 스타일 - 검정색 (#2c2c2c) - 최우선 적용 */
    .stButton > button[kind="secondary"],
    button[kind="secondary"],
    [data-testid="baseButton-secondary"] {
        background-color: #2c2c2c !important;
        color: white !important;
        border: 1px solid #2c2c2c !important;
        border-radius: 12px !important;
        height: 50px !important;
        font-size: 18px !important;
        font-weight: 600 !important;
    }
    
    .stButton > button[kind="secondary"]:hover,
    button[kind="secondary"]:hover,
    [data-testid="baseButton-secondary"]:hover {
        background-color: #3c3c3c !important;
        border-color: #3c3c3c !important;
    }
    
    /* 비밀번호 변경, 회원 탈퇴하기 버튼 - 회색 (#919191) */
    .stButton > button:not([kind="secondary"]):not([kind="primary"]) {
        background-color: #919191 !important;
        color: white !important;
        border: 1px solid #919191 !important;
        border-radius: 6px !important;
        height: 37px !important;
        font-size: 14px !important;
        font-weight: 400 !important;
        transition: all 0.3s ease;
    }
    
    .stButton > button:not([kind="secondary"]):not([kind="primary"]):hover {
        background-color: #7a7a7a !important;
        border-color: #7a7a7a !important;
    }
    
    .stButton > button:not([kind="secondary"]):not([kind="primary"]):active {
        background-color: #6a6a6a !important;
    }
    
    /* 저장하기 버튼 스타일 (회원가입의 가입하기 버튼과 동일 - 검정색) */
    .stButton > button[kind="primary"] {
        background-color: #2c2c2c !important;
        color: white !important;
        border: 1px solid #2c2c2c !important;
        border-radius: 6px !important;
        height: 37px !important;
        font-size: 14px !important;
        font-weight: 400 !important;
        transition: all 0.3s ease;
    }
    
    .stButton > button[kind="primary"]:hover {
        background-color: #3c3c3c !important;
        border-color: #3c3c3c !important;
    }
    
    .stButton > button[kind="primary"]:active {
        background-color: #1c1c1c !important;
    }
    
    /* 회색 버튼 스타일 (비밀번호 변경, 회원 탈퇴하기) */
    button[data-testid="baseButton-secondary"][aria-label*="gray_btn_1"],
    button[data-testid="baseButton-secondary"][aria-label*="gray_btn_2"],
    .stButton button[key="gray_btn_1"],
    .stButton button[key="gray_btn_2"] {
        background-color: #919191 !important;
        color: white !important;
        border: 1px solid #919191 !important;
        border-radius: 6px !important;
        height: 37px !important;
        font-size: 14px !important;
        font-weight: 400 !important;
    }
    
    button[data-testid="baseButton-secondary"][aria-label*="gray_btn_1"]:hover,
    button[data-testid="baseButton-secondary"][aria-label*="gray_btn_2"]:hover,
    .stButton button[key="gray_btn_1"]:hover,
    .stButton button[key="gray_btn_2"]:hover {
        background-color: #7a7a7a !important;
        border-color: #7a7a7a !important;
    }
    
    /* 에러 메시지 스타일 */
    .error-message {
        color: red !important;
        font-size: 10px !important;
        font-weight: 600 !important;
        margin-top: 2px !important;
        margin-left: 20% !important;
        position: absolute !important;
        z-index: 1000 !important;
        background: white !important;
        padding: 5px !important;
    }
    
    /* 구분선 스타일 */
    .divider {
        border-top: 1px solid #ddd !important;
        margin: 28px 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 본문 컨텐츠
    st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)
    
    # 제목
    st.markdown("""<div style="margin-top: 0px;"></div>""", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="
        text-align: center;
        margin-bottom: 42px;
    ">
        <h1 style="
            font-size: 34px;
            font-weight: 700;
            color: black;
            margin: 0;
            line-height: 1;
        ">내 정보</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # 사용자 정보 가져오기
    user = get_current_user()
    
    if not user:
        st.error("사용자 정보를 불러올 수 없습니다.")
        if st.button("로그인 페이지로"):
            logout_user()
            st.switch_page("pages/1_login.py")
            st.stop()
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # 세션 상태 초기화
    if 'nickname_checked' not in st.session_state:
        st.session_state.nickname_checked = False
    if 'last_checked_nickname' not in st.session_state:
        st.session_state.last_checked_nickname = user.get('nickname', '')
    
    # 닉네임 검증 함수
    def validate_nickname(nickname):
        if not nickname:
            return False, "특수문자 제외, 한글/영문/숫자로 최소 3자~최대 8자리까지 입력 가능합니다."
        if len(nickname) < 3 or len(nickname) > 8:
            return False, "특수문자 제외, 한글/영문/숫자로 최소 3자~최대 8자리까지 입력 가능합니다."
        if not re.match(r'^[가-힣a-zA-Z0-9]+$', nickname):
            return False, "특수문자 제외, 한글/영문/숫자로 최소 3자~최대 8자리까지 입력 가능합니다."
        return True, ""
    
    # 닉네임 중복 확인 함수
    def check_nickname_duplicate(nickname):
        try:
            client = get_supabase_client()
            # 현재 사용자의 닉네임이 아닌 경우만 중복 확인
            result = client.table('users').select('nickname').eq('nickname', nickname).neq('email', user.get('email')).execute()
            return len(result.data) == 0
        except Exception as e:
            st.error(f"중복 확인 중 오류가 발생했습니다: {str(e)}")
            return False
    
    # 이메일 (텍스트로만 표시)
    col_label1, col_text1 = st.columns([1.2, 4.8])
    with col_label1:
        st.markdown("""
        <p style="
            font-size: 17px;
            font-weight: 600;
            color: black;
            line-height: 50px;
            height: 50px;
            margin: 0;
            padding-top: 0;
            display: flex;
            align-items: center;
        ">이메일</p>
        """, unsafe_allow_html=True)
    
    with col_text1:
        st.markdown(f"""
        <p style="
            font-size: 16px;
            font-weight: 400;
            color: black;
            line-height: 50px;
            height: 50px;
            margin: 0;
            padding-top: 0;
            display: flex;
            align-items: center;
        ">{user.get('email', '')}</p>
        """, unsafe_allow_html=True)
    
    st.markdown("""<div style="margin: 46px 0;"></div>""", unsafe_allow_html=True)
    
    # 닉네임 (수정 가능 + 중복 확인 버튼)
    col_label2, col_input2, col_btn2 = st.columns([1.2, 3.6, 1.2], gap="small")
    with col_label2:
        st.markdown("""
        <p style="
            font-size: 17px;
            font-weight: 600;
            color: black;
            line-height: 50px;
            height: 50px;
            margin: 0;
            padding-top: 0;
            display: flex;
            align-items: center;
        ">닉네임</p>
        """, unsafe_allow_html=True)
    
    with col_input2:
        nickname_input = st.text_input(
            "닉네임",
            value=user.get('nickname', ''),
            key="nickname",
            placeholder="",
            label_visibility="collapsed"
        )
    
    with col_btn2:
        nickname_check_btn = st.button("중복 확인", key="nickname_check_btn", type="secondary", use_container_width=True)
    
    # 닉네임 검증 메시지
    nickname_valid, nickname_msg = validate_nickname(nickname_input)
    if nickname_input and not nickname_valid:
        st.markdown(f'<div class="error-message">{nickname_msg}</div>', unsafe_allow_html=True)
    
    # 닉네임 중복 확인 처리
    if nickname_check_btn:
        if nickname_input:
            if validate_nickname(nickname_input)[0]:
                # 기존 닉네임과 동일한 경우
                if nickname_input == user.get('nickname', ''):
                    show_success("현재 사용 중인 닉네임입니다.")
                    st.session_state.nickname_checked = True
                    st.session_state.last_checked_nickname = nickname_input
                elif check_nickname_duplicate(nickname_input):
                    show_success("사용 가능한 닉네임입니다.")
                    st.session_state.nickname_checked = True
                    st.session_state.last_checked_nickname = nickname_input
                else:
                    show_error("이미 사용 중인 닉네임입니다.")
                    st.session_state.nickname_checked = False
            else:
                show_error("닉네임 형식을 확인해주세요.")
                st.session_state.nickname_checked = False
        else:
            show_error("닉네임을 입력해주세요.")
            st.session_state.nickname_checked = False
    
    # 닉네임 값이 변경되면 중복 확인 상태 초기화
    if nickname_input != st.session_state.last_checked_nickname:
        st.session_state.nickname_checked = False
    
    st.markdown("""<div style="margin: 40px 0;"></div>""", unsafe_allow_html=True)
    
    # 휴대폰 번호 (수정 가능)
    col_label3, col_input3 = st.columns([1.2, 4.8])
    with col_label3:
        st.markdown("""
        <p style="
            font-size: 17px;
            font-weight: 600;
            color: black;
            line-height: 50px;
            height: 50px;
            margin: 0;
            padding-top: 0;
            display: flex;
            align-items: center;
        ">휴대폰 번호</p>
        """, unsafe_allow_html=True)
    
    with col_input3:
        phone_input = st.text_input(
            "휴대폰 번호",
            value=user.get('phone', ''),
            key="phone",
            placeholder="",
            label_visibility="collapsed"
        )
    
    st.markdown("""<div style="margin: 49px 0 0 0;"></div>""", unsafe_allow_html=True)
    
    # 비밀번호 변경 / 회원 탈퇴하기 버튼
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        change_password_btn = st.button("비밀번호 변경", use_container_width=True, key="gray_btn_1")
    
    with col_btn2:
        delete_account_btn = st.button("회원 탈퇴하기", use_container_width=True, key="gray_btn_2")
    
    # JavaScript로 회색 버튼 스타일 강제 적용
    st.components.v1.html("""
    <script>
    (function() {
        function applyGrayStyle() {
            const buttons = window.parent.document.querySelectorAll('button');
            buttons.forEach(btn => {
                const text = btn.textContent.trim();
                if (text === '비밀번호 변경' || text === '회원 탈퇴하기') {
                    btn.style.setProperty('background-color', '#919191', 'important');
                    btn.style.setProperty('color', 'white', 'important');
                    btn.style.setProperty('border', '1px solid #919191', 'important');
                    btn.style.setProperty('border-radius', '6px', 'important');
                    btn.style.setProperty('height', '37px', 'important');
                    btn.style.setProperty('font-size', '14px', 'important');
                    btn.style.setProperty('font-weight', '400', 'important');
                    
                    btn.onmouseenter = function() {
                        this.style.setProperty('background-color', '#7a7a7a', 'important');
                        this.style.setProperty('border-color', '#7a7a7a', 'important');
                    };
                    
                    btn.onmouseleave = function() {
                        this.style.setProperty('background-color', '#919191', 'important');
                        this.style.setProperty('border-color', '#919191', 'important');
                    };
                }
            });
        }
        
        setTimeout(applyGrayStyle, 100);
        setTimeout(applyGrayStyle, 500);
        setTimeout(applyGrayStyle, 1000);
    })();
    </script>
    """, height=0)
    
    # 버튼 이벤트 처리
    if change_password_btn:
        show_error("비밀번호 변경 기능은 준비 중입니다.")
    
    if delete_account_btn:
        st.session_state.show_delete_confirm = True
    
    # 회원 탈퇴 확인 다이얼로그
    if "show_delete_confirm" not in st.session_state:
        st.session_state.show_delete_confirm = False
    
    @st.dialog("회원 탈퇴")
    def delete_account_dialog():
        st.write("회원 탈퇴하시겠습니까?")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("확인", use_container_width=True, key="delete_confirm"):
                try:
                    client = get_supabase_client()
                    
                    # 1. user_schools 테이블에서 사용자의 관심 학교 삭제
                    client.table('user_schools').delete().eq('user_id', user['id']).execute()
                    
                    # 2. posts 테이블에서 사용자의 게시글 삭제 (또는 user_id를 null로 변경)
                    client.table('posts').delete().eq('user_id', user['id']).execute()
                    
                    # 3. comments 테이블에서 사용자의 댓글 삭제 (또는 user_id를 null로 변경)
                    client.table('comments').delete().eq('user_id', user['id']).execute()
                    
                    # 4. users 테이블에서 사용자 정보 삭제
                    client.table('users').delete().eq('id', user['id']).execute()
                    
                    # 5. 현재 로그인한 사용자 삭제 (Auth)
                    # admin이 아닌 일반 사용자 삭제 방법 사용
                    try:
                        # Supabase Python 클라이언트에서는 auth.update()로 사용자 삭제 불가능
                        # 대신 로그아웃만 처리하고 Auth 계정은 유지
                        # (실제 삭제는 Supabase Dashboard에서 수동으로 처리하거나 서버 측 API 필요)
                        client.auth.sign_out()
                    except:
                        pass
                    
                    # 6. 세션 정리
                    st.session_state.logged_in = False
                    st.session_state.user = None
                    st.session_state.access_token = None
                    st.session_state.user_data = None
                    st.session_state.show_delete_confirm = False
                    
                    # 7. 성공 메시지 표시 후 로그인 페이지로 이동
                    st.success("회원 탈퇴가 완료되었습니다.")
                    st.session_state.delete_success = True
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"회원 탈퇴 중 오류가 발생했습니다: {str(e)}")
                    
        with col2:
            if st.button("취소", use_container_width=True, key="delete_cancel"):
                st.session_state.show_delete_confirm = False
                st.rerun()
    
    if st.session_state.show_delete_confirm:
        delete_account_dialog()
    
    st.markdown("""<div style="margin: 30px 0;"></div>""", unsafe_allow_html=True)
    
    # 저장하기 버튼 (가입하기 버튼과 동일한 스타일)
    update_btn = st.button("저장하기", use_container_width=True, key="update_btn", type="primary")
    
    if update_btn:
        # 정보 업데이트 로직
        try:
            client = get_supabase_client()
            
            # 닉네임이나 전화번호가 변경되었는지 확인
            nickname_changed = nickname_input != user.get('nickname')
            phone_changed = phone_input != user.get('phone')
            
            if nickname_changed or phone_changed:
                # 닉네임이 변경된 경우 중복 확인 필요
                if nickname_changed and not st.session_state.nickname_checked:
                    show_error("닉네임 중복 확인을 해주세요.")
                    return
                
                # users 테이블 업데이트
                update_data = {
                    "nickname": nickname_input,
                    "phone": phone_input
                }
                
                result = client.table('users').update(update_data).eq('email', user['email']).execute()
                
                if result.data:
                    # 세션 상태 업데이트
                    if 'user_data' in st.session_state:
                        st.session_state.user_data['nickname'] = nickname_input
                        st.session_state.user_data['phone'] = phone_input
                    
                    # 중복 확인 상태 리셋
                    st.session_state.last_checked_nickname = nickname_input
                    st.session_state.nickname_checked = False
                    
                    show_success("정보가 수정되었습니다.")
                else:
                    show_error("정보 수정 중 오류가 발생했습니다.")
            else:
                show_error("변경된 정보가 없습니다.")
        
        except Exception as e:
            show_error(f"정보 수정 중 오류가 발생했습니다: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)  # content-wrapper


if __name__ == "__main__":
    main()
