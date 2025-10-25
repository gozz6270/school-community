"""
로그인 페이지
캠퍼스링크 - 대학교 커뮤니티 서비스
"""

import streamlit as st
import time
from utils.auth import is_logged_in, login_user
from utils.dialogs import show_error, show_success
from utils.supabase_client import get_supabase_client
from utils.styles import hide_sidebar

# ============================================
# 페이지 설정
# ============================================
st.set_page_config(
    page_title="로그인 - 캠퍼스링크",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 이미 로그인한 경우 홈으로 리다이렉트
if is_logged_in():
    st.switch_page("pages/3_home.py")

# ============================================
# CSS 스타일 (Figma 디자인 기준) - 사이드바 숨김 포함
# ============================================
st.markdown("""
<style>
    /* 사이드바 완전히 숨기기 - 최우선 적용 (애니메이션 제거) */
    [data-testid="stSidebar"],
    section[data-testid="stSidebar"],
    .css-1d391kg,
    [data-testid="collapsedControl"] {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        min-width: 0 !important;
        max-width: 0 !important;
        transition: none !important;
        animation: none !important;
    }
    
    /* 햨버거 메뉴 버튼 숨기기 */
    button[kind="header"],
    [data-testid="collapsedControl"] {
        display: none !important;
        transition: none !important;
    }
    
    /* 전체 컨테이너 */
    .main {
        background-color: white;
    }
    
    /* 메인 블록 컨테이너 상단/하단 패딩 */
    .stMainBlockContainer,
    [data-testid="stMainBlockContainer"],
    .block-container {
        padding-top: 6rem !important;
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
    
    /* 버튼 스타일 - 어두운 회색 (#2c2c2c) */
    .stButton > button {
        background-color: #2c2c2c !important;
        color: white !important;
        border: 1px solid #2c2c2c !important;
        border-radius: 6px !important;
        height: 37px !important;
        font-size: 14px !important;
        font-weight: 400 !important;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #3c3c3c !important;
        border-color: #3c3c3c !important;
    }
    
    .stButton > button:active {
        background-color: #1c1c1c !important;
    }
    
    /* 다이얼로그(팝업) 완전 중앙 정렬 */
    section[data-testid="stModal"] {
        position: fixed !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
        width: auto !important;
        max-width: 90% !important;
    }
    
    /* 다이얼로그 오버레이 배경 */
    [data-testid="stModal"] {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    /* 다이얼로그 내부 컨테이너 */
    section[data-testid="stModal"] > div {
        position: static !important;
        top: auto !important;
        left: auto !important;
        transform: none !important;
    }
    
    /* 다이얼로그 본문 */
    [role="dialog"] {
        position: relative !important;
        top: auto !important;
        left: auto !important;
        margin: 0 auto !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# 로고 및 타이틀 섹션 (한 줄로 표시)
# ============================================
st.markdown("""<div style="margin-top: 28px;"></div>""", unsafe_allow_html=True)

# 로고와 타이틀을 한 줄로 중앙 정렬
st.markdown("""
<div style="
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 14px;
    margin-bottom: 80px;
">
    <div style="
        width: 49px;
        height: 49px;
        background-color: #D3D3D3;
        border-radius: 50%;
        flex-shrink: 0;
    "></div>
    <h1 style="
        font-size: 45px;
        font-weight: 700;
        margin: 0;
        line-height: 1;
    ">캠퍼스링크</h1>
</div>
""", unsafe_allow_html=True)

# ============================================
# 로그인 폼 (라벨 왼쪽 + Input 오른쪽 가로 배치)
# ============================================

# 아이디 입력 (가로 배치)
col_label1, col_input1 = st.columns([1, 7])
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

with col_input1:
    user_id_input = st.text_input(
        "이메일",
        key="login_user_id",
        placeholder="example@email.com",
        label_visibility="collapsed"
    )

st.markdown("""<div style="margin: 20px 0;"></div>""", unsafe_allow_html=True)

# 비밀번호 입력 (가로 배치)
col_label2, col_input2 = st.columns([1, 7])
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
    ">비밀번호</p>
    """, unsafe_allow_html=True)

with col_input2:
    password_input = st.text_input(
        "비밀번호",
        type="password",
        key="login_password",
        placeholder="",
        label_visibility="collapsed"
    )

st.markdown("""<div style="margin: 40px 0 0 0;"></div>""", unsafe_allow_html=True)

# ============================================
# 버튼 영역 (회원가입 | 로그인)
# ============================================
col1, col2 = st.columns(2)

with col1:
    signup_button = st.button("회원가입", use_container_width=True, key="btn_signup")

with col2:
    login_button = st.button("로그인", use_container_width=True, key="btn_login")

# ============================================
# 하단 링크 영역
# ============================================
# 구분선 (버튼과 동일한 간격)
st.markdown("""
<div style="margin-top: 10px;">
    <hr style="
        border: none;
        border-top: 1px solid #aaa9a9;
        margin: 0 0 16px 0;
    ">
</div>
""", unsafe_allow_html=True)

# 하단 링크
st.markdown("""
<p style="
    text-align: center;
    color: #727171;
    font-size: 16px;
    font-weight: 400;
    margin: 0;
">
    아이디 찾기<span style="margin: 0 10px;">|</span>비밀번호 찾기
</p>
""", unsafe_allow_html=True)

# ============================================
# 버튼 이벤트 처리
# ============================================

# 회원가입 버튼 클릭
if signup_button:
                st.switch_page("pages/2_signup.py")
        
# 로그인 버튼 클릭
if login_button:
    # 1. 입력값 검증
    if not user_id_input or not password_input:
        show_error("이메일과 비밀번호를 입력하세요.")
    else:
        try:
            # 2. Supabase Auth 로그인 시도 (이메일 직접 사용)
            success, message = login_user(user_id_input, password_input)
            
            if success:
                # 로그인 성공 - 바로 홈 화면으로 이동
                st.switch_page("pages/3_home.py")
            else:
                # 로그인 실패
                show_error("이메일 또는 비밀번호가 올바르지 않습니다.")
        except Exception as e:
            show_error(f"로그인 오류: {str(e)}")
