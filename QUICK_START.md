# 🚀 Quick Start - Correct URLs

## ✅ Step-by-Step

### 1. Start Backend (Terminal 1)
```powershell
python dashboard_backend.py
```

**Wait for this message:**
```
API will be available at: http://localhost:5000
```

### 2. Test Backend (Optional)
Open in browser: **http://localhost:5000**

You should see:
```json
{
  "message": "Spark Streaming Lab Dashboard API",
  "status": "running",
  "endpoints": {...}
}
```

### 3. Start Frontend (Terminal 2)
```powershell
cd dashboard_frontend
npm start
```

**Browser will automatically open:** **http://localhost:3000**

---

## 📍 Correct URLs

| Service | URL | What You'll See |
|---------|-----|-----------------|
| **Backend API** | `http://localhost:5000` | API information |
| **Backend Health** | `http://localhost:5000/api/health` | `{"status":"ok"}` |
| **Frontend Dashboard** | `http://localhost:3000` | **← This is your dashboard!** |

---

## ⚠️ Common Mistakes

❌ **Wrong:** `http://localhost:5000/dashboard`  
✅ **Correct:** `http://localhost:3000` (frontend)

❌ **Wrong:** `http://localhost:3000/api/data/overview`  
✅ **Correct:** `http://localhost:5000/api/data/overview` (backend API)

❌ **Wrong:** Trying to access dashboard on port 5000  
✅ **Correct:** Dashboard is on port 3000, API is on port 5000

---

## 🔍 If You See "URL Not Found"

1. **Check which URL you're using:**
   - Dashboard = `http://localhost:3000` ✅
   - API = `http://localhost:5000` ✅

2. **Verify backend is running:**
   - Open: `http://localhost:5000`
   - Should show API info (not error)

3. **Verify frontend is running:**
   - Check Terminal 2 for "Compiled successfully!"
   - Browser should auto-open to `http://localhost:3000`

4. **Check browser console (F12):**
   - Look for red errors
   - Check Network tab for failed requests

---

## ✅ Success Indicators

**Backend Running:**
- Terminal shows: "Running on http://127.0.0.1:5000"
- Browser at `http://localhost:5000` shows JSON

**Frontend Running:**
- Terminal shows: "Compiled successfully!"
- Browser opens to `http://localhost:3000`
- Dashboard displays with charts

---

## 🆘 Still Having Issues?

See `TROUBLESHOOTING.md` for detailed help!

