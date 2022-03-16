from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData
import os


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@postgres:5432/appraisal"
# SQLALCHEMY_DATABASE_URL = "postgresql://appraisal2:password@db:8434/appraisal"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
metadata = MetaData()
