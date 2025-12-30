# 온라인 이력서

## 📌 최근 완료한 프로젝트

### 프로젝트명: Building Maintenance Management System (건물 유지보수 관리 시스템)

**GitHub Repository**: https://github.com/doublesilver/maintenance-app

**서비스 URL**:
- Frontend (Vercel): https://maintenance-app-swart.vercel.app
- Backend (Railway): https://maintenance-app-production-9c47.up.railway.app

**데모 계정**:
```
최고 관리자 계정
이메일: admin@system.local
비밀번호: qwer1234
```

---

## ⏱️ 프로젝트 소요 시간

**전체 기간**: 2024년 12월 (약 2주)
**본인 투입 시간**: 약 40시간
- 설계 및 기획: 4시간
- 백엔드 개발 (FastAPI): 12시간
- 프론트엔드 개발 (Next.js 14): 16시간
- 배포 및 인프라 설정: 4시간
- 역할 기반 접근 제어 (RBAC) 구현: 4시간

---

## 🎯 프로젝트 개요

건물 유지보수 요청을 효율적으로 관리할 수 있는 풀스택 웹 애플리케이션입니다.

### 주요 기능
- **역할 기반 접근 제어 (RBAC)**: super_admin, admin, user 3단계 권한 체계
- **최고 관리자 시스템**: 사용자 역할 관리, 환경변수 기반 보안 설정
- **유지보수 요청 관리**: CRUD 작업, 상태 추적 (대기/진행중/완료)
- **실시간 통계 대시보드**: 요청 상태별/카테고리별/우선순위별 집계
- **JWT 인증**: Access Token 기반 보안 인증, Rate Limiting

### 기술 스택
**Backend**:
- FastAPI 0.115.6 (Python 웹 프레임워크)
- SQLite (데이터베이스)
- JWT 인증 (python-jose)
- Bcrypt 비밀번호 해싱
- SlowAPI Rate Limiting

**Frontend**:
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- Axios (API 통신)

**인프라**:
- Railway (백엔드 배포)
- Vercel (프론트엔드 배포)
- GitHub Actions (CI/CD)

---

## 💡 가장 어려웠던 문제와 해결 방식

### 문제: 로그인 후 404 에러 발생 및 역할별 리다이렉션 실패

**상황**:
로그인 성공 후 존재하지 않는 `/dashboard` 경로로 리다이렉트되어 404 에러가 발생했습니다. 또한 사용자 역할(admin/user)에 관계없이 모든 사용자가 동일한 페이지로 이동하는 문제가 있었습니다.

**원인 분석**:
1. 로그인 페이지가 하드코딩된 `/dashboard` 경로로 리다이렉트
2. 실제로는 `/admin/dashboard`와 `/user/dashboard`만 존재
3. 로그인 시 사용자 역할 정보를 확인하지 않음

**해결 과정**:
1. 로그인 성공 후 `/api/auth/me` 엔드포인트를 호출하여 사용자 역할 정보를 조회
2. 역할에 따라 조건부 리다이렉트 로직 구현:
   - `admin` 또는 `super_admin` → `/admin/dashboard`
   - `user` → `/user/dashboard`
3. 일반 사용자 전용 대시보드 페이지(`/user/dashboard`) 신규 생성
4. 각 역할별로 접근 가능한 기능을 명확히 분리 (본인 요청만 조회 vs 전체 요청 관리)

**결과**:
사용자 역할에 맞는 대시보드로 자동 리다이렉트되며, 권한에 따른 기능 접근 제어가 정상적으로 작동합니다.

---

## 🏗️ 아키텍처 특징

### 1. 역할 기반 접근 제어 (RBAC)
```
⭐ super_admin (최고 관리자)
├─ 모든 사용자 역할 관리 (승격/강등)
├─ 모든 유지보수 요청 관리
└─ 시스템 통계 조회

👑 admin (관리자)
├─ 모든 유지보수 요청 관리
└─ 통계 조회

👤 user (일반 사용자)
├─ 본인 요청만 조회/삭제
└─ 새 요청 등록
```

### 2. 보안 설계
- JWT 기반 토큰 인증
- Bcrypt 비밀번호 해싱 (72바이트 제한 처리)
- Rate Limiting (로그인 API: 10회/분)
- 환경변수 기반 민감 정보 관리
- 프로덕션 환경에서 Swagger UI 비활성화

### 3. 자동 초기화 시스템
- 백엔드 시작 시 최고 관리자 계정 자동 생성
- 환경변수로 이메일/비밀번호 커스터마이징 가능
- 중복 생성 방지 로직

---

## 📊 주요 성과

1. **완전한 역할 기반 권한 시스템 구현**
   - 3단계 역할 계층 구조
   - 역할별 API 엔드포인트 접근 제어
   - 자기 자신의 역할 변경 방지

2. **프로덕션 배포 완료**
   - Railway + Vercel을 활용한 자동 CI/CD 구축
   - 환경변수 기반 설정 관리
   - HTTPS 적용 및 CORS 설정

3. **사용자 경험 최적화**
   - 로딩 상태 표시
   - 에러 핸들링 및 사용자 친화적 에러 메시지
   - 반응형 디자인 (모바일/데스크톱 대응)

---

## 🔗 관련 링크

- **GitHub**: https://github.com/doublesilver/maintenance-app
- **Frontend**: https://maintenance-app-swart.vercel.app
- **Backend API**: https://maintenance-app-production-9c47.up.railway.app
- **최고 관리자 가이드**: [SUPER_ADMIN_GUIDE.md](https://github.com/doublesilver/maintenance-app/blob/main/SUPER_ADMIN_GUIDE.md)
- **보안 설정 가이드**: [SECURITY_SETUP.md](https://github.com/doublesilver/maintenance-app/blob/main/SECURITY_SETUP.md)

---

## 💻 로컬 실행 방법

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

---

*이 프로젝트는 실제 서비스 가능한 수준의 코드 품질과 보안을 목표로 개발되었습니다.*
