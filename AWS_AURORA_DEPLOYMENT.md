# AWS Aurora PostgreSQL Deployment Guide

This guide explains how to deploy the Full Stack FastAPI application with AWS Aurora PostgreSQL database on Vercel.

## Architecture

- **Frontend**: React + Vite deployed to Vercel
- **Backend**: FastAPI deployed to Vercel Serverless Functions
- **Database**: AWS Aurora PostgreSQL with IAM authentication

## Environment Variables for Backend

Add these environment variables to your Vercel backend project:

### AWS Aurora Credentials
```
AWS_ACCOUNT_ID="641944125102"
AWS_REGION="us-east-1"
AWS_RESOURCE_ARN="arn:aws:rds:us-east-1:641944125102:cluster:fastapi1db"
AWS_ROLE_ARN="arn:aws:iam::641944125102:role/Vercel/access-fastapi1db"
PGDATABASE="postgres"
PGHOST="provisioning"
PGPORT="5432"
PGSSLMODE="require"
PGUSER="postgres"
```

### Application Configuration
```
ENVIRONMENT=production
SECRET_KEY=NUoNcuvS0VH-wyojBw3sI4DLK8N6L1AniimXwfnl8d0
FIRST_SUPERUSER=admin@example.com
FIRST_SUPERUSER_PASSWORD=Ixdyfmpx_pnhsV1Dq1LHe47xlZ-dXIhvyMgncSq7hhw
POSTGRES_SERVER=provisioning
POSTGRES_PORT=5432
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=0EHavgt33T87dhwvs7Kp8ZsZjBp4W_SaPUiKQ_S6QQM
BACKEND_CORS_ORIGINS=http://localhost:5173,https://your-frontend-url.vercel.app
```

## Deployment Steps

### 1. Deploy Backend to Vercel

1. Go to Vercel Dashboard: https://vercel.com/dashboard
2. Click "Add New" → "Project"
3. Select your GitHub repository: `Creativityliberty/backendfastapi`
4. Set Framework Preset: FastAPI
5. Set Root Directory: `backend`
6. Add all environment variables above
7. Click "Deploy"

### 2. Deploy Frontend to Vercel

1. Click "Add New" → "Project"
2. Select the same GitHub repository
3. Set Root Directory: `frontend`
4. Add environment variable: `VITE_API_URL=https://your-backend-url.vercel.app`
5. Click "Deploy"

### 3. Run Database Migrations

After backend deployment, run migrations:

```bash
# Pull environment variables locally
vercel env pull

# Run migrations
cd backend
alembic upgrade head
```

## IAM Authentication

The backend uses AWS RDS IAM authentication for secure database connections:

- No hardcoded passwords in code
- Temporary tokens generated automatically
- SSL connection required
- Role-based access control

## Testing the Deployment

1. **Backend API**: Visit `https://your-backend-url.vercel.app/docs`
2. **Frontend**: Visit `https://your-frontend-url.vercel.app`
3. **Login**: Use admin@example.com with your superuser password

## Troubleshooting

### Database Connection Issues
- Check AWS IAM role permissions
- Verify Vercel OIDC federation is configured
- Ensure SSL mode is set to "require"
- Check Aurora cluster is in "Available" status

### CORS Errors
- Update `BACKEND_CORS_ORIGINS` to include your frontend URL
- Ensure frontend URL is added to the environment variables

### Deployment Failures
- Check all environment variables are set correctly
- Verify AWS credentials are properly configured
- Check Vercel logs for specific error messages

## Security Notes

- IAM tokens are temporary (15 minutes max)
- SSL connections are enforced
- No database passwords stored in code
- Role-based access through AWS IAM

## Monitoring

- Check Vercel logs for deployment issues
- Monitor AWS Aurora metrics in AWS Console
- Use Sentry for error tracking (if configured)
