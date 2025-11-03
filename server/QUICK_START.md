# 🚀 Carely Backend - Quick Start Guide

## ⚡ Fastest Way to Test

### Option 1: Run Helper Scripts (Easiest!)

**Run Tests:**
```bash
./run_tests.sh
```

**Start Server:**
```bash
./run_server.sh
```
Then visit: **http://localhost:8000/docs**

---

## 🐍 Manual Testing

### From Terminal:
```bash
cd /Users/arvindrangarajan/PythonLab/Carely/backend
source venv/bin/activate
python quick_test.py
```

### Start Server:
```bash
cd /Users/arvindrangarajan/PythonLab/Carely/backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🎯 Running from Cursor/VS Code

### Issue: "ModuleNotFoundError: No module named 'app'"

**Solution:** Don't click the Run button on individual files. Instead:

### Method 1: Use Debug Configurations
1. Go to the **Run and Debug** panel (left sidebar)
2. Select from dropdown:
   - **"Python: Quick Test"** - Run tests
   - **"Python: FastAPI"** - Start server
3. Click the green play button ▶️

### Method 2: Use Integrated Terminal
1. Open terminal in Cursor (`` Ctrl + ` ``)
2. Run:
   ```bash
   cd Carely/backend
   source venv/bin/activate
   python quick_test.py
   ```

### Method 3: Change Python Interpreter
1. Press **`Cmd + Shift + P`**
2. Type: **`Python: Select Interpreter`**
3. Choose: **`./Carely/backend/venv/bin/python`**
4. Look at bottom-right corner to verify it changed

---

## ✅ Test Results

When tests run successfully, you'll see:

```
============================================================
🏥 Carely AI Backend - Quick Test
============================================================

1. Testing Health Endpoint...
   ✅ Health check passed!

2. Testing Root Endpoint...
   ✅ Root endpoint works!

3. Testing Patient Registration...
   ✅ Patient registered successfully!
   (or ⚠️ Patient already exists)

4. Testing Login...
   ✅ Login successful!

5. Testing Protected Endpoint...
   ✅ Authorization works!

6. Testing Appointment Creation...
   ✅ Appointment created!

7. Testing Support Ticket Creation...
   ✅ Support ticket created!

============================================================
✨ Testing Complete!
============================================================
```

---

## 🌐 Interactive API Testing

After starting the server:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **API Root:** http://localhost:8000

### Quick Test in Browser:
1. Visit http://localhost:8000/docs
2. Try the **GET /api/v1/health/** endpoint
3. Click "Try it out" → "Execute"
4. You should see a healthy status response! ✅

---

## 🔧 Troubleshooting

### "ModuleNotFoundError: No module named 'fastapi'"
**Solution:** Activate the virtual environment first!
```bash
source venv/bin/activate
```

### "ModuleNotFoundError: No module named 'app'"
**Solution:** Run from the backend directory:
```bash
cd /Users/arvindrangarajan/PythonLab/Carely/backend
```

### "Extra inputs are not permitted" (Google API keys)
**Solution:** Already fixed! The config now ignores extra env vars.

### Cursor using wrong Python interpreter
**Solution:** 
1. Bottom-right corner → Click Python version
2. Select: `./Carely/backend/venv/bin/python`

---

## 📚 More Information

- **Detailed Testing:** See [TEST_GUIDE.md](./TEST_GUIDE.md)
- **Deployment:** See [../DEPLOYMENT.md](../DEPLOYMENT.md)
- **README:** See [README.md](./README.md)

---

## 🎉 You're Ready!

The backend is fully functional with:
- ✅ Patient Management
- ✅ Authentication (JWT)
- ✅ Appointments
- ✅ Medical Records
- ✅ Support Tickets
- ✅ Interactive API Docs

Happy coding! 🚀

