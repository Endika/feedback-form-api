# 📝 Feedback Form System

Flexible Multi-Language Feedback Form System built with FastAPI, following Domain-Driven Design and Hexagonal Architecture principles.

## 🎯 Features

- ✅ Multiple types of feedback forms (product feedback, support ticket, survey, custom)
- ✅ Multi-language support for forms and questions
- ✅ Multiple question types (text, rating, multiple choice)
- ✅ Full CRUD operations for forms (backoffice)
- ✅ Form retrieval and response submission (mobile/web apps)
- ✅ Response viewing (backoffice)
- ✅ Production-ready architecture with proper separation of concerns

## ⚙️ Prerequisites

- Python 3.11+
- Poetry (for dependency management)

## 🚀 Quick Installation

```bash
make install
```

## 💡 Basic Usage

### Start the API server

```bash
make run
```

The API will be available at `http://localhost:8000`

### API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Example: Create a Form (Backoffice)

```bash
curl -X POST "http://localhost:8000/api/v1/backoffice/forms" \
  -u admin:admin \
  -H "Content-Type: application/json" \
  -d '{
    "type": "product_feedback",
    "name": {
      "en": "Product Feedback",
      "es": "Feedback del Producto"
    },
    "description": {
      "en": "Help us improve our product",
      "es": "Ayúdanos a mejorar nuestro producto"
    },
    "questions": [
      {
        "type": "rating",
        "text": {
          "en": "How satisfied are you?",
          "es": "¿Qué tan satisfecho estás?"
        },
        "required": true,
        "min_rating": 1,
        "max_rating": 5
      },
      {
        "type": "text",
        "text": {
          "en": "Additional comments",
          "es": "Comentarios adicionales"
        },
        "required": false
      }
    ]
  }'
```

### Example: Get Form (Mobile/Web Apps)

```bash
# Simple request
curl -X GET "http://localhost:8000/api/v1/mobile/forms/{form_id}"

# With campaign tags (for reference/tracking)
curl -X GET "http://localhost:8000/api/v1/mobile/forms/{form_id}?campaign=summer2024&source=email&group=premium_users"
```

### Example: Submit a Response (Mobile/Web Apps)

```bash
curl -X POST "http://localhost:8000/api/v1/mobile/responses?campaign=summer2024&source=email&group=premium" \
  -H "Content-Type: application/json" \
  -d '{
    "form_id": "<form_id>",
    "answers": [
      {
        "question_id": "<question_id>",
        "value": 5
      },
      {
        "question_id": "<question_id>",
        "value": "Great product!"
      }
    ],
    "tags": {
      "utm_source": "newsletter",
      "utm_medium": "email"
    }
  }'
```

**Note**: Tags from query parameters (`campaign`, `source`, `group`) are automatically merged with tags in the request body.

### Example: GDPR - Access User Data

```bash
# Get all data for a user
curl -X GET "http://localhost:8000/api/v1/gdpr/data/user-123"

# Export user data as JSON file
curl -X GET "http://localhost:8000/api/v1/gdpr/data/user-123/export" -o user_data.json

# Delete all user data
curl -X DELETE "http://localhost:8000/api/v1/gdpr/data/user-123"
```

## 📋 Main Commands

- `make install` - Install dependencies
- `make test` - Run unit tests
- `make test-integration` - Run integration tests
- `make test-all` - Run all tests
- `make lint` - Run linters (Ruff)
- `make type-check` - Run type checking (mypy)
- `make format` - Format code
- `make clean` - Clean artifacts
- `make run` - Run the application

## 🏗️ Project Structure

```
project/
├── domain/              # Domain layer (entities, value objects, repositories)
├── application/         # Application layer (use cases, DTOs, mappers)
├── infrastructure/      # Infrastructure layer (mock repositories, config)
├── presentation/        # Presentation layer (FastAPI routers)
└── tests/               # Tests organized by layers
```

## 🔧 Architecture

The system follows **Domain-Driven Design (DDD)** with **Hexagonal Architecture**:

