#!/usr/bin/env python3
"""Quick test script for Carely AI Backend"""
from fastapi.testclient import TestClient
from app.main import app

# Create test client
client = TestClient(app)

print("=" * 60)
print("🏥 Carely AI Backend - Quick Test")
print("=" * 60)

# Test 1: Health Check
print("\n1. Testing Health Endpoint...")
response = client.get("/api/v1/health/")
if response.status_code == 200:
    print("   ✅ Health check passed!")
    print(f"   Status: {response.json()['status']}")
else:
    print(f"   ❌ Failed with status {response.status_code}")

# Test 2: Root Endpoint
print("\n2. Testing Root Endpoint...")
response = client.get("/")
if response.status_code == 200:
    print("   ✅ Root endpoint works!")
    print(f"   Message: {response.json()['message']}")
else:
    print(f"   ❌ Failed with status {response.status_code}")

# Test 3: Register Patient
print("\n3. Testing Patient Registration...")
patient_data = {
    "email": "test.patient@carely.ai",
    "password": "SecurePassword123",
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "1990-01-15",
    "phone_number": "+1-555-0100",
    "blood_type": "O+",
    "allergies": "None",
    "preferred_language": "en"
}
response = client.post("/api/v1/auth/register", json=patient_data)
if response.status_code == 201:
    print("   ✅ Patient registered successfully!")
    patient = response.json()
    print(f"   Patient ID: {patient['id']}")
    print(f"   Name: {patient['first_name']} {patient['last_name']}")
    print(f"   Email: {patient['email']}")
elif response.status_code == 400:
    print("   ⚠️  Patient already exists (expected if running multiple times)")
else:
    print(f"   ❌ Failed with status {response.status_code}")
    print(f"   Error: {response.json()}")

# Test 4: Login
print("\n4. Testing Login...")
login_data = {
    "username": "test.patient@carely.ai",
    "password": "SecurePassword123"
}
response = client.post("/api/v1/auth/login", data=login_data)
if response.status_code == 200:
    print("   ✅ Login successful!")
    token_data = response.json()
    token = token_data["access_token"]
    print(f"   Token: {token[:30]}...")
    
    # Test 5: Protected Endpoint
    print("\n5. Testing Protected Endpoint (Get Current User)...")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/auth/me", headers=headers)
    if response.status_code == 200:
        print("   ✅ Authorization works!")
        user = response.json()
        print(f"   Logged in as: {user['first_name']} {user['last_name']}")
    else:
        print(f"   ❌ Failed with status {response.status_code}")
    
    # Test 6: Create Appointment
    print("\n6. Testing Appointment Creation...")
    appointment_data = {
        "patient_id": 1,
        "doctor_name": "Dr. Sarah Johnson",
        "appointment_type": "consultation",
        "scheduled_time": "2025-11-20T10:00:00",
        "duration_minutes": 30,
        "reason": "Annual checkup",
        "is_virtual": False
    }
    response = client.post("/api/v1/appointments/", json=appointment_data, headers=headers)
    if response.status_code == 201:
        print("   ✅ Appointment created!")
        appt = response.json()
        print(f"   Doctor: {appt['doctor_name']}")
        print(f"   Time: {appt['scheduled_time']}")
        print(f"   Status: {appt['status']}")
    else:
        print(f"   ❌ Failed with status {response.status_code}")
        print(f"   Error: {response.json()}")
    
    # Test 7: Create Support Ticket
    print("\n7. Testing Support Ticket Creation...")
    ticket_data = {
        "category": "technical",
        "subject": "Cannot access medical records",
        "description": "I am unable to view my medical records in the portal",
        "language": "en",
        "priority": "medium",
        "contact_email": "test.patient@carely.ai"
    }
    response = client.post("/api/v1/support-tickets/", json=ticket_data, headers=headers)
    if response.status_code == 201:
        print("   ✅ Support ticket created!")
        ticket = response.json()
        print(f"   Ticket #: {ticket['ticket_number']}")
        print(f"   Status: {ticket['status']}")
        print(f"   Priority: {ticket['priority']}")
    else:
        print(f"   ❌ Failed with status {response.status_code}")
else:
    print(f"   ❌ Login failed with status {response.status_code}")

print("\n" + "=" * 60)
print("✨ Testing Complete!")
print("=" * 60)
print("\n📖 For interactive testing, run:")
print("   uvicorn app.main:app --reload")
print("   Then visit: http://localhost:8000/docs")
print("\n📚 See TEST_GUIDE.md for comprehensive testing instructions")
print("=" * 60)


