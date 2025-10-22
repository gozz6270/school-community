"""
홈 페이지
관심 학교 상태에 따른 다른 화면 표시
"""

import streamlit as st
from datetime import datetime, timezone
from config.settings import PAGE_CONFIG, POST_CATEGORIES
from utils.auth import require_login, logout_user, get_current_user
from utils.supabase_client import get_supabase_client
from utils.styles import hide_sidebar

# 페이지 설정 - centered로 변경
st.set_page_config(
    page_title="캠퍼스링크",
    page_icon="🏫",
    layout="centered"
)

# 사이드바 숨김
hide_sidebar()

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

def get_user_schools_count():
    """현재 사용자의 관심 학교 개수 반환"""
    try:
        user = get_current_user()
        if not user:
            return 0
        
        supabase = get_supabase_client()
        response = supabase.table("user_schools").select("id").eq("user_id", user["id"]).execute()
        
        return len(response.data) if response.data else 0
    except Exception as e:
        st.error(f"관심 학교 정보를 가져오는 중 오류가 발생했습니다: {str(e)}")
        return 0

def get_user_schools():
    """현재 사용자의 관심 학교 목록 반환"""
    try:
        user = get_current_user()
        if not user:
            return []
        
        supabase = get_supabase_client()
        response = supabase.table("user_schools").select("""
            id,
            schools (
                id,
                name
            )
        """).eq("user_id", user["id"]).execute()
        
        if response.data:
            # schools 정보를 평면화
            schools = []
            for item in response.data:
                if item.get('schools'):
                    school_info = item['schools']
                    school_info['user_school_id'] = item['id']  # user_schools 테이블의 ID 추가
                    schools.append(school_info)
            return schools
        
        return []
    except Exception as e:
        st.error(f"관심 학교 목록을 가져오는 중 오류가 발생했습니다: {str(e)}")
        return []

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
                    <a href="?" target="_self" class="logo-text" style="text-decoration: none; color: inherit; cursor: pointer;">캠퍼스링크</a>
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
    
    
    
    
    
        
    
