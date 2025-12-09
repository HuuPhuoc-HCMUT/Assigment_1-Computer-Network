
import requests

BASE_URL = "http://127.0.0.1:9001"

def test_health():
    r = requests.get(f"{BASE_URL}/")
    assert r.status_code == 200
    print("✓ GET / ok")

def test_login():
    r = requests.post(
        f"{BASE_URL}/login",
        json={"username": "user1", "password": "123456"}
    )
    assert r.status_code == 200
    assert r.json().get("ok") is True
    print("✓ POST /login ok")

def test_start():
    r = requests.post(
        f"{BASE_URL}/start",
        json={"port": 9301}
    )
    assert r.status_code == 200
    assert "port" in r.json()
    print("✓ POST /start ok")

def test_get_peers():
    r = requests.get(f"{BASE_URL}/peers?channel=global")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    print("✓ GET /peers ok")

def test_broadcast():
    r = requests.post(
        f"{BASE_URL}/broadcast",
        json={
            "channel": "global",
            "message": "hello from test"
        }
    )
    assert r.status_code == 200
    assert r.json().get("ok") is True
    print("✓ POST /broadcast ok")

def test_get_messages():
    r = requests.get(f"{BASE_URL}/messages?channel=global")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    print("✓ GET /messages ok")


if __name__ == "__main__":
    print("=== RUN PEER SERVER API TESTS ===")
    test_health()
    test_login()
    test_start()
    test_get_peers()
    test_broadcast()
    test_get_messages()
    print("=== ALL TESTS PASSED ✅ ===")
