"""
게시글 열람 페이지 (댓글 포함)
"""

import streamlit as st
import streamlit.components.v1 as components
from config.settings import PAGE_CONFIG
from utils.auth import require_login, get_current_user, logout_user, validate_session
from utils.dialogs import delete_confirm_dialog
from utils.styles import hide_sidebar
from utils.supabase_client import get_supabase_client

# 페이지 설정 - 홈 화면과 동일하게 centered로 변경
st.set_page_config(
    page_title="캠퍼스링크",
    page_icon="🏫",
    layout="centered"
)

# 사이드바 숨김
hide_sidebar()

def render_header(has_schools=False):
    """헤더 렌더링 - 전체 너비
    
    Args:
        has_schools (bool): 학교가 추가되었는지 여부
    """
    user = get_current_user()
    nickname = user.get('nickname', '사용자') if user else '사용자'
    
    # URL 쿼리 파라미터 확인
    query_params = st.query_params
    
    # 버튼 액션 처리
    if "action" in query_params:
        action = query_params["action"]
        
        if action == "logout":
            logout_user()
            st.query_params.clear()
            st.switch_page("pages/1_login.py")
        elif action == "schools":
            st.query_params.clear()
            st.switch_page("pages/4_add_school.py")
        elif action == "mypage":
            st.query_params.clear()
            st.switch_page("pages/8_mypage.py")
    
    # 헤더 스타일링
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

    /* 헤더 전체 너비 - 20% 축소 */
    .header-full-width {
        width: 100vw;
        position: fixed;
        top: 0;
        left: 0;
        margin-top: 0rem;
        padding: 16px 0;  /* 20px → 16px */
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
        padding: 0 16px;  /* 20px → 16px */
        width: 100%;
    }

    .left-section {
        display: flex;
        align-items: center;
        gap: 16px;  /* 20px → 16px */
    }

    .logo-section {
        display: flex;
        align-items: center;
        gap: 12px;  /* 15px → 12px */
    }

    .logo-icon {
        width: 35px;  /* 44px → 35px */
        height: 35px;  /* 44px → 35px */
        background-color: #e3e3e3;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;  /* 20px → 16px */
    }

    .logo-text {
        font-size: 19px;  /* 24px → 19px */
        font-weight: bold;
        color: black;
    }

    .search-section {
        display: flex;
        align-items: center;
        gap: 8px;  /* 10px → 8px */
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
        width: 16px;  /* 20px → 16px */
        height: 16px;  /* 20px → 16px */
        background-color: transparent;
        border: none;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        font-size: 14px;  /* 18px → 14px */
    }

    .right-section {
        display: flex;
        align-items: center;
        gap: 8px;  /* 10px → 8px */
    }

    .nickname {
        font-size: 12px;  /* 15px → 12px */
        font-weight: bold;
        color: black;
        margin-right: 8px;  /* 10px → 8px */
    }

    .header-buttons {
        display: flex;
        gap: 8px;  /* 10px → 8px */
        align-items: center;
    }

    .header-button {
        width: 66px;  /* 83px → 66px */
        height: 29px;  /* 36px → 29px */
        border-radius: 6px;  /* 8px → 6px */
        background-color: #e3e3e3;
        border: 1px solid #767676;
        font-size: 13px;  /* 16px → 13px */
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

    # 헤더 HTML (쿼리 파라미터로 액션 전달)
    # 학교 추가 여부에 따라 검색창 활성화/비활성화
    search_class = "enabled" if has_schools else "disabled"
    search_disabled = "" if has_schools else "disabled"
    
    st.markdown(f"""
    <div class="header-full-width">
        <div class="header-content">
            <div class="left-section">
                <div class="logo-section">
                    <div class="logo-icon"></div>
                    <a href="/" target="_self" class="logo-text" style="text-decoration: none; color: inherit; cursor: pointer;">캠퍼스링크</a>
                </div>
                <div class="search-section">
                    <input type="text" class="search-input {search_class}" placeholder="" {search_disabled}>
                    <div class="search-button">
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

def increment_view_count(post_id):
    """게시글 조회수 증가"""
    try:
        supabase = get_supabase_client()
        # 현재 조회수 가져오기
        response = supabase.table("posts").select("view_count").eq("id", post_id).execute()
        if response.data:
            current_count = response.data[0].get('view_count', 0)
            # 조회수 +1
            supabase.table("posts").update({"view_count": current_count + 1}).eq("id", post_id).execute()
    except Exception as e:
        st.error(f"조회수 증가 중 오류: {str(e)}")

def main():
    """게시글 열람 페이지 메인 함수"""
    
    # 로그인 확인 (미로그인 시 자동 리다이렉트)
    require_login()
    
    # 세션 유효성 검증 (보안 강화)
    if not validate_session():
        st.error("세션이 유효하지 않습니다. 다시 로그인해주세요.")
        st.stop()
    
    # 헤더 렌더링 (학교가 있다고 가정)
    render_header(has_schools=True)
    
    # 스타일 적용 (홈 화면과 동일한 스타일)
    st.markdown("""
    <style>
        /* 사이드바 완전히 숨기기 */
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
        [data-testid="collapsedControl"],
        button[data-testid="collapsedControl"],
        .st-emotion-cache-1gwvy71,
        [data-testid="baseButton-header"] {
            display: none !important;
            visibility: hidden !important;
            width: 0 !important;
            height: 0 !important;
            opacity: 0 !important;
            position: absolute !important;
        }
        
        /* 전체 컨테이너 */
        .main {
            background-color: white;
        }
        
        /* 홈 화면과 동일한 패딩 스타일 */
        .main .block-container {
            padding-top: 80px !important; /* 헤더 높이만큼 */
            padding-bottom: 0rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        
        .stMainBlockContainer {
            padding-top: 80px !important; /* 헤더 높이만큼 */
            padding-bottom: 0rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        
        [data-testid="stMainBlockContainer"] {
            padding-top: 80px !important; /* 헤더 높이만큼 */
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        
        .stVerticalBlock {
            padding-top: 0rem !important;
        }
        
        .stElementContainer {
            padding-top: 0rem !important;
        }
        
        [data-testid="stVerticalBlock"] {
            padding-top: 0rem !important;
        }
        
        [data-testid="stElementContainer"] {
            padding-top: 0rem !important;
        }
        
        /* Vertical Block 간격 제거 */
        .stVerticalBlock,
        [data-testid="stVerticalBlock"] {
            gap: 0 !important;
        }
        
        /* 홈 화면과 동일한 게시글 스타일 */
        .post-item {
            background-color: white;
            padding: 1.5rem 0;
            border-bottom: none; /* 밑줄 제거 */
        }
        
        .post-header {
            display: flex;
            align-items: center;
            margin-bottom: 18px;
        }
        
        .profile-image {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background-color: #e3e3e3;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 12px;
        }
        
        .post-meta {
            flex: 1;
        }
        
        .post-nickname {
            font-size: 16px;
            font-weight: 600;
            color: #333;
            margin-bottom: 2px;
        }
        
        .post-time {
            font-size: 14px;
            color: #999;
        }
        
        .more-icon {
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            color: #999;
        }
        
        .more-icon svg {
            width: 20px;
            height: 20px;
        }
        
        .post-title {
            font-size: 18px;
            font-weight: 600;
            color: #1e1e1e;
            margin-bottom: 8px;
            line-height: 1.4;
        }
        
        .post-content {
            font-size: 16px;
            color: #666;
            line-height: 1.5;
            margin-bottom: 8px;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        
        .post-stats {
            display: flex;
            justify-content: center;
            gap: 180px;
            font-size: 16px;
            color: #666;
            margin-top: 20px;
        }
        
        .stat-item {
            display: flex;
            align-items: center;
            gap: 6px;
        }
        
        .stat-item svg {
            width: 20px;
            height: 20px;
        }
        
        .stat-item span {
            font-size: 16px;
        }
        
        /* 뒤로가기 버튼 스타일 */
        .back-button {
            background-color: #f0f0f0;
            color: black;
            border: 1px solid #ddd;
            padding: 8px 16px;
            border-radius: 8px;
            font-size: 16px;
            margin-bottom: 20px;
        }
        
        /* 댓글 섹션 스타일 - 컨테이너 밖으로 확장 */
        .element-container:has(.comment-section) {
            width: 100vw !important;
            max-width: 100vw !important;
            margin-left: calc(-50vw + 50%) !important;
            margin-right: calc(-50vw + 50%) !important;
            padding: 0 !important;
        }
        
        .comment-section {
            margin-top: 30px;
            width: 100% !important;
            max-width: 100% !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        
        .comment-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px; /* 간격 증가 */
        }
        
        /* 댓글 헤더의 컬럼 정렬 */
        .comment-header [data-testid="column"] {
            display: flex;
            align-items: center;
        }
        
        /* 버튼이 있는 컬럼에 상단 여백 추가 */
        div[data-testid="column"]:has(.comment-title) + div[data-testid="column"] {
            padding-top: 2px;
        }
        
        /* 스마트폰에서도 한 줄 유지 */
        @media (max-width: 768px) {
            .comment-header [data-testid="column"] {
                min-width: 0;
                flex: 1;
            }
            
            div[data-testid="column"]:has(.comment-title) {
                flex: 1;
                min-width: 0;
            }
            
            div[data-testid="column"]:has(.comment-title) + div[data-testid="column"] {
                flex: 0 0 auto;
                min-width: 60px;
            }
            
            /* 스마트폰에서 댓글 라벨 아래 여백 */
            div[data-testid="column"]:has(.comment-title) {
                margin-bottom: 8px;
            }
        }
        
        .comment-title {
            font-size: 16.8px; /* 기존보다 20% 증대 */
            font-weight: 600;
            color: black;
            margin: 0;
            display: flex;
            align-items: center;
            height: 100%;
        }
        
        .comment-submit-btn-header {
            background-color: #8d8d8d;
            color: white;
            border: none;
            padding: 5.6px 11.2px; /* 30% 줄임 */
            border-radius: 5.6px; /* 30% 줄임 */
            font-size: 9.8px; /* 30% 줄임 */
            font-weight: 600;
            cursor: pointer;
        }
        
        /* 댓글 헤더 버튼 스타일 - 더 직접적인 선택자 */
        button[key="comment_submit_header"] {
            background-color: #8d8d8d !important;
            color: white !important;
            border: none !important;
            padding: 1px 3px !important;
            border-radius: 1.5px !important;
            font-size: 0.8rem !important; /* 요청: 0.8rem */
            font-weight: 600 !important;
            height: auto !important;
            min-height: auto !important;
            width: auto !important;
        }
        
        /* 추가적인 버튼 스타일링 */
        [data-testid="column"]:last-child .stButton > button {
            background-color: #8d8d8d !important;
            color: white !important;
            border: none !important;
            padding: 1px 3px !important;
            border-radius: 1.5px !important;
            font-size: 0.8rem !important; /* 요청: 0.8rem */
            font-weight: 600 !important;
            height: auto !important;
            min-height: auto !important;
        }

        /* Streamlit이 생성하는 동적 클래스에 직접 적용 (안정적 보정) */
        .st-emotion-cache-12j140x {
            font-size: 0.8rem !important;
        }
        
        /* 댓글 입력 영역 - 글쓰기 화면과 동일한 스타일 */
        .comment-input-container {
            position: relative;
            margin-bottom: 20px;
            width: 100% !important;
        }
        
        /* 텍스트 영역 전체 너비로 확장 */
        .stTextArea {
            width: 100% !important;
            margin-top: 1rem !important;
        }
        
        .stTextArea > div {
            width: 100% !important;
        }
        
        /* 텍스트 영역 스타일 - 글쓰기 화면과 동일 */
        .stTextArea > div > div > textarea {
            border: 1px solid #aaa9a9 !important; /* 글쓰기 화면과 동일 */
            border-radius: 8px !important;
            padding: 16px !important;
            font-size: 16px !important;
            font-family: inherit !important;
            background-color: white !important;
            color: black !important;
            resize: vertical !important;
            min-height: 115px !important;
            width: 100% !important; /* 전체 너비 사용 */
            box-sizing: border-box !important;
        }
        
        .stTextArea > div > div > textarea:focus {
            border: 1px solid #aaa9a9 !important; /* 글쓰기 화면과 동일 */
            box-shadow: none !important;
            outline: none !important;
        }
        
        /* textarea 이중선 제거 */
        .stTextArea > div {
            border: none !important;
        }
        
        /* apply 버튼 숨기기 */
        .stTextArea button {
            display: none !important;
        }
        
        /* "Press Ctrl+Enter to apply" 메시지 숨기기 */
        .stTextArea [data-testid="InputInstructions"] {
            display: none !important;
        }
        
        .stTextArea div[class*="InputInstructions"] {
            display: none !important;
        }
        
        /* textarea의 부모 div도 border 제거 */
        .stTextArea > div > div {
            border: none !important;
            box-shadow: none !important;
        }
        
        /* 라벨 숨기기 */
        .stTextArea label {
            display: none !important;
        }
        
        /* 문자 카운터 스타일 */
        .comment-counter {
            position: absolute;
            bottom: 10px;
            right: 15px;
            font-size: 16px;
            color: #797979;
        }
        
        /* 버튼 스타일 - 글쓰기 화면과 동일 */
        .stButton > button {
            background-color: #2c2c2c !important;
            color: white !important;
            border: 1px solid #2c2c2c !important;
            border-radius: 6px !important;
            height: 37px !important;
            font-size: 14px !important;
            font-weight: 400 !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton > button:hover {
            background-color: #3c3c3c !important;
            border-color: #3c3c3c !important;
        }
        
        .stButton > button:active {
            background-color: #1c1c1c !important;
        }
        
        /* 댓글 목록 스타일 - 게시글과 동일하게 */
        .comment-item {
            background-color: white;
            padding: 1.5rem 0;
            margin-left: 20px; /* 내어쓰기 */
            margin-right: 0; /* 오른쪽 여백은 섹션에서 처리 */
            border-bottom: 1px solid #e3e3e3; /* 댓글 하단에 구분선 */
        }
        
        .comment-item:first-child {
            margin-top: 0.8rem; /* input box와의 간격 */
        }
        
        /* 마지막 댓글은 구분선 제거 */
        .comment-item:last-child {
            border-bottom: none;
        }
        
        .comment-header {
            display: flex;
            align-items: center;
            margin-bottom: 18px;
        }
        
        .comment-profile-image {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background-color: #e3e3e3;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 12px;
        }
        
        .comment-meta {
            flex: 1;
        }
        
        .comment-nickname {
            font-size: 16px;
            font-weight: 600;
            color: #333;
            margin-bottom: 2px;
        }
        
        .comment-time {
            font-size: 14px;
            color: #999;
        }
        
        .comment-more-icon {
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            color: #999;
        }
        
        .comment-more-icon svg {
            width: 20px;
            height: 20px;
        }
        
        .comment-content-text {
            font-size: 16px;
            color: #666;
            line-height: 1.5;
            margin-bottom: 8px;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        
        /* 구분선 스타일 */
        .divider {
            height: 1px;
            background-color: #e3e3e3;
            margin: 20px 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # 게시글 ID를 query parameter 또는 session_state에서 가져오기
    query_params = st.query_params
    post_id = query_params.get("id") or st.session_state.get("current_post_id", None)
    
    if not post_id:
        st.warning("게시글을 찾을 수 없습니다.")
        if st.button("← 홈으로 돌아가기"):
            st.switch_page("pages/3_home.py")
        return
    
    # 조회수 증가 (한 번만 실행되도록 세션 체크)
    if f"viewed_{post_id}" not in st.session_state:
        increment_view_count(post_id)
        st.session_state[f"viewed_{post_id}"] = True
    
    # 게시글 데이터 가져오기
    try:
        supabase = get_supabase_client()
        response = supabase.table("posts").select("""
            *,
            users (nickname)
        """).eq("id", post_id).execute()
        
        if not response.data:
            st.warning("게시글을 찾을 수 없습니다.")
            return
        
        post = response.data[0]
    except Exception as e:
        st.error(f"게시글을 불러오는 중 오류가 발생했습니다: {str(e)}")
        return
    
    # 댓글 개수 가져오기
    try:
        comments_response = supabase.table("comments").select("id", count="exact").eq("post_id", post_id).execute()
        comment_count = comments_response.count if comments_response.count else 0
    except:
        comment_count = 0
    
    # 작성자 정보
    author_nickname = post.get('users', {}).get('nickname', '익명') if post.get('users') else '익명'
    
    # 홈 화면과 동일한 시간 포맷팅 함수
    def format_time_ago(created_at_str):
        """
        게시 시간을 '~전' 형식으로 포맷팅
        - 오늘: 1분 전~59분 전, 1시간 전~23시간 전
        - 1일 전~6일 전 (자정 기준으로 날짜 변경 시 1일 전)
        - 7일 이상: YY.MM.DD. 형식
        """
        try:
            # ISO 형식 파싱
            created_at = datetime.fromisoformat(created_at_str.replace('Z', '+00:00'))
            now = datetime.now(timezone.utc)
            
            # 한국 시간으로 변환 (UTC+9)
            from datetime import timedelta
            kst_now = now + timedelta(hours=9)
            kst_created = created_at + timedelta(hours=9)
            
            # 자정 기준으로 날짜 차이 계산
            kst_now_date = kst_now.date()
            kst_created_date = kst_created.date()
            days_diff = (kst_now_date - kst_created_date).days
            
            # 오늘 작성된 글 (날짜가 같은 경우)
            if days_diff == 0:
                # 시간 차이 계산
                diff = now - created_at
                
                # 분 단위 (1분~59분)
                minutes = int(diff.total_seconds() / 60)
                if minutes < 60:
                    return f"{minutes}분 전" if minutes > 0 else "방금 전"
                
                # 시간 단위 (1시간~23시간)
                hours = int(diff.total_seconds() / 3600)
                return f"{hours}시간 전"
            
            # 1일 전~6일 전 (자정이 지난 경우)
            if 1 <= days_diff <= 6:
                return f"{days_diff}일 전"
            
            # 7일 이상: YY.MM.DD. 형식
            return kst_created.strftime('%y.%m.%d.')
            
        except Exception as e:
            return created_at_str
    
    # 날짜 포맷팅 (홈 화면과 동일한 방식)
    from datetime import datetime, timezone
    created_at = post.get('created_at', '')
    if created_at:
        time_str = format_time_ago(created_at)
    else:
        time_str = '날짜 없음'
    
    # 작성자 정보 표시 (홈 화면과 동일한 구조)
    st.markdown(f"""
    <div class="post-item">
        <div class="post-header">
            <div class="profile-image"></div>
            <div class="post-meta">
                <div class="post-nickname">{author_nickname}</div>
                <div class="post-time">{time_str}</div>
            </div>
            <div class="more-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="12" cy="12" r="2" fill="currentColor"/>
                    <circle cx="12" cy="5" r="2" fill="currentColor"/>
                    <circle cx="12" cy="19" r="2" fill="currentColor"/>
                </svg>
            </div>
        </div>
    <div class="post-title">{post.get('title', '제목 없음')}</div>
        <div class="post-content">{post.get('content', '내용이 없습니다.')}</div>
    <div class="post-stats">
            <div class="stat-item">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M21 15C21 15.5304 20.7893 16.0391 20.4142 16.4142C20.0391 16.7893 19.5304 17 19 17H7L3 21V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H19C19.5304 3 20.0391 3.21071 20.4142 3.58579C20.7893 3.96086 21 4.46957 21 5V15Z" stroke="#666" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
        <span>댓글 {comment_count}</span>
            </div>
            <div class="stat-item">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M1 12S5 4 12 4S23 12 23 12S19 20 12 20S1 12 1 12Z" stroke="#666" stroke-width="2"/>
                    <circle cx="12" cy="12" r="3" stroke="#666" stroke-width="2"/>
                </svg>
        <span>조회수 {post.get('view_count', 0):,}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 구분선
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # 댓글 섹션
    st.markdown('<div class="comment-section">', unsafe_allow_html=True)
    
    # 댓글 헤더 (제목과 달기 버튼) - 하나의 영역으로 통합
    col1, col2 = st.columns([1, 0.2])
    with col1:
        st.markdown('<div style="font-size: 20px; font-weight: 600; color: black; display: flex; align-items: center; height: 100%;">댓글</div>', unsafe_allow_html=True)
    with col2:
        submit_comment = st.button("댓글 달기", key="comment_submit_header", use_container_width=True)
    
    # 댓글 입력창 (헤더 아래에 표시 - 별도 컨테이너)
    comment = st.text_area(
        "댓글을 입력하세요", 
        height=115, 
        max_chars=800,
        key="comment_input",
        label_visibility="collapsed"
    )
    
    # 문자 카운터 표시 (실시간 업데이트용 ID 추가)
    comment_length = len(comment) if comment else 0
    st.markdown(f"""
    <div id="comment-counter" style="text-align: right; margin-top: 5px; font-size: 16px; color: #797979;">
        {comment_length} / 800
    </div>
    """, unsafe_allow_html=True)
    
    # 실시간 글자 수 업데이트 JavaScript
    components.html("""
    <script>
    (function() {
        function updateCommentCounter() {
            const commentTextarea = window.parent.document.querySelector('textarea[aria-label="댓글을 입력하세요"]');
            const commentCounter = window.parent.document.getElementById('comment-counter');
            
            if (commentTextarea && commentCounter && !commentTextarea.hasAttribute('data-listener')) {
                commentTextarea.setAttribute('data-listener', 'true');
                commentTextarea.addEventListener('input', function() {
                    const length = this.value.length;
                    commentCounter.textContent = length + '/800';
                });
            }
        }
        
        // 초기 실행
        updateCommentCounter();
        
        // MutationObserver로 DOM 변경 감지
        const observer = new MutationObserver(function(mutations) {
            updateCommentCounter();
        });
        
        observer.observe(window.parent.document.body, {
            childList: true,
            subtree: true
        });
        
        // 페이지 로드 후에도 재실행
        setTimeout(updateCommentCounter, 500);
        setTimeout(updateCommentCounter, 1000);
        setTimeout(updateCommentCounter, 2000);
    })();
    </script>
    """, height=0)
        
    # 댓글 달기 버튼 처리
    if submit_comment:
        if comment and comment.strip():
            # 댓글 저장 로직
            try:
                user = get_current_user()
                supabase = get_supabase_client()
                supabase.table("comments").insert({
                    "post_id": post_id,
                    "user_id": user["id"],
                    "content": comment.strip()
                }).execute()
                st.success("댓글이 작성되었습니다!")
                st.rerun()
            except Exception as e:
                st.error(f"댓글 작성 중 오류가 발생했습니다: {str(e)}")
        else:
            st.error("댓글을 입력해 주세요", icon="🚨")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 댓글 목록 (해당 게시글의 실제 댓글)
    try:
        comments_response = supabase.table("comments").select("""
            *,
            users (nickname)
        """).eq("post_id", post_id).order("created_at", desc=True).execute()
        
        comments = comments_response.data if comments_response.data else []
        
        if comments:
            for i, comment in enumerate(comments):
                # 댓글 작성자 정보
                comment_author = comment.get('users', {}).get('nickname', '익명') if comment.get('users') else '익명'
                
                # 댓글 시간 포맷팅
                comment_time = format_time_ago(comment['created_at'])
                
                # 댓글 내용 표시 (게시글과 동일한 스타일)
                st.markdown(f"""
                <div class="comment-item">
                    <div class="comment-header">
                        <div class="comment-profile-image"></div>
                        <div class="comment-meta">
                            <div class="comment-nickname">{comment_author}</div>
                            <div class="comment-time">{comment_time}</div>
                        </div>
                        <div class="comment-more-icon">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <circle cx="12" cy="12" r="2" fill="currentColor"/>
                                <circle cx="12" cy="5" r="2" fill="currentColor"/>
                                <circle cx="12" cy="19" r="2" fill="currentColor"/>
                            </svg>
                        </div>
                    </div>
                    <div class="comment-content-text">{comment.get('content', '')}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # 마지막 댓글이 아닌 경우에만 구분선 추가
                if i < len(comments) - 1:
                    st.markdown('<div style="height: 1px; background-color: #e3e3e3; margin: 10px 0 10px 20px;"></div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"댓글을 불러오는 중 오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    main()


