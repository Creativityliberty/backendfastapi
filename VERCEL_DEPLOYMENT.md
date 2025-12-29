# Vercel Deployment Guide

This guide explains how to deploy the Full Stack FastAPI application to Vercel.

## Architecture

- **Frontend**: React + Vite deployed to Vercel
- **Backend**: FastAPI deployed to Vercel Serverless Functions
- **Database**: PostgreSQL (use Vercel Postgres or external provider)

## Prerequisites

1. Vercel account: https://vercel.com
2. GitHub repository connected (already done)
3. PostgreSQL database (Vercel Postgres or external)

## Deployment Steps

### 1. Deploy Backend (FastAPI)

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy backend from backend directory
cd backend
vercel --prod
```

Or use the Vercel Dashboard:
1. Go to https://vercel.com/dashboard
2. Click "Add New" → "Project"
3. Import your GitHub repository
4. Select "Backend" as root directory
5. Add environment variables (see below)
6. Deploy

### 2. Deploy Frontend (React)

1. Go to https://vercel.com/dashboard
2. Click "Add New" → "Project"
3. Import your GitHub repository
4. Select "Frontend" as root directory
5. Add environment variable: `VITE_API_URL=https://your-backend-url.vercel.app`
6. Deploy

### 3. Environment Variables

**Backend (.env):**
```
ENVIRONMENT=production
SECRET_KEY=<your-secret-key>
FIRST_SUPERUSER=admin@example.com
FIRST_SUPERUSER_PASSWORD=<your-password>
POSTGRES_SERVER=<your-postgres-host>
POSTGRES_PORT=5432
POSTGRES_DB=app
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<your-postgres-password>
```

**Frontend (.env):**
```
VITE_API_URL=https://your-backend-url.vercel.app
```

### 4. Database Setup

**Option A: Vercel Postgres**
1. In Vercel Dashboard, go to Storage
2. Create a new Postgres database
3. Copy connection string to backend environment variables

**Option B: External PostgreSQL**
- Use Railway, Render, or any PostgreSQL provider
- Update `POSTGRES_SERVER` and credentials in backend env vars

### 5. Run Migrations

After deployment, run database migrations:

```bash
# Locally (with production DB credentials)
cd backend
alembic upgrade head
```

Or add a post-deployment script in `backend/vercel.json`.

## Troubleshooting

- **Backend not starting**: Check environment variables are set correctly
- **Frontend API errors**: Verify `VITE_API_URL` matches your backend URL
- **Database connection**: Ensure PostgreSQL is accessible from Vercel IPs
- **CORS errors**: Update `BACKEND_CORS_ORIGINS` in backend .env

## Useful Links

- Vercel Docs: https://vercel.com/docs
- FastAPI on Vercel: https://vercel.com/guides/deploying-python
- Vercel Postgres: https://vercel.com/storage/postgres
