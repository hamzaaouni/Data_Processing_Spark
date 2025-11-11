# 🌐 Sharing Dashboard on Network

## How to Access Dashboard from Another Laptop

### On Your Laptop (Host):

1. **Backend is already running** on `http://192.168.6.92:5000` ✅

2. **Start Frontend** (if not already running):
   ```powershell
   cd dashboard_frontend
   npm start
   ```

3. **Note the IP addresses:**
   - Backend API: `http://192.168.6.92:5000`
   - Frontend Dashboard: `http://192.168.6.92:3000` (React will show this)

### On Another Laptop (Same WiFi):

1. **Open browser** and go to:
   ```
   http://192.168.6.92:3000
   ```

2. **The dashboard will automatically connect to:**
   ```
   http://192.168.6.92:5000
   ```

## How It Works

The frontend now automatically detects:
- **If accessed via `localhost:3000`** → Uses `localhost:5000` for API
- **If accessed via `192.168.6.92:3000`** → Uses `192.168.6.92:5000` for API

This means it works automatically for both local and network access!

## Important Notes

### ✅ Backend Must Be Accessible on Network

Your backend is already configured correctly:
- Running on `0.0.0.0` (all interfaces)
- Accessible at `http://192.168.6.92:5000`

### ✅ Frontend Must Be Accessible on Network

When you run `npm start`, React will show:
```
On Your Network:  http://192.168.6.92:3000
```

**If it only shows `localhost:3000`:**
- React might be binding to localhost only
- Check your firewall settings
- Make sure both devices are on the same WiFi network

### 🔥 Firewall Settings

**Windows Firewall might block connections:**

1. Open **Windows Defender Firewall**
2. Click **Allow an app through firewall**
3. Allow **Python** and **Node.js** through firewall
4. Or temporarily disable firewall for testing

## Testing

### From Your Laptop:
- `http://localhost:3000` → Dashboard
- `http://localhost:5000` → API

### From Another Laptop:
- `http://192.168.6.92:3000` → Dashboard
- `http://192.168.6.92:5000` → API (test this first!)

## Troubleshooting

### "Cannot connect to API" on another laptop

1. **Test API directly:**
   - On the other laptop, open: `http://192.168.6.92:5000/api/health`
   - Should show: `{"status":"ok"}`

2. **If API doesn't work:**
   - Check Windows Firewall
   - Verify backend is running
   - Make sure both devices are on same WiFi

3. **If dashboard doesn't load:**
   - Check browser console (F12) for errors
   - Verify the API URL in console logs

### React only shows localhost

If React only shows `localhost:3000`:
- It's still accessible via network IP
- Just use `http://192.168.6.92:3000` directly
- The frontend will automatically detect and use the network IP for API calls

## Quick Test

1. **On your laptop:** Open `http://192.168.6.92:5000/api/health`
2. **On other laptop:** Open `http://192.168.6.92:5000/api/health`
3. Both should show: `{"status":"ok"}`

If step 2 works, the dashboard will work too!

