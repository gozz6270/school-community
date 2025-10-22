"""
회원가입 페이지
캠퍼스링크 - 대학교 커뮤니티 서비스
"""

import streamlit as st
import re
import time
from utils.supabase_client import get_supabase_client
from utils.dialogs import show_error, show_success
from utils.styles import hide_sidebar

# ============================================
# 페이지 설정
# ============================================
st.set_page_config(
    page_title="회원가입 - 캠퍼스링크",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================
# CSS 스타일 (로그인 페이지와 동일한 구조) - 사이드바 숨김 포함
# ============================================
st.markdown("""
<style>
    /* 사이드바 완전히 숨기기 - 최우선 적용 */
    [data-testid="stSidebar"],
    section[data-testid="stSidebar"],
    .css-1d391kg,
    [data-testid="collapsedControl"] {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        min-width: 0 !important;
        max-width: 0 !important;
    }
    
    /* 햄버거 메뉴 버튼 숨기기 */
    button[kind="header"],
    [data-testid="collapsedControl"] {
        display: none !important;
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
    
    /* 중복 확인 버튼 스타일 - 검정색 (#2c2c2c) */
    .stButton > button[kind="secondary"] {
        background-color: #2c2c2c !important;
        color: white !important;
        border: 1px solid #2c2c2c !important;
        border-radius: 12px !important;
        height: 50px !important;
        font-size: 18px !important;
        font-weight: 600 !important;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background-color: #3c3c3c !important;
        border-color: #3c3c3c !important;
    }
    
    /* 가입하기 버튼 스타일 - 기본 회색 */
    .stButton > button[kind="primary"] {
        background-color: #919191 !important;
        color: white !important;
        border: 1px solid #919191 !important;
        border-radius: 6px !important;
        height: 37px !important;
        font-size: 14px !important;
        font-weight: 400 !important;
        transition: all 0.3s ease;
        opacity: 0.6 !important;
        cursor: default !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background-color: #919191 !important;
        border-color: #919191 !important;
        opacity: 0.6 !important;
        cursor: default !important;
    }
    
    /* 가입하기 버튼 활성화 상태 (모든 항목 정상 입력 시) */
    .stButton > button[kind="primary"].active {
        background-color: #2c2c2c !important;
        border-color: #2c2c2c !important;
        opacity: 1 !important;
        cursor: default !important;
    }
    
    .stButton > button[kind="primary"].active:hover {
        background-color: #3c3c3c !important;
        border-color: #3c3c3c !important;
        opacity: 1 !important;
        cursor: default !important;
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
    
    /* 팝업(모달) 확인 버튼 스타일 - 검정색 (성공 팝업 포함) */
    .stModal .stButton > button,
    [data-testid="stModal"] .stButton > button,
    section[data-testid="stModal"] .stButton > button,
    [role="dialog"] .stButton > button,
    div[data-testid="stModal"] button,
    section[data-testid="stModal"] button,
    [role="dialog"] button,
    /* 성공 팝업 특별 처리 */
    .stSuccess .stButton > button,
    [data-testid="stSuccess"] .stButton > button,
    .stAlert .stButton > button,
    [data-testid="stAlert"] .stButton > button,
    /* 모든 모달 내 버튼 */
    .stModal button,
    [data-testid="stModal"] button,
    section[data-testid="stModal"] button,
    [role="dialog"] button,
    /* 성공/에러 팝업 버튼 강제 적용 */
    .stSuccess button,
    .stError button,
    .stWarning button,
    .stInfo button,
    /* 더 구체적인 선택자들 */
    div[data-testid="stSuccess"] button,
    div[data-testid="stError"] button,
    div[data-testid="stWarning"] button,
    div[data-testid="stInfo"] button,
    /* 모든 알림 컴포넌트의 버튼 */
    .stAlert button,
    .stAlert .stButton button,
    /* 모달 내 모든 버튼 강제 적용 */
    [data-testid="stModal"] button,
    section[data-testid="stModal"] button,
    [role="dialog"] button,
    /* Streamlit 기본 알림 스타일 오버라이드 */
    .stAlert .stButton > button,
    .stSuccess .stButton > button,
    .stError .stButton > button,
    .stWarning .stButton > button,
    .stInfo .stButton > button {
        background-color: #2c2c2c !important;
        color: white !important;
        border: 1px solid #2c2c2c !important;
        border-radius: 8px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
    }
    
    .stModal .stButton > button:hover,
    [data-testid="stModal"] .stButton > button:hover,
    section[data-testid="stModal"] .stButton > button:hover,
    [role="dialog"] .stButton > button:hover,
    div[data-testid="stModal"] button:hover,
    section[data-testid="stModal"] button:hover,
    [role="dialog"] button:hover,
    .stSuccess .stButton > button:hover,
    [data-testid="stSuccess"] .stButton > button:hover,
    .stAlert .stButton > button:hover,
    [data-testid="stAlert"] .stButton > button:hover,
    .stModal button:hover,
    [data-testid="stModal"] button:hover,
    section[data-testid="stModal"] button:hover,
    [role="dialog"] button:hover,
    .stSuccess button:hover,
    .stError button:hover,
    .stWarning button:hover,
    .stInfo button:hover,
    div[data-testid="stSuccess"] button:hover,
    div[data-testid="stError"] button:hover,
    div[data-testid="stWarning"] button:hover,
    div[data-testid="stInfo"] button:hover,
    .stAlert button:hover,
    .stAlert .stButton button:hover,
    [data-testid="stModal"] button:hover,
    section[data-testid="stModal"] button:hover,
    [role="dialog"] button:hover,
    .stAlert .stButton > button:hover,
    .stSuccess .stButton > button:hover,
    .stError .stButton > button:hover,
    .stWarning .stButton > button:hover,
    .stInfo .stButton > button:hover {
        background-color: #3c3c3c !important;
        border-color: #3c3c3c !important;
    }
    
    /* 구분선 스타일 */
    .divider {
        border-top: 1px solid #ddd !important;
        margin: 28px 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'user_id_checked' not in st.session_state:
    st.session_state.user_id_checked = False
if 'nickname_checked' not in st.session_state:
    st.session_state.nickname_checked = False
if 'phone_checked' not in st.session_state:
    st.session_state.phone_checked = False
if 'last_checked_user_id' not in st.session_state:
    st.session_state.last_checked_user_id = ""
if 'last_checked_nickname' not in st.session_state:
    st.session_state.last_checked_nickname = ""
if 'last_checked_phone' not in st.session_state:
    st.session_state.last_checked_phone = ""

# 검증 함수들
def validate_user_id(user_id):
    if not user_id:
        return False, "최소 3자~최대13자 이내 영문(소문자), 숫자로 입력해주세요."
    if len(user_id) < 3 or len(user_id) > 13:
        return False, "최소 3자~최대13자 이내 영문(소문자), 숫자로 입력해주세요."
    if not re.match(r'^[a-z0-9]+$', user_id):
        return False, "최소 3자~최대13자 이내 영문(소문자), 숫자로 입력해주세요."
    return True, ""

def validate_password(password):
    if not password:
        return False, "비밀번호는 영문/숫자/특수문자 각 1개 이상 사용하여 최소 8자 이상 입력해주세요."
    if len(password) < 8:
        return False, "비밀번호는 영문/숫자/특수문자 각 1개 이상 사용하여 최소 8자 이상 입력해주세요."
    if not re.search(r'[a-zA-Z]', password):
        return False, "비밀번호는 영문/숫자/특수문자 각 1개 이상 사용하여 최소 8자 이상 입력해주세요."
    if not re.search(r'[0-9]', password):
        return False, "비밀번호는 영문/숫자/특수문자 각 1개 이상 사용하여 최소 8자 이상 입력해주세요."
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "비밀번호는 영문/숫자/특수문자 각 1개 이상 사용하여 최소 8자 이상 입력해주세요."
    return True, ""

def validate_password_confirm(password, password_confirm):
    if not password_confirm:
        return False, "입력한 비밀번호와 일치하지 않습니다."
    if password != password_confirm:
        return False, "입력한 비밀번호와 일치하지 않습니다."
    return True, ""

def validate_nickname(nickname):
    if not nickname:
        return False, "특수문자 제외, 한글/영문/숫자로 최소 3자~최대 8자리까지 입력 가능합니다."
    if len(nickname) < 3 or len(nickname) > 8:
        return False, "특수문자 제외, 한글/영문/숫자로 최소 3자~최대 8자리까지 입력 가능합니다."
    if not re.match(r'^[가-힣a-zA-Z0-9]+$', nickname):
        return False, "특수문자 제외, 한글/영문/숫자로 최소 3자~최대 8자리까지 입력 가능합니다."
    return True, ""

def validate_phone(phone):
    if not phone:
        return False, "잘못된 휴대폰번호입니다. 다시 입력해주세요."
    if not re.match(r'^01[0-9]-?[0-9]{3,4}-?[0-9]{4}$', phone):
        return False, "잘못된 휴대폰번호입니다. 다시 입력해주세요."
    return True, ""

def validate_email(email):
    if not email:
        return False, "이메일 형식이 올바르지 않습니다. 다시 입력해 주세요."
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return False, "이메일 형식이 올바르지 않습니다. 다시 입력해 주세요."
    return True, ""

# 중복 확인 함수들

def check_nickname_duplicate(nickname):
    try:
        supabase = get_supabase_client()
        result = supabase.table('users').select('nickname').eq('nickname', nickname).execute()
        return len(result.data) == 0
    except Exception as e:
        st.error(f"중복 확인 중 오류가 발생했습니다: {str(e)}")
        return False


def check_email_duplicate(email):
    try:
        supabase = get_supabase_client()
        result = supabase.table('users').select('email').eq('email', email).execute()
        return len(result.data) == 0
    except Exception as e:
        st.error(f"중복 확인 중 오류가 발생했습니다: {str(e)}")
        return False

# ============================================
# 제목 섹션 (로그인 페이지와 동일한 구조)
# ============================================
st.markdown("""<div style="margin-top: 0px;"></div>""", unsafe_allow_html=True)

# 제목만 중앙 정렬
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
    ">회원 가입</h1>
</div>
""", unsafe_allow_html=True)

# ============================================
# 회원가입 폼 (로그인 페이지와 동일한 구조)
# ============================================

# 아이디 입력 (가로 배치)
col_label1, col_input1, col_btn1 = st.columns([1.2, 3.6, 1.2])
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
        key="user_id",
        placeholder="example@email.com",
        label_visibility="collapsed"
    )

