# 🚒 Fire Department Analytics - Professional React Application

## ✨ What You're Getting

A **production-ready, professional full-stack application** with:

- ✅ **React 18** with Vite (fast, modern)
- ✅ **Material-UI** (professional design system)
- ✅ **React Router** (smooth navigation)
- ✅ **Recharts** (beautiful interactive charts)
- ✅ **Node.js + Express** backend (REST API)
- ✅ **Python Analytics** (smart reports)
- ✅ **JSON Database** (no setup needed!)

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Dependencies

```bash
# Backend
cd backend
npm install
cd ..

# Frontend
cd frontend
npm install
cd ..
```

### Step 2: Start Backend

```bash
cd backend
node server.js
```

You should see:
```
🚒 ====================================
   Fire Department Analytics API
   ====================================
   
   🚀 Server: http://localhost:3001
```

### Step 3: Start Frontend (New Terminal)

```bash
cd frontend
npm run dev
```

You should see:
```
  VITE v5.0.8  ready in 500 ms

  ➜  Local:   http://localhost:5173/
```

### Step 4: Open Browser

Go to: **http://localhost:5173**

**You should see a beautiful React dashboard! 🎉**

---

## 📁 Project Structure

```
fire-dept-react-app/
├── frontend/               # React Application
│   ├── src/
│   │   ├── components/
│   │   │   └── Layout.jsx           # App layout with navigation
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx        # Main dashboard with KPIs
│   │   │   ├── Analytics.jsx        # Analytics tables
│   │   │   ├── Vendors.jsx          # Vendor performance
│   │   │   ├── Geographic.jsx       # Geographic visualization
│   │   │   └── Upload.jsx           # File upload
│   │   ├── services/
│   │   │   └── api.js               # API service layer
│   │   ├── App.jsx                  # Main app component
│   │   ├── main.jsx                 # Entry point
│   │   └── index.css                # Global styles
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
│
├── backend/                # Node.js Backend
│   ├── server.js                    # Express server
│   ├── routes/                      # API routes
│   └── package.json
│
├── python-engine/          # Python Analytics
│   ├── analytics.py                 # Data processing
│   ├── report_generator.py          # PDF/Excel reports
│   └── api_bridge.py                # API integration
│
├── data/                   # JSON Database
│   ├── incidents.json               # 500 incidents
│   ├── vendors.json                 # 50 vendors
│   ├── vendor_deliveries.json       # 200 deliveries
│   └── fire_stations.json           # 138 stations
│
└── reports/                # Generated reports
    └── (PDF and Excel files)
```

---

## 🎨 Features

### 🏠 Dashboard Page
- **8 Animated KPI Cards**
  - Total Incidents
  - Recent Incidents (30 days)
  - Average Response Time
  - Critical Incidents
  - Total Casualties
  - Total Injuries
  - Active Stations
  - Property Damage

- **4 Interactive Charts**
  - Bar Chart: Incident Distribution by Type
  - Pie Chart: Severity Breakdown
  - Line Chart: Monthly Trends
  - Bar Chart: Top Incident Causes

### 📊 Analytics Page
- State-wise Analysis Table (Top 10 states)
- Response Time Analysis by Severity
- Color-coded severity badges
- Sortable columns

### 🏢 Vendors Page
- Vendor Performance Leaderboard
- Rankings with on-time percentages
- Quality scores and defect tracking
- Interactive bar chart comparison

### 🗺️ Geographic Page
- State-wise incident distribution chart
- Heat map placeholder (ready for map integration)
- Top 10 states visualization

### 📤 Upload Page
- Drag & drop file upload
- CSV/Excel support
- Upload status feedback
- Success/error messages

### 📄 Report Generation (Header Buttons)
- **Download PDF** - Professional multi-page report
- **Download Excel** - Interactive workbook with charts

---

## 🔧 Configuration

### Backend Environment
The backend is pre-configured and works out of the box with JSON files.

No database setup needed!

### Frontend Proxy
Vite is configured to proxy API calls to the backend automatically.

---

## 📊 API Endpoints

All available at `http://localhost:3001/api`:

### Dashboard
- `GET /dashboard/kpis` - Dashboard KPIs

