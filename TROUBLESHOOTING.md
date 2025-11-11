# 🔧 Dashboard Troubleshooting Guide

## Error: "The requested URL was not found on the server"

This error usually means one of these issues:

### ✅ Solution 1: Check if Backend is Running

1. **Open a new PowerShell window**
2. **Run:** `python dashboard_backend.py`
3. **You should see:**
   ```
   API will be available at: http://localhost:5000
   ```
4. **Test the API:** Open your browser and go to:
   - `http://localhost:5000` - Should show API info
   - `http://localhost:5000/api/health` - Should show `{"status":"ok"}`

### ✅ Solution 2: Check the Correct URLs

**Backend API (Flask):**
- Root: `http://localhost:5000`
- Health: `http://localhost:5000/api/health`
- Data: `http://localhost:5000/api/data/overview`

**Frontend Dashboard (React):**
- Dashboard: `http://localhost:3000`

**Important:** Make sure you're accessing the correct URL!

### ✅ Solution 3: Check Port Conflicts

**Port 5000 (Backend) in use?**
```powershell
# Check what's using port 5000
netstat -ano | findstr :5000
```

**Port 3000 (Frontend) in use?**
- React will automatically ask to use a different port (like 3001)
- Just say yes, or close the app using port 3000

### ✅ Solution 4: Verify Data Files Exist

The backend needs data files to work:

```powershell
# Check if data files exist
dir stock_stream\batch_*.json
```

If no files exist:
1. Run the Spark lab first: `python lab7.py` or `.\run-docker.ps1`
2. Wait for it to generate batch files
3. Then start the dashboard

### ✅ Solution 5: Check Browser Console

1. Open the dashboard in browser (`http://localhost:3000`)
2. Press `F12` to open Developer Tools
3. Go to **Console** tab
4. Look for error messages
5. Go to **Network** tab
6. Check if API calls are failing (red entries)

### ✅ Solution 6: Restart Everything

1. **Stop both services** (Ctrl+C in both terminals)
2. **Restart backend:**
   ```powershell
   python dashboard_backend.py
   ```
3. **Wait 3 seconds**
4. **Test backend:** Open `http://localhost:5000` in browser
5. **Restart frontend:**
   ```powershell
   cd dashboard_frontend
   npm start
   ```

## Common Issues

### ❌ "Cannot connect to API"
- **Fix:** Make sure `python dashboard_backend.py` is running
- **Test:** Visit `http://localhost:5000/api/health`

### ❌ "No data available"
- **Fix:** Run Spark lab first to generate data
- **Check:** `stock_stream/` folder should have `batch_*.json` files

### ❌ "ModuleNotFoundError: No module named 'flask'"
- **Fix:** Run `pip install flask flask-cors`

### ❌ Frontend shows blank page
- **Check:** Browser console (F12) for errors
- **Check:** Network tab for failed API calls
- **Verify:** Backend is running on port 5000

### ❌ Port already in use
- **Backend (5000):** Close other apps or change port in `dashboard_backend.py`
- **Frontend (3000):** React will suggest another port, accept it

## Quick Diagnostic Commands

```powershell
# 1. Check if backend is running
curl http://localhost:5000/api/health
# OR open in browser: http://localhost:5000/api/health

# 2. Check if data files exist
dir stock_stream\batch_*.json | measure

# 3. Check Python packages
python -c "import flask; import flask_cors; print('OK')"

# 4. Check Node.js
node --version
npm --version
```

## Still Having Issues?

1. **Check both terminals are running:**
   - Terminal 1: Backend (Flask)
   - Terminal 2: Frontend (React)

2. **Verify URLs:**
   - Backend: `http://localhost:5000`
   - Frontend: `http://localhost:3000`

3. **Check for errors in:**
   - Backend terminal (Python errors)
   - Frontend terminal (npm errors)
   - Browser console (F12)

4. **Make sure data exists:**
   - `stock_stream/` folder has `batch_*.json` files
   - If not, run Spark lab first

