# CARELY AI
Multilingual Support Ticket Routing Agent - Healthcare Assistant Application

## Project Overview

Carely AI is a comprehensive healthcare assistant platform featuring:

- **FastAPI Backend**: RESTful API with JWT authentication
- **Patient Management**: Complete patient profile and medical history management
- **Appointment Scheduling**: Book, manage, and track medical appointments
- **Medical Records**: Secure storage and retrieval of medical information
- **Support Tickets**: Multilingual support ticket routing system
- **Modern Architecture**: Clean, scalable, production-ready code

## Repository Structure

```
Carely-AI/
├── backend/               # FastAPI backend application
│   ├── app/              # Main application code
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Core functionality (config, security)
│   │   ├── db/           # Database configuration
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   └── main.py       # Application entry point
│   ├── requirements.txt  # Python dependencies
│   ├── vercel.json       # Vercel deployment config
│   ├── Dockerfile        # Docker configuration
│   └── README.md         # Backend documentation
├── Demo/                 # Demo and examples
├── DEPLOYMENT.md         # Deployment guide
└── README.md            # This file
```

## Quick Start

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Access the API**:
   - API: http://localhost:8000
   - Interactive Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## API Features

### Authentication & Authorization
- JWT-based authentication
- Secure password hashing with bcrypt
- Role-based access control

### Core Endpoints

#### Health Check
- `GET /api/v1/health` - Service health status

#### Authentication
- `POST /api/v1/auth/register` - Register new patient
- `POST /api/v1/auth/login` - Login and get access token
- `GET /api/v1/auth/me` - Get current user profile

#### Patient Management
- `GET /api/v1/patients/` - List patients
- `GET /api/v1/patients/{id}` - Get patient details
- `PUT /api/v1/patients/{id}` - Update patient information
- `DELETE /api/v1/patients/{id}` - Deactivate patient account

#### Appointments
- `POST /api/v1/appointments/` - Create appointment
- `GET /api/v1/appointments/` - List appointments
- `GET /api/v1/appointments/{id}` - Get appointment details
- `PUT /api/v1/appointments/{id}` - Update appointment
- `DELETE /api/v1/appointments/{id}` - Cancel appointment

#### Medical Records
- `POST /api/v1/medical-records/` - Create medical record
- `GET /api/v1/medical-records/` - List medical records
- `GET /api/v1/medical-records/{id}` - Get record details
- `PUT /api/v1/medical-records/{id}` - Update record

#### Support Tickets (Multilingual)
- `POST /api/v1/support-tickets/` - Create support ticket
- `GET /api/v1/support-tickets/` - List support tickets
- `GET /api/v1/support-tickets/{id}` - Get ticket details
- `GET /api/v1/support-tickets/number/{number}` - Get by ticket number
- `PUT /api/v1/support-tickets/{id}` - Update ticket

## Technology Stack

- **Framework**: FastAPI 0.109.0
- **Database**: SQLAlchemy (SQLite/PostgreSQL/MySQL)
- **Authentication**: JWT with python-jose
- **Validation**: Pydantic v2
- **Documentation**: OpenAPI/Swagger
- **Security**: bcrypt password hashing

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

### Recommended Platforms
- **Railway**: Best for full-stack backends with databases
- **Render**: Free tier with PostgreSQL support
- **Fly.io**: Container-based deployment
- **Vercel**: Serverless (requires external database)

## Development

### Project Setup
```bash
# Clone repository
git clone https://github.com/arvindrangarajan2024/Carely-AI.git
cd Carely-AI/backend

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload
```

### Testing
```bash
pytest
```

### Code Quality
```bash
black app/
isort app/
flake8 app/
```

## Documentation

- Backend API Documentation: See `/backend/README.md`
- Deployment Guide: See `DEPLOYMENT.md`
- Interactive API Docs: Visit `/docs` when running the server

## Security

- JWT-based authentication
- Password hashing with bcrypt
- CORS configuration
- Environment-based configuration
- SQL injection prevention via SQLAlchemy ORM

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

For questions or issues:
- Email: support@carely-ai.com
- GitHub Issues: https://github.com/arvindrangarajan2024/Carely-AI/issues