### Analytics
- `GET /analytics/incidents-by-type`
- `GET /analytics/incidents-by-severity`
- `GET /analytics/by-state`
- `GET /analytics/monthly-trends`
- `GET /analytics/response-time`
- `GET /analytics/top-causes`
- `GET /analytics/geographic`

### Vendors
- `GET /vendors/performance`

### Reports
- `POST /reports/generate-pdf`
- `POST /reports/generate-excel`

### Upload
- `POST /data/upload`

---

## 🎯 What Makes This Professional

### Frontend (React)
- ✅ **Proper component structure**
- ✅ **React Router** for navigation
- ✅ **Material-UI** for consistent design
- ✅ **Service layer** for API calls
- ✅ **Loading states** and error handling
- ✅ **Responsive design**
- ✅ **Dark theme** (professional look)

### Backend (Node.js)
- ✅ **Express.js** web framework
- ✅ **CORS** enabled
- ✅ **Error handling** middleware
- ✅ **Python integration** for analytics
- ✅ **File upload** support

### Code Quality
- ✅ **Clean code** structure
- ✅ **Reusable components**
- ✅ **Proper state management**
- ✅ **Error boundaries**
- ✅ **Production-ready**

---

## 🐛 Troubleshooting

### Backend Won't Start
```
Error: Cannot find module 'express'
```
**Solution:**
```bash
cd backend
rm -rf node_modules package-lock.json
npm install
```

### Frontend Won't Start
```
Error: Cannot find module 'vite'
```
**Solution:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### API Calls Failing
**Check:**
1. Backend is running on port 3001
2. Check backend terminal for errors
3. Open browser console (F12) for errors

### Charts Not Showing
**Wait for data to load.** If still not showing:
1. Check backend is running
2. Check browser console for errors
3. Make sure backend terminal shows no errors

---

## 🚀 Demo Tips

### For Your Client Presentation:

1. **Start with Dashboard** (Wow factor!)
   - Show live KPI cards
   - Point out the interactive charts
   - Click on different chart elements

2. **Navigate to Analytics**
   - Show state-wise data
   - Explain response time analysis

3. **Show Vendor Performance**
   - Rankings
   - Performance metrics
   - Visual comparison chart

4. **Generate Reports**
   - Click "PDF" button → Show professional report
   - Click "Excel" button → Open Excel with charts

5. **Explain Architecture**
   - React frontend (modern, fast)
   - Node.js backend (scalable)
   - Python analytics (smart reports)
   - Easy to add database later

---

## 📈 Next Steps (After Demo Success)

If client approves, you can upgrade to:

1. **PostgreSQL Database**
   - Replace JSON files
   - Add Sequelize ORM
   - Full CRUD operations

2. **Authentication**
   - User login
   - Role-based access
   - JWT tokens

3. **Real-time Updates**
   - WebSockets
   - Live dashboard
   - Push notifications

4. **Deployment**
   - Frontend: Vercel (free)
   - Backend: Railway/Render (free tier)
   - Database: Supabase (free tier)

---

## 🎉 Success Checklist

Before demo, verify:

- [ ] Backend starts without errors
- [ ] Frontend opens at localhost:5173
- [ ] Dashboard loads with data
- [ ] All 8 KPI cards show numbers
- [ ] Charts render properly
- [ ] Can navigate between pages
- [ ] PDF download works
- [ ] Excel download works
- [ ] No errors in browser console
- [ ] Looks professional and polished

---

## 💡 Tips

### Development Mode
- Frontend has **Hot Module Replacement** (instant updates)
- Backend needs manual restart after code changes
- Use `npm run dev` in backend for auto-restart with nodemon

### Production Build
```bash
cd frontend
npm run build
```
Creates optimized production build in `dist/` folder

---

## ✨ You're All Set!

Your professional Fire Department Analytics application is ready!

**Open two terminals:**
1. Terminal 1: `cd backend && node server.js`
2. Terminal 2: `cd frontend && npm run dev`

**Open browser:**
- http://localhost:5173

**Enjoy your beautiful React app! 🚀**

---

## 📞 Need Help?

Common issues:
1. Port already in use → Change PORT in backend/.env
2. CORS errors → Backend CORS is configured for localhost:5173
3. API errors → Check backend terminal for Python errors

**Your demo is going to be amazing! 🔥**
