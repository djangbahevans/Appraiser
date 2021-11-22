from fastapi import APIRouter, Depends, HTTPException, Body, FastAPI
from datetime import datetime, time, timedelta
from main import get_db, oauth2_scheme
from pydantic import UUID4, EmailStr
from sqlalchemy.orm import Session
from typing import List, Optional
from . import crud, schemas
from uuid import UUID


router = APIRouter()

# READ STAFF DETAILS


@router.get("/")
async def read_staff(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await crud.read_staff_auth(token, db)

# READ SUPERVISORS


@router.get("/supervisors/")
async def read_supervisors(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await crud.read_supervisors_auth(token, db)

# READ STAFF BY NAME


@router.get("/{name}/")
async def read_staff_by_name(name: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await crud.read_staff_by_name_auth(name, token, db)

# READ STAFF ROLES


@router.get("/roles/")
async def read_roles(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await crud.read_roles_auth(token, db)


# READ DEADLINES
@router.get("/deadline/")
async def read_deadline_table(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await crud.read_deadline_table_auth(token, db)


# READ DEADLINES
@router.get("/deadline/start/")
async def read_start_deadline(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await crud.read_start_deadline_table_auth(token, db)


@router.get("/deadline/mid/")
async def read_mid_deadline(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await crud.read_mid_deadline_table_auth(token, db)


@router.get("/deadline/end/")
async def read_end_deadline(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await crud.read_end_deadline_table_auth(token, db)


# DEACTIVATE STAFF
@router.get("/deactivatestaff/{staff_id}/")
async def deactivate_staff(staff_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await crud.deactivate_staff_auth(staff_id, token, db)

# REACTIVATE STAFF


@router.get("/reactivatestaff/{staff_id}/")
async def reactivate_staff(staff_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await crud.reactivate_staff_auth(staff_id, token, db)

# CREATE STAFF DETAILS


@router.post("/")
async def create_staff(payload: schemas.UserCreate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await crud.create_staff_auth(payload.fname, payload.sname, payload.oname, payload.email, payload.supervisor, payload.gender, payload.department, payload.positions, payload.grade, payload.appointment, payload.roles, token, db)

# CREATE STAFF ROLES


@router.post("/roles/")
async def create_roles(payload: schemas.create_roles, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await crud.create_roles_auth(payload.role_description, token, db)

# CREATE DEADLINES


@router.post("/deadline/")
async def create_deadline(payload: schemas.create_deadline, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await crud.create_deadline_auth(payload.deadline_type, payload.start_date, payload.ending, token, db)


# UPDATE STAFF DETAILS
@router.put("/")
async def update_staff(payload: schemas.update_staff, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await crud.update_staff_auth(payload.staff_id, payload.fname, payload.sname, payload.oname, payload.email, payload.supervisor, payload.gender, payload.department, payload.positions, payload.grade, payload.appointment, payload.roles, token, db)

# UPDATE DEADLINE


@router.put("/Deadline/")
async def update_deadline_table(deadline: schemas.update_deadline, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await crud.update_deadline_auth(deadline, token, db)

# UPDATE STAFF ROLES


@router.put("/roles/")
async def update_roles(payload: schemas.update_roles, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await crud.update_roles_auth(payload.role_id, payload.role_description, token, db)


# DELETE STAFF DETAILS
@router.delete("/{staff_id}/")
async def delete_staff(staff_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await crud.delete_staff_auth(staff_id, token, db)

# DELETE STAFF ROLES


@router.delete("/{role_id}/")
async def delete_roles(role_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await crud.delete_roles_auth(role_id, token, db)

# DELETE DEADLINE


@router.delete("/deadline/{deadline_id}/")
async def delete_deadline(deadline_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await crud.delete_deadline_auth(deadline_id, token, db)
