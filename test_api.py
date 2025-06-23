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
    Тестує всі ендпоінти API в правильній послідовності.
    """
    print("🚀 Початок тестування API...")

    # Тестові дані
    test_user = {"email": "test@example.com", "password": "TestPassword123"}

    test_post = {
        "text": "Це тестовий пост для перевірки функціональності API!"
    }

    try:
        # 1. Перевірка здоров'я API
        print("\n1️⃣ Перевірка health check...")
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health Status: {response.status_code}")
        if response.status_code == 200:
            print(f"✅ API працює: {response.json()}")

        # 2. Реєстрація користувача
        print("\n2️⃣ Тестування реєстрації...")
        response = requests.post(
            f"{BASE_URL}/auth/signup",
            json=test_user,
            headers={"Content-Type": "application/json"},
        )
        print(f"Signup Status: {response.status_code}")

        if response.status_code == 201:
            signup_data = response.json()
            token = signup_data["access_token"]
            print(f"✅ Реєстрація успішна! Токен отримано.")
        else:
            print(f"❌ Помилка реєстрації: {response.text}")
            return

        # 3. Авторизація
        print("\n3️⃣ Тестування авторизації...")
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json=test_user,
            headers={"Content-Type": "application/json"},
        )
        print(f"Login Status: {response.status_code}")

        if response.status_code == 200:
            login_data = response.json()
            token = login_data["access_token"]  # Оновлюємо токен
            print(f"✅ Авторизація успішна!")
        else:
            print(f"❌ Помилка авторизації: {response.text}")

        # Заголовки для автентифікованих запитів
        auth_headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        # 4. Створення посту
        print("\n4️⃣ Тестування створення посту...")
        response = requests.post(
            f"{BASE_URL}/posts/", json=test_post, headers=auth_headers
        )
        print(f"Create Post Status: {response.status_code}")

        if response.status_code == 201:
            post_data = response.json()
            post_id = post_data["id"]
            print(f"✅ Пост створено! ID: {post_id}")
            print(f"Текст: {post_data['text']}")
        else:
            print(f"❌ Помилка створення посту: {response.text}")
            return

        # 5. Отримання постів (перша спроба - запит до БД)
        print("\n5️⃣ Тестування отримання постів (запит до БД)...")
        response = requests.get(f"{BASE_URL}/posts/", headers=auth_headers)
        print(f"Get Posts Status: {response.status_code}")

        if response.status_code == 200:
            posts_data = response.json()
            print(f"✅ Отримано {len(posts_data)} постів з БД")
            for post in posts_data:
                print(f"  - Пост {post['id']}: {post['text'][:50]}...")
        else:
            print(f"❌ Помилка отримання постів: {response.text}")

        # 6. Отримання постів (друга спроба - з кешу)
        print("\n6️⃣ Тестування кешування (запит з кешу)...")
        start_time = time.time()
        response = requests.get(f"{BASE_URL}/posts/", headers=auth_headers)
        end_time = time.time()
        response_time = (end_time - start_time) * 1000

        print(f"Get Posts (Cache) Status: {response.status_code}")
        print(f"Час відповіді: {response_time:.2f} мс")

        if response.status_code == 200:
            cached_posts_data = response.json()
            print(f"✅ Отримано {len(cached_posts_data)} постів з кешу")

        # 7. Статистика постів
        print("\n7️⃣ Тестування статистики...")
        response = requests.get(
            f"{BASE_URL}/posts/stats", headers=auth_headers
        )
        print(f"Stats Status: {response.status_code}")

        if response.status_code == 200:
            stats_data = response.json()
            print(f"✅ Статистика отримана:")
            print(f"  - Всього постів: {stats_data['total_posts']}")
            print(f"  - Записів у кеші: {stats_data['cache_info']['size']}")

        # 8. Створення ще одного посту
        print("\n8️⃣ Створення другого посту...")
        test_post2 = {
            "text": "Другий тестовий пост для перевірки інвалідації кешу"
        }
        response = requests.post(
            f"{BASE_URL}/posts/", json=test_post2, headers=auth_headers
        )

        if response.status_code == 201:
            post_data2 = response.json()
            post_id2 = post_data2["id"]
            print(f"✅ Другий пост створено! ID: {post_id2}")

        # 9. Видалення посту
        print("\n9️⃣ Тестування видалення посту...")
        response = requests.delete(
            f"{BASE_URL}/posts/{post_id}", headers=auth_headers
        )
        print(f"Delete Post Status: {response.status_code}")

        if response.status_code == 200:
            delete_data = response.json()
            print(f"✅ Пост видалено: {delete_data['message']}")
        else:
            print(f"❌ Помилка видалення посту: {response.text}")

        # 10. Перевірка постів після видалення
        print("\n🔟 Перевірка постів після видалення...")
        response = requests.get(f"{BASE_URL}/posts/", headers=auth_headers)

        if response.status_code == 200:
            final_posts = response.json()
            print(f"✅ Залишилось {len(final_posts)} постів")
            for post in final_posts:
                print(f"  - Пост {post['id']}: {post['text'][:50]}...")

        # 11. Тестування валідації великого посту (1MB)
        print("\n1️⃣1️⃣ Тестування валідації розміру посту...")
        large_text = "А" * (1024 * 1024 + 1)  # Більше 1MB
        large_post = {"text": large_text}

        response = requests.post(
            f"{BASE_URL}/posts/", json=large_post, headers=auth_headers
        )
        print(f"Large Post Status: {response.status_code}")

        if response.status_code == 422:
            print("✅ Валідація розміру працює - великий пост відхилено")
        else:
            print(
                f"❌ Очікувалась помилка валідації, але отримано: {response.status_code}"
            )

        print("\n🎉 Всі тести завершено!")

    except requests.exceptions.ConnectionError:
        print(
            "❌ Помилка підключення до API. Переконайтесь, що сервер запущено на http://localhost:8000"
        )
    except Exception as e:
        print(f"❌ Помилка тестування: {str(e)}")


def test_invalid_token():
    """
    Тестує поведінку API з недійсним токеном.
    """
    print("\n🔒 Тестування недійсного токена...")

    invalid_headers = {
        "Authorization": "Bearer invalid-token-here",
        "Content-Type": "application/json",
    }

    response = requests.get(f"{BASE_URL}/posts/", headers=invalid_headers)

    if response.status_code == 401:
        print("✅ Недійсний токен правильно відхилено")
    else:
        print(
            f"❌ Очікувалась помилка 401, але отримано: {response.status_code}"
        )


if __name__ == "__main__":
    test_api()
    test_invalid_token()
    print("\n📋 Тестування завершено. Перевірте результати вище.")
