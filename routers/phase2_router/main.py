from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import UUID4, EmailStr
from sqlalchemy.orm import Session
from typing import List, Optional
from . import crud, schemas
from main import get_db


router = APIRouter()


# READ PHASE-2 DETAILS
@router.get("/midyearreview/")
async def read_mid_year_review(db: Session = Depends(get_db)):
    return await crud.read_mid_year_review(db)


# READ MIDYEAR REVIEW
@router.get("/midyearreviewid/{appraisal_form_id}/")
async def read_midyear_review(appraisal_form_id: int, db: Session = Depends(get_db)):
    return await crud.read_midyear_review(appraisal_form_id, db)


# READ TARGETS
@router.get("/targets/")
async def targets(appraisal_form_id: int, db: Session = Depends(get_db)):
    return await crud.read_targets(appraisal_form_id, db)


# READ APPRAISAL FORM
@router.get("/appraisalform/")
async def read_appraisal_form(db: Session = Depends(get_db)):
    return await crud.read_appraisal_form(db)


# READ ANNUAL PLAN
@router.get("/annualplan/")
async def read_annual_plan(db: Session = Depends(get_db)):
    return await crud.read_annual_plan(db)


# READ ANNUAL APPRAISAL
@router.get("/annualappraisal/")
async def read_annual_appraisal(db: Session = Depends(get_db)):
    return await crud.read_annual_appraisal(db)


# GET HASH DETAILS
@router.get("/formdetails/{hash}/")
async def verify_hash_form(hash: str, db: Session = Depends(get_db)):
    return await crud.verify_hash_form(hash, db)

# READ HASH TABLE


@router.get("/hashdetails/")
async def read_hash_form(db: Session = Depends(get_db)):
    return await crud.read_hash_form(db)


# READ DEADLINES
@router.get("/deadline/")
async def read_deadline_table(db: Session = Depends(get_db)):
    return await crud.read_deadline_table(db)


# CREATE MID-YEAR REVIEW
@router.post("/midyearreview/")
async def create_mid_year_review(payload: schemas.create_mid_year_review, db: Session = Depends(get_db)):
    return await crud.create_mid_year_review(payload.progress_review, payload.appraisal_form_id, payload.competency, payload.submit, db)

# UPDATE PHASE-2 DETAILS
# @router.put("/midyearreview/")


async def update_mid_year_review(mid_year_review: schemas.update_mid_year_review, db: Session = Depends(get_db)):
    return await crud.update_mid_year_review(mid_year_review, db)


# DELETE PHASE-2 DETAILS
# @router.delete("/midyearreview/{midyear_review_id}/")
async def delete_mid_year_review(midyear_review_id: int, db: Session = Depends(get_db)):
    return await crud.delete_mid_year_review(midyear_review_id, db)
