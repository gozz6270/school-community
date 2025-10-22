"""
공통 스타일 유틸리티
캠퍼스링크 - 대학교 커뮤니티 서비스
"""

import streamlit as st


def hide_sidebar():
    """모든 페이지에서 사이드바를 완전히 숨김"""
    st.markdown("""
    <style>
        /* 사이드바 완전히 숨기기 - 최우선 적용 */
        [data-testid="stSidebar"],
        section[data-testid="stSidebar"],
        .css-1d391kg {
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
            visibility: hidden !important;
        }
        
        /* 메인 컨텐츠 영역을 전체 너비로 확장 */
        .main .block-container {
            max-width: 100% !important;
            padding-left: 5rem !important;
            padding-right: 5rem !important;
        }
    </style>
    """, unsafe_allow_html=True)

