# AWS 배포 체크리스트

## ✅ 지금까지 완료된 것
- ✅ Vercel 프론트엔드 배포: https://maintenance-app-azure.vercel.app
- ✅ GitHub 저장소: https://github.com/doublesilver/maintenance-app
- ✅ 로컬 백엔드 테스트 완료
- ✅ README Vercel URL 업데이트

---

## 📋 AWS 배포 남은 작업 (순서대로)

### 1. AWS 계정 결제수단 등록 ⭐⭐⭐ (선행 필수)
**현재 상태**: 결제수단 미등록

**해야 할 일**:
1. AWS Console 접속: https://console.aws.amazon.com
2. 우측 상단 계정명 클릭 → **Billing and Cost Management**
3. **Payment methods** → **Add payment method**
4. 카드 정보 입력 및 등록

**예상 비용**:
- EC2 t3.micro (프리티어): **무료** (12개월)
- 프리티어 초과 시: ~$10/월

---

### 2. GitHub About 섹션 설정 ⭐⭐
**위치**: https://github.com/doublesilver/maintenance-app

**설정 방법**:
1. 저장소 페이지 상단 **About** 톱니바퀴 아이콘 클릭
2. 입력:
   - **Description**: `AI 기반 스마트 건물 유지보수 요청 관리 플랫폼`
   - **Website**: `https://maintenance-app-azure.vercel.app`
   - **Topics** (하나씩 입력):
     - `nextjs`
     - `fastapi`
     - `openai`
     - `celery`
     - `redis`
     - `websocket`
     - `typescript`
     - `python`
     - `tailwindcss`
     - `vercel`
3. **Save changes**

---

### 3. AWS EC2 인스턴스 생성 및 백엔드 배포 ⭐⭐⭐

#### 3-1. EC2 인스턴스 시작

```bash
# AWS Console에서:
# 1. EC2 → Launch Instance
# 2. 설정:
#    - Name: maintenance-backend
#    - AMI: Ubuntu Server 22.04 LTS
#    - Instance type: t3.micro (프리티어)
#    - Key pair: 새로 생성 (maintenance-key.pem 다운로드)
#    - Security Group:
#      - SSH (22): 내 IP
#      - HTTP (80): 0.0.0.0/0
#      - Custom TCP (8000): 0.0.0.0/0
#      - Custom TCP (5555): 내 IP (Flower)
# 3. Launch instance
```

#### 3-2. EC2 접속 및 환경 설정

```bash
# 로컬에서 SSH 접속
ssh -i "maintenance-key.pem" ubuntu@YOUR_EC2_IP

# 서버에서 실행
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv redis-server nginx -y

# Redis 시작
sudo systemctl start redis-server
sudo systemctl enable redis-server

# 프로젝트 클론
git clone https://github.com/doublesilver/maintenance-app.git
cd maintenance-app/backend

# Python 가상환경 설정
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 환경변수 설정
nano .env
# 입력:
# OPENAI_API_KEY=your-key-here
# REDIS_URL=redis://localhost:6379/0
# SECRET_KEY=building-maintenance-secret-key-2025-doublesilver
# DATABASE_URL=sqlite:///./maintenance.db
```

#### 3-3. Systemd 서비스 설정

**FastAPI 서비스** (`/etc/systemd/system/maintenance-api.service`):
```ini
[Unit]
Description=Maintenance API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/maintenance-app/backend
Environment="PATH=/home/ubuntu/maintenance-app/backend/venv/bin"
ExecStart=/home/ubuntu/maintenance-app/backend/venv/bin/python main_v2.py

[Install]
WantedBy=multi-user.target
```

**Celery Worker 서비스** (`/etc/systemd/system/celery-worker.service`):
```ini
[Unit]
Description=Celery Worker
After=network.target redis.service

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/maintenance-app/backend
Environment="PATH=/home/ubuntu/maintenance-app/backend/venv/bin"
ExecStart=/home/ubuntu/maintenance-app/backend/venv/bin/celery -A celery_app worker --loglevel=info

[Install]
WantedBy=multi-user.target
```

**서비스 시작**:
```bash
sudo systemctl daemon-reload
sudo systemctl start maintenance-api
sudo systemctl start celery-worker
sudo systemctl enable maintenance-api
sudo systemctl enable celery-worker

# 상태 확인
sudo systemctl status maintenance-api
sudo systemctl status celery-worker
```

#### 3-4. Nginx 설정

**`/etc/nginx/sites-available/maintenance`**:
```nginx
server {
    listen 80;
    server_name YOUR_EC2_IP;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /ws {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/maintenance /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

### 4. Vercel 환경변수 업데이트 ⭐⭐⭐

```bash
# Vercel Dashboard에서:
# 1. maintenance-app 프로젝트 → Settings → Environment Variables
# 2. NEXT_PUBLIC_API_URL 수정:
#    - 기존: http://localhost:8000
#    - 새값: http://YOUR_EC2_IP
# 3. Save
# 4. Deployments → 최신 배포 → Redeploy
```

---

### 5. README 최종 업데이트 ⭐⭐

```markdown
### 🌐 라이브 데모

- **Frontend**: [https://maintenance-app-azure.vercel.app](https://maintenance-app-azure.vercel.app)
- **API 문서**: [http://YOUR_EC2_IP/docs](http://YOUR_EC2_IP/docs)
- **GitHub**: [https://github.com/doublesilver/maintenance-app](https://github.com/doublesilver/maintenance-app)
```

---

### 6. 면접 준비 문서 작성 ⭐⭐

**파일**: `INTERVIEW_PREP.md`

**포함 내용**:
1. 프로젝트 개요 (30초 엘리베이터 피치)
2. 기술 스택 선택 이유
3. 어려웠던 점과 해결 방법
4. 성능 개선 사항 (25배 향상)
5. "바이브 코딩" 증명
6. 예상 질문 10개 + 답변

---

## 🚀 배포 후 테스트 체크리스트

- [ ] EC2에서 API 접근: `curl http://localhost:8000/health`
- [ ] 외부에서 API 접근: `curl http://YOUR_EC2_IP/docs`
- [ ] Vercel 프론트엔드에서 API 호출 테스트
- [ ] 요청 제출 → AI 분류 → 대시보드 확인
- [ ] Celery Worker 로그 확인: `sudo journalctl -u celery-worker -f`
- [ ] Redis 연결 확인: `redis-cli ping`

---

## 📊 예상 소요 시간

| 작업 | 시간 |
|------|------|
| AWS 결제수단 등록 | 5분 |
| GitHub About 설정 | 2분 |
| EC2 생성 및 설정 | 30분 |
| 백엔드 배포 | 20분 |
| Vercel 환경변수 업데이트 | 5분 |
| README 업데이트 | 5분 |
| 면접 준비 문서 | 1시간 |
| **총합** | **약 2시간** |

---

## ⚠️ 주의사항

1. **보안**:
   - EC2 Security Group에서 SSH는 본인 IP만 허용
   - `.env` 파일 절대 GitHub에 커밋 X
   - OpenAI API Key 노출 방지

2. **비용**:
   - 프리티어 t3.micro 사용 (12개월 무료)
   - 사용 후 반드시 인스턴스 중지/삭제

3. **테스트**:
   - 각 단계마다 테스트 후 다음 진행
   - 로그 확인: `sudo journalctl -u maintenance-api -f`

---

**AWS 결제수단 등록 후 시작하세요!** 🚀
