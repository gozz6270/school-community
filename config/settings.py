"""
프로젝트 기본 설정값
페이지 제목, 아이콘 등 전역 설정
"""

# 페이지 기본 설정
PAGE_CONFIG = {
    "page_title": "대학교 커뮤니티",
    "page_icon": "🎓",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# 앱 기본 정보
APP_NAME = "대학교 커뮤니티"
APP_DESCRIPTION = "대학교별 커뮤니티 플랫폼"

# 게시판 카테고리
POST_CATEGORIES = [
    "자유게시판",
    "질문게시판",
    "정보공유",
    "스터디",
    "동아리",
    "기타"
]

# 페이지 경로
PAGES = {
    "login": "pages/1_login.py",
    "signup": "pages/2_signup.py",
    "home": "pages/3_home.py",
    "add_school": "pages/4_add_school.py",
    "school_search": "pages/5_school_search.py",
    "view_post": "pages/6_view_post.py",
    "write_post": "pages/7_write_post.py",
    "mypage": "pages/8_mypage.py"
}





