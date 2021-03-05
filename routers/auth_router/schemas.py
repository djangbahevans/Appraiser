from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from datetime import datetime, time, timedelta
from typing import List, Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
import datetime


class UserBase(BaseModel):
    fname: str
    sname: str
    oname: str
    email: str
    supervisor: int
    gender: str
    roles: str
    department: str
    positions: str
    grade: int
    appointment: Optional[datetime.datetime]
class UpdateStaff(BaseModel):
    staff_id:int
    fname: str
    sname: str
    oname: str
    email: str
    supervisor: int
    gender: str
    roles: str
    department: str
    positions: str
    grade: int
    appointment: Optional[datetime.datetime]
class UpdateDeadline(BaseModel):
    deadline_id: int
    deadline_type: str
    start_date: Optional[datetime.datetime]
    ending: Optional[datetime.datetime] 
class UserCreate(UserBase):
    pass  
class update_staff(UpdateStaff):
    pass
class User(UserBase):
    id: int
class DeleteStaff(BaseModel):
    staff_id: int
class delete_staff(DeleteStaff):
    pass
class DeadlineTable(BaseModel):
    deadline_type: str
    start_date: Optional[datetime.datetime]
    ending: Optional[datetime.datetime]
class DeleteDeadline(BaseModel):
    deadline_id: int
class delete_deadline(DeleteDeadline):
    pass        
class create_deadline(DeadlineTable):
    pass
class update_deadline(UpdateDeadline):
    pass
class read_deadline_table(BaseModel):
    deadline_type: DeadlineTable
    start_date: DeadlineTable
    ending: DeadlineTable
    deadline_id: DeadlineTable

class CreateRoles(BaseModel):
    role_description: str
class create_roles(CreateRoles):
    pass

class UpdateRoles(BaseModel):
    role_id: int
    role_description: str
class update_roles(UpdateRoles):
    pass