with col_btn1:
        user_id_check_btn = st.button("중복 확인", key="user_id_check_btn", type="secondary", use_container_width=True)

# 이메일 검증 메시지
user_id_valid, user_id_msg = validate_email(user_id_input)
if user_id_input and not user_id_valid:
    st.markdown(f'<div class="error-message">{user_id_msg}</div>', unsafe_allow_html=True)

# 이메일 중복 확인 처리
if user_id_check_btn:
    if user_id_input:
        if validate_email(user_id_input)[0]:
            if check_email_duplicate(user_id_input):
                show_success("사용 가능한 이메일입니다.")
                st.session_state.user_id_checked = True
                st.session_state.last_checked_user_id = user_id_input
            else:
                show_error("이미 사용 중인 이메일입니다.")
        else:
            show_error("이메일 형식을 확인해주세요.")
    else:
        show_error("이메일을 입력해주세요.")

# 아이디 값이 변경되면 중복 확인 상태 초기화
if user_id_input != st.session_state.last_checked_user_id:
    st.session_state.user_id_checked = False

st.markdown("""<div style="margin: 20px 0;"></div>""", unsafe_allow_html=True)

# 비밀번호 입력 (가로 배치)
col_label2, col_input2 = st.columns([1.2, 4.8])
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
        key="password",
        placeholder="",
        label_visibility="collapsed"
    )


