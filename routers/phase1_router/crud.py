from ..auth_router.crud import UnAuthorised, is_token_blacklisted, utils, HTTPException, jwt, sys
from fastapi import Depends, HTTPException, Response, status, Body, Header
from fastapi import Depends, HTTPException, BackgroundTasks
from ..user_router.crud import read_user_by_id
from starlette.responses import JSONResponse
from datetime import datetime, date
from sqlalchemy.orm import Session
from . import models, schemas
from .. import email


# READ APPRAISAL FORM
async def read_appraisal_form(db: Session):
    res = db.execute(
        """SELECT department, grade, positions, appraisal_form_id, date, staff_id FROM public.appraisal_form;""")  # READ FROM TABLE
    res = res.fetchall()
    return res


async def read_appraisal_form_auth(token: str, db: Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await read_appraisal_form(db)
        else:
            return UnAuthorised('Not qualified')
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(
            sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="access token expired", headers={
                            "WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=500, detail="decode error not enough arguments", headers={
                            "WWW-Authenticate": "Bearer"})


# READ ANNUAL PLAN
async def read_annual_plan(db: Session):
    res = db.execute("""SELECT result_areas, target, resources, appraisal_form_id, annual_plan_id
	FROM public.annual_plan;""")  # READ FROM TABLE
    res = res.fetchall()
    return res


async def read_annual_plan_auth(token: str, db: Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await read_annual_plan(db)
        else:
            return UnAuthorised('Not qualified')
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(
            sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="access token expired", headers={
                            "WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=500, detail="decode error not enough arguments", headers={
                            "WWW-Authenticate": "Bearer"})


# READ ANNUAL APPRAISAL
async def read_annual_appraisal(db: Session):
    res = db.execute(
        """SELECT public.get_appraisal_form();""")  # READ FROM DB FUNCTION
    res = res.fetchall()
    return res


async def read_annual_appraisal_auth(token: str, db: Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await read_annual_appraisal(db)
        else:
            return UnAuthorised('Not qualified')
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(
            sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="access token expired", headers={
                            "WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=500, detail="decode error not enough arguments", headers={
                            "WWW-Authenticate": "Bearer"})


# READ HASH TABLE
async def read_hash_form(db: Session):
    res = db.execute(
        """SELECT public.get_entire_hash_table();""")  # READ FROM DB FUNCTION
    res = res.fetchall()
    return res


async def read_hash_form_auth(token: str, db: Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await read_hash_form(db)
        else:
            return UnAuthorised('Not qualified')
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(
            sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="access token expired", headers={
                            "WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=500, detail="decode error not enough arguments", headers={
                            "WWW-Authenticate": "Bearer"})


# READ DEADLINES
async def read_deadline_table(db: Session):
    res = db.execute(""" SELECT deadline_type, start_date, ending, deadline_id
	FROM public.deadline; """)  # READ DEADLINES FROM TABLE
    res = res.fetchall()
    return res


async def read_deadline_table_auth(token: str, db: Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        data = await read_user_by_id(token_data['id'], db)
        data = data.user_type_id
        print(data)
        if data == 1:
            return await read_deadline_table(db)
        else:
            return UnAuthorised('Not qualified')
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(
            sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="access token expired", headers={
                            "WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=500, detail="decode error not enough arguments", headers={
                            "WWW-Authenticate": "Bearer"})


# READ HASH FORM
async def verify_hash_form(hash_: str, db: Session):
    res = db.execute(""" SELECT public.get_hash_verification(:hash_) """, {
                     'hash_': hash_})  # READ FROM DB FUNCTION
    res = res.fetchall()
    return res


async def verify_hash_form_auth(hash_: str, token: str, db: Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await verify_hash_form(hash_, db)
        else:
            return UnAuthorised('Not qualified')
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(
            sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="access token expired", headers={
                            "WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=500, detail="decode error not enough arguments", headers={
                            "WWW-Authenticate": "Bearer"})


# CREATE APPRAISAL FORM
async def appraisal_form(department, grade, positions, date, staff_id, db: Session):
    res = db.execute("""insert into public.appraisal_form(department, grade, positions, date, staff_id)
    values(:department, :grade, :positions, :date, :staff_id);""",
                     {'department': department, 'grade': grade, 'positions': positions, 'date': date, 'staff_id': staff_id})  # CRREATE INTO TABLE
    db.commit()
    return JSONResponse(status_code=200, content={"message": "appraisal form has been created"})

# CREATE ANNUAL PLAN


async def create_annual_plan(result_areas, target, resources, appraisal_form_id, submit, db: Session):
    query = db.execute(
        """ SELECT ending FROM public.deadline WHERE deadline_type = 'Start'; """)  # READ DEADLINE FOR PHASE-1
    query = query.first()[0]
    if query >= date.today():  # CHECK IF DEADLINE HAS NOT PASSED BEFORE CREATING ANNUAL PLAN
        res = db.execute("""INSERT INTO public.annual_plan(
	                    result_areas, target, resources, appraisal_form_id, submit)
	                    values(:result_areas, :target, :resources, :appraisal_form_id, :submit) on conflict (appraisal_form_id) do 
	                    update set result_areas = EXCLUDED.result_areas, target = EXCLUDED.target, resources = EXCLUDED.resources, submit = EXCLUDED.submit; """,
                         {'result_areas': result_areas, 'target': target, 'resources': resources, 'appraisal_form_id': appraisal_form_id, 'submit': submit})  # CREATE INTO TABLE
        db.commit()
        if submit == 1:
            # SEND ANNUAL PLAN DETAILS TO SUPERVISOR'S EMAIL TO REVIEW AND APPROVE
            await email.start.approve_annual_plan(appraisal_form_id)
        else:
            pass

        return JSONResponse(status_code=200, content={"message": "annual plan has been created"})
    else:
        return JSONResponse(status_code=404, content={"message": "deadline has passed!"})


# CREATE ANNUAL APPRAISAL
async def create_annual_appraisal(comment, field, appraisal_form_id, db: Session):
    res = db.execute("""insert into public.annual_appraisal(comment, field, appraisal_form_id)
    values(:comment, :field, :appraisal_form_id);""",
                     {'comment': comment, 'field': field, 'appraisal_form_id': appraisal_form_id})  # INSERT INTO TABLE
    db.commit()
    return JSONResponse(status_code=200, content={"message": "annual appraisal has been created"})

# CREATE APPRAISAL FORM(YEARLY)


async def create_appraisal_form(deadline, department, positions, grade, date, staff_id, progress_review, remarks, assessment, score, weight, comment, db: Session):
    res = db.execute("""SELECT public.create_appraisal_form(deadline:deadline, department:department, positions:positions, grade:grade, date:date, staff_id:staff_id, progress_review:progress_review, remarks:remarks, assessment:assessment, score:score, weight:weight, comment:comment);""",
                     {'deadline': deadline, 'department': department, 'positions': positions, 'grade': grade, 'date': date, 'staff_id': staff_id, 'progress_review': progress_review, 'remarks': remarks, 'assessment': assessment, 'score': score, 'weight': weight, 'comment': comment})  # INSERT INTO TABLE
    db.commit()
    return res


# UPDATE APPRAISAL FORM
async def update_appraisal_form(appraisal_form: schemas.update_appraisal_form, db: Session):
    res = db.execute("""UPDATE public.appraisal_form
	SET appraisal_form_id = :appraisal_form_id, department = :department, grade = :grade, position = :positions, date = :date, staff_id = :staff_id
	WHERE appraisal_form_id = :appraisal_form_id;""",
                     {'appraisal_form_id': appraisal_form.appraisal_form_id, 'department': appraisal_form.department, 'grade': appraisal_form.grade, 'positions': appraisal_form.positions, 'date': appraisal_form.date, 'staff_id': appraisal_form.staff_id})  # UPDATE IN TABLE
    db.commit()
    return JSONResponse(status_code=200, content={"message": "appraisal form has been updated"})


async def update_appraisal_form_auth(appraisal_form: schemas.update_appraisal_form, token: str, db: Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await update_appraisal_form(appraisal_form, db)
        else:
            return UnAuthorised('Not qualified')
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(
            sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="access token expired", headers={
                            "WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=500, detail="decode error not enough arguments", headers={
                            "WWW-Authenticate": "Bearer"})


# UPDATE ANNUAL PLAN
async def update_annual_plan(annual_plan: schemas.update_annual_plan, db: Session):
    res = db.execute("""UPDATE public.annual_plan 
    SET result_areas = :result_areas, target = :target, resources = :resources, appraisal_form_id = :appraisal_form_id, annual_plan_id = :annual_plan_id
	WHERE annual_plan_id = :annual_plan_id;""",
                     {'result_areas': annual_plan.result_areas, 'target': annual_plan.target, 'resources': annual_plan.resources, 'appraisal_form_id': annual_plan.appraisal_form_id, 'annual_plan_id': annual_plan.annual_plan_id})  # UPDATE IN TABLE
    db.commit()
    return JSONResponse(status_code=200, content={"message": "annual plan has been updated"})


async def update_annual_plan_auth(annual_plan: schemas.update_annual_plan, token: str, db: Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await update_annual_plan(annual_plan, db)
        else:
            return UnAuthorised('Not qualified')
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(
            sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="access token expired", headers={
                            "WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=500, detail="decode error not enough arguments", headers={
                            "WWW-Authenticate": "Bearer"})


# UPDATE ANNUAL APPRAISAL
async def update_annual_appraisal(annual_appraisal: schemas.create_annual_appraisal, db: Session):
    res = db.execute("""UPDATE public.annual_appraisal
	SET comment = :comment, field = :field, appraisal_form_id = :appraisal_form_id, annual_appraisal_id = :annual_appraisal_id
	WHERE annual_appraisal_id = :annual_appraisal_id;""",
                     {'comment': annual_appraisal.comment, 'field': annual_appraisal.field, 'appraisal_form_id': annual_appraisal.appraisal_form_id, 'annual_appraisal_id': annual_appraisal.annual_appraisal_id})  # UPDATE IN TABLE
    db.commit()
    return JSONResponse(status_code=200, content={"message": "annual appraisal has been updated"})


async def update_annual_appraisal_auth(annual_appraisal: schemas.update_annual_appraisal, token: str, db: Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await update_annual_appraisal(annual_appraisal, db)
        else:
            return UnAuthorised('Not qualified')
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(
            sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="access token expired", headers={
                            "WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=500, detail="decode error not enough arguments", headers={
                            "WWW-Authenticate": "Bearer"})


# DELETE APPRAISAL FORM
async def delete_appraisal_form(appraisal_form_id: int, db: Session):
    res = db.execute("""DELETE FROM public.appraisal_form
	WHERE appraisal_form_id = :appraisal_form_id;""",
                     {'appraisal_form_id': appraisal_form_id})  # DELETE FROM TABLE
    db.commit()
    return JSONResponse(status_code=200, content={"message": "appraisal form has been deleyed"})


async def delete_appraisal_form_auth(appraisal_form_id: int, token: str, db: Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await delete_appraisal_form(appraisal_form_id, db)
        else:
            return UnAuthorised('Not qualified')
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(
            sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="access token expired", headers={
                            "WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=500, detail="decode error not enough arguments", headers={
                            "WWW-Authenticate": "Bearer"})


# DELETE ANNUAL PLAN
async def delete_annual_plan(annual_plan_id: int, db: Session):
    res = db.execute("""DELETE FROM public.annual_plan
	WHERE annual_plan_id = :annual_plan_id;""",
                     {'annual_plan_id': annual_plan_id})  # DELETE FROM TABLE
    db.commit()
    return JSONResponse(status_code=200, content={"message": "annual plan has been deleted"})


async def delete_annual_plan_auth(annual_plan_id: int, token: str, db: Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await delete_annual_plan(annual_plan_id, db)
        else:
            return UnAuthorised('Not qualified')
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(
            sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="access token expired", headers={
                            "WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=500, detail="decode error not enough arguments", headers={
                            "WWW-Authenticate": "Bearer"})


# DELETE ANNUAL APPRAISAL
async def delete_annual_appraisal(annual_appraisal_id: int, db: Session):
    res = db.execute("""DELETE FROM public.annual_appraisal
	WHERE annual_appraisal_id = :annual_appraisal_id;""",
                     {'annual_appraisal_id': annual_appraisal_id})  # DELETE FROM TABLE
    db.commit()
    return JSONResponse(status_code=200, content={"message": "annual appraisal has been deleted"})


async def delete_annual_appraisal_auth(annual_appraisal_id: int, token: str, db: Session):
    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await delete_annual_appraisal(annual_appraisal_id, db)
        else:
            return UnAuthorised('Not qualified')
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(
            sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="access token expired", headers={
                            "WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=500, detail="decode error not enough arguments", headers={
                            "WWW-Authenticate": "Bearer"})
