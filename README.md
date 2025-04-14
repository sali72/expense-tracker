# 🏦 Expense Tracker Microservice

A robust and scalable expense tracking microservice built with FastAPI and MongoDB, with nginx as a reverse proxy and integration with an external authentication service.

## 🚀 Features

- 🔐 Secure authentication integration with external auth service
- 💾 MongoDB-based data persistence
- 🐳 Docker containerization for easy deployment
- 📊 Comprehensive E2E testing
- 🔄 Asynchronous operations
- 📝 Clean architecture and code organization
- 🔐 Reverse proxy with nginx for unified access and security
- 🔀 Microservices architecture with separate auth service

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Database**: MongoDB (for expense tracker), PostgreSQL (for auth service)
- **ORM**: Beanie (MongoDB ODM)
- **Authentication**: External Auth Service
- **Containerization**: Docker & Docker Compose
- **Reverse Proxy**: Nginx
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
   - Create a `.env` file for the expense tracker service configuration
   - Create a `.auth-service.env` file for the auth service configuration
   - Configure your MongoDB and PostgreSQL connection details

3. **Run with Docker**
   ```bash
   docker-compose up --build
   ```

4. **Access Services**
   - Expense Tracker API: http://localhost/expense-tracker
   - Auth Service API: http://localhost/auth-service

5. **Run Tests**
   ```bash
   pytest
   ```

## 📚 API Documentation

Once the service is running, access the interactive API documentation at:
- Expense Tracker API: `http://localhost/expense-tracker/docs`
- Auth Service API: `http://localhost/auth-service/docs`

Both services are proxied through nginx on port 80:
- The expense tracker service is available at the `/expense-tracker/` path
- The authentication service is available at the `/auth-service/` path

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
