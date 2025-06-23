# Social Media API

FastAPI application with MVC architecture for social media with JWT authentication, caching and complete data validation.

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

## 🚀 Features

- **MVC Architecture**: Separation into 3 layers (Controllers, Services, Models)
- **JWT Authentication**: Secure token-based authentication
- **Payload Validation**: Automatic size checking up to 1MB
- **Caching**: TTL cache for 5 minutes optimization
- **Dependency Injection**: Automatic authentication through DI
- **Complete Documentation**: Swagger UI and ReDoc
- **Type Validation**: Pydantic schemas with extended validation
- **Poetry**: Modern dependency and virtual environment management

## 📋 Requirements

- Python 3.8+
- Poetry 1.2+
- MySQL 5.7+ (optional, SQLite used by default)

## 🛠 Installation

### Via Poetry (recommended)

1. **Clone repository**

```bash
git clone https://github.com/your-username/social-media-api.git
cd social-media-api
```

2. **Install Poetry**

```bash
curl -sSL https://install.python-poetry.org | python3 -
# or via pip
pip install poetry
```

3. **Install dependencies**

```bash
poetry install
```

### Via pip (legacy)

```bash
pip install -r requirements.txt
```

3. **Database setup**

- Create MySQL database `fastapi_app`
- Update `DATABASE_URL` in `.env` file according to your settings

4. **Environment variables setup**

```bash
# .env file (already created)
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/fastapi_app
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🚀 Running

### Via Poetry (recommended)

```bash
# Development with auto-reload
poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Production
poetry run uvicorn main:app --host 0.0.0.0 --port 8000

# Manual run
poetry run python main.py
```

### Via standard Python

```bash
python main.py
```

Or via uvicorn:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

API will be available at: http://localhost:8000

## 📖 API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔗 Endpoints

### Authentication

#### 1. User Registration

```http
POST /auth/signup
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "MySecurePassword123"
}
```

**Response:**

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

#### 2. User Login

```http
POST /auth/login
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "MySecurePassword123"
}
```

### Posts

#### 3. Create Post

```http
POST /posts/
Authorization: Bearer <jwt-token>
Content-Type: application/json

{
    "text": "This is my new post!"
}
```

#### 4. Get All Posts

```http
GET /posts/
Authorization: Bearer <jwt-token>
```

#### 5. Delete Post

```http
DELETE /posts/{post_id}
Authorization: Bearer <jwt-token>
```

## 🏗 MVC Architecture

### Models (models/)

- `user.py` - SQLAlchemy user model
- `post.py` - SQLAlchemy post model

### Views/Controllers (controllers/)

- `auth_controller.py` - Authentication endpoints
- `post_controller.py` - Post endpoints

### Services (services/)

- `user_service.py` - User business logic
- `post_service.py` - Post business logic

### Additional Components

#### Schemas (schemas/)

- `user.py` - Pydantic user schemas
- `post.py` - Pydantic post schemas

#### Utils (utils/)

- `auth.py` - JWT and password hashing
- `dependencies.py` - Dependency injection
- `cache.py` - Caching system

#### Database (database/)

- `config.py` - SQLAlchemy configuration

## 🔒 Security

- **Password Hashing**: bcrypt
- **JWT Tokens**: HS256 algorithm
- **Password Validation**: Minimum 8 characters, letters and digits
- **CORS**: Configured for development

## 📊 Caching

- **TTL**: 5 minutes (300 seconds)
- **Maximum records**: 1000
- **Auto invalidation**: On post create/delete

## 🧪 Testing

### Automated Testing

```bash
# Via Poetry
poetry run python test_api.py

# Via Python
python test_api.py
```

### Manual Testing

1. **Registration**:

```bash
curl -X POST "http://localhost:8000/auth/signup" \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com", "password": "Password123"}'
```

2. **Create Post**:

```bash
curl -X POST "http://localhost:8000/posts/" \
     -H "Authorization: Bearer <your-token>" \
     -H "Content-Type: application/json" \
     -d '{"text": "My first post!"}'
```

3. **Get Posts**:

```bash
curl -X GET "http://localhost:8000/posts/" \
     -H "Authorization: Bearer <your-token>"
```

## 📈 Monitoring

### Health Check

```http
GET /health
```

### Post Statistics

```http
GET /posts/stats
Authorization: Bearer <jwt-token>
```

## 🚨 Error Handling

API returns standardized errors:

- **400**: Invalid data
- **401**: Invalid token
- **404**: Resource not found
- **422**: Validation error
- **500**: Server error

## 📝 Validation

### Password

- Minimum 8 characters
- At least one letter
- At least one digit
- At least one uppercase letter

### Post

- Minimum 1 character
- Maximum 1MB

## 🔧 Poetry Commands

```bash
# Install dependencies
poetry install

# Add new dependency
poetry add package-name

# Add dev dependency
poetry add --group dev package-name

# Run in virtual environment
poetry run python script.py

# Activate virtual environment
poetry shell

# Show dependency information
poetry show

# Update dependencies
poetry update

# Export to requirements.txt
poetry export -f requirements.txt --output requirements.txt

# Publish package
poetry publish --build
```

## 🎯 Useful Scripts

```bash
# Development
poetry run uvicorn main:app --reload     # Run with auto-reload
poetry run python main.py               # Manual run
poetry run python test_api.py           # Run tests

# Code formatting (after installing dev dependencies)
poetry run black .                      # Format Python code
poetry run isort .                      # Sort imports
poetry run flake8 .                     # Linting
```

## 🔧 Production Environment Setup

1. Change `JWT_SECRET_KEY` to a secure key
2. Configure proper `DATABASE_URL`
3. Limit CORS origins
4. Enable HTTPS
5. Add rate limiting

## 🤝 Contributing

1. Fork the project
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request
