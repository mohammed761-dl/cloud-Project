# User Management API

A simple FastAPI-based REST API for managing users with CRUD operations.

## Features

- ✅ Create new users
- ✅ List all users
- ✅ Get user by ID
- ✅ Update user information
- ✅ Delete users
- ✅ Email validation
- ✅ Docker support
- ✅ Interactive API documentation (Swagger UI)

## Prerequisites

- Python 3.10+
- Docker (optional)

## Installation

### Local Setup

1. Clone the repository:

```bash
git clone https://github.com/mohammed761-dl/cloud-Project.git
cd cloud-Project
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the API:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## Docker Setup

1. Build the image:

```bash
docker build -t user-mgmt-api .
```

2. Run the container:

```bash
docker run -p 8000:8000 user-mgmt-api:latest
```

## API Endpoints

| Method | Endpoint           | Description                                |
| ------ | ------------------ | ------------------------------------------ |
| GET    | `/`                | API information & available endpoints      |
| GET    | `/docs`            | Interactive API documentation (Swagger UI) |
| POST   | `/users/`          | Create a new user                          |
| GET    | `/users/`          | List all users                             |
| GET    | `/users/{user_id}` | Get a specific user                        |
| PUT    | `/users/{user_id}` | Update a user                              |
| DELETE | `/users/{user_id}` | Delete a user                              |

## Usage Examples

### Create a User

```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "is_active": true
  }'
```

### List All Users

```bash
curl -X GET "http://localhost:8000/users/"
```

### Get User by ID

```bash
curl -X GET "http://localhost:8000/users/{user_id}"
```

### Update User

```bash
curl -X PUT "http://localhost:8000/users/{user_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "jane_doe",
    "email": "jane@example.com",
    "is_active": true
  }'
```

### Delete User

```bash
curl -X DELETE "http://localhost:8000/users/{user_id}"
```

## Interactive Documentation

Once the API is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Technologies Used

- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation using Python type hints
- **Uvicorn** - ASGI server
- **Docker** - Containerization

## License

MIT License
