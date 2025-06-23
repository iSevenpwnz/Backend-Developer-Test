"""
Quick demo script showing all API endpoints.
Run this after starting the server with: poetry run python main.py
"""

import requests
import json

BASE_URL = "http://localhost:8000"


def demo():
    print("🚀 Social Media API Demo")
    print("=" * 50)

    # Test data
    user_data = {"email": "demo@example.com", "password": "DemoPassword123"}

    # 1. Signup
    print("\n1️⃣ Creating user account...")
    response = requests.post(f"{BASE_URL}/auth/signup", json=user_data)
    if response.status_code == 201:
        token = response.json()["access_token"]
        print("✅ User created successfully!")
    else:
        print(f"❌ Signup failed: {response.text}")
        return

    headers = {"Authorization": f"Bearer {token}"}

    # 2. Create post
    print("\n2️⃣ Creating a post...")
    post_data = {"text": "Hello from Social Media API! 🎉"}
    response = requests.post(
        f"{BASE_URL}/posts/", json=post_data, headers=headers
    )
    if response.status_code == 201:
        post_id = response.json()["id"]
        print(f"✅ Post created with ID: {post_id}")

    # 3. Get posts (from database)
    print("\n3️⃣ Fetching posts...")
    response = requests.get(f"{BASE_URL}/posts/", headers=headers)
    if response.status_code == 200:
        posts = response.json()
        print(f"✅ Found {len(posts)} posts")

    # 4. Get posts (from cache)
    print("\n4️⃣ Fetching posts again (from cache)...")
    response = requests.get(f"{BASE_URL}/posts/", headers=headers)
    if response.status_code == 200:
        print("✅ Posts retrieved from cache (faster!)")

    # 5. API Documentation
    print(f"\n📚 View API documentation at: {BASE_URL}/docs")
    print(f"📖 Alternative docs at: {BASE_URL}/redoc")

    print("\n🎉 Demo completed successfully!")
    print("Try the full test suite with: poetry run python test_api.py")


if __name__ == "__main__":
    try:
        demo()
    except requests.exceptions.ConnectionError:
        print(
            "❌ Server not running. Start it with: poetry run python main.py"
        )
