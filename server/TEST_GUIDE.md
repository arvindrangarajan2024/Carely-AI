# Carely AI Backend - Testing Guide

## Quick Start Testing

### Step 1: Start the Server

```bash
cd /Users/arvindrangarajan/PythonLab/Carely/backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Step 2: Open Interactive Documentation

Visit: **http://localhost:8000/docs**

This opens **Swagger UI** - a beautiful, interactive API testing interface!

---

## Testing Workflow Example

### 1. **Health Check** (No Auth Required)

**Endpoint:** `GET /api/v1/health/`

In Swagger UI:
1. Click "Health" section
2. Click "GET /api/v1/health/"
3. Click "Try it out"
4. Click "Execute"

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "Carely AI Healthcare Assistant API",
  "timestamp": "2025-10-27T01:15:06.562496",
  "version": "1.0.0"
}
```

### 2. **Register a New Patient**

**Endpoint:** `POST /api/v1/auth/register`

1. Click "Authentication" section
2. Click "POST /api/v1/auth/register"
3. Click "Try it out"
4. Fill in the request body:

```json
{
  "email": "john.doe@example.com",
  "password": "SecurePass123",
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "1990-05-15",
  "phone_number": "+1-555-0123",
  "blood_type": "O+",
  "allergies": "Penicillin",
  "preferred_language": "en"
}
```

5. Click "Execute"

**Expected Response (201 Created):**
```json
{
  "email": "john.doe@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "id": 1,
  "is_active": true,
  "created_at": "2025-10-27T01:20:00.000000",
  ...
}
```

### 3. **Login (Get JWT Token)**

**Endpoint:** `POST /api/v1/auth/login`

1. Click "POST /api/v1/auth/login"
2. Click "Try it out"
3. Fill in credentials:
   - **username:** `john.doe@example.com` (use email)
   - **password:** `SecurePass123`

4. Click "Execute"

**Expected Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

5. **Copy the access_token value!**

### 4. **Authorize Future Requests**

1. Click the green **"Authorize"** button at the top right
2. In the popup, paste your token in the "Value" field
3. Click "Authorize"
4. Click "Close"

Now all protected endpoints will use your authentication! 🔒

### 5. **Get Current User Info**

**Endpoint:** `GET /api/v1/auth/me`

1. Click "GET /api/v1/auth/me"
2. Click "Try it out"
3. Click "Execute"

**Response:**
```json
{
  "id": 1,
  "email": "john.doe@example.com",
  "first_name": "John",
  "last_name": "Doe",
  ...
}
```

### 6. **Create an Appointment**

**Endpoint:** `POST /api/v1/appointments/`

```json
{
  "patient_id": 1,
  "doctor_name": "Dr. Sarah Smith",
  "appointment_type": "consultation",
  "scheduled_time": "2025-11-15T10:00:00",
  "duration_minutes": 30,
  "reason": "Annual checkup",
  "is_virtual": false
}
```

### 7. **Create a Support Ticket**

**Endpoint:** `POST /api/v1/support-tickets/`

```json
{
  "category": "appointment",
  "subject": "Need to reschedule appointment",
  "description": "I need to change my appointment from Nov 15 to Nov 20",
  "language": "en",
  "priority": "medium",
  "contact_email": "john.doe@example.com"
}
```

**Response includes ticket number:**
```json
{
  "id": 1,
  "ticket_number": "TKT-A3B5C7D9",
  "status": "open",
  ...
}
```

---

## Method 2: Using cURL (Command Line)

### 1. Health Check
```bash
curl http://localhost:8000/api/v1/health/
```

### 2. Register Patient
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jane@example.com",
    "password": "SecurePass456",
    "first_name": "Jane",
    "last_name": "Smith",
    "date_of_birth": "1985-03-20",
    "phone_number": "+1-555-0456",
    "preferred_language": "en"
  }'
```

### 3. Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=jane@example.com&password=SecurePass456"
```

Save the token:
```bash
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 4. Get Current User (Protected)
```bash
curl http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

