from datetime import date

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from .. import email
from ..auth_router.crud import (HTTPException, UnAuthorised,
                                is_token_blacklisted, jwt, sys, utils)
from . import schemas


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


async def read_hod_approved_list(user_id: int, db: Session):
    res = db.execute(
        """SELECT public.get_list_of_hod_commented(:user_id)""", {
            'user_id': user_id})  # GET FROM DB FUNCTION
    res = res.fetchall()
    return res


async def read_hod_approved_list_auth(user_id: int, token: str, db: Session):
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


async def read_final_completed_list(user_id: int, db: Session):
    res = db.execute("""SELECT public.get_list_of_final_completed(:user_id)""", {
        'user_id': user_id})  # GET FROM DB FUNCTION
    res = res.fetchall()
    return res


async def read_final_completed_list_auth(user_id: int, token: str, db: Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await read_final_completed_list(user_id, db)
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
            await email.end.add_head_of_division_comments(payload.appraisal_form_id)
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

        return JSONResponse(status_code=200, content={"message": "appraisees comment on workplan created"})
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
            await email.end.final_form_details(payload.appraisal_form_id)
            # else:
            pass

        return JSONResponse(status_code=200, content={"message": "head of division's comments created"})
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
    overall_performance = db.execute("""SELECT firstname, lastname, middlename, email, core_assessments, non_core_assessments, performance_assessment, overall_total, overall_performance_rating
	FROM public.view_users_form_details where appraisal_form_id=:appraisal_form_id;""", {
        'appraisal_form_id': appraisal_form_id})
    overall_performance = overall_performance.fetchall()
    return overall_performance


async def final_form_details(appraisal_form_id, db: Session):
    final_form_details = db.execute("""SELECT view_users_form_details.appraisal_form_id, view_users_form_details.firstname, view_users_form_details.lastname, view_users_form_details.middlename,       view_users_form_details.email, view_users_form_details.gender, view_users_form_details.staff_id, view_users_form_details.supervisor, view_users_form_details.supervisor_fname, view_users_form_details.supervisor_oname, view_users_form_details.supervisor_sname, view_users_form_details.supervisor_email, view_users_form_details.roles, view_users_form_details.role_description, view_users_form_details.department, view_users_form_details.positions, view_users_form_details.grade, view_users_form_details.result_areas, view_users_form_details.target, view_users_form_details.resources, view_users_form_details.start_status, view_users_form_details.submit, view_users_form_details.annual_plan_status, view_users_form_details.annual_plan_comment, view_users_form_details.progress_review, view_users_form_details.remarks, view_users_form_details.midyear_review_status, view_users_form_details.competency, view_users_form_details.mid_status, view_users_form_details.midyear_review_comment, view_users_form_details.end_status, view_users_form_details.average_per_rating, view_users_form_details.average_total, view_users_form_details.average_per_rating_id, view_users_form_details.appraisal_comment_on_workplan, view_users_form_details.training_development_comments, view_users_form_details.core_assessments, view_users_form_details.non_core_assessments, view_users_form_details.appraisees_comments_and_plan, view_users_form_details.head_of_divisions_comments, view_users_form_details.endofyear_review, view_users_form_details.performance_assessment, view_users_form_details.overall_total, view_users_form_details.overall_performance_rating, view_users_form_details.appointment, view_users_form_details.supervisor_position, view_users_form_details.supervisor_role, view_users_form_details.supervisor_appointment,view_end.appraisal_form_id, view_end.comments, view_end.status, view_end.approved_date, view_end.submit, view_end.weight, view_end.final_score, view_end.performance_details_id, performance_details.p_a as performance_assessments, view_users_form_details.training_received_programme, view_users_form_details.training_received_date,view_users_form_details.training_received_institution
	FROM public.view_users_form_details inner join public.view_end on view_users_form_details.appraisal_form_id=view_end.appraisal_form_id inner join performance_details on view_users_form_details.appraisal_form_id=performance_details.appraisal_form_id where view_users_form_details.appraisal_form_id=:appraisal_form_id;""", {
        'appraisal_form_id': appraisal_form_id})
    final_form_details = final_form_details.fetchall()
    return final_form_details
