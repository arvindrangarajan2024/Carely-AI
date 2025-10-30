# Carely AI - Healthcare Assistant Backend

A comprehensive FastAPI backend for a healthcare assistant application with multilingual support ticket routing.

## Features

- **Patient Management**: Register, authenticate, and manage patient profiles
- **Appointment Scheduling**: Create, update, and manage medical appointments
- **Medical Records**: Store and retrieve patient medical history
- **Support Tickets**: Multilingual support ticket system with intelligent routing
- **Authentication**: Secure JWT-based authentication
- **RESTful API**: Clean, well-documented REST API endpoints
- **Database**: SQLAlchemy ORM with support for multiple databases

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLAlchemy (SQLite by default, supports PostgreSQL, MySQL)
- **Authentication**: JWT with bcrypt password hashing
- **Validation**: Pydantic v2
- **Documentation**: Auto-generated OpenAPI (Swagger UI)

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/      # API endpoints
│   │       └── api.py          # Router aggregation
│   ├── core/
│   │   ├── config.py          # Configuration settings
│   │   └── security.py        # Security utilities
│   ├── db/
│   │   ├── base.py            # Database base
│   │   └── session.py         # Database session
│   ├── models/                # SQLAlchemy models
│   ├── schemas/               # Pydantic schemas
│   └── main.py                # Application entry point
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.11+
- pip
- virtualenv (recommended)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/arvindrangarajan2024/Carely-AI.git
   cd Carely-AI/backend
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

5. **Run the application**:
   ```bash
   cd app
   uvicorn main:app --reload
   ```

   Or from the backend directory:
   ```bash
   python -m uvicorn app.main:app --reload
   ```

6. **Access the API**:
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Docker Deployment

1. **Build and run with Docker Compose**:
   ```bash
   docker-compose up -d
   ```

2. **Access the API**:
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new patient
- `POST /api/v1/auth/login` - Login and get access token
- `GET /api/v1/auth/me` - Get current user info

### Patients
- `GET /api/v1/patients/` - List all patients
- `GET /api/v1/patients/{id}` - Get patient by ID
- `PUT /api/v1/patients/{id}` - Update patient
- `DELETE /api/v1/patients/{id}` - Deactivate patient

### Appointments
- `POST /api/v1/appointments/` - Create appointment
- `GET /api/v1/appointments/` - List appointments
- `GET /api/v1/appointments/{id}` - Get appointment by ID
- `PUT /api/v1/appointments/{id}` - Update appointment
- `DELETE /api/v1/appointments/{id}` - Cancel appointment

### Medical Records
- `POST /api/v1/medical-records/` - Create medical record
- `GET /api/v1/medical-records/` - List medical records
- `GET /api/v1/medical-records/{id}` - Get record by ID
- `PUT /api/v1/medical-records/{id}` - Update record

### Support Tickets
- `POST /api/v1/support-tickets/` - Create support ticket
- `GET /api/v1/support-tickets/` - List support tickets
- `GET /api/v1/support-tickets/{id}` - Get ticket by ID
- `GET /api/v1/support-tickets/number/{number}` - Get ticket by number
- `PUT /api/v1/support-tickets/{id}` - Update ticket

### Health
- `GET /api/v1/health/` - Health check endpoint

## Configuration

Key configuration options in `.env`:

```env
# Application
APP_NAME=Carely AI - Healthcare Assistant
DEBUG=False

# Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# Database
DATABASE_URL=sqlite:///./carely.db

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
```

## Database

The application uses SQLite by default. To use PostgreSQL or MySQL:

1. Update `DATABASE_URL` in `.env`:
   ```env
   # PostgreSQL
   DATABASE_URL=postgresql://user:password@localhost/carely
   
   # MySQL
   DATABASE_URL=mysql://user:password@localhost/carely
   ```

2. Install the appropriate database driver:
   ```bash
   pip install psycopg2-binary  # PostgreSQL
   pip install pymysql          # MySQL
   ```

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black app/
isort app/
```

### Database Migrations (Alembic)
```bash
# Initialize Alembic (if not done)
alembic init alembic

# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

## Security Considerations

- Change `SECRET_KEY` in production
- Use HTTPS in production
- Enable rate limiting
- Implement proper access control
- Regular security audits
- Keep dependencies updated

## License

MIT License - See LICENSE file for details

## Support

For support, email support@carely-ai.com or create an issue in the GitHub repository.

