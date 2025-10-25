"""
학교 추가/검색 페이지
Figma 디자인: https://www.figma.com/design/HHDev1QHqPB31yP9lENPD9/%EC%BA%A0%ED%8D%BC%EC%8A%A4%EB%A7%81%ED%81%AC-%ED%99%94%EB%A9%B4-%EC%84%A4%EA%B3%84%EC%84%9C?node-id=4-425&m=dev
"""

import streamlit as st
from config.settings import PAGE_CONFIG
from utils.styles import hide_sidebar
from utils.auth import require_login, get_current_user, logout, logout_user
from utils.supabase_client import get_supabase_client
from utils.dialogs import show_warning

# 페이지 설정 - centered로 변경 (홈 화면과 동일)
st.set_page_config(
    page_title="캠퍼스링크",
    page_icon="🏫",
    layout="centered"
)

# 사이드바 숨김
hide_sidebar()


def render_header(has_schools=False):
    """헤더 렌더링 - 홈 화면과 동일"""
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
            st.stop()
        elif action == "home":
            st.query_params.clear()
            st.switch_page("pages/3_home.py")
        elif action == "schools":
            st.query_params.clear()
            # 이미 학교 검색 페이지에 있으므로 새로고침
            st.rerun()
        elif action == "mypage":
            st.query_params.clear()
            st.switch_page("pages/8_mypage.py")
    
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


def search_schools(keyword: str) -> list:
    """학교 검색"""
    if not keyword:
        return []
    try:
        client = get_supabase_client()
        response = (
            client.table("schools")
            .select("*")  # 모든 컬럼 선택 (id, name 등)
            .ilike("name", f"%{keyword.strip()}%")
            .limit(20)
            .execute()
        )
        
        return response.data or []
    except Exception as e:
        st.error(f"❌ 검색 중 오류 발생: {str(e)}")
        return []


def get_user_schools() -> list:
    """사용자의 관심 학교 목록 가져오기"""
    try:
        user = get_current_user()
        if not user:
            return []
        
        client = get_supabase_client()
        response = client.table("user_schools").select("""
            id,
            school_id,
            schools (
                id,
                name
            )
        """).eq("user_id", user["id"]).execute()
        
        if response.data:
            # 데이터 평면화
            schools = []
            for item in response.data:
                if item.get('schools'):
                    school_info = item['schools']
                    school_info['user_school_id'] = item['id']  # user_schools 테이블의 ID
                    schools.append(school_info)
            return schools
        
        return []
    except Exception:
        return []


def add_school_to_user(school_id: int) -> tuple[bool, str]:
    """사용자의 관심 학교에 추가
    
    Returns:
        tuple[bool, str]: (성공 여부, 메시지)
    """
    try:
        user = get_current_user()
        if not user:
            return False, "사용자 정보를 찾을 수 없습니다."
        
        client = get_supabase_client()
        
        # 현재 추가된 학교 개수 확인
        count_result = client.table("user_schools").select("id", count="exact").eq("user_id", user["id"]).execute()
        current_count = count_result.count if count_result.count else 0
        
        if current_count >= 5:
            return False, "최대 5개까지만 추가할 수 있습니다."
        
        # 이미 추가된 학교인지 확인
        existing = client.table("user_schools").select("id").eq("user_id", user["id"]).eq("school_id", school_id).execute()
        
        if existing.data and len(existing.data) > 0:
            return False, "이미 추가된 학교입니다."
        
        # 관심 학교에 추가
        client.table("user_schools").insert({
            "user_id": user["id"],
            "school_id": school_id
        }).execute()
        
        return True, "학교가 추가되었습니다."
    except Exception as e:
        return False, f"오류가 발생했습니다: {str(e)}"


def remove_school_from_user(user_school_id: int) -> bool:
    """사용자의 관심 학교에서 삭제"""
    try:
        client = get_supabase_client()
        client.table("user_schools").delete().eq("id", user_school_id).execute()
        return True
    except Exception:
        return False


