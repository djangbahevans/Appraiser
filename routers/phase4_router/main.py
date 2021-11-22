from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Body
from pydantic import UUID4, EmailStr
from sqlalchemy.orm import Session
from typing import List, Optional
from . import crud, schemas
from main import get_db, oauth2_scheme
from datetime import datetime

router = APIRouter()


@router.get("/appraiseescommentlist/")
async def read_appraisees_commented_list(user_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await crud.read_appraisees_commented_list_auth(user_id, token, db)


@router.get("/appraiseesnotcommentlist/")
async def read_appraisees_not_commented_list(user_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await crud.read_appraisees_not_commented_list_auth(user_id, token, db)


@router.get("/appraiserscommentlist/")
async def read_appraisers_commented_list(user_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await crud.read_appraisers_commented_list_auth(user_id, token, db)


@router.get("/appraisersnotcommentlist/")
async def read_appraisers_not_commented_list(user_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await crud.read_appraisers_not_commented_list_auth(user_id, token, db)


@router.get("/finalcompletedlist/")
async def read_final_completed_list(user_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await crud.read_final_completed_list_auth(user_id, token, db)


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


@router.get("/endofyearreview/")
async def end_of_year_review(appraisal_form_id: int, db: Session = Depends(get_db)):
    return await crud.read_endofyear_review(appraisal_form_id, db)


@router.post("/appraiserscommentonworkplan/")
async def aprpaisers_comment_on_work_plan(payload: schemas.AprpaisersComment0nWorkPlan, db: Session = Depends(get_db)):
    return await crud.aprpaisers_comment_on_work_plan(payload, db)


@router.post("/trainingdevelopmentcomments/")
async def training_development_comments(payload: schemas.TrainingDevelopmentComments, db: Session = Depends(get_db)):
    return await crud.training_development_comments(payload, db)


@router.post("/appraiseescommentsandplans/")
async def appraisees_comments_and_plan(payload: schemas.AppraiseesCommentsAndPlans, db: Session = Depends(get_db)):
    return await crud.appraisees_comments_and_plan(payload, db)


@router.post("/headofdivisionscomments/")
async def head_of_divisions_comments(payload: schemas.HeadOfDivisionsComments, db: Session = Depends(get_db)):
    return await crud.head_of_divisions_comments(payload, db)
