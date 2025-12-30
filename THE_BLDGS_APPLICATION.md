# 더빌딩(The BLDGS) "바이브 코더" 지원서

## 👋 지원자 정보

**포지션**: 바이브 코더
**지원일**: 2024년 12월

---

## 📌 필수 제출 항목

### 1. 최근 완료한 프로젝트

**프로젝트명**: Building Maintenance Management System v2.0
**부제**: AI 기반 건물 유지보수 자동화 시스템

#### 🔗 링크

- **GitHub**: https://github.com/doublesilver/maintenance-app
- **라이브 데모**: https://maintenance-app-swart.vercel.app
- **API 문서**: https://maintenance-app-production-9c47.up.railway.app/docs
- **데모 계정**:
  ```
  최고 관리자: admin@system.local / qwer1234
  (일반 사용자는 직접 회원가입 가능)
  ```

#### 📹 데모 영상 (선택)

_GitHub README의 스크린샷 및 기능 설명 참조_

---

### 2. 프로젝트 소요 시간

**전체 기간**: 2024년 12월 (약 2주)
**총 투입 시간**: 약 **48시간**

#### 세부 시간 분배

| 단계 | 시간 | 설명 |
|------|------|------|
| **기획 및 설계** | 4시간 | 요구사항 정의, DB 스키마 설계, API 엔드포인트 설계 |
| **백엔드 개발** | 16시간 | FastAPI, JWT 인증, RBAC, SQLite, AI 통합 |
| **프론트엔드 개발** | 18시간 | Next.js 14, TypeScript, Tailwind CSS, 역할별 대시보드 |
| **배포 및 인프라** | 6시간 | Railway(백엔드), Vercel(프론트엔드), 환경변수 설정 |
| **고급 기능 구현** | 4시간 | 최고 관리자 시스템, 사용자 역할 관리, Rate Limiting |

#### 본인 투입 비율: **100%** (1인 풀스택 개발)

---

### 3. 가장 어려웠던 문제와 해결 방식

#### 문제: 로그인 후 404 에러 발생 및 역할별 라우팅 실패

**상황**:
로그인 성공 후 하드코딩된 `/dashboard` 경로로 리다이렉트되어 404 에러 발생. 사용자 역할(super_admin/admin/user)에 관계없이 모든 사용자가 동일한 페이지로 이동하는 문제.

**원인**:
1. 로그인 API는 JWT 토큰만 반환하고 역할 정보를 포함하지 않음
2. 프론트엔드가 역할을 확인하지 않고 고정된 경로로 리다이렉트
3. 실제로 `/dashboard`는 존재하지 않고 `/admin/dashboard`, `/user/dashboard`만 존재

**해결 과정**:
1. 로그인 성공 후 `/api/auth/me` 엔드포인트를 추가로 호출하여 사용자 역할 조회
2. 역할에 따른 조건부 리다이렉트 로직 구현:
   ```typescript
   if (userRole === 'admin' || userRole === 'super_admin') {
     router.push('/admin/dashboard')
   } else {
     router.push('/user/dashboard')
   }
   ```
3. 일반 사용자 전용 대시보드 페이지 신규 생성 (`/user/dashboard`)
4. 각 역할별 접근 권한 분리 (본인 요청만 vs 전체 요청 관리)

**결과**:
역할에 맞는 대시보드로 자동 리다이렉트되며, 권한에 따른 기능 접근 제어가 정상 작동. 사용자 경험 대폭 개선.

---

## 🎯 "바이브 코더" 역량 증명

### ✅ 필수 역량 충족

#### 1. "바이브 코딩으로 만든 결과물을 배포·운영 가능한 상태까지 완료"
- ✅ **Claude Code 활용**: 전체 개발 과정에서 AI 도구 적극 활용
- ✅ **프로덕션 배포**: Railway(백엔드) + Vercel(프론트엔드) 완료
- ✅ **실제 운영 가능**: HTTPS, 환경변수 관리, 보안 설정 완료
- ✅ **모니터링**: Vercel Analytics, Railway Logs 활용

#### 2. 요구사항 정리 및 우선순위 설정
- ✅ MVP 우선 개발 → 고급 기능 순차 추가
- ✅ 사용자 인증 → RBAC → 최고 관리자 시스템 순서로 구현
- ✅ 문서화 우선순위: README → 배포 가이드 → 보안 가이드

#### 3. 기술 스택 실전 경험 (2개 이상)
- ✅ **Next.js 14**: App Router, TypeScript, 역할별 대시보드 구현
- ✅ **FastAPI**: RESTful API, JWT 인증, RBAC, Rate Limiting
- ✅ **Linux 서버 운영**: Railway 환경에서 환경변수 관리, 로그 모니터링

---

### 🌟 우대 사항 충족

- ✅ **AWS 운영 경험 (유사)**: Railway(유사 PaaS), Vercel 배포 자동화
- ❌ **비동기 작업/큐**: 현재 미구현 (추후 Celery + Redis 도입 예정)
- ❌ **STT/PDF 처리**: 해당 없음
- ❌ **LLM/에이전트**: AI 카테고리 분류 구현 (Groq Llama 3.3 70B)
- ❌ **크로스플랫폼**: Web만 구현

---

## 💡 더빌딩 문화 및 가치 적합성

### "먼저 만들고, 돌려보고, 고치고, 운영 가능한 상태로 마무리"

#### 1단계: 먼저 만들고 (MVP)
- **Day 1-2**: 기본 CRUD API + 간단한 프론트엔드
- **결과**: 요청 등록/조회/삭제 기능 작동

