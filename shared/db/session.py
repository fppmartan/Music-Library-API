import os 
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession 
from dotenv import load_dotenv 
 
load_dotenv() 
 
DATABASE_URL = os.getenv("DATABASE_URL") 
 
if DATABASE_URL.startswith("postgresql://"): 
    DATABASE_URL = DATABASE_URL.replace("postgresql://", 
"postgresql+asyncpg://", 1) 
 
if "sslmode=require" in DATABASE_URL: 
    DATABASE_URL = DATABASE_URL.replace("?sslmode=require", 
"").replace("&sslmode=require", "") 
    DATABASE_URL += "?ssl=require" 
 
engine = create_async_engine(DATABASE_URL, echo=False) 
 
AsyncSessionFactory = async_sessionmaker( 
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False, 
)