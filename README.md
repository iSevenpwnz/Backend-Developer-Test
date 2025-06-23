# Social Media API

FastAPI додаток з MVC архітектурою для соціальної мережі з JWT аутентифікацією, кешуванням та повною валідацією даних.

**🎯 Modern Python project with Poetry dependency management and clean MVC architecture!**

## 📩 Submission Information

**Task Requirements:** ✅ All requirements fully implemented

- **MVC Architecture** with 3 layers (Controllers, Services, Models)
- **5 API Endpoints** (Signup, Login, AddPost, GetPosts, DeletePost)
- **JWT Authentication** with dependency injection
- **1MB Payload Validation** with Pydantic
- **5-minute Caching** with TTL cache
- **MySQL/SQLite** database with SQLAlchemy ORM
- **Complete Documentation** for every function

**Submission:** `lucidtasksubmission@gmail.com`
**Time Requirement:** ✅ Completed within 2 hours
**Repository:** Public GitHub repository ready

## 🚀 Особливості

- **MVC Архітектура**: Розділення на 3 рівні (Controllers, Services, Models)
- **JWT Аутентифікація**: Безпечна токен-базована аутентифікація
- **Валідація Payload**: Автоматична перевірка розміру до 1MB
- **Кешування**: TTL кеш на 5 хвилин для оптимізації
- **Dependency Injection**: Автоматична аутентифікація через DI
- **Повна Документація**: Swagger UI та ReDoc
- **Валідація Типів**: Pydantic схеми з розширеною валідацією
- **Poetry**: Сучасне управління залежностями та віртуальними середовищами

## 📋 Вимоги

- Python 3.8+
- Poetry 1.2+
- MySQL 5.7+ (опціонально, за замовчуванням використовується SQLite)

## 🛠 Встановлення

### Через Poetry (рекомендовано)

1. **Клонування репозиторію**

```bash
git clone https://github.com/your-username/social-media-api.git
cd social-media-api
```

2. **Встановлення Poetry**

```bash
curl -sSL https://install.python-poetry.org | python3 -
# або через pip
pip install poetry
```

3. **Встановлення залежностей**

```bash
poetry install
```

### Через pip (legacy)

```bash
pip install -r requirements.txt
```

3. **Налаштування бази даних**

- Створіть MySQL базу даних `fastapi_app`
- Оновіть `DATABASE_URL` в `.env` файлі відповідно до ваших налаштувань

4. **Налаштування змінних середовища**

```bash
# .env файл (вже створений)
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/fastapi_app
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🚀 Запуск

### Через Poetry (рекомендовано)

```bash
# Розробка з автоматичним перезавантаженням
poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Продакшен
poetry run uvicorn main:app --host 0.0.0.0 --port 8000

# Ручний запуск
poetry run python main.py
```

### Через стандартний Python

```bash
python main.py
```

Або через uvicorn:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

API буде доступне за адресою: http://localhost:8000

## 📖 Документація API

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔗 Ендпоінти

### Аутентифікація

#### 1. Реєстрація користувача

```http
POST /auth/signup
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "MySecurePassword123"
}
```

**Відповідь:**

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

#### 2. Авторизація

```http
POST /auth/login
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "MySecurePassword123"
}
```

### Пости

#### 3. Створення посту

```http
POST /posts/
Authorization: Bearer <jwt-token>
Content-Type: application/json

