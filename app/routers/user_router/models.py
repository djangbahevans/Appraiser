import secrets
from datetime import datetime

from app.database import Base, SessionLocal
from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        event)
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    staff_id = Column(Integer, nullable=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=True)
    status = Column(Boolean, default=True)
    user_type_id = Column(Integer, ForeignKey("user_type.id"), nullable=True)
    department_type_id = Column(Integer, ForeignKey(
        "department_type.id"), nullable=True)

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


class ResetPasswordToken(Base):
    __tablename__ = "reset_password_token"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    token = Column(String, index=True)
    date_created = Column(DateTime, default=datetime.utcnow)

    @staticmethod
    def generate_token():
        token = secrets.token_urlsafe(4)
        return sha256.hash(token)

    @staticmethod
    def verify_token(token, hash):
        return sha256.verify(token, hash)


class UserType(Base):
    __tablename__ = "user_type"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, unique=True, index=True)

    users = relationship('User', backref="user_type")


@event.listens_for(UserType.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    db = SessionLocal()
    db.add_all([UserType(title='System Admin'), UserType(
        title='Appraiser'), UserType(title='Appraisee')])
    db.commit()


class DepartmentType(Base):
    __tablename__ = "department_type"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, unique=True, index=True)

    users = relationship('User', backref="department_type")


@event.listens_for(DepartmentType.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    db = SessionLocal()
    db.add_all([DepartmentType(title='System Admin'), DepartmentType(title='Research'), DepartmentType(
        title='Consultancy'), DepartmentType(title='Finance'), DepartmentType(title='Corporate'), DepartmentType(title='Academics')])
    db.commit()
