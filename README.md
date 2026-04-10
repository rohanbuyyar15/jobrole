# AI Resume Analysis & Job Role Prediction System

A complete Next.js (Frontend) and Flask (Backend) application.

## Prerequisites
- Node.js
- Python 3.10+

## 1. Running Locally (Backend)
1. Open a terminal and navigate to the `backend` folder.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask server:
   ```bash
   python app.py
   ```
   (Server will run on `http://localhost:5000`)

## 2. Running Locally (Frontend)
1. Open a new terminal and navigate to the `frontend` folder.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Create a `.env.local` file inside the `frontend` folder and set the backend URL:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:5000
   ```
4. Run the Next.js app:
   ```bash
   npm run dev
   ```
   (App will run on `http://localhost:3000`)

---

## Deployment Guide (Production)

### Backend Deployment (Render)
1. Push your code to a GitHub repository.
2. Go to [Render](https://render.com/) and create a new **Web Service**.
3. Connect your GitHub repository.
4. Set the Root Directory to `backend` (if supported by Render settings) or make the repo backend-specific.
5. Set Build Command: `pip install -r requirements.txt`
6. Set Start Command: `gunicorn app:app`
7. Ensure the Python Version is read from `runtime.txt` (3.10.0).
8. Deploy and copy the Render URL (e.g., `https://resume-api-xxxx.onrender.com`).

### Frontend Deployment (Vercel)
1. Push your code to the GitHub repository.
2. Go to [Vercel](https://vercel.com/) and click **Add New Project**.
3. Import your GitHub repository.
4. Set the Framework Preset to **Next.js**.
5. Set the Root Directory to `frontend`.
6. Add Environment Variable:
   - Name: `NEXT_PUBLIC_API_URL`
   - Value: `YOUR_RENDER_BACKEND_URL` (from the step above)
7. Click **Deploy**.