---

## Method 3: Using Python Requests

Create a test script:

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# 1. Register
response = requests.post(f"{BASE_URL}/auth/register", json={
    "email": "test@example.com",
    "password": "Test123456",
    "first_name": "Test",
    "last_name": "User",
    "date_of_birth": "1995-01-01",
    "preferred_language": "en"
})
print("Register:", response.status_code)

# 2. Login
response = requests.post(f"{BASE_URL}/auth/login", data={
    "username": "test@example.com",
    "password": "Test123456"
})
token = response.json()["access_token"]
print("Token:", token[:20] + "...")

# 3. Get user info
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
print("User:", response.json()["first_name"])

# 4. Create appointment
response = requests.post(f"{BASE_URL}/appointments/", headers=headers, json={
    "patient_id": 1,
    "doctor_name": "Dr. Johnson",
    "appointment_type": "consultation",
    "scheduled_time": "2025-11-20T14:00:00",
    "duration_minutes": 30,
    "reason": "Follow-up visit"
})
print("Appointment:", response.status_code)
```

---

## Method 4: Using the Test Client (For Development)

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Test health endpoint
response = client.get("/api/v1/health/")
assert response.status_code == 200
print(response.json())

# Test registration
response = client.post("/api/v1/auth/register", json={
    "email": "dev@example.com",
    "password": "DevPass123",
    "first_name": "Dev",
    "last_name": "User",
    "date_of_birth": "1992-06-15",
    "preferred_language": "en"
})
assert response.status_code == 201
print("Created user:", response.json()["id"])
```

---

## Testing Checklist

### ✅ Core Functionality
- [ ] Health check works
- [ ] Can register new patient
- [ ] Can login and get JWT token
- [ ] Can access protected endpoints with token
- [ ] Cannot access protected endpoints without token

### ✅ Patient Management
- [ ] Can view patient profile
- [ ] Can update patient information
- [ ] Can deactivate account

### ✅ Appointments
- [ ] Can create appointment
- [ ] Can list appointments
- [ ] Can update appointment
- [ ] Can cancel appointment
- [ ] Cannot schedule in the past
- [ ] Cannot schedule too far in future

### ✅ Medical Records
- [ ] Can create medical record
- [ ] Can view patient's records
- [ ] Cannot view other patients' records

### ✅ Support Tickets
- [ ] Can create support ticket
- [ ] Ticket number is generated
- [ ] Can view tickets by status
- [ ] Can search by ticket number

### ✅ Security
- [ ] Passwords are hashed (not stored as plain text)
- [ ] JWT tokens expire after configured time
- [ ] Users can only access their own data
- [ ] Invalid tokens are rejected

---

## Common Issues & Solutions

### Issue: "ImportError: cannot import name 'Patient'"
**Solution:** This was a circular import. Already fixed in the code!

### Issue: "Database is locked"
**Solution:** SQLite limitation. Only one writer at a time. For production, use PostgreSQL.

### Issue: "401 Unauthorized"
**Solution:** 
1. Make sure you're logged in and have a token
2. Click "Authorize" in Swagger UI and paste your token
3. Check token hasn't expired (default: 7 days)

### Issue: "422 Unprocessable Entity"
**Solution:** Check your request body matches the schema:
- Email must be valid format
- Password must be 8+ characters
- Date fields must be YYYY-MM-DD format
- Required fields must be present

---

## Database Inspection

View the SQLite database:

```bash
cd /Users/arvindrangarajan/PythonLab/Carely/backend
sqlite3 carely.db

# View tables
.tables

# View patients
SELECT * FROM patients;

# View appointments
SELECT * FROM appointments;

# Exit
.quit
```

---

## Next Steps

1. **Test all endpoints** using Swagger UI
2. **Create test data** for your frontend development
3. **Try error cases** (invalid data, missing auth, etc.)
4. **Check the database** to see data persistence
5. **Test with your frontend** when ready

For production deployment, see `DEPLOYMENT.md`!