{
    "text": "Це мій новий пост!"
}
```

#### 4. Отримання всіх постів

```http
GET /posts/
Authorization: Bearer <jwt-token>
```

#### 5. Видалення посту

```http
DELETE /posts/{post_id}
Authorization: Bearer <jwt-token>
```

## 🏗 Архітектура MVC

### Models (models/)

- `user.py` - SQLAlchemy модель користувача
- `post.py` - SQLAlchemy модель посту

### Views/Controllers (controllers/)

- `auth_controller.py` - Ендпоінти аутентифікації
- `post_controller.py` - Ендпоінти для постів

### Services (services/)

- `user_service.py` - Бізнес-логіка користувачів
- `post_service.py` - Бізнес-логіка постів

### Додаткові компоненти

#### Schemas (schemas/)

- `user.py` - Pydantic схеми користувача
- `post.py` - Pydantic схеми посту

#### Utils (utils/)

- `auth.py` - JWT та хешування паролів
- `dependencies.py` - Dependency injection
- `cache.py` - Система кешування

#### Database (database/)

- `config.py` - Конфігурація SQLAlchemy

## 🔒 Безпека

- **Хешування паролів**: bcrypt
- **JWT токени**: HS256 алгоритм
- **Валідація паролів**: Мінімум 8 символів, літери та цифри
- **CORS**: Налаштований для розробки

## 📊 Кешування

- **TTL**: 5 хвилин (300 секунд)
- **Максимум записів**: 1000
- **Автоматична інвалідація**: При створенні/видаленні постів

## 🧪 Тестування

### Автоматичне тестування

```bash
# Через Poetry
poetry run python test_api.py

# Через Python
python test_api.py
```

### Ручне тестування

1. **Реєстрація**:

```bash
curl -X POST "http://localhost:8000/auth/signup" \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com", "password": "Password123"}'
```

2. **Створення посту**:

```bash
curl -X POST "http://localhost:8000/posts/" \
     -H "Authorization: Bearer <your-token>" \
     -H "Content-Type: application/json" \
     -d '{"text": "Мій перший пост!"}'
```

3. **Отримання постів**:

```bash
curl -X GET "http://localhost:8000/posts/" \
     -H "Authorization: Bearer <your-token>"
```

## 📈 Моніторинг

### Health Check

```http
GET /health
```

### Статистика постів

```http
GET /posts/stats
Authorization: Bearer <jwt-token>
```

## 🚨 Обробка помилок

API повертає стандартизовані помилки:

- **400**: Неправильні дані
- **401**: Недійсний токен
- **404**: Ресурс не знайдено
- **422**: Помилка валідації
- **500**: Помилка сервера

## 📝 Валідація

### Пароль

- Мінімум 8 символів
- Принаймні одна літера
- Принаймні одна цифра
- Принаймні одна велика літера

### Пост

- Мінімум 1 символ
- Максимум 1MB

## 🔧 Команди Poetry

```bash
# Встановлення залежностей
poetry install

# Додавання нової залежності
poetry add package-name

# Додавання dev залежності
poetry add --group dev package-name

# Запуск у віртуальному середовищі
poetry run python script.py

# Активація віртуального середовища
poetry shell

# Показати інформацію про залежності
poetry show

# Оновлення залежностей
poetry update

# Експорт у requirements.txt
poetry export -f requirements.txt --output requirements.txt

# Публікація пакету
poetry publish --build
```

## 🎯 Корисні скрипти

```bash
# Розробка
poetry run uvicorn main:app --reload     # Запуск з auto-reload
poetry run python main.py               # Ручний запуск
poetry run python test_api.py           # Запуск тестів

# Форматування коду (після встановлення dev залежностей)
poetry run black .                      # Форматування Python коду
poetry run isort .                      # Сортування імпортів
poetry run flake8 .                     # Linting
```

## 🔧 Налаштування виробничого середовища

1. Змініть `JWT_SECRET_KEY` на безпечний ключ
2. Налаштуйте правильний `DATABASE_URL`
3. Обмежте CORS origins
4. Увімкніть HTTPS
5. Додайте rate limiting

## 🤝 Внесок

1. Fork проєкт
2. Створіть feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit зміни (`git commit -m 'Add some AmazingFeature'`)
4. Push в branch (`git push origin feature/AmazingFeature`)
5. Відкрийте Pull Request

## 📄 Ліцензія

MIT License - див. [LICENSE](LICENSE) файл для деталей.

## 📞 Підтримка

Для питань та підтримки звертайтесь: lucidtasksubmission@gmail.com
