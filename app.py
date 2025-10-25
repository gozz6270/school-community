"""
대학교 커뮤니티 메인 진입점
"""

import streamlit as st
from config.settings import PAGE_CONFIG
from utils.auth import init_auth

# 페이지 설정
st.set_page_config(**PAGE_CONFIG)

# 세션 상태 초기화
init_auth()

# 이미 로그인된 경우 홈으로 리다이렉트
if st.session_state.logged_in:
    st.switch_page("pages/3_home.py")
    st.stop()

# 비로그인 상태인 경우 로그인 페이지로 리다이렉트
st.switch_page("pages/1_login.py")
st.stop()

