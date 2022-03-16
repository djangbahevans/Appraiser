from starlette.responses import JSONResponse
from datetime import date
from sqlalchemy.orm import Session
from . import schemas
from .. import email


# READ MID-YEAR REVIEW
async def read_mid_year_review(db: Session):
    res = db.execute(
        """SELECT midyear_review_id, progress_review, remarks, mid_status, appraisal_form_id, competency FROM public.midyear_review;""")
    res = res.fetchall()
    return res

# READ MID-YEAR REVIEW WITH APPRAISAL FORM ID


async def read_midyear_review(appraisal_form_id, db: Session):
    res = db.execute("""SELECT * FROM public.midyear_review where appraisal_form_id=:appraisal_form_id;""", {
                     'appraisal_form_id': appraisal_form_id})
    res = res.fetchall()
    return res


# READ TARGETS
async def read_targets(appraisal_form_id, db: Session):
    res = db.execute("""SELECT target FROM public.annual_plan where appraisal_form_id=:appraisal_form_id;""", {
                     'appraisal_form_id': appraisal_form_id})
    res = res.fetchall()
    return res


# READ APPRAISAL FORM
async def read_appraisal_form(db: Session):
    res = db.execute(
        """SELECT department, grade, positions, appraisal_form_id, date, staff_id FROM public.appraisal_form;""")  # READ FROM TABLE
    res = res.fetchall()
    return res


# READ ANNUAL PLAN
async def read_annual_plan(db: Session):
    res = db.execute("""SELECT result_areas, target, resources, appraisal_form_id, annual_plan_id
	FROM public.annual_plan;""")  # READ FROM TABLE
    res = res.fetchall()
    return res


# READ ANNUAL APPRAISAL
async def read_annual_appraisal(db: Session):
    res = db.execute(
        """SELECT public.get_appraisal_form();""")  # READ FROM DB FUNCTION
    res = res.fetchall()
    return res


# READ HASH TABLE
async def read_hash_form(db: Session):
    res = db.execute(
        """SELECT public.get_entire_hash_table();""")  # READ FROM DB FUNCTION
    res = res.fetchall()
    return res


# READ DEADLINES
async def read_deadline_table(db: Session):
    res = db.execute(""" SELECT deadline_type, start_date, ending, deadline_id
	FROM public.deadline; """)  # READ FROM TABLE
    res = res.fetchall()
    return res


# READ HASH FORM
async def verify_hash_form(hash_: str, db: Session):
    res = db.execute(""" SELECT public.get_hash_verification(:hash_) """, {
                     'hash_': hash_})  # READ FROM DB FUNCTION
    res = res.fetchall()
    return res


# CREATE MID-YEAR REVIEW
async def create_mid_year_review(progress_review, appraisal_form_id, competency, submit, db: Session):
    query = db.execute(
        """ SELECT ending FROM public.deadline WHERE deadline_type = 'Mid'; """)  # READ DEADLINE FOR PHASE-1
    query = query.first()[0]
    if query >= date.today():  # CHECK IF DEADLINE HAS NOT PASSED BEFORE CREATING ANNUAL PLAN
        res = db.execute("""INSERT INTO public.midyear_review(
	                    progress_review, appraisal_form_id, competency, submit)
	                    values(:progress_review, :appraisal_form_id, :competency, :submit) on conflict (appraisal_form_id) do 
	                    update set progress_review = EXCLUDED.progress_review, competency = EXCLUDED.competency,  submit = EXCLUDED.submit; """,
                         {'progress_review': progress_review,  'appraisal_form_id': appraisal_form_id, 'competency': competency, 'submit': submit})  # CREATE INTO TABLE
        db.commit()
        if submit == 1:
            # SEND ANNUAL PLAN DETAILS TO SUPERVISOR'S EMAIL TO REVIEW AND APPROVE
            await email.mid.approve_mid_year_review(appraisal_form_id)
        else:
            pass

        return JSONResponse(status_code=200, content={"message": "mid-year review has been created"})
    else:
        return JSONResponse(status_code=404, content={"message": "deadline has passed!"})


# UPDATE PHASE-2 DETAILS
async def update_mid_year_review(mid_year_review: schemas.update_mid_year_review, db: Session):
    res = db.execute("""UPDATE public.midyear_review
	SET midyear_review_id = :midyear_review_id, progress_review = :progress_review, remarks = :remarks, mid_status = :mid_status, appraisal_form_id = :appraisal_form_id, annual_plan_id = :annual_plan_id
	WHERE midyear_review_id = :midyear_review_id;""",
                     {'midyear_review_id': mid_year_review.midyear_review_id, 'progress_review': mid_year_review.progress_review, 'remarks': mid_year_review.remarks, 'mid_status': mid_year_review.mid_status, 'appraisal_form_id': mid_year_review.appraisal_form_id, 'annual_plan_id': mid_year_review.annual_plan_id})
    db.commit()
    return JSONResponse(status_code=200, content={"message": "mid-year review has been updated"})


# DELETE MID-YEAR REVIEW
async def delete_mid_year_review(midyear_review_id: int, db: Session):
    res = db.execute("""DELETE FROM public.midyear_review
	WHERE midyear_review_id = :midyear_review_id;""",
                     {'midyear_review_id': midyear_review_id})
    db.commit()
    return JSONResponse(status_code=200, content={"message": "mid-year review has been deleted"})