def render_no_schools_screen():
    """관심 학교가 없을 때의 화면"""
    
    st.markdown("""
    <style>
    /* 배너를 담고 있는 stMarkdown 컨테이너를 전체 너비로 */
    .element-container:has(.custom-banner) {
        width: 100vw !important;
        max-width: 100vw !important;
        margin-left: calc(-50vw + 50%) !important;
        margin-right: calc(-50vw + 50%) !important;
        padding: 0 !important;
    }
    
    /* 배너 HTML 스타일 - 좌우 꽉 차게 */
    .custom-banner {
        width: 100% !important;
        max-width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 0;
        overflow: hidden;
    }
    
    .custom-banner img {
        width: 100% !important;
        max-width: 100% !important;
        height: auto;
        display: block;
        border-radius: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
        vertical-align: bottom;
        object-fit: cover !important;
    }
    
    /* Streamlit 기본 이미지 스타일 덮어쓰기 */
    .st-emotion-cache-3uj0rx img,
    [data-testid="stMarkdown"] img {
        object-fit: cover !important;
    }
    
    /* 스마트폰 사이즈 (768px 이하) */
    @media (max-width: 768px) {
        .custom-banner {
            height: 200px !important;
            overflow: hidden !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
        }
        
        .custom-banner img {
            width: auto !important;
            height: 100% !important;
            max-width: none !important;
            min-width: 100% !important;
            object-fit: cover !important;
            object-position: center !important;
            position: relative !important;
            left: 50% !important;
            transform: translateX(-50%) !important;
        }
    }
    
    .no-schools-container {
        background-color: #f9f8f8;
        border: 2px dashed #cfcece;
        border-radius: 45px;
        padding: 80px 40px;
        margin: 50px auto 60px auto;
        max-width: 709px;
        min-height: 200px;
        text-align: center;
        position: relative;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        cursor: pointer;
        transition: all 0.3s ease;
        margin-top: 6rem;
        margin-bottom: 100px;
    }
    
    .no-schools-container:hover {
        background-color: #e0e0e0;
        border-color: #666;
    }
    
    .no-schools-title {
        font-size: 19px;
        color: black;
        margin-bottom: 20px;
        font-weight: 400;
    }
    
    .plus-icon {
        width: 60px;
        height: 60px;
        background-color: black;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
        transition: transform 0.2s ease;
    }
    
    .no-schools-container:hover .plus-icon {
        transform: scale(1.1);
    }
    
    .plus-icon svg {
        width: 30px;
        height: 30px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 헤더 여백 추가 (헤더 높이만큼)
    st.markdown("""
    <div style="height: 80px;"></div>
    """, unsafe_allow_html=True)
    
    # 메인 배너 영역 (pupu.png 이미지)
    import base64
    try:
        with open("assets/pupu.png", "rb") as f:
            banner_base64 = base64.b64encode(f.read()).decode()
        
        st.markdown(f"""
        <div class="custom-banner">
            <img src="data:image/png;base64,{banner_base64}" alt="배너" />
        </div>
        """, unsafe_allow_html=True)
    except:
        st.markdown("""
        <div class="custom-banner" style="background: #e3e3e3; height: 200px;">
        </div>
        """, unsafe_allow_html=True)
    
    # 학교가 있을 때와 동일한 구조를 위한 4개의 빈 블록 추가 (헤더 여백 생성)
    st.markdown("""
    <div class="stVerticalBlock st-emotion-cache-tn0cau e196pkbe2" data-testid="stVerticalBlock" style="height: 0; overflow: hidden;"></div>
    <div class="stVerticalBlock st-emotion-cache-tn0cau e196pkbe2" data-testid="stVerticalBlock" style="height: 0; overflow: hidden;"></div>
    <div class="stVerticalBlock st-emotion-cache-tn0cau e196pkbe2" data-testid="stVerticalBlock" style="height: 0; overflow: hidden;"></div>
    <div class="stVerticalBlock st-emotion-cache-tn0cau e196pkbe2" data-testid="stVerticalBlock" style="height: 0; overflow: hidden;"></div>
    """, unsafe_allow_html=True)
    
    # 클릭 가능한 박스 (쿼리 파라미터 방식)
    st.markdown("""
    <a href="?add_school=true" target="_self" style="text-decoration: none; color: inherit;">
        <div class="no-schools-container">
        <div class="no-schools-title">관심 학교를 추가해 주세요.</div>
        <div class="plus-icon">
            <svg width="30" height="30" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 5V19M5 12H19" stroke="white" stroke-width="2" stroke-linecap="round"/>
            </svg>
        </div>
    </div>
    </a>
    """, unsafe_allow_html=True)
    
    
        
def get_posts_for_school(school_id, category="전체", offset=0, limit=15):
    """학교별 게시글 목록 가져오기 (댓글 개수 포함)"""
    try:
        supabase = get_supabase_client()
        
        # 기본 쿼리 (users 테이블과 조인하여 작성자 정보 가져오기)
        query = supabase.table("posts").select("""
            id,
            title,
            content,
            created_at,
            user_id,
            school_id,
            view_count,
            users (
                nickname
            )
        """).eq("school_id", school_id).order("created_at", desc=True)
        
        # 페이지네이션
        query = query.range(offset, offset + limit - 1)
        
        response = query.execute()
        posts = response.data if response.data else []
        
        # 각 게시글의 댓글 개수 가져오기
        for post in posts:
            try:
                comments_response = supabase.table("comments").select("id", count="exact").eq("post_id", post['id']).execute()
                post['comment_count'] = comments_response.count if comments_response.count else 0
            except:
                post['comment_count'] = 0
        
        return posts
    except Exception as e:
        st.error(f"게시글을 불러오는 중 오류가 발생했습니다: {str(e)}")
        return []

def save_tab_state(user_id, school_id, category, posts_count):
    """탭 상태 저장 (세션 스토리지 사용)"""
    # user_preferences 테이블이 없으므로 세션 스토리지 사용
    if 'tab_states' not in st.session_state:
        st.session_state.tab_states = {}
    
    st.session_state.tab_states[f"{user_id}_{school_id}"] = {
        "category": category,
        "posts_count": posts_count
    }

def get_tab_state(user_id, school_id):
    """탭 상태 가져오기 (세션 스토리지 사용)"""
    if 'tab_states' not in st.session_state:
        return "전체", 0
    
    key = f"{user_id}_{school_id}"
    if key in st.session_state.tab_states:
        state = st.session_state.tab_states[key]
        return state["category"], state["posts_count"]
    
    return "전체", 0

def save_last_selected_tab(user_id, school_id):
    """마지막 선택한 탭 저장 (세션 스토리지 사용)"""
    if 'last_selected_tab' not in st.session_state:
        st.session_state.last_selected_tab = {}
    
    st.session_state.last_selected_tab[user_id] = school_id

def get_last_selected_tab(user_id):
    """마지막 선택한 탭 가져오기 (세션 스토리지 사용)"""
    if 'last_selected_tab' not in st.session_state:
        return None
    
    return st.session_state.last_selected_tab.get(user_id)
        
def render_with_schools_screen():
    """관심 학교가 있을 때의 화면"""
    # 스타일 추가
    st.markdown("""
    <style>
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
    .stAppViewContainer {
        gap: 0 !important;
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
    
    /* 배너와 탭 사이의 밑줄 제거 및 간격 추가 */
    .stTabs {
        border-top: none !important;
        margin-top: 2rem !important;
        padding-top: 0 !important;
    }
    
    [data-testid="stTabs"] {
        border-top: none !important;
        margin-top: 2rem !important;
        padding-top: 0 !important;
    }
    
    /* 탭 버튼 컨테이너의 상단 테두리 제거 및 폰트 크기 증가 */
    .stTabs [data-baseweb="tab-list"] {
        border-top: none !important;
        margin-top: 0 !important;
        padding-top: 0 !important;
        gap: 1rem !important;  /* 탭 간격 1rem */
    }
    
    /* 탭 버튼 간격 추가 */
    .stTabs [data-baseweb="tab"] {
        margin-right: 1rem !important;
    }
    
    .stTabs [data-baseweb="tab"]:last-child {
        margin-right: 0 !important;
    }
    
    /* 탭 버튼 텍스트 크기 증가 - 모든 가능한 선택자 */
    .stTabs [data-baseweb="tab-list"] button,
    .stTabs [data-baseweb="tab"],
    .stTabs button,
    [data-testid="stTabs"] button,
    [data-baseweb="tab-list"] button,
    [data-baseweb="tab"],
    button[role="tab"],
    .stTabs [role="tab"] {
        font-size: 16px !important;
    }
    
    /* 탭 내부 텍스트도 강제로 크기 조정 */
    .stTabs [data-baseweb="tab-list"] button > div,
    .stTabs [data-baseweb="tab"] > div,
    button[role="tab"] > div {
        font-size: 16px !important;
    }
    
    /* 플로팅 글쓰기 버튼 */
    .floating-write-button {
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 60px;
        height: 60px;
        background-color: #2c2c2c;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        z-index: 1000;
        transition: all 0.3s ease;
        text-decoration: none;
    }
    
    .floating-write-button:hover {
        background-color: #3c3c3c;
        transform: scale(1.1);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
    }
    
    .floating-write-button svg {
        width: 24px;
        height: 24px;
        color: white;
    }
    
    /* 게시글 스타일 */
    .post-item {
        background-color: white;
        padding: 1.5rem 0;
        cursor: pointer;
        transition: all 0.2s ease;
        border-bottom: 1px solid #e3e3e3;  /* 밑줄 추가 */
    }
    
    .post-item:last-child {
        border-bottom: none;  /* 마지막 게시글은 밑줄 없음 */
    }
    
    .post-item:hover {
        background-color: #f8f9fa;
    }
    
    /* Streamlit 기본 구조 사용 시 */
    [data-testid="stVerticalBlock"] > div {
        border-bottom: 1px solid #e3e3e3;
        padding: 1rem 0;
    }
    
    /* 첫 번째와 마지막 게시글의 선 제거 */
    [data-testid="stVerticalBlock"] > div:first-child {
        border-top: none;
        padding-top: 0;
    }
    
    [data-testid="stVerticalBlock"] > div:last-child {
        border-bottom: none;
        padding-bottom: 0;
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
    
    /* 배너를 담고 있는 stMarkdown 컨테이너를 전체 너비로 */
    .element-container:has(.custom-banner) {
        width: 100vw !important;
        max-width: 100vw !important;
        margin-left: calc(-50vw + 50%) !important;
        margin-right: calc(-50vw + 50%) !important;
        padding: 0 !important;
    }
    
    /* 배너 HTML 스타일 - 좌우 꽉 차게 */
    .custom-banner {
        width: 100% !important;
        max-width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 0;
        overflow: hidden;
    }
    
    .custom-banner img {
        width: 100% !important;
        max-width: 100% !important;
        height: auto;
        display: block;
        border-radius: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
        vertical-align: bottom;
        object-fit: cover !important;  /* scale-down 대신 cover 사용 */
    }
    
    /* Streamlit 기본 이미지 스타일 덮어쓰기 */
    .st-emotion-cache-3uj0rx img,
    [data-testid="stMarkdown"] img {
        object-fit: cover !important;  /* scale-down 끄기 */
    }
    
    /* 스마트폰 사이즈 (768px 이하) */
    @media (max-width: 768px) {
        .custom-banner {
            height: 200px !important;  /* 고정 높이 */
            overflow: hidden !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
        }
        
        .custom-banner img {
            width: auto !important;  /* 높이 기준으로 자동 조절 */
            height: 100% !important;  /* 높이 100% */
            max-width: none !important;
            min-width: 100% !important;  /* 최소한 가로 100% */
            object-fit: cover !important;
            object-position: center !important;  /* 중앙 정렬 */
            position: relative !important;
            left: 50% !important;
            transform: translateX(-50%) !important;
        }
    }
    
    </style>
    """, unsafe_allow_html=True)
    
    # 배너 이미지를 base64로 인코딩하여 삽입
    import base64
    try:
        with open("assets/pupu.png", "rb") as f:
            banner_base64 = base64.b64encode(f.read()).decode()
        
        st.markdown(f"""
        <div class="custom-banner">
            <img src="data:image/png;base64,{banner_base64}" alt="배너" />
        </div>
        """, unsafe_allow_html=True)
    except:
        st.markdown("""
        <div class="custom-banner" style="background: #e3e3e3; height: 200px;">
    </div>
    """, unsafe_allow_html=True)
    
    # 사용자의 관심 학교 목록 가져오기
    schools = get_user_schools()
    
    if not schools:
        st.info("관심 학교를 불러오는 중 오류가 발생했습니다.")
        return
    
    # 현재 사용자 정보
    user = get_current_user()
    if not user:
        return
    
    # 마지막 선택한 탭 가져오기
    last_selected_school_id = get_last_selected_tab(user["id"])
    
    # 쿼리 파라미터로 선택된 학교 확인
    query_params = st.query_params
    selected_school_id = query_params.get("school_id")
    
    # 기본 선택 학교 설정
    if not selected_school_id and last_selected_school_id:
        selected_school_id = last_selected_school_id
    
    if not selected_school_id:
        selected_school_id = schools[0]['id'] if schools else None
    
    # 학교 탭을 Streamlit 네이티브로 생성
    school_names = [school['name'] for school in schools]
    tabs = st.tabs(school_names)
        
    # 선택된 탭 인덱스 찾기
    selected_tab_index = 0
    for idx, school in enumerate(schools):
        if school['id'] == selected_school_id:
            selected_tab_index = idx
            break
    
    # 각 탭 렌더링
    for idx, tab in enumerate(tabs):
        with tab:
            school = schools[idx]
            
            # 탭 상태 복원
            saved_category, saved_posts_count = get_tab_state(user["id"], school['id'])
            
            # 게시글 목록 표시
            posts = get_posts_for_school(school['id'], "전체", 0, max(saved_posts_count, 15))
            
            if posts:
                for post in posts:
                    # 게시 시간 포맷팅 (새로운 규칙 적용)
                    time_str = format_time_ago(post['created_at'])
                    
                    # 실제 작성자 닉네임 가져오기
                    author_nickname = post.get('users', {}).get('nickname', '익명') if post.get('users') else '익명'
                    
                    # 댓글 개수와 조회수 가져오기
                    comment_count = post.get('comment_count', 0)
                    view_count = post.get('view_count', 0)
                    
                    # 게시글을 클릭 가능한 링크로 만들기 (쿼리 파라미터 방식)
                    st.markdown(f"""
                    <a href="?page=view_post&id={post['id']}" target="_self" style="text-decoration: none; color: inherit;">
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
                            <div class="post-title">{post['title']}</div>
                            <div class="post-content">{post['content']}</div>
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
                                    <span>조회수 {view_count}</span>
                                </div>
                            </div>
                        </div>
                    </a>
                    """, unsafe_allow_html=True)
            else:
                st.info("아직 게시글이 없습니다.")
            
            # 탭 상태 저장
            save_tab_state(user["id"], school['id'], "전체", len(posts) if posts else 0)
            
            # 현재 탭이 렌더링되면 활성 탭으로 간주하여 세션에 저장
            st.session_state.current_active_school_id = school['id']
    
    # 각 탭에 글쓰기 버튼 추가하는 방식으로 변경
    # 현재 활성 탭을 감지하기 위해 각 탭마다 버튼 생성
    
    # 플로팅 글쓰기 버튼
    st.markdown("""
    <a href="?action=write_post" target="_self" class="floating-write-button" style="text-decoration: none;">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 5V19M5 12H19" stroke="white" stroke-width="2" stroke-linecap="round"/>
        </svg>
    </a>
    """, unsafe_allow_html=True)

def main():
    """홈 페이지 메인 함수"""
    
    # 로그인 확인 (미로그인 시 자동 리다이렉트)
    require_login()
    
    # 쿼리 파라미터 확인
    query_params = st.query_params
    
    # 게시글 상세 페이지로 이동 감지
    if "page" in query_params and query_params["page"] == "view_post":
        post_id = query_params.get("id")
        if post_id:
            st.session_state.current_post_id = post_id
            st.switch_page("pages/6_view_post.py")
    
    # 글쓰기 페이지로 이동 감지
    if "action" in query_params and query_params["action"] == "write_post":
        # 현재 활성 탭의 학교를 세션에 저장
        user = get_current_user()
        if user:
            # last_selected_tab에서 현재 활성 탭 확인 (가장 신뢰할 수 있는 방법)
            current_active_school_id = None
            if "last_selected_tab" in st.session_state and user["id"] in st.session_state.last_selected_tab:
                current_active_school_id = st.session_state.last_selected_tab[user["id"]]
            
            # 폴백: 현재 화면에 보여지는 학교들에서 첫 번째
            if not current_active_school_id:
                schools = get_user_schools()
                if schools:
                    current_active_school_id = schools[0]['id']
            
            # 현재 활성 탭의 학교 ID를 글쓰기용 세션에 저장
            st.session_state.current_school_id = current_active_school_id
            # 글쓰기 페이지의 선택 상태 초기화 (새로 전달된 학교로 설정되도록)
            if "selected_school_idx" in st.session_state:
                del st.session_state.selected_school_idx
            if "write_page_initialized" in st.session_state:
                del st.session_state.write_page_initialized
            # 학교 목록 캐시 갱신
            st.session_state.cached_schools = schools
        st.switch_page("pages/7_write_post.py")
    
    # 쿼리 파라미터 확인 (학교 추가 버튼 클릭 감지)
    query_params = st.query_params
    if "add_school" in query_params:
        # 학교 추가 페이지로 이동
        st.switch_page("pages/4_add_school.py")
    
    # 관심 학교 개수 확인
    schools_count = get_user_schools_count()
    
    # 헤더 렌더링 (학교 추가 여부 전달)
    render_header(has_schools=(schools_count > 0))
    
    # 관심 학교 상태에 따른 화면 렌더링
    if schools_count == 0:
        render_no_schools_screen()
    else:
        render_with_schools_screen()

if __name__ == "__main__":
    main()
