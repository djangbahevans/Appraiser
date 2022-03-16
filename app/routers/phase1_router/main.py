from app.database import get_db
from app.main import oauth2_scheme
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from . import crud, schemas

router = APIRouter()


# GET APPRAISAL FORM
@router.get("/appraisalform/")
async def read_appraisal_form(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await crud.read_appraisal_form_auth(token, db)

# READ ANNUAL PLAN


@router.get("/annualplan/")
async def read_annual_plan(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await crud.read_annual_plan_auth(token, db)

# READ ANNUAL APPRAISAL


@router.get("/annualappraisal/")
async def read_annual_appraisal(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await crud.read_annual_appraisal_auth(token, db)

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
async def read_deadline_table(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await crud.read_deadline_table_auth(token, db)


# CREATE APPRAISAL FORM
# @router.post("/appraisalform/")
async def appraisal_form(payload: schemas.appraisal_form, db: Session = Depends(get_db)):
    return await crud.appraisal_form(payload.department, payload.grade, payload.positions, payload.date, payload.staff_id, db)

# CREATE ANNUAL PLAN


@router.post("/annualplan/")
async def create_annual_plan(payload: schemas.create_annual_plan, db: Session = Depends(get_db)):
    return await crud.create_annual_plan(payload.result_areas, payload.target, payload.resources, payload.appraisal_form_id, payload.submit, db)


# CREATE APPRAISAL FORM(YEARLY)
# @router.post("/createappraisalform/")
async def create_appraisal_form(payload: schemas.create_appraisal_form, db: Session = Depends(get_db)):
    return await crud.create_appraisal_form(payload.deadline, payload.department, payload.positions, payload.grade, payload.date, payload.staff_id, payload.progress_review, payload.remarks, payload.assessment, payload.score, payload.weight, payload.comment, db)


# CREATE ANNUAL APPRAISAL
# @router.post("/annualappraisal/")
async def create_annual_appraisal(payload: schemas.create_annual_appraisal, db: Session = Depends(get_db)):
    return await crud.create_annual_appraisal(payload.comment, payload.field, payload.appraisal_form_id, db)


# UPDATE APPRAISAL FORM
# @router.put("/appraisalform/")
async def update_appraisal_form(appraisal_form: schemas.update_appraisal_form, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await crud.update_appraisal_form_auth(appraisal_form, token, db)

# UPDATE ANNUAL PLAN
# @router.put("/annualplan/")


async def update_annual_plan(payload: schemas.update_annual_plan, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await crud.update_annual_plan_auth(payload, token, db)

# UPDATE ANNUAL APPRAISAL
# @router.put("/annualaprpaisal/")


async def update_annual_appraisal(annual_appraisal: schemas.update_annual_appraisal, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await crud.update_annual_appraisal_auth(annual_appraisal, token, db)


# DELETE ANNUAL PLAN
# @router.delete("/annualalan/{annual_plan_id}/")
async def delete_annual_plan(annual_plan_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await crud.delete_annual_plan_auth(annual_plan_id, token, db)

# DELETE APPRAISAL FORM
# @router.delete("/appraisalform/{appraisal_form_id}/")


async def delete_appraisal_form(appraisal_form_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await crud.delete_appraisal_form_auth(appraisal_form_id, token, db)

# DELETE ANNUAL APPRAISAL
# @router.delete("/annualappraisal/{annual_appraisal_id}/")


async def delete_annual_appraisal(annual_appraisal_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await crud.delete_annual_appraisal_auth(annual_appraisal_id, token, db)
