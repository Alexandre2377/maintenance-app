"""
간단한 DB 조회 스크립트

사용법:
    python admin_db_viewer.py
"""
import sqlite3

def view_users():
    """모든 사용자 조회"""
    conn = sqlite3.connect("maintenance.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT id, email, full_name, role, created_at FROM users ORDER BY id")
    users = cursor.fetchall()

    if not users:
        print("사용자가 없습니다.")
        conn.close()
        return

    print("\n" + "="*100)
    print(f"{'ID':<5} {'Email':<30} {'Name':<20} {'Role':<10} {'Created':<20}")
    print("-"*100)

    for user in users:
        role_icon = "👑" if user["role"] == "admin" else "👤"
        print(f"{user['id']:<5} {user['email']:<30} {user['full_name'] or 'N/A':<20} {role_icon} {user['role']:<9} {user['created_at']:<20}")

    print("="*100)
    print(f"Total: {len(users)} users\n")

    conn.close()

def view_requests():
    """모든 요청 조회"""
    conn = sqlite3.connect("maintenance.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT r.id, u.email, r.description, r.status, r.category, r.created_at
        FROM requests r
        LEFT JOIN users u ON r.user_id = u.id
        ORDER BY r.created_at DESC
        LIMIT 10
    """)
    requests = cursor.fetchall()

    if not requests:
        print("요청이 없습니다.")
        conn.close()
        return

    print("\n" + "="*120)
    print(f"{'ID':<5} {'User Email':<25} {'Description':<40} {'Status':<12} {'Category':<15}")
    print("-"*120)

    for req in requests:
        desc = req["description"][:37] + "..." if len(req["description"]) > 40 else req["description"]
        print(f"{req['id']:<5} {req['email'] or 'Unknown':<25} {desc:<40} {req['status']:<12} {req['category'] or 'N/A':<15}")

    print("="*120)
    print(f"Showing latest 10 requests\n")

    conn.close()

if __name__ == "__main__":
    print("\n📊 Database Viewer\n")

    print("👥 Users:")
    view_users()

    print("\n📋 Recent Requests:")
    view_requests()
