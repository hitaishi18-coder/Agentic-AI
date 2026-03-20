# Tea House API

A simple FastAPI-based REST API for managing a tea collection with CRUD operations.

## 📋 Features

- **Get All Teas**: Retrieve the complete list of available teas
- **Add Tea**: Add a new tea to the collection
- **Update Tea**: Modify existing tea details by ID
- **Delete Tea**: Remove a tea from the collection by ID
- **Welcome Endpoint**: Get a greeting message

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd c:\Users\DELL\Desktop\fastapi
   ```

2. **Create and activate the virtual environment:**
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies:**
   ```bash
   python -m pip install fastapi uvicorn
   ```

## 📦 Dependencies

- **FastAPI** - Modern web framework for building APIs
- **Uvicorn** - ASGI server for running FastAPI applications
- **Pydantic** - Data validation using Python type annotations

## 🏃 Running the Server

Activate the virtual environment (if not already active), then run:

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## 📚 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/teas` | Get all teas |
| POST | `/teas` | Add a new tea |
| PUT | `/teas/{tea_id}` | Update a tea by ID |
| DELETE | `/teas/{tea_id}` | Delete a tea by ID |

## 📤 Data Model

```json
{
  "id": 1,
  "name": "Green Tea",
  "origin": "China"
}
```

### Tea Schema

- **id** (integer): Unique identifier for the tea
- **name** (string): Name of the tea
- **origin** (string): Origin/source country of the tea

## 🔧 Example Usage

### Welcome Message
```bash
curl http://127.0.0.1:8000/
```

### Get All Teas
```bash
curl http://127.0.0.1:8000/teas
```

### Add a New Tea
```bash
curl -X POST http://127.0.0.1:8000/teas \
  -H "Content-Type: application/json" \
  -d '{"id": 1, "name": "Green Tea", "origin": "China"}'
```

### Update a Tea
```bash
curl -X PUT http://127.0.0.1:8000/teas/1 \
  -H "Content-Type: application/json" \
  -d '{"id": 1, "name": "Premium Green Tea", "origin": "Japan"}'
```

### Delete a Tea
```bash
curl -X DELETE http://127.0.0.1:8000/teas/1
```

## 🛠️ Interactive API Documentation

FastAPI automatically provides two interactive API documentation interfaces:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

Use these to test endpoints directly in your browser.

## ⚠️ Notes

- The tea collection is stored in memory and will be reset when the server restarts
- For production use, consider adding a database (SQLAlchemy, MongoDB, etc.)
- Error handling for edge cases (duplicate IDs, not found errors) can be enhanced

## 📝 License

This project is open source and available for educational purposes.
