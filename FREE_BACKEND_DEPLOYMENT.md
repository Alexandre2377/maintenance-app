# 무료 백엔드 배포 옵션 (해외결제 불필요)

## 🎯 추천 서비스 비교

| 서비스 | 무료 티어 | Redis | 백그라운드 작업 | 난이도 | 추천도 |
|--------|----------|-------|----------------|--------|--------|
| **Railway** | 500시간/월 | ✅ | ✅ Celery | 쉬움 | ⭐⭐⭐⭐⭐ |
| **Render** | 750시간/월 | ❌ | ❌ | 쉬움 | ⭐⭐⭐ |
| **Fly.io** | 3개 VM 무료 | ✅ | ✅ | 중간 | ⭐⭐⭐⭐ |
| **Koyeb** | 무제한 | ❌ | ❌ | 쉬움 | ⭐⭐ |

---

## 🚀 추천: Railway (가장 적합!)

### 왜 Railway?
- ✅ **GitHub 연동만으로 배포** (카드 불필요)
- ✅ **Redis 지원** (Celery 작업 큐 가능)
- ✅ **무료 500시간/월** (약 20일 상시 가동)
- ✅ **자동 배포** (Git push만 하면 됨)
- ✅ **환경변수 관리 쉬움**

---

## 📋 Railway 배포 가이드 (30분)

### 1단계: Railway 가입 및 프로젝트 생성

```bash
# Railway 사이트 접속
https://railway.app

# GitHub로 로그인 (카드 필요 없음!)
1. "Login with GitHub" 클릭
2. GitHub 계정 연동
```

### 2단계: Redis 서비스 추가

```
Dashboard에서:
1. "New Project" 클릭
2. "Deploy from GitHub repo" 선택
3. maintenance-app 선택
4. "Add a service" → "Database" → "Add Redis"
```

### 3단계: Backend 서비스 설정

```
1. "Add a service" → "GitHub Repo" → maintenance-app 선택
2. Settings 클릭:
   - Root Directory: backend
   - Start Command: python main_v2.py
   - Watch Paths: backend/**
```

### 4단계: 환경변수 설정

```
Variables 탭에서 추가:

OPENAI_API_KEY=your-openai-key-here
DATABASE_URL=sqlite:///./maintenance.db
SECRET_KEY=building-maintenance-secret-key-2025-doublesilver
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Redis는 자동으로 REDIS_URL 설정됨
```

### 5단계: Celery Worker 서비스 추가

```
1. "Add a service" → "GitHub Repo" → maintenance-app 선택
2. Settings:
   - Root Directory: backend
   - Start Command: celery -A celery_app worker --loglevel=info
   - Watch Paths: backend/**
```

### 6단계: 배포 URL 확인

```
Settings → Domains → Generate Domain
예시: https://maintenance-backend.up.railway.app
```

---

## 🔄 대안 1: Render (Redis 없이)

Celery 없이 동기 처리만 사용하는 버전

### 배포 방법

```bash
# Render 접속
https://render.com

# GitHub 연동
1. "New +" → "Web Service"
2. maintenance-app 연결
3. 설정:
   - Name: maintenance-backend
   - Root Directory: backend
   - Build Command: pip install -r requirements.txt
   - Start Command: uvicorn main_v2:app --host 0.0.0.0 --port 10000
```

### 환경변수
```
OPENAI_API_KEY=your-key
DATABASE_URL=sqlite:///./maintenance.db
```

**주의**: Redis가 없어서 Celery 작동 안 함 (동기 처리만 가능)

---

## 🔄 대안 2: Fly.io (가장 강력, 조금 복잡)

### 배포 방법

```bash
# Fly CLI 설치
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"

# 로그인 (GitHub 계정)
fly auth login

# 프로젝트 초기화
cd C:\projact\backend
fly launch

# Redis 생성
fly redis create

# 배포
fly deploy
```

---

## ⚡ 빠른 결정 가이드

### 상황별 추천:

1. **Celery + Redis 필요** (비동기 작업 중요)
   → **Railway** 사용 ⭐⭐⭐⭐⭐

2. **빠르게 배포만 하고 싶음** (동기 처리 괜찮음)
   → **Render** 사용 ⭐⭐⭐

3. **완전히 무료로 오래 사용**
   → **Fly.io** 사용 ⭐⭐⭐⭐

---

## 🎯 Railway로 지금 바로 배포하기

### 준비물
- ✅ GitHub 계정 (이미 있음)
- ✅ OpenAI API Key (이미 있음)
- ✅ 5분의 시간

### 단계별 체크리스트

- [ ] https://railway.app 접속
- [ ] GitHub로 로그인
- [ ] New Project → Deploy from GitHub
- [ ] maintenance-app 선택
- [ ] Redis 서비스 추가
- [ ] Backend 서비스 설정 (Root Directory: backend)
- [ ] 환경변수 입력
- [ ] Celery Worker 서비스 추가
- [ ] Domain 생성
- [ ] 배포 완료!

---

## 📝 Railway 배포 후 할 일

### 1. Vercel 환경변수 업데이트
```
NEXT_PUBLIC_API_URL=https://your-railway-url.up.railway.app
```

### 2. README 업데이트
```markdown
- **API 문서**: [https://your-railway-url.up.railway.app/docs](https://your-railway-url.up.railway.app/docs)
```

### 3. 테스트
```bash
# API 접근 테스트
curl https://your-railway-url.up.railway.app/docs

# Vercel에서 요청 제출 테스트
```

---

## 💰 비용 비교

| 서비스 | 무료 티어 | 초과 시 |
|--------|----------|---------|
| Railway | 500시간/월 | $10/월 추가 500시간 |
| Render | 750시간/월 | $7/월 |
| Fly.io | 3 VM 무료 | 사용량 기반 |

**면접용으로는 Railway 500시간이면 충분합니다!**

---

## 🚀 Railway 배포를 시작하시겠습니까?

지금 https://railway.app 접속해서 GitHub로 로그인하세요!

5분이면 배포 완료됩니다. 🎉