- **Domain Layer**: Pure business logic, independent of external concerns
- **Application Layer**: Use cases orchestrate domain operations
- **Infrastructure Layer**: Concrete implementations (currently mocked)
- **Presentation Layer**: FastAPI HTTP endpoints

## 👥 API Consumers

The API is designed for two types of consumers:

### Backoffice
- **Base URL**: `/api/v1/backoffice/`
- **Authentication**: HTTP Basic Auth (username/password)
  - Configure in `.env`: `BACKOFFICE_USERNAME` and `BACKOFFICE_PASSWORD`
  - Default: `admin` / `admin` (change in production!)
- **Endpoints**:
  - `POST /forms` - Create form (requires auth)
  - `GET /forms` - List all forms (requires auth)
  - `GET /forms/{form_id}` - Get form details (requires auth)
  - `PUT /forms/{form_id}` - Update form (requires auth)
  - `DELETE /forms/{form_id}` - Delete form (requires auth)
  - `GET /responses` - View responses (optional, requires auth)

### Mobile/Web Apps
- **Base URL**: `/api/v1/mobile/`
- **Endpoints**:
  - `GET /forms/{form_id}?campaign=X&source=Y&group=Z` - Get form to display (tags optional, for reference)
  - `POST /responses?campaign=X&source=Y&group=Z` - Submit form response (tags stored with response)
- **Tags/Campaigns**: 
  - Tags can be passed as query parameters: `campaign`, `source`, `group`
  - Tags are stored with each response for tracking and analytics
  - Example: `/api/v1/mobile/responses?campaign=summer2024&source=email&group=premium_users`

### GDPR (General Data Protection Regulation)
- **Base URL**: `/api/v1/gdpr/data/`
- **Endpoints**:
  - `GET /{user_id}` - Get all user data (Right to Access - Art. 15 GDPR)
  - `GET /{user_id}/export` - Export user data as JSON (Right to Portability - Art. 20 GDPR)
  - `DELETE /{user_id}` - Delete all user data (Right to Erasure - Art. 17 GDPR)
- **Usage**: Users can access, export, or delete their personal data by providing their `user_id`

## 📝 Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
ENVIRONMENT=development
DEBUG=true
APP_NAME=feedback-form-system
API_SECRET_KEY=your-secret-key-minimum-32-characters
```

## 🧪 Testing

Tests follow the **GWT (Given-When-Then)** format and are organized by layers.

```bash
make test          # Unit tests
make test-integration  # Integration tests
make test-all      # All tests
```

## 🔮 Next Steps

### Multilingual Support
For storing multilingual form/question data in the database:
- **Current approach is appropriate** - dictionaries are standard for stored multilingual data
- Libraries like `fastapi-babel` are better suited for UI messages, error messages, and API documentation
- If you need pluralization or complex formatting, consider `fastapi-babel` for error messages only
- Keep `MultilingualText` for domain data (forms, questions) as it's simple and flexible

### Dependency Injection Improvements
**Current Issue:**
- Global variables in `dependencies.py` for singleton pattern

**Suggested Improvements:**
- Use a more robust DI container (e.g., `dependency-injector`)
- Or use FastAPI's `Depends()` for automatic dependency injection

### Database Migration (Moving from Mock to Real Database)

To migrate from mock repositories to a real database implementation:

1. **Create new repository implementation** in `infrastructure/persistence/`:
   ```python
   class PostgreSQLFormRepository(FormRepository):
       def __init__(self, db_connection):
           self._db = db_connection
       
       async def create(self, form: Form) -> Form:
           # PostgreSQL implementation
           ...
   ```

2. **Update** `infrastructure/config/dependencies.py`:
   ```python
   def get_form_repository() -> FormRepository:
       global _form_repository
       if _form_repository is None:
           # Change only this line:
           _form_repository = PostgreSQLFormRepository(get_db_connection())
           # _form_repository = MockFormRepository()  # ← Comment/remove
       return _form_repository
   ```

The architecture is designed to support this migration - only the repository implementations need to change, the domain and application layers remain unchanged.
