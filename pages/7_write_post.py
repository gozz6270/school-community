"""
글쓰기 페이지
"""

import streamlit as st
import streamlit.components.v1 as components
from config.settings import PAGE_CONFIG
from utils.auth import require_login, get_current_user
from utils.styles import hide_sidebar
from utils.supabase_client import get_supabase_client
from utils.dialogs import show_success, show_error

# 페이지 설정
st.set_page_config(
    page_title="글쓰기 - 캠퍼스링크",
    page_icon="✍️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 사이드바 숨김
hide_sidebar()

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
            return [{"id": item["schools"]["id"], "name": item["schools"]["name"]} for item in response.data]
        return []
    except Exception as e:
        st.error(f"관심 학교 정보를 가져오는 중 오류가 발생했습니다: {str(e)}")
        return []

def main():
    """글쓰기 페이지 메인 함수"""
    
    # 로그인 확인 (미로그인 시 자동 리다이렉트)
    require_login()
    
    # 스타일 적용 (회원가입/홈 화면 스타일 참고)
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
        
        /* 상단 패딩 */
        .stMainBlockContainer,
        [data-testid="stMainBlockContainer"],
        .block-container {
            padding-top: 3rem !important;
            padding-bottom: 3rem !important;
        }
        
        /* Vertical Block 간격 제거 */
        .stVerticalBlock,
        [data-testid="stVerticalBlock"] {
            gap: 0 !important;
        }
        
        /* Element Container 기본 간격 제거 */
        .stElementContainer,
        [data-testid="stElementContainer"] {
            margin-bottom: 0 !important;
            padding-bottom: 0 !important;
        }
        
        /* 특정 요소들에 상단 마진 추가 */
        .stRadio {
            margin-top: 5px !important;
        }
        
        .stTextInput {
            margin-top: 10px !important;
        }
        
        .stTextArea {
            margin-top: 10px !important;
        }
        
        .stButton {
            margin-top: 30px !important;
        }
        
        /* 제목 링크 아이콘 숨김 */
        h1 a {
            display: none !important;
        }
        
        /* 라디오 버튼 컨테이너 (한 줄에 최대 5개) */
        .school-radio-container {
            margin-top: 1rem;
            margin-bottom: 20px;
        }
        
        .school-radio-container .stRadio {
            margin-bottom: 0;
        }
        
        .school-radio-container .stRadio > div {
            gap: 0 !important;
        }
        
        /* Streamlit의 라벨 숨김 */
        .school-radio-container .stRadio > label[data-testid="stWidgetLabel"] {
            display: none !important;
        }
        
        /* 라디오 버튼 그룹 - flex-wrap으로 5개씩 줄바꿈 */
        .school-radio-container .stRadio div[role="radiogroup"] {
            display: flex !important;
            flex-wrap: wrap !important;
            gap: 10px 20px !important;
            align-items: flex-start !important;
        }
        
        /* 각 라디오 버튼 아이템 - 5개씩 배치 (20% - gap 고려) */
        .school-radio-container .stRadio div[role="radiogroup"] > label {
            flex: 0 0 calc(20% - 16px) !important;
            max-width: calc(20% - 16px) !important;
            min-width: 100px !important;
            padding: 8px 12px !important;
            cursor: pointer !important;
            font-size: 16px !important;
            font-weight: 400 !important;
            color: #333 !important;
            display: flex !important;
            align-items: center !important;
            gap: 8px !important;
            pointer-events: auto !important;
        }
        
        .school-radio-container .stRadio div[role="radiogroup"] > label:hover {
            background-color: #f5f5f5 !important;
            border-radius: 4px !important;
        }
        
        /* 라디오 버튼 기본 동작 유지 */
        .school-radio-container .stRadio div[role="radiogroup"] > label {
            pointer-events: auto !important;
        }
        
        .school-radio-container .stRadio div[role="radiogroup"] > label input[type="radio"] {
            pointer-events: auto !important;
        }
        
        /* 라디오 버튼 원형 아이콘 스타일 */
        .school-radio-container .stRadio div[role="radiogroup"] > label > div:first-child {
            display: flex !important;
            flex-shrink: 0 !important;
        }
        
        /* 선택된 라디오 버튼 */
        .school-radio-container .stRadio div[role="radiogroup"] > label[data-checked="true"] {
            color: #2c2c2c !important;
            font-weight: 600 !important;
        }
        
        /* 글자 수 표시 컨테이너 */
        .input-with-counter {
            position: relative;
            margin-top: 1rem;
            margin-bottom: 20px;
        }
        
        .textarea-with-counter {
            position: relative;
            margin-top: 1rem;
            margin-bottom: 20px;
        }
        
        /* 글자 수 표시 스타일 */
        .char-counter {
            font-size: 16px;
            color: #000000;
            font-weight: 400;
            text-align: right;
            margin-top: 5px;
            pointer-events: none;
        }
        
        /* 제목 글자 수 */
        .input-with-counter .title-counter {
            margin-top: 5px;
        }
        
        /* 내용 글자 수 */
        .textarea-with-counter .content-counter {
            margin-top: 5px;
        }
        
        /* 입력 필드 외부 컨테이너 */
        .stTextInput > div {
            position: relative !important;
            background: transparent !important;
            z-index: 1 !important;
        }
        
        /* data-baseweb="input" 컨테이너 */
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
        
        /* data-baseweb="base-input" 컨테이너 */
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
        
        /* 제목 입력 필드 */
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
        
        /* Press Enter to apply 메시지 숨김 */
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
        
        /* 라벨 스타일 (collapsed 상태에서 완전히 숨김) */
        .stTextInput > label {
            display: none !important;
        }
        
        /* 본문 입력 필드 외부 컨테이너 */
        .stTextArea > div {
            position: relative !important;
            background: transparent !important;
        }
        
        /* data-baseweb="textarea" 컨테이너 */
        .stTextArea div[data-baseweb="textarea"] {
            background: transparent !important;
            padding: 0 !important;
            border: none !important;
            box-shadow: none !important;
        }
        
        /* data-baseweb="base-input" 컨테이너 */
        .stTextArea div[data-baseweb="base-input"] {
            background: transparent !important;
            padding: 0 !important;
            border: none !important;
            box-shadow: none !important;
        }
        
        /* 본문 입력 필드 */
        .stTextArea textarea {
            border: 1px solid #aaa9a9 !important;
            border-radius: 8px !important;
            font-size: 16px !important;
            padding: 16px !important;
            resize: none !important;
            background-color: white !important;
            box-sizing: border-box !important;
            width: 100% !important;
        }
        
        /* 텍스트 영역 모든 상태에서 테두리 유지 */
        .stTextArea textarea:focus,
        .stTextArea textarea:active,
        .stTextArea textarea:focus-visible,
        .stTextArea textarea:focus-within {
            border: 1px solid #aaa9a9 !important;
            border-color: #aaa9a9 !important;
            outline: none !important;
            outline-width: 0 !important;
            outline-style: none !important;
            box-shadow: none !important;
        }
        
        /* Streamlit 기본 포커스 스타일 완전 제거 */
        .stTextArea div[data-baseweb="textarea"]:focus-within,
        .stTextArea div[data-baseweb="textarea"]:focus,
        .stTextArea div[data-baseweb="textarea"]:active,
        .stTextArea div[data-baseweb="base-input"]:focus-within,
        .stTextArea div[data-baseweb="base-input"]:focus,
        .stTextArea div[data-baseweb="base-input"]:active {
            border: none !important;
            border-color: transparent !important;
            box-shadow: none !important;
            outline: none !important;
        }
        
        /* Press Enter to apply 메시지 숨김 (textarea) */
        .stTextArea [data-testid="InputInstructions"] {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            height: 0 !important;
            width: 0 !important;
            position: absolute !important;
        }
        
        .stTextArea div[data-testid="stMarkdownContainer"] {
            display: none !important;
            visibility: hidden !important;
        }
        
        /* 라벨 스타일 (collapsed 상태에서 완전히 숨김) */
        .stTextArea label {
            display: none !important;
        }
        
        /* 기본 버튼 스타일 - 검정색 (#2c2c2c) */
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
        
        /* 저장하기 버튼 특별 스타일 */
        .save-button-container {
            margin-top: 5px;
        }
        
        .save-button-container .stButton > button {
            width: 100% !important;
            cursor: pointer !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # 글쓰기 제목 (회원가입 스타일, 왼쪽 정렬)
    st.markdown("""
    <div style="margin-bottom: 0;">
        <h1 style="
            font-size: 34px;
            font-weight: 700;
            color: black;
            margin: 0;
            line-height: 1;
            text-align: left;
        ">글쓰기</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # 사용자의 관심 학교 목록 가져오기 (캐싱)
    if "cached_schools" not in st.session_state:
        st.session_state.cached_schools = get_user_schools()
    
    schools = st.session_state.cached_schools
    
    if not schools:
        st.warning("관심 학교를 먼저 추가해주세요.")
        if st.button("관심 학교 추가하기"):
            st.switch_page("pages/4_add_school.py")
        return
    
    # 현재 선택된 학교 결정 로직
    user = get_current_user()
    current_school_id = None
    default_index = 0
    
    # 1. 세션의 current_school_id 확인
    if "current_school_id" in st.session_state:
        current_school_id = st.session_state.current_school_id
    
    # 2. last_selected_tab에서 가져오기
    if not current_school_id and user and "last_selected_tab" in st.session_state:
        if user["id"] in st.session_state.last_selected_tab:
            current_school_id = st.session_state.last_selected_tab[user["id"]]
    
    # 3. 첫 번째 학교를 기본값으로
    if not current_school_id and schools:
        current_school_id = schools[0]['id']
    
    # 4. 해당 학교의 인덱스 찾기
    if current_school_id:
        for idx, school in enumerate(schools):
            if str(school['id']) == str(current_school_id):
                default_index = idx
                break
    
    
    
    # 대학교 선택 라벨
    st.markdown("""
    <p style="
        font-size: 17px;
        font-weight: 600;
        color: black;
        margin-top: 40px;
        margin-bottom: 5px;
    ">대학교 선택</p>
    """, unsafe_allow_html=True)
    
    # 라디오 버튼으로 학교 선택 (한 줄에 최대 5개)
    st.markdown('<div class="school-radio-container" style="margin-top: 1rem;">', unsafe_allow_html=True)
    
    school_names = [school['name'] for school in schools]
    
    # 홈에서 새로운 학교가 전달되었을 때만 업데이트 (한 번만 실행)
    if current_school_id and "write_page_initialized" not in st.session_state:
        for idx, school in enumerate(schools):
            if str(school['id']) == str(current_school_id):
                default_index = idx
                st.session_state.write_page_initialized = True
                break
    
    selected_school_idx = st.radio(
        "대학교 선택",
        range(len(schools)),
        format_func=lambda x: school_names[x],
        index=default_index,
        key="school_radio",
        label_visibility="collapsed",
        horizontal=True
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    selected_school = schools[selected_school_idx]
    
    
    # 선택된 학교를 별도 키에 저장 (홈에서 전달받은 current_school_id는 보존)
    st.session_state.working_school_id = selected_school['id']
    
    # 제목 라벨
    st.markdown("""
    <p style="
        font-size: 17px;
        font-weight: 600;
        color: black;
        margin-top: 20px;
        margin-bottom: 5px;
    ">제목</p>
    """, unsafe_allow_html=True)
    
    # 제목 입력 컨테이너 (글자 수 표시 포함)
    st.markdown('<div class="input-with-counter" style="margin-top: 1rem;">', unsafe_allow_html=True)
    
    # 제목 입력 (최대 40자)
    title = st.text_input(
        "제목",
        placeholder="제목을 입력하세요",
        max_chars=40,
        key="title_input",
        label_visibility="collapsed"
    )
    
    # 제목 글자 수 표시 (실시간 업데이트용 ID 추가)
    st.markdown(f'''
    <div id="title-counter" class="char-counter title-counter">{len(title)}/40</div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 내용 라벨
    st.markdown("""
    <p style="
        font-size: 17px;
        font-weight: 600;
        color: black;
        margin-top: 20px;
        margin-bottom: 5px;
    ">내용</p>
    """, unsafe_allow_html=True)
    
    # 본문 입력 컨테이너 (글자 수 표시 포함)
    st.markdown('<div class="textarea-with-counter" style="margin-top: 1rem;">', unsafe_allow_html=True)
    
    # 본문 입력 (최대 800자)
    content = st.text_area(
            "내용",
            placeholder="내용을 입력하세요",
        height=300,
        max_chars=800,
        key="content_input",
        label_visibility="collapsed"
    )
    
    # 내용 글자 수 표시 (실시간 업데이트용 ID 추가)
    st.markdown(f'''
    <div id="content-counter" class="char-counter content-counter">{len(content)}/800</div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 실시간 글자 수 업데이트 및 라디오 버튼 고정 JavaScript
    components.html("""
    <script>
    (function() {
        function updateCounters() {
            // 제목 입력 필드 실시간 카운터
            const titleInput = window.parent.document.querySelector('input[aria-label="제목"]');
            const titleCounter = window.parent.document.getElementById('title-counter');
            
            if (titleInput && titleCounter && !titleInput.hasAttribute('data-listener')) {
                titleInput.setAttribute('data-listener', 'true');
                titleInput.addEventListener('input', function() {
                    const length = this.value.length;
                    titleCounter.textContent = length + '/40';
                });
            }
            
            // 내용 입력 필드 실시간 카운터
            const contentTextarea = window.parent.document.querySelector('textarea[aria-label="내용"]');
            const contentCounter = window.parent.document.getElementById('content-counter');
            
            if (contentTextarea && contentCounter && !contentTextarea.hasAttribute('data-listener')) {
                contentTextarea.setAttribute('data-listener', 'true');
                contentTextarea.addEventListener('input', function() {
                    const length = this.value.length;
                    contentCounter.textContent = length + '/800';
                });
            }
        }
        
        // 라디오 버튼 문제 해결을 위해 JavaScript 개입 제거
        
        // 초기 실행
        updateCounters();
        
        // MutationObserver로 DOM 변경 감지
        const observer = new MutationObserver(function(mutations) {
            updateCounters();
        });
        
        observer.observe(window.parent.document.body, {
            childList: true,
            subtree: true
        });
        
        // 페이지 로드 후에도 재실행
        setTimeout(updateCounters, 500);
        setTimeout(updateCounters, 1000);
        setTimeout(updateCounters, 2000);
    })();
    </script>
    """, height=0)
    
    st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)
    
    # 저장하기 버튼 (전체 너비, 항상 활성화)
    st.markdown('<div class="save-button-container">', unsafe_allow_html=True)
    save_button = st.button("저장하기", use_container_width=True, key="save_button")
    st.markdown('</div>', unsafe_allow_html=True)

    # 저장 처리: 팝업 없이 즉시 저장
    if save_button:
        if len(title.strip()) > 0 and len(content.strip()) > 0:
            try:
                user = get_current_user()
                if not user:
                    show_error("로그인이 필요합니다.")
                else:
                    supabase = get_supabase_client()
                    post_data = {
                        "title": title.strip(),
                        "content": content.strip(),
                        "user_id": user["id"],
                        "school_id": selected_school["id"],
                        "view_count": 0
                    }
                    response = supabase.table("posts").insert(post_data).execute()
                    if response.data:
                        show_success("게시글이 작성되었습니다!")
                        st.switch_page("pages/3_home.py")
                    else:
                        show_error("게시글 작성 중 오류가 발생했습니다.")
            except Exception as e:
                show_error(f"오류: {str(e)}")
        else:
            show_error("제목과 내용을 모두 입력해 주세요.")
    
if __name__ == "__main__":
    main()
