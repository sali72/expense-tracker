# 🏦 Expense Tracker Microservice

A robust and scalable expense tracking microservice built with FastAPI and MongoDB, following industry best practices.

## 🚀 Features

- 🔐 Secure authentication integration with external auth service
- 💾 MongoDB-based data persistence
- 🐳 Docker containerization
- 📊 Comprehensive E2E testing
- 🔄 Asynchronous operations
- 📝 Clean architecture and code organization

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Database**: MongoDB
- **Authentication**: External Auth Service
- **Containerization**: Docker
- **Testing**: pytest
- **Package Management**: uv

## 📋 Prerequisites

- Python 3.8+
- Docker and Docker Compose
- MongoDB
- Access to Auth Service ([auth-service](https://github.com/sali72/auth-service))

## 🚀 Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/expense-tracker.git
   cd expense-tracker
   ```

2. **Environment Setup**
   - Create a `.env` file based on the configuration in `app/core/config.py`
   - Set up your MongoDB connection details
   - Configure the auth service URL

3. **Run with Docker**
   ```bash
   docker-compose up --build
   ```

4. **Run Tests**
   ```bash
   pytest
   ```

## 📚 API Documentation

Once the service is running, access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🏗️ Project Structure

```
expense-tracker/
├── app/
│   ├── api/         # API routes and endpoints
│   ├── core/        # Core configurations
│   ├── crud/        # Database operations
│   ├── models/      # Data models
│   ├── tests/       # Test suite
│   └── main.py      # Application entry point
├── docker-compose.yml
├── Dockerfile
└── pyproject.toml
```

## 🔒 Authentication

This service relies on an external authentication service. You can either:
- Use the provided [auth-service](https://github.com/sali72/auth-service)
- Implement your own authentication system

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2025 Seyed Ali Hashemi
