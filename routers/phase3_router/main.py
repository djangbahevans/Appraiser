from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Body
from pydantic import UUID4, EmailStr
from sqlalchemy.orm import Session
from typing import List, Optional
from . import crud, schemas
from main import get_db
from datetime import datetime

router = APIRouter()


@router.get("/competencedetails/")
async def read_competency_details(appraisal_form_id: int, db: Session = Depends(get_db)):
    return await crud.read_competency_details(appraisal_form_id, db)


@router.get("/performancedetails/")
async def read_performance_details(appraisal_form_id: int, db: Session = Depends(get_db)):
    return await crud.read_performance_details(appraisal_form_id, db)


# @router.get("/annualappraisal/")
async def read_annual_appraisal(db: Session = Depends(get_db)):
    return await crud.read_annual_appraisal(db)


@router.get("/competencies/")
async def read_competencies(db: Session = Depends(get_db)):
    return await crud.read_competencies(db)


@router.get("/endofyearreview/")
async def end_of_year_review(db: Session = Depends(get_db)):
    return await crud.read_endofyear_review(db)


# @router.post("/annualappraisal/")
async def create_annual_appraisal(payload: schemas.create_annual_appraisal, db: Session = Depends(get_db)):
    return await crud.create_annual_appraisal(payload, db)


@router.post("/competencydetails/")
async def create_competency_details(score: List[schemas.CompDetails], db: Session = Depends(get_db)):
    return await crud.competence_details(score, db)


@router.post("/performancedetails/")
async def create_performance_details(payload: schemas.create_performance_details, db: Session = Depends(get_db)):
    return await crud.performance_details(payload.appraisal_form_id, payload.weight, payload.comments, payload.final_score, payload.approved_date, payload.submit, db)
