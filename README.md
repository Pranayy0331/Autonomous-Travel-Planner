# Autonomous Travel Planner

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

Autonomous Travel Planner is a full-stack, AI-powered vacation builder web application. It automates the creation of custom trip itineraries, budgets, packing lists, weather projections, maps, and integrates a conversational AI companion.

Built using **Python Flask**, **SQLite**, **SQLAlchemy**, **Leaflet.js**, and custom modern web standards (HTML5/CSS3/JavaScript).

---

## Key Features

1. **Secure Authentication**: Built-in User registration, password complexity checks, secure hashing, and cookie session tracking.
2. **AI Travel Schedule Generator**: Complete day-wise plans with locations, timing breakdown, attractions, hotels, and restaurant selections.
3. **Interactive Maps**: Client-side **Leaflet.js** map centered on destinations (no API keys required).
4. **Checked Packing List**: Asynchronous interactive packing lists. Check off items directly on screen; states are saved in the DB instantly.
5. **AI Assistant Chatbot**: Sidebar companion that answers travel queries (weather, emergency info, pricing) and alters itineraries live.
6. **Dual Mode Theme**: Responsive Light and Dark mode selector with persistence.
7. **Admin Dashboard**: Consolidated inspector showing accounts and travel plan records with instant AJAX deletions.

---

## Project Structure

```
autonomous-travel-planner/
├── app.py                     # Flask main application logic & endpoints
├── models.py                  # SQLAlchemy SQLite database definitions
├── auth.py                    # Password validation and authentication routines
├── travel_generator.py        # AI generator core and Chatbot handler
├── requirements.txt           # Required Python packages configuration
├── README.md                  # Setup guidelines and product description
├── static/
│   ├── css/
│   │   └── style.css          # Design stylesheet with layout templates
│   └── js/
│       └── main.js            # Main global animations, alerts, and theme script
└── templates/
    ├── base.html              # Core parent visual master template
    ├── index.html             # Landing page
    ├── login.html             # Secure user log in portal
    ├── register.html          # Registration form with checks
    ├── dashboard.html         # User workspace panels
    ├── planner.html           # Parameters input wizard with progress bars
    ├── trip_detail.html       # Tabbed itinerary detail pages, maps, & chatbot
    ├── history.html           # Personal past trip listings
    ├── profile.html           # Travel profile preferences & password update
    └── admin.html             # Management console tables
```

---

## Setup & Running Locally

### 1. Prerequisites
- **Python 3.8 or higher** must be installed on your operating system.

### 2. Environment Setup & Dependency Installation
Navigate to the project root directory and run the following terminal commands:

```bash
# Create virtual environment (optional but recommended)
python -m venv venv
# Activate virtual environment (Windows Powershell)
.\venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt
```

### 3. Launch Flask Server
Run the Flask server script:
```bash
python app.py
```
The server will boot and begin listening on **`http://127.0.0.1:5000/`**.

### 4. Default Seeded Accounts
For testing and validation, a default **Admin** account is automatically created upon initial launch:
- **Username / Email**: `admin` or `admin@travelplanner.com`
- **Password**: `Password123`

Log in using the above credentials to gain full access to both the dashboard and the **Admin Console** (accessible from the navigation bar).

---

## Deploying to Render.com (Live Public Link)

You can deploy this project directly to **Render** in just a few minutes:

### Option 1: Automatic Blueprint (Recommended)
1. Push your project code to a **GitHub** or **GitLab** repository.
2. Sign in to your [Render Dashboard](https://dashboard.render.com/).
3. Click **New +** and select **Blueprint**.
4. Connect your repository. Render will automatically detect `render.yaml` and configure:
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Click **Apply**. Render will build and deploy the app, giving you a live URL like:
   `https://autonomous-travel-planner.onrender.com`

### Option 2: Manual Web Service
1. In Render Dashboard, click **New +** -> **Web Service**.
2. Connect your GitHub repository.
3. Configure the following fields:
   - **Name**: `autonomous-travel-planner`
   - **Runtime**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: `Free`
4. Under **Environment Variables**, add:
   - `PYTHON_VERSION`: `3.10.12`
   - `SECRET_KEY`: *(click generate or enter a random string)*
   - `FLASK_DEBUG`: `false`
5. Click **Create Web Service**. Once deployment finishes, your live link will be displayed at the top of the service page!

