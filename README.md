# 🎓 대학교 커뮤니티

Streamlit과 Supabase를 활용한 대학교별 커뮤니티 플랫폼

## 📋 프로젝트 구조

```
school-community/
├── .env.example          # 환경변수 예시 파일
├── .gitignore           # Git 무시 파일 설정
├── requirements.txt     # Python 패키지 의존성
├── app.py              # 메인 진입점
├── README.md           # 프로젝트 문서
├── config/
│   └── settings.py     # 기본 설정값
├── utils/
│   ├── supabase_client.py  # Supabase 클라이언트
│   ├── auth.py             # 인증 관련 함수
│   └── dialogs.py          # 재사용 가능한 팝업
├── components/
│   └── school_search.py    # 학교 검색 컴포넌트
└── pages/
    ├── 1_login.py          # 로그인 페이지
    ├── 2_signup.py         # 회원가입 페이지
    ├── 3_home.py           # 홈 화면
    ├── 4_add_school.py     # 관심학교 추가
    ├── 5_school_search.py  # 학교 검색
    ├── 6_view_post.py      # 게시글 열람
    ├── 7_write_post.py     # 글쓰기
    └── 8_mypage.py         # 마이페이지
```

## 🚀 시작하기

### 1. 환경 설정

```bash
# 가상환경 생성 (선택사항)
python -m venv venv

# 가상환경 활성화
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt
```

### 2. 환경변수 설정

`.env.example` 파일을 복사하여 `.env` 파일을 생성하고, Supabase 정보를 입력하세요.

```bash
cp .env.example .env
```

`.env` 파일을 열어 다음 정보를 입력:

```
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_anon_key_here
```

### 3. 실행

```bash
streamlit run app.py
```

## 📦 필요한 패키지

- `streamlit` - 웹 애플리케이션 프레임워크
- `supabase` - Supabase 클라이언트
- `python-dotenv` - 환경변수 관리
- `bcrypt` - 비밀번호 암호화

## 🔧 주요 기능 (예정)

- ✅ 사용자 인증 (로그인/회원가입)
- ✅ 학교별 커뮤니티
- ✅ 게시글 작성/조회/수정/삭제
- ✅ 댓글 기능
- ✅ 좋아요 기능
- ✅ 관심학교 관리
- ✅ 마이페이지

## 📝 개발 상태

현재 프로젝트는 기본 구조만 생성된 상태입니다.
각 파일에는 기본 틀과 주석이 포함되어 있으며, 실제 기능 구현은 단계별로 진행될 예정입니다.

## 🗄️ 데이터베이스 스키마 (예정)

Supabase에 다음 테이블들이 필요합니다:

- `users` - 사용자 정보
- `schools` - 학교 정보
- `user_schools` - 사용자-학교 관계
- `posts` - 게시글
- `comments` - 댓글
- `likes` - 좋아요

## 📄 라이선스

이 프로젝트는 교육 목적으로 생성되었습니다.





