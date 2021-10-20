from ..auth_router.crud import UnAuthorised, is_token_blacklisted, utils, HTTPException, jwt
from fastapi import Depends, HTTPException, Response, status, Body, Header
from fastapi import Depends, HTTPException, BackgroundTasks
from starlette.responses import JSONResponse
from datetime import datetime, date
from sqlalchemy.orm import Session
from . import models, schemas
from .. import email
from typing import List
# READ END OF YEAR REVIEW


async def read_annual_appraisal(db: Session):
    res = db.execute("""SELECT * FROM public.annual_appraisal;""")
    res = res.fetchall()
    return res


async def read_competency_details(appraisal_form_id, db: Session):
    res = db.execute(
        """SELECT * FROM public.competency_details where appraisal_form_id=:appraisal_form_id;""", {
            'appraisal_form_id': appraisal_form_id})
    res = res.fetchall()
    return res


async def read_performance_details(appraisal_form_id, db: Session):
    res = db.execute("""SELECT * FROM public.performance_details  where appraisal_form_id=:appraisal_form_id;""", {
        'appraisal_form_id': appraisal_form_id})
    res = res.fetchall()
    return res


async def read_competencies(db: Session):
    res = db.execute(""" SELECT * FROM public.competency; """)
    res = res.fetchall()
    return res


async def read_specific_competency(competency_id, db: Session):
    res = db.execute(""" SELECT category, sub, main, weight FROM public.competency where competency_id=:competency_id; """, {
                     'competency_id': competency_id})
    res = res.fetchall()
    return res


async def read_endofyear_review(appraisal_form_id, db: Session):
    res = db.execute(""" SELECT * FROM public.endofyear_review where appraisal_form_id=:appraisal_form_id; """, {
        'appraisal_form_id': appraisal_form_id})
    res = res.fetchall()
    return res


# CREATE END OF YEAR REVIEW

async def create_annual_appraisal(payload: schemas.AnnualAppraisal, db: Session):
    query = db.execute(
        """ SELECT ending FROM public.deadline WHERE deadline_type = 'End'; """)  # READ DEADLINE FOR PHASE-1
    query = query.first()[0]
    if query >= date.today():  # CHECK IF DEADLINE HAS NOT PASSED BEFORE CREATING ANNUAL PLAN
        res = db.execute("""INSERT INTO public.annual_appraisal(
	                    result_areas, target, resources, appraisal_form_id, submit)
	                    values(:result_areas, :target, :resources, :appraisal_form_id, :submit) on conflict (appraisal_form_id) do 
	                    update set result_areas = EXCLUDED.result_areas, target = EXCLUDED.target, resources = EXCLUDED.resources, submit = EXCLUDED.submit; """,
                         {'appraisal_form_id': payload.appraisal_form_id, 'submit': payload.submit})  # CREATE INTO TABLE
        db.commit()
        if payload.submit == 1:
            # SEND ANNUAL PLAN DETAILS TO SUPERVISOR'S EMAIL TO REVIEW AND APPROVE
            await email.start.approve_annual_plan(payload.appraisal_form_id)
        else:
            pass

        return JSONResponse(status_code=200, content={"message": "annual plan has been created"})
    else:
        return JSONResponse(status_code=404, content={"message": "deadline has passed!"})


async def competence_details(payload: List[schemas.CompDetails],  db: Session):

    query = db.execute(
        """ SELECT ending FROM public.deadline WHERE deadline_type = 'End'; """)  # READ DEADLINE FOR PHASE-1
    query = query.first()[0]
    if query >= date.today():  # CHECK IF DEADLINE HAS NOT PASSED BEFORE CREATING ANNUAL PLAN
        for payload in payload:
            db.execute("""do $$
                            BEGIN
                            FOR i in 1..32 LOOP
                            INSERT INTO public.competency_details(competency_id, appraisal_form_id, grade, submit)
                            values(:competency_id, :appraisal_form_id, :grade, :submit)
                            on conflict (competency_id, appraisal_form_id) do 
                            update set grade = EXCLUDED.grade, submit = EXCLUDED.submit;
                            END LOOP;
                            END;
                            $$; """,
                       {'competency_id': payload.competency_id, 'appraisal_form_id': payload.appraisal_form_id, 'grade': payload.grade, 'submit': payload.submit, })  # CREATE INTO TABLE
            if payload.submit == 1:
                # SEND COMPETENCE DETAILS TO SUPERVISOR'S EMAIL TO REVIEW AND APPROVE
                # await email.end.approve_competence_details(payload.appraisal_form_id)
                # else:
                pass
        db.commit()

        return JSONResponse(status_code=200, content={"message": "competence details has been created"})
    else:
        return JSONResponse(status_code=404, content={"message": "deadline has passed!"})


async def performance_details(appraisal_form_id, weight, comments, final_score, approved_date, submit, db: Session):
    query = db.execute(
        """ SELECT ending FROM public.deadline WHERE deadline_type = 'End'; """)  # READ DEADLINE FOR PHASE-1
    query = query.first()[0]
    if query >= date.today():  # CHECK IF DEADLINE HAS NOT PASSED BEFORE CREATING ANNUAL PLAN
        res = db.execute("""INSERT INTO public.performance_details(appraisal_form_id, weight, comments, final_score, approved_date, submit)
	                            values(:appraisal_form_id, :weight, :comments, :final_score, :approved_date, :submit) on conflict (appraisal_form_id) do 
	                                update set weight = EXCLUDED.weight, comments = EXCLUDED.comments, final_score = EXCLUDED.final_score, approved_date = EXCLUDED.approved_date, submit = EXCLUDED.submit; """,
                         {'appraisal_form_id': appraisal_form_id, 'weight': weight, 'comments': comments, 'final_score': final_score, 'approved_date': approved_date, 'submit': submit})  # CREATE INTO TABLE
        db.commit()
        if submit == 1:
            # SEND PERFORMANCE PLAN DETAILS TO SUPERVISOR'S EMAIL TO REVIEW AND APPROVE
            await email.end.approve_performance_details(appraisal_form_id)
            # else:
            pass

        return JSONResponse(status_code=200, content={"message": "performance details has been created"})
    else:
        return JSONResponse(status_code=404, content={"message": "deadline has passed!"})
