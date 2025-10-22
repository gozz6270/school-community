"""
대학교 커뮤니티 메인 진입점
로그인 확인 후 홈으로 리다이렉트
"""

import streamlit as st
from config.settings import PAGE_CONFIG
from utils.auth import init_session_state, is_logged_in

# 페이지 설정
st.set_page_config(**PAGE_CONFIG)

def main():
    """메인 함수"""
    # 세션 상태 초기화
    init_session_state()
    
    # 로그인 상태 확인
    if is_logged_in():
        # 로그인된 경우 홈 페이지로 리다이렉트
        st.switch_page("pages/3_home.py")
    else:
        # 로그인되지 않은 경우 로그인 페이지로 리다이렉트
        st.switch_page("pages/1_login.py")

if __name__ == "__main__":
    main()

