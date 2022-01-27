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


@router.get("/performanceassessmentscore")
async def read_performance_assessment_score(appraisal_form_id: int, db: Session = Depends(get_db)):
    return await crud.performance_assessment_score(appraisal_form_id, db)


@router.get("/coreperformanceassessmentscore")
async def read_core_performance_assessment_score(appraisal_form_id: int, db: Session = Depends(get_db)):
    return await crud.core_performance_assessment_score(appraisal_form_id, db)


@router.get("/noncoreperformanceassessmentscore")
async def read_non_core_performance_assessment_score(appraisal_form_id: int, db: Session = Depends(get_db)):
    return await crud.non_core_performance_assessment_score(appraisal_form_id, db)


@router.get("/overalltotalscore")
async def overall_total_score(appraisal_form_id: int, db: Session = Depends(get_db)):
    return await crud.overall_total_score(appraisal_form_id, db)


@router.get("/overallperformancerating")
async def overall_performance_rating(appraisal_form_id: int, db: Session = Depends(get_db)):
    return await crud.overall_performance_rating(appraisal_form_id, db)


@router.get("/overallperformance")
async def overall_performance(appraisal_form_id: int, db: Session = Depends(get_db)):
    return await crud.overall_performance(appraisal_form_id, db)


# @router.get("/annualappraisal/")
async def read_annual_appraisal(db: Session = Depends(get_db)):
    return await crud.read_annual_appraisal(db)


@router.get("/competencies/")
async def read_competencies(db: Session = Depends(get_db)):
    return await crud.read_competencies(db)


@router.get("/competencies/{id}/")
async def read_competency_by_id(competency_id: int, db: Session = Depends(get_db)):
    return await crud.read_specific_competency(competency_id, db)


@router.get("/endofyearreview/")
async def end_of_year_review(appraisal_form_id: int, db: Session = Depends(get_db)):
    return await crud.read_endofyear_review(appraisal_form_id, db)


# @router.post("/annualappraisal/")
async def create_annual_appraisal(payload: schemas.create_annual_appraisal, db: Session = Depends(get_db)):
    return await crud.create_annual_appraisal(payload, db)


@router.post("/competencydetails/")
async def create_competency_details(score: List[schemas.CompDetails], db: Session = Depends(get_db)):
    return await crud.competence_details(score, db)


@router.post("/performancedetails/")
async def create_performance_details(payload: schemas.create_performance_details, db: Session = Depends(get_db)):
    return await crud.performance_details(payload.appraisal_form_id, payload.weight, payload.comments, payload.final_score, payload.approved_date, payload.submit, payload.p_a, db)


@router.post("/trainingreceived/")
async def training_received(payload: schemas.training_received, db: Session = Depends(get_db)):
    return await crud.training_received(payload.institution, payload.training_date, payload.programme, payload.appraisal_form_id, payload.submit, db)
