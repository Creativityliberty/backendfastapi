"""
AWS RDS IAM Authentication for PostgreSQL
"""
import os
import boto3
from botocore.credentials import AssumeRoleCredentialFetcher
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import logging

logger = logging.getLogger(__name__)

def get_rds_iam_token():
    """Get IAM authentication token for AWS RDS PostgreSQL"""
    try:
        # Get AWS credentials
        aws_region = os.getenv("AWS_REGION", "us-east-1")
        pg_host = os.getenv("POSTGRES_SERVER")
        pg_port = os.getenv("POSTGRES_PORT", "5432")
        pg_user = os.getenv("POSTGRES_USER", "postgres")
        
        # Create RDS client
        client = boto3.client('rds', region_name=aws_region)
        
        # Generate auth token
        token = client.generate_db_auth_token(
            DBHostname=pg_host,
            Port=pg_port,
            Username=pg_user,
            Region=aws_region
        )
        
        return token
    except Exception as e:
        logger.error(f"Error generating RDS IAM token: {e}")
        # Fallback to regular password if IAM fails
        return os.getenv("POSTGRES_PASSWORD", "")

def get_database_url():
    """Get database URL with IAM authentication"""
    pg_host = os.getenv("POSTGRES_SERVER")
    pg_port = os.getenv("POSTGRES_PORT", "5432")
    pg_db = os.getenv("POSTGRES_DB", "app")
    pg_user = os.getenv("POSTGRES_USER", "postgres")
    pg_sslmode = os.getenv("PGSSLMODE", "require")
    
    # Use IAM token for authentication
    password = get_rds_iam_token()
    
    return f"postgresql+asyncpg://{pg_user}:{password}@{pg_host}:{pg_port}/{pg_db}?ssl={pg_sslmode}"

# Create async engine
engine = create_async_engine(
    get_database_url(),
    echo=True,
    future=True,
)

# Create session factory
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db() -> AsyncSession:
    """Get database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
