from ..auth_router.crud import UnAuthorised, is_token_blacklisted, utils, HTTPException, jwt, sys
from fastapi import Depends, HTTPException, Response, status, Body, Header
from fastapi import Depends, HTTPException, BackgroundTasks
from starlette.responses import JSONResponse
from datetime import datetime, date
from sqlalchemy.orm import Session
from . import models, schemas
from .. import email
from typing import List

# READ END OF YEAR REVIEW


async def read_appraisees_commented_list(user_id: int, db: Session):
    res = db.execute(
        """SELECT public.get_list_of_appraisee_commented(:user_id)""", {
            'user_id': user_id})  # GET FROM DB FUNCTION
    res = res.fetchall()
    return res


async def read_appraisees_commented_list_auth(user_id: int, token: str, db: Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await read_appraisees_commented_list(user_id, db)
        else:
            raise HTTPException(status_code=401, detail="{}".format(
                sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(
            sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="access token expired", headers={
                            "WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=500, detail="decode error not enough arguments", headers={
                            "WWW-Authenticate": "Bearer"})


async def read_appraisees_not_commented_list(user_id: int, db: Session):
    res = db.execute("""SELECT public.get_list_of_appraisees_not_commented(:user_id)""", {
        'user_id': user_id})  # GET FROM DB FUNCTION
    res = res.fetchall()
    return res


async def read_appraisees_not_commented_list_auth(user_id: int, token: str, db: Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await read_appraisees_not_commented_list(user_id, db)
        else:
            raise HTTPException(status_code=401, detail="{}".format(
                sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(
            sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="access token expired", headers={
                            "WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=500, detail="decode error not enough arguments", headers={
                            "WWW-Authenticate": "Bearer"})


async def read_appraisers_commented_list(user_id: int, db: Session):
    res = db.execute(
        """SELECT public.get_list_of_appraisers_commented(:user_id)""", {
            'user_id': user_id})  # GET FROM DB FUNCTION
    res = res.fetchall()
    return res


async def read_appraisers_commented_list_auth(user_id: int, token: str, db: Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await read_appraisers_commented_list(user_id, db)
        else:
            raise HTTPException(status_code=401, detail="{}".format(
                sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(
            sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="access token expired", headers={
                            "WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=500, detail="decode error not enough arguments", headers={
                            "WWW-Authenticate": "Bearer"})


async def read_appraisers_not_commented_list(user_id: int, db: Session):
    res = db.execute("""SELECT public.get_list_of_appraisers_not_commented(:user_id)""", {
        'user_id': user_id})  # GET FROM DB FUNCTION
    res = res.fetchall()
    return res


async def read_appraisers_not_commented_list_auth(user_id: int, token: str, db: Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await read_appraisers_not_commented_list(user_id, db)
        else:
            raise HTTPException(status_code=401, detail="{}".format(
                sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(
            sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="access token expired", headers={
                            "WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=500, detail="decode error not enough arguments", headers={
                            "WWW-Authenticate": "Bearer"})


async def read_endofyear_review(appraisal_form_id, db: Session):
    res = db.execute(""" SELECT * FROM public.endofyear_review where appraisal_form_id=:appraisal_form_id; """, {
        'appraisal_form_id': appraisal_form_id})
    res = res.fetchall()
    return res


# CREATE END OF YEAR REVIEW

async def aprpaisers_comment_on_work_plan(payload: schemas.AprpaisersComment0nWorkPlan, db: Session):
    query = db.execute(
        """ SELECT ending FROM public.deadline WHERE deadline_type = 'End'; """)  # READ DEADLINE FOR PHASE-1
    query = query.first()[0]
    if query >= date.today():  # CHECK IF DEADLINE HAS NOT PASSED BEFORE CREATING COMMENT
        res = db.execute("""INSERT INTO public.endofyear_review(
	                    appraisers_comment_on_workplan, appraisal_form_id, submit)
	                    values(:appraisers_comment_on_workplan, :appraisal_form_id, :submit) on conflict (appraisal_form_id) do
	                    update set appraisers_comment_on_workplan = EXCLUDED.appraisers_comment_on_workplan,  submit = EXCLUDED.submit; """,
                         {'appraisers_comment_on_workplan': payload.appraisers_comment_on_workplan, 'appraisal_form_id': payload.appraisal_form_id, 'submit': payload.submit})  # CREATE INTO TABLE
        db.commit()
        if payload.submit == 1:
            # SEND COMMENT ON WORK PLAN TO HEAD OF DIVISION'S EMAIL TO REVIEW AND ALSO ADD COMMENTS
            # await email.start.approve_annual_plan(payload.appraisal_form_id)
            # else:
            pass

        return JSONResponse(status_code=200, content={"message": "appraisers comment on workplan has been created"})
    else:
        return JSONResponse(status_code=404, content={"message": "deadline has passed!"})


async def training_development_comments(payload: schemas.TrainingDevelopmentComments, db: Session):
    query = db.execute(
        """ SELECT ending FROM public.deadline WHERE deadline_type = 'End'; """)  # READ DEADLINE FOR PHASE-1
    query = query.first()[0]
    if query >= date.today():  # CHECK IF DEADLINE HAS NOT PASSED BEFORE CREATING COMMENT
        res = db.execute("""INSERT INTO public.endofyear_review(
	                    training_development_comments, appraisal_form_id, submit)
	                    values(:training_development_comments, :appraisal_form_id, :submit) on conflict (appraisal_form_id) do
	                    update set training_development_comments = EXCLUDED.training_development_comments,  submit = EXCLUDED.submit; """,
                         {'training_development_comments': payload.training_development_comments, 'appraisal_form_id': payload.appraisal_form_id, 'submit': payload.submit})  # CREATE INTO TABLE
        db.commit()
        if payload.submit == 1:
            # SEND ANNUAL PLAN DETAILS TO SUPERVISOR'S EMAIL TO REVIEW AND APPROVE
            # await email.start.approve_annual_plan(payload.appraisal_form_id)
            # else:
            pass

        return JSONResponse(status_code=200, content={"message": "appraisers comment on workplan has been created"})
    else:
        return JSONResponse(status_code=404, content={"message": "deadline has passed!"})


async def appraisees_comments_and_plan(payload: schemas.AppraiseesCommentsAndPlans, db: Session):
    query = db.execute(
        """ SELECT ending FROM public.deadline WHERE deadline_type = 'End'; """)  # READ DEADLINE FOR PHASE-1
    query = query.first()[0]
    if query >= date.today():  # CHECK IF DEADLINE HAS NOT PASSED BEFORE CREATING COMMENT
        res = db.execute("""INSERT INTO public.endofyear_review(
	                    appraisees_comments_and_plan, training_development_comments, appraisal_form_id, submit)
	                    values(:appraisees_comments_and_plan, :training_development_comments, :appraisal_form_id, :submit) on conflict (appraisal_form_id) do
	                    update set appraisees_comments_and_plan = EXCLUDED.appraisees_comments_and_plan, training_development_comments=EXCLUDED.training_development_comments,  submit = EXCLUDED.submit; """,
                         {'appraisees_comments_and_plan': payload.appraisees_comments_and_plan, 'training_development_comments': payload.training_development_comments, 'appraisal_form_id': payload.appraisal_form_id, 'submit': payload.submit})  # CREATE INTO TABLE
        db.commit()
        if payload.submit == 1:
            # SEND COMMENT ON WORK PLAN TO SUPERVISOR'S EMAIL TO REVIEW AND ALSO ADD COMMENTS
            await email.end.add_comment_on_workplan(payload.appraisal_form_id)
            # else:
            pass

        return JSONResponse(status_code=200, content={"message": "appraisers comment on workplan has been created"})
    else:
        return JSONResponse(status_code=404, content={"message": "deadline has passed!"})


async def head_of_divisions_comments(payload: schemas.HeadOfDivisionsComments, db: Session):
    query = db.execute(
        """ SELECT ending FROM public.deadline WHERE deadline_type = 'End'; """)  # READ DEADLINE FOR PHASE-1
    query = query.first()[0]
    if query >= date.today():  # CHECK IF DEADLINE HAS NOT PASSED BEFORE CREATING COMMENT
        res = db.execute("""INSERT INTO public.endofyear_review(
	                    head_of_divisions_comments, appraisal_form_id, submit)
	                    values(:head_of_divisions_comments, :appraisal_form_id, :submit) on conflict (appraisal_form_id) do
	                    update set head_of_divisions_comments = EXCLUDED.head_of_divisions_comments,  submit = EXCLUDED.submit; """,
                         {'head_of_divisions_comments': payload.head_of_divisions_comments, 'appraisal_form_id': payload.appraisal_form_id, 'submit': payload.submit})  # CREATE INTO TABLE
        db.commit()
        if payload.submit == 1:
            # SEND ANNUAL PLAN DETAILS TO SUPERVISOR'S EMAIL TO REVIEW AND APPROVE
            # await email.start.approve_annual_plan(payload.appraisal_form_id)
            # else:
            pass

        return JSONResponse(status_code=200, content={"message": "appraisers comment on workplan has been created"})
    else:
        return JSONResponse(status_code=404, content={"message": "deadline has passed!"})


async def performance_assessment_score(appraisal_form_id, db: Session):
    pascore = db.execute("""SELECT avg(score) as value FROM public.vw_competency where appraisal_form_id=:appraisal_form_id;""", {
        'appraisal_form_id': appraisal_form_id})
    pascore = pascore.fetchall()
    return pascore


async def core_performance_assessment_score(appraisal_form_id, db: Session):
    cpascore = db.execute("""SELECT avg(score)*0.6 as value FROM public.vw_competency where appraisal_form_id=:appraisal_form_id and category='Core';""", {
        'appraisal_form_id': appraisal_form_id})
    cpascore = cpascore.fetchall()
    return cpascore


async def non_core_performance_assessment_score(appraisal_form_id, db: Session):
    ncpascore = db.execute("""SELECT avg(score)*0.6 as value FROM public.vw_competency where appraisal_form_id=:appraisal_form_id and category='None Core';""", {
        'appraisal_form_id': appraisal_form_id})
    ncpascore = ncpascore.fetchall()
    return ncpascore


async def overall_total_score(appraisal_form_id, db: Session):
    otscore = db.execute("""SELECT avg(score)*0.6 as value FROM public.vw_competency where appraisal_form_id=:appraisal_form_id;""", {
        'appraisal_form_id': appraisal_form_id})
    otscore = otscore.fetchall()
    return otscore


async def overall_performance_rating(appraisal_form_id, db: Session):
    oprating = db.execute("""SELECT (avg(score)*0.6)*100 as value FROM public.vw_competency where appraisal_form_id=:appraisal_form_id;""", {
        'appraisal_form_id': appraisal_form_id})
    oprating = oprating.fetchall()
    return oprating


async def overall_performance(appraisal_form_id, db: Session):
    overall_performance = db.execute("""SELECT avg(score) as pa_score,avg(score)*0.6 as cpa_score,avg(score)*0.6 as ncpa_score,avg(score)*0.6 as ot_score,(avg(score)*0.6)*100 as op_rating  FROM public.vw_competency where appraisal_form_id=:appraisal_form_id;""", {
        'appraisal_form_id': appraisal_form_id})
    overall_performance = overall_performance.fetchall()
    return overall_performance