# 비밀번호 검증 메시지
password_valid, password_msg = validate_password(password_input)
if password_input and not password_valid:
    st.markdown(f'<div class="error-message">{password_msg}</div>', unsafe_allow_html=True)

st.markdown("""<div style="margin: 20px 0;"></div>""", unsafe_allow_html=True)

# 비밀번호 확인 입력 (가로 배치)
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
    ">비밀번호 확인</p>
    """, unsafe_allow_html=True)

with col_input3:
    password_confirm_input = st.text_input(
        "비밀번호 확인",
        type="password",
        key="password_confirm",
        placeholder="",
        label_visibility="collapsed"
    )


# 비밀번호 확인 검증 메시지
password_confirm_valid, password_confirm_msg = validate_password_confirm(password_input, password_confirm_input)
if password_confirm_input and not password_confirm_valid:
    st.markdown(f'<div class="error-message">{password_confirm_msg}</div>', unsafe_allow_html=True)

# 구분선
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# 닉네임 입력 (가로 배치)
col_label4, col_input4, col_btn4 = st.columns([1.2, 3.6, 1.2])
with col_label4:
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

with col_input4:
    nickname_input = st.text_input(
        "닉네임",
        key="nickname",
        placeholder="",
        label_visibility="collapsed"
    )

with col_btn4:
        nickname_check_btn = st.button("중복 확인", key="nickname_check_btn", type="secondary", use_container_width=True)

# 닉네임 검증 메시지
nickname_valid, nickname_msg = validate_nickname(nickname_input)
if nickname_input and not nickname_valid:
    st.markdown(f'<div class="error-message">{nickname_msg}</div>', unsafe_allow_html=True)

# 닉네임 중복 확인 처리
if nickname_check_btn:
    if nickname_input:
        if validate_nickname(nickname_input)[0]:
            if check_nickname_duplicate(nickname_input):
                show_success("사용 가능한 닉네임입니다.")
                st.session_state.nickname_checked = True
                st.session_state.last_checked_nickname = nickname_input
            else:
                show_error("이미 사용 중인 닉네임입니다.")
        else:
            show_error("닉네임 형식을 확인해주세요.")
    else:
        show_error("닉네임을 입력해주세요.")

# 닉네임 값이 변경되면 중복 확인 상태 초기화
if nickname_input != st.session_state.last_checked_nickname:
    st.session_state.nickname_checked = False

st.markdown("""<div style="margin: 20px 0;"></div>""", unsafe_allow_html=True)

# 휴대폰 번호 입력 (가로 배치)
col_label5, col_input5 = st.columns([1.2, 4.8])
with col_label5:
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

with col_input5:
    phone_input = st.text_input(
        "휴대폰 번호",
        key="phone",
        placeholder="",
        label_visibility="collapsed"
    )

# 휴대폰 번호 검증 메시지
phone_valid, phone_msg = validate_phone(phone_input)
if phone_input and not phone_valid:
    st.markdown(f'<div class="error-message">{phone_msg}</div>', unsafe_allow_html=True)



st.markdown("""<div style="margin: 49px 0 0 0;"></div>""", unsafe_allow_html=True)

# 가입하기 버튼 활성화 상태 확인
def is_signup_button_active():
    """모든 필드가 정상적으로 입력되고 중복 확인이 완료되었는지 확인"""
    return (
        user_id_input and user_id_valid and st.session_state.user_id_checked and
        password_input and password_valid and
        password_confirm_input and password_confirm_valid and
        nickname_input and nickname_valid and st.session_state.nickname_checked and
        phone_input and phone_valid
    )

# ============================================
# 가입하기 버튼
# ============================================
# 버튼 활성화 상태 확인
button_active = is_signup_button_active()

# 가입하기 버튼
signup_btn = st.button("가입하기", use_container_width=True, key="signup_btn")

# 가입하기 버튼 활성화 상태에 따른 스타일 적용
if button_active:
    st.markdown("""
    <script>
        // 가입하기 버튼이 활성화된 경우 검정색으로 변경
        setTimeout(function() {
            const signupBtn = document.querySelector('button[kind="primary"]');
            if (signupBtn) {
                signupBtn.classList.add('active');
            }
        }, 100);
    </script>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <script>
        // 가입하기 버튼이 비활성화된 경우 회색으로 유지
        setTimeout(function() {
            const signupBtn = document.querySelector('button[kind="primary"]');
            if (signupBtn) {
                signupBtn.classList.remove('active');
            }
        }, 100);
    </script>
    """, unsafe_allow_html=True)

# ============================================
# 가입 처리
# ============================================
if signup_btn:
    # 모든 필드 검증
    all_valid = True
    
    # 아이디 검증
    if not user_id_input or not user_id_valid or not st.session_state.user_id_checked:
        all_valid = False
    
    # 비밀번호 검증
    if not password_input or not password_valid:
        all_valid = False
    
    # 비밀번호 확인 검증
    if not password_confirm_input or not password_confirm_valid:
        all_valid = False
    
    # 닉네임 검증
    if not nickname_input or not nickname_valid or not st.session_state.nickname_checked:
        all_valid = False
    
    # 휴대폰 번호 검증
    if not phone_input or not phone_valid:
        all_valid = False
    
    # 이메일 검증
    if not user_id_input or not user_id_valid or not st.session_state.user_id_checked:
        all_valid = False
    
    # 모든 항목이 입력되지 않은 경우 확인 팝업 표시
    if not all_valid:
        show_error("모든 항목을 입력해 주세요.")
    else:
        try:
            # Supabase Auth 회원가입
            supabase = get_supabase_client()
            auth_response = supabase.auth.sign_up({
                "email": user_id_input,
                "password": password_input
            })
            
            if auth_response.user:
                # public.users 테이블에 추가 정보 저장
                user_data = {
                    "email": user_id_input,
                    "nickname": nickname_input,
                    "phone": phone_input
                }
                
                result = supabase.table('users').insert(user_data).execute()
                
                if result.data:
                    # 회원가입 후 자동 로그인 방지를 위해 세션 정리
                    supabase.auth.sign_out()
                    
                    # session_state 초기화
                    st.session_state.logged_in = False
                    st.session_state.user = None
                    st.session_state.access_token = None
                    st.session_state.user_data = None
                    
                    show_success("회원가입이 완료되었습니다!", "pages/1_login.py")
                else:
                    st.error("PostgreSQL DB 저장 중 오류가 발생했습니다.")
            else:
                st.error("Supabase Auth 회원가입 실패")
        
        except Exception as e:
            st.error(f"회원가입 중 오류가 발생했습니다: {str(e)}")