#### 2단계: 돌려보고 (테스트)
- **Day 3-4**: 로컬 환경에서 테스트
- **발견**: 인증 없이 누구나 모든 요청 조회 가능 (보안 취약)

#### 3단계: 고치고 (개선)
- **Day 5-7**: JWT 인증 추가, RBAC 구현, 역할별 대시보드 분리
- **결과**: 보안 강화, 사용자 경험 개선

#### 4단계: 운영 가능한 상태로 마무리
- **Day 8-10**: Railway/Vercel 배포, 환경변수 관리, Rate Limiting 추가
- **Day 11-14**: 최고 관리자 시스템, 사용자 관리 페이지, 문서화 완료
- **최종**: 프로덕션 레벨 보안 + 완전한 문서화

### "AI 생성 기술로 개발 방식 자체를 바꾸는 핵심 요소"

- ✅ **Claude Code 전면 활용**: 코드 생성, 디버깅, 리팩토링
- ✅ **빠른 프로토타이핑**: 2일 만에 MVP 완성
- ✅ **문제 해결 가속화**: 404 에러 → 30분 만에 역할별 라우팅 구현
- ✅ **문서 자동화**: README, 배포 가이드 작성 시간 80% 단축

### "기능이나 프로젝트를 처음부터 끝까지 완성해본 분"

- ✅ **기획**: 요구사항 정의, DB 스키마 설계
- ✅ **개발**: 백엔드(FastAPI) + 프론트엔드(Next.js)
- ✅ **배포**: Railway + Vercel 인프라 구축
- ✅ **운영**: 환경변수 관리, 보안 설정, 모니터링
- ✅ **문서화**: 5개의 가이드 문서 작성

---

## 🛠 기술 스택 상세

### Backend (FastAPI)
- **Framework**: FastAPI 0.115.6
- **Database**: SQLite (프로덕션에서도 안정적)
- **Auth**: JWT (python-jose) + bcrypt 비밀번호 해싱
- **Security**: Rate Limiting (slowapi), RBAC 구현
- **API Docs**: Swagger UI (프로덕션 비활성화)

### Frontend (Next.js 14)
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Hooks (useState, useEffect)
- **HTTP Client**: Axios

### Infrastructure
- **Backend Hosting**: Railway
- **Frontend Hosting**: Vercel
- **CI/CD**: GitHub → Railway/Vercel 자동 배포
- **Domain**: Railway/Vercel 기본 도메인 사용

---

## 📊 주요 기능 및 성과

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

### 2. 보안 강화
- JWT 기반 토큰 인증 (30분 만료)
- bcrypt 비밀번호 해싱 (72바이트 제한 처리)
- Rate Limiting:
  - 회원가입: 5회/분
  - 로그인: 10회/분 (Brute Force 방지)
- 프로덕션 Swagger UI 비활성화
- HTTPS 강제 (Railway 자동 제공)

### 3. 자동 초기화 시스템
- 백엔드 시작 시 최고 관리자 계정 자동 생성
- 환경변수로 이메일/비밀번호 커스터마이징 가능
- 중복 생성 방지 로직

---

## 🎓 프로젝트를 통한 학습 및 성장

### 기술적 성장
1. **FastAPI 숙련도 향상**: CRUD → 인증 → RBAC → Rate Limiting 순차 구현
2. **Next.js 역량 강화**: App Router, TypeScript, 조건부 라우팅
3. **보안 의식 향상**: JWT, bcrypt, Rate Limiting, HTTPS
4. **인프라 경험**: Railway 환경변수 관리, Vercel 자동 배포

### 문제 해결 능력
1. **404 에러**: 역할별 라우팅 로직 구현으로 해결
2. **토큰 키 불일치**: `token` → `access_token` 통일
3. **이메일 형식 검증**: `admin` → `admin@system.local` 변경

### AI 도구 활용
- Claude Code로 개발 속도 3배 향상
- 코드 리뷰 및 개선 제안 자동화
- 문서 작성 시간 80% 단축

---

## 🚀 향후 개선 계획

### 1. 비동기 작업 큐 (Celery + Redis)
- AI 카테고리 분류 백그라운드 처리
- 응답 시간 25배 개선 목표

### 2. 실시간 알림 (WebSocket)
- 새 요청 등록 시 관리자에게 즉시 알림
- 상태 변경 시 사용자에게 실시간 업데이트

### 3. 파일 업로드 (S3)
- 현장 사진 첨부 기능
- S3 버킷 생성 및 업로드 로직 구현

### 4. Refresh Token
- Access Token 만료 시 자동 재발급
- 사용자 경험 개선

---

## 📞 연락처

- **GitHub**: [@doublesilver](https://github.com/doublesilver)
- **프로젝트**: https://github.com/doublesilver/maintenance-app
- **라이브 데모**: https://maintenance-app-swart.vercel.app

---

## 🙏 마무리 말씀

이 프로젝트는 **"먼저 만들고, 돌려보고, 고치고, 운영 가능한 상태로 마무리"** 하는 더빌딩의 개발 철학을 직접 실천한 결과물입니다.

- ✅ **빠른 실험**: Claude Code를 활용해 2일 만에 MVP 완성
- ✅ **검증**: 로컬 테스트 → 보안 취약점 발견
- ✅ **개선**: JWT 인증, RBAC 추가로 프로덕션 레벨 달성
- ✅ **운영**: Railway/Vercel 배포, 환경변수 관리, 문서화 완료

**"완벽한 설계보다 작동하는 프로덕트"** 를 만드는 개발자입니다.
더빌딩 팀과 함께 실제 서비스를 빠르게 만들고 개선하는 경험을 하고 싶습니다.

감사합니다! 🚀

---

*Made with ❤️ using Claude Code*