def main() -> None:
    require_login()
    
    # 헤더 렌더링
    render_header(has_schools=True)
    
    # 본문 스타일 (Figma 디자인 참고)
    st.markdown("""
    <style>
    /* 본문 컨테이너 상단 여백 (헤더 높이만큼) */
    .content-wrapper {
        margin-top: 70px;
        padding: 20px 0;
    }
    
    /* 학교 검색 카드 - 테두리 제거 */
    .school-search-card {
        background: white;
        border: none;
        border-radius: 0;
        padding: 24px;
        margin-bottom: 16px;
    }
    
    .search-card-title {
        font-size: 20px;
        font-weight: 700;
        color: #111;
        margin-bottom: 1rem;
    }
    
    /* 검색 결과 아이템 */
    .school-result-item {
        padding: 16px 12px;
        border-bottom: 1px solid #f0f0f0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .school-result-item:last-child {
        border-bottom: none;
    }
    
    .school-name {
        font-size: 16px;
        font-weight: 600;
        color: #111;
        margin-bottom: 4px;
    }
    
    .school-location {
        font-size: 13px;
        color: #777;
    }
    
    /* 안내 텍스트 */
    .search-hint {
        font-size: 14px;
        color: #999;
        text-align: center;
        padding: 40px 20px;
    }
    
    
    /* 검색 버튼 검정색으로 변경 */
    .stButton > button[kind="primary"] {
        background-color: #000000 !important;
        color: white !important;
        border: none !important;
        height: 38px !important;
        padding: 0 12px !important;
        font-size: 14px !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background-color: #333333 !important;
    }
    
    /* 추가/삭제 버튼도 동일한 크기로 */
    .stButton > button[kind="secondary"],
    .stButton > button:not([kind="primary"]) {
        height: 38px !important;
        padding: 0 12px !important;
        font-size: 0.8rem !important;
    }
    
    /* Streamlit 버튼 내부 텍스트 크기 조정 */
    .st-emotion-cache-12j140x {
        font-size: 0.8rem !important;
    }
    
    /* 모든 버튼 텍스트 컨테이너 */
    .stButton p {
        font-size: 0.8rem !important;
    }
    
    /* 특정 emotion 캐시 클래스 수정 */
    .st-emotion-cache-wfksaw {
        justify-content: center !important;
        align-items: center !important;
        display: flex !important;
    }
    
    .st-emotion-cache-kt9vas {
        flex: 0 !important;
    }
    
    /* 버튼 오른쪽 정렬 - 모든 경우에 적용 */
    [data-testid="column"] > div:has(.stButton) {
        display: flex !important;
        justify-content: flex-end !important;
        align-items: center !important;
    }
    
    [data-testid="column"] .stButton {
        display: flex !important;
        justify-content: flex-end !important;
        margin-left: auto !important;
    }
    
    /* emotion 캐시 클래스들도 모두 처리 */
    [data-testid="column"] [class*="emotion-cache"] > .stButton,
    [data-testid="column"] div[class*="st-emotion"] > .stButton {
        margin-left: auto !important;
    }
    
    /* 버튼 컨테이너 자체 */
    .stButton {
        text-align: right !important;
    }
    
    /* 버튼이 줄어들지 않도록 */
    .stButton button {
        flex-shrink: 0 !important;
        min-width: fit-content !important;
        white-space: nowrap !important;
    }
    
    
    /* 입력 필드 외부 컨테이너 */
    .stTextInput > div {
        position: relative !important;
        background: transparent !important;
        z-index: 1 !important;
    }
    
    /* data-baseweb="input" 컨테이너 */
    .stTextInput div[data-baseweb="input"] {
        background: transparent !important;
        padding: 0 !important;
        position: relative !important;
        z-index: 2 !important;
        overflow: visible !important;
        border: none !important;
        box-shadow: none !important;
    }
    
    /* data-baseweb="base-input" 컨테이너 */
    .stTextInput div[data-baseweb="base-input"] {
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
        font-size: 14px !important;
        padding: 0 16px !important;
        box-sizing: border-box !important;
        background-color: white !important;
        width: 100% !important;
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
    .stTextInput [data-testid="InputInstructions"],
    [data-testid="InputInstructions"] {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        position: absolute !important;
    }
    
    /* 스마트폰 해상도에서 삭제/추가 버튼 너비 조정 */
    @media (max-width: 768px) {
        .stButton > button {
            width: 100% !important;
            min-width: 80px !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 본문 컨텐츠
    st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)
    
    # 나의 관심 학교 섹션
    st.markdown('<div class="school-search-card">', unsafe_allow_html=True)
    st.markdown('<div style="font-size: 20px; font-weight: 700; color: #111; margin-bottom: 3rem;">나의 관심 학교</div>', unsafe_allow_html=True)
    
    # 관심 학교 목록 가져오기
    my_schools = get_user_schools()
    
    if my_schools:
        for i, school in enumerate(my_schools):
            cols = st.columns([4, 1])
            
            with cols[0]:
                st.write(school.get("name", ""))
            
            with cols[1]:
                if st.button("삭제", key=f"remove_{school.get('user_school_id')}", type="secondary", use_container_width=True):
                    remove_school_from_user(school.get('user_school_id'))
                    st.rerun()
            
            # 항목 간 여백
            st.markdown('<div style="margin-bottom: 2rem;"></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="search-hint">아직 추가한 학교가 없습니다.</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # school-search-card
    
    # 학교 검색 카드
    st.markdown('<div class="school-search-card">', unsafe_allow_html=True)
    st.markdown('<div style="border-top: 1px solid #e0e0e0; padding-top: 2rem; margin-bottom: 2rem;"></div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size: 20px; font-weight: 700; color: #111; margin-bottom: 4rem;">학교 검색</div>', unsafe_allow_html=True)
    
    # 검색 입력 및 버튼
    col1, col2 = st.columns([5, 1])
    with col1:
        keyword = st.text_input(
            "학교명 입력",
            placeholder="학교명을 입력하세요 (예: 서울대학교)",
            label_visibility="collapsed",
            key="school_search_input"
        )
    with col2:
        search_clicked = st.button("검색", use_container_width=True, type="primary")
    
    # 검색 실행
    results = []
    if search_clicked:
        if keyword.strip():
            results = search_schools(keyword)
            st.session_state.last_search_keyword = keyword
            st.session_state.search_results = results
        else:
            st.warning("검색어를 입력해주세요.")
    
    # 이전 검색 결과 표시
    if "search_results" in st.session_state and not search_clicked:
        results = st.session_state.search_results
    
    # 이미 추가된 학교 ID 목록
    my_school_ids = [school.get('id') for school in my_schools]
    
    # 검색 결과에서 이미 추가된 학교 제외
    filtered_results = [school for school in results if school.get('id') not in my_school_ids]
    
    # 검색 결과 표시
    if filtered_results:
        st.markdown('<div style="margin-top: 3rem;"></div>', unsafe_allow_html=True)
        for idx, school in enumerate(filtered_results):
            cols = st.columns([4, 1])
            
            with cols[0]:
                st.write(school.get("name", ""))
            
            with cols[1]:
                if st.button("추가", key=f"add_{school.get('id')}", use_container_width=True):
                    success, message = add_school_to_user(school.get('id'))
                    if success:
                        st.rerun()
                    else:
                        show_warning(message)
            
            # 항목 간 여백
            st.markdown('<div style="margin-bottom: 2rem;"></div>', unsafe_allow_html=True)
    
    elif results and len(filtered_results) == 0:
        st.markdown('<div class="search-hint">검색된 학교가 모두 이미 추가되어 있습니다.</div>', unsafe_allow_html=True)
    
    elif "search_results" in st.session_state and len(st.session_state.search_results) == 0 and search_clicked:
        st.markdown('<div class="search-hint">검색 결과가 없습니다.</div>', unsafe_allow_html=True)
    
    else:
        st.markdown('<div class="search-hint">학교명을 입력하고 검색 버튼을 눌러주세요.</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # school-search-card
    
    st.markdown('</div>', unsafe_allow_html=True)  # content-wrapper


if __name__ == "__main__":
    main()


