import pytest
from fastapi.testclient import TestClient
from main import app, init_db
import os
import sqlite3

client = TestClient(app)

# 테스트 데이터베이스 설정
@pytest.fixture(autouse=True)
def setup_test_db():
    # 테스트 전 데이터베이스 초기화
    if os.path.exists("test_maintenance.db"):
        os.remove("test_maintenance.db")

    # main.py의 DB 연결을 테스트 DB로 변경
    import main
    original_get_db = main.get_db

    from contextlib import contextmanager
    @contextmanager
    def test_get_db():
        conn = sqlite3.connect("test_maintenance.db")
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    main.get_db = test_get_db
    init_db()

    yield

    # 테스트 후 정리
    main.get_db = original_get_db
    if os.path.exists("test_maintenance.db"):
        os.remove("test_maintenance.db")

def test_read_root():
    """루트 엔드포인트 테스트"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Building Maintenance API is running"}

def test_create_request():
    """요청 생성 테스트"""
    request_data = {
        "description": "The water heater is not working",
        "location": "Building A, Floor 2",
        "contact_info": "010-1234-5678"
    }

    response = client.post("/api/requests", json=request_data)
    assert response.status_code == 200

    data = response.json()
    assert data["description"] == request_data["description"]
    assert data["location"] == request_data["location"]
    assert data["contact_info"] == request_data["contact_info"]
    assert "category" in data
    assert "priority" in data
    assert data["status"] == "pending"

def test_get_all_requests():
    """모든 요청 조회 테스트"""
    # 먼저 요청 생성
    client.post("/api/requests", json={
        "description": "Broken window in office",
        "location": "Office 301"
    })

    response = client.get("/api/requests")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_request_by_id():
    """특정 요청 조회 테스트"""
    # 요청 생성
    create_response = client.post("/api/requests", json={
        "description": "Air conditioner is too cold",
        "location": "Meeting Room"
    })
    request_id = create_response.json()["id"]

    # 조회
    response = client.get(f"/api/requests/{request_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == request_id
    assert data["description"] == "Air conditioner is too cold"

def test_get_nonexistent_request():
    """존재하지 않는 요청 조회 테스트"""
    response = client.get("/api/requests/99999")
    assert response.status_code == 404

def test_update_request_status():
    """요청 상태 업데이트 테스트"""
    # 요청 생성
    create_response = client.post("/api/requests", json={
        "description": "Light bulb replacement needed"
    })
    request_id = create_response.json()["id"]

    # 상태 업데이트
    update_data = {"status": "in_progress"}
    response = client.patch(f"/api/requests/{request_id}", json=update_data)
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "in_progress"

def test_update_request_priority():
    """요청 우선순위 업데이트 테스트"""
    # 요청 생성
    create_response = client.post("/api/requests", json={
        "description": "Elevator maintenance"
    })
    request_id = create_response.json()["id"]

    # 우선순위 업데이트
    update_data = {"priority": "urgent"}
    response = client.patch(f"/api/requests/{request_id}", json=update_data)
    assert response.status_code == 200

    data = response.json()
    assert data["priority"] == "urgent"

def test_delete_request():
    """요청 삭제 테스트"""
    # 요청 생성
    create_response = client.post("/api/requests", json={
        "description": "Test request to delete"
    })
    request_id = create_response.json()["id"]

    # 삭제
    response = client.delete(f"/api/requests/{request_id}")
    assert response.status_code == 200

    # 삭제 확인
    get_response = client.get(f"/api/requests/{request_id}")
    assert get_response.status_code == 404

def test_delete_nonexistent_request():
    """존재하지 않는 요청 삭제 테스트"""
    response = client.delete("/api/requests/99999")
    assert response.status_code == 404

def test_get_stats():
    """통계 조회 테스트"""
    # 여러 요청 생성
    client.post("/api/requests", json={"description": "Electrical issue"})
    client.post("/api/requests", json={"description": "Plumbing problem"})
    client.post("/api/requests", json={"description": "HVAC maintenance"})

    response = client.get("/api/stats")
    assert response.status_code == 200

    data = response.json()
    assert "total" in data
    assert "by_status" in data
    assert "by_category" in data
    assert "by_priority" in data
    assert data["total"] >= 3

def test_filter_by_status():
    """상태별 필터링 테스트"""
    # 요청 생성
    create_response = client.post("/api/requests", json={
        "description": "Filter test"
    })
    request_id = create_response.json()["id"]

    # 상태 변경
    client.patch(f"/api/requests/{request_id}", json={"status": "completed"})

    # 필터링 조회
    response = client.get("/api/requests?status=completed")
    assert response.status_code == 200

    data = response.json()
    assert all(req["status"] == "completed" for req in data)

def test_request_validation():
    """요청 유효성 검증 테스트"""
    # 빈 description
    response = client.post("/api/requests", json={})
    assert response.status_code == 422

def test_multiple_requests():
    """다중 요청 처리 테스트"""
    requests_data = [
        {"description": "Request 1", "location": "Location 1"},
        {"description": "Request 2", "location": "Location 2"},
        {"description": "Request 3", "location": "Location 3"},
    ]

    for req_data in requests_data:
        response = client.post("/api/requests", json=req_data)
        assert response.status_code == 200

    # 모든 요청 확인
    response = client.get("/api/requests")
    assert response.status_code == 200
    assert len(response.json()) >= 3

def test_user_registration():
    """사용자 회원가입 테스트"""
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }

    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 200

    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]
    assert data["role"] == "user"
    assert "password" not in data  # 비밀번호는 응답에 포함되지 않아야 함

def test_duplicate_email_registration():
    """중복 이메일 회원가입 테스트"""
    user_data = {
        "email": "duplicate@example.com",
        "password": "password123",
        "full_name": "User One"
    }

    # 첫 번째 회원가입
    response1 = client.post("/api/auth/register", json=user_data)
    assert response1.status_code == 200

    # 중복 회원가입 시도
    response2 = client.post("/api/auth/register", json=user_data)
    assert response2.status_code == 400
    assert "already registered" in response2.json()["detail"].lower()

def test_user_login():
    """사용자 로그인 테스트"""
    # 먼저 사용자 등록
    user_data = {
        "email": "login@example.com",
        "password": "loginpassword123",
        "full_name": "Login User"
    }
    client.post("/api/auth/register", json=user_data)

    # 로그인
    login_data = {
        "username": "login@example.com",  # OAuth2PasswordRequestForm uses 'username'
        "password": "loginpassword123"
    }
    response = client.post("/api/auth/login", data=login_data)
    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password():
    """잘못된 비밀번호로 로그인 시도 테스트"""
    # 사용자 등록
    user_data = {
        "email": "wrongpass@example.com",
        "password": "correctpassword",
        "full_name": "Test User"
    }
    client.post("/api/auth/register", json=user_data)

    # 잘못된 비밀번호로 로그인
    login_data = {
        "username": "wrongpass@example.com",
        "password": "wrongpassword"
    }
    response = client.post("/api/auth/login", data=login_data)
    assert response.status_code == 401

def test_login_nonexistent_user():
    """존재하지 않는 사용자 로그인 테스트"""
    login_data = {
        "username": "nonexistent@example.com",
        "password": "anypassword"
    }
    response = client.post("/api/auth/login", data=login_data)
    assert response.status_code == 401

def test_get_current_user():
    """현재 로그인한 사용자 정보 조회 테스트"""
    # 사용자 등록 및 로그인
    user_data = {
        "email": "currentuser@example.com",
        "password": "password123",
        "full_name": "Current User"
    }
    client.post("/api/auth/register", json=user_data)

    login_response = client.post("/api/auth/login", data={
        "username": "currentuser@example.com",
        "password": "password123"
    })
    token = login_response.json()["access_token"]

    # 인증된 요청
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

    data = response.json()
    assert data["email"] == "currentuser@example.com"
    assert data["full_name"] == "Current User"

def test_get_current_user_without_token():
    """토큰 없이 사용자 정보 조회 시도 테스트"""
    response = client.get("/api/auth/me")
    assert response.status_code == 401

def test_get_current_user_invalid_token():
    """잘못된 토큰으로 사용자 정보 조회 테스트"""
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": "Bearer invalid_token_here"}
    )
    assert response.status_code == 401

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=main", "--cov-report=html"])
