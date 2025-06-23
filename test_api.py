"""
Test script for API functionality verification.
Performs complete testing cycle of all endpoints.
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"


def test_api():
    """
    Tests all API endpoints in correct order.
    """
    print("🚀 Starting API testing...")

    # Test data
    test_user = {"email": "test@example.com", "password": "TestPassword123"}

    test_post = {"text": "This is a test post to verify API functionality!"}

    try:
        # 1. API health check
        print("\n1️⃣ Testing health check...")
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health Status: {response.status_code}")
        if response.status_code == 200:
            print(f"✅ API is running: {response.json()}")

        # 2. User registration
        print("\n2️⃣ Testing registration...")
        response = requests.post(
            f"{BASE_URL}/auth/signup",
            json=test_user,
            headers={"Content-Type": "application/json"},
        )
        print(f"Signup Status: {response.status_code}")

        if response.status_code == 201:
            signup_data = response.json()
            token = signup_data["access_token"]
            print(f"✅ Registration successful! Token received.")
        else:
            print(f"❌ Registration error: {response.text}")
            return

        # 3. Authorization
        print("\n3️⃣ Testing authorization...")
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json=test_user,
            headers={"Content-Type": "application/json"},
        )
        print(f"Login Status: {response.status_code}")

        if response.status_code == 200:
            login_data = response.json()
            token = login_data["access_token"]  # Update token
            print(f"✅ Authorization successful!")
        else:
            print(f"❌ Authorization error: {response.text}")

        # Headers for authenticated requests
        auth_headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        # 4. Create post
        print("\n4️⃣ Testing post creation...")
        response = requests.post(
            f"{BASE_URL}/posts/", json=test_post, headers=auth_headers
        )
        print(f"Create Post Status: {response.status_code}")

        if response.status_code == 201:
            post_data = response.json()
            post_id = post_data["id"]
            print(f"✅ Post created! ID: {post_id}")
            print(f"Text: {post_data['text']}")
        else:
            print(f"❌ Post creation error: {response.text}")
            return

        # 5. Get posts (first attempt - database request)
        print("\n5️⃣ Testing get posts (database request)...")
        response = requests.get(f"{BASE_URL}/posts/", headers=auth_headers)
        print(f"Get Posts Status: {response.status_code}")

        if response.status_code == 200:
            posts_data = response.json()
            print(f"✅ Retrieved {len(posts_data)} posts from DB")
            for post in posts_data:
                print(f"  - Post {post['id']}: {post['text'][:50]}...")
        else:
            print(f"❌ Get posts error: {response.text}")

        # 6. Get posts (second attempt - from cache)
        print("\n6️⃣ Testing caching (cache request)...")
        start_time = time.time()
        response = requests.get(f"{BASE_URL}/posts/", headers=auth_headers)
        end_time = time.time()
        response_time = (end_time - start_time) * 1000

        print(f"Get Posts (Cache) Status: {response.status_code}")
        print(f"Response time: {response_time:.2f} ms")

        if response.status_code == 200:
            cached_posts_data = response.json()
            print(f"✅ Retrieved {len(cached_posts_data)} posts from cache")

        # 7. Post statistics
        print("\n7️⃣ Testing statistics...")
        response = requests.get(
            f"{BASE_URL}/posts/stats", headers=auth_headers
        )
        print(f"Stats Status: {response.status_code}")

        if response.status_code == 200:
            stats_data = response.json()
            print(f"✅ Statistics retrieved:")
            print(f"  - Total posts: {stats_data['total_posts']}")
            print(f"  - Cache records: {stats_data['cache_info']['size']}")

        # 8. Create another post
        print("\n8️⃣ Creating second post...")
        test_post2 = {"text": "Second test post to verify cache invalidation"}
        response = requests.post(
            f"{BASE_URL}/posts/", json=test_post2, headers=auth_headers
        )

        if response.status_code == 201:
            post_data2 = response.json()
            post_id2 = post_data2["id"]
            print(f"✅ Second post created! ID: {post_id2}")

        # 9. Delete post
        print("\n9️⃣ Testing post deletion...")
        response = requests.delete(
            f"{BASE_URL}/posts/{post_id}", headers=auth_headers
        )
        print(f"Delete Post Status: {response.status_code}")

        if response.status_code == 200:
            delete_data = response.json()
            print(f"✅ Post deleted: {delete_data['message']}")
        else:
            print(f"❌ Post deletion error: {response.text}")

        # 10. Check posts after deletion
        print("\n🔟 Checking posts after deletion...")
        response = requests.get(f"{BASE_URL}/posts/", headers=auth_headers)

        if response.status_code == 200:
            final_posts = response.json()
            print(f"✅ {len(final_posts)} posts remaining")
            for post in final_posts:
                print(f"  - Post {post['id']}: {post['text'][:50]}...")

        # 11. Test large post validation (1MB)
        print("\n1️⃣1️⃣ Testing post size validation...")
        large_text = "A" * (1024 * 1024 + 1)  # More than 1MB
        large_post = {"text": large_text}

        response = requests.post(
            f"{BASE_URL}/posts/", json=large_post, headers=auth_headers
        )
        print(f"Large Post Status: {response.status_code}")

        if response.status_code == 422:
            print("✅ Size validation works - large post rejected")
        else:
            print(
                f"❌ Expected validation error, but got: {response.status_code}"
            )

        print("\n🎉 All tests completed!")

    except requests.exceptions.ConnectionError:
        print(
            "❌ Connection error to API. Make sure server is running at http://localhost:8000"
        )
    except Exception as e:
        print(f"❌ Testing error: {str(e)}")


def test_invalid_token():
    """
    Tests API behavior with invalid token.
    """
    print("\n🔒 Testing invalid token...")

    invalid_headers = {
        "Authorization": "Bearer invalid-token-here",
        "Content-Type": "application/json",
    }

    response = requests.get(f"{BASE_URL}/posts/", headers=invalid_headers)

    if response.status_code == 401:
        print("✅ Invalid token properly rejected")
    else:
        print(f"❌ Expected 401 error, but got: {response.status_code}")


if __name__ == "__main__":
    test_api()
    test_invalid_token()
    print("\n📋 Testing completed. Check results above.")
