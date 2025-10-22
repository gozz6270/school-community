"""
학교 검색 컴포넌트
재사용 가능한 학교 검색 UI
"""

import streamlit as st
from utils.supabase_client import get_supabase_client

def search_schools(keyword: str) -> list:
    """
    학교 검색 함수
    
    Args:
        keyword: 검색 키워드
    
    Returns:
        list: 검색된 학교 목록
    """
    try:
        supabase = get_supabase_client()
        # TODO: Supabase에서 학교 검색
        # 예시 반환값: [{"id": 1, "name": "서울대학교", "location": "서울"}, ...]
    except Exception:
        pass
    pass

def render_school_search_component(on_select_callback=None):
    """
    학교 검색 컴포넌트 렌더링
    
    Args:
        on_select_callback: 학교 선택 시 실행할 콜백 함수
    """
    st.subheader("🔍 학교 검색")
    
    # 검색 입력
    search_keyword = st.text_input(
        "학교명을 입력하세요",
        placeholder="예: 서울대학교",
        key="school_search_input"
    )
    
    # 검색 버튼
    if st.button("검색", key="school_search_button"):
        if search_keyword:
            # TODO: 검색 결과 표시
            results = search_schools(search_keyword)
            
            if results:
                st.session_state.search_results = results
            else:
                st.info("검색 결과가 없습니다.")
        else:
            st.warning("검색어를 입력하세요.")
    
    # 검색 결과 표시
    if "search_results" in st.session_state and st.session_state.search_results:
        st.write("### 검색 결과")
        
        for school in st.session_state.search_results:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**{school.get('name')}**")
                st.caption(school.get('location', ''))
            
            with col2:
                if st.button("선택", key=f"select_school_{school.get('id')}"):
                    if on_select_callback:
                        on_select_callback(school)


