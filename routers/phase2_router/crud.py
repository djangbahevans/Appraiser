from fastapi import Depends, HTTPException, BackgroundTasks
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
from . import schemas

async def read_mid_year_review(db:Session):
    res = db.execute("""SELECT midyear_review_id, progress_review, remarks, mid_status, appraisal_form_id, annual_plan_id
	FROM public.midyear_review;""")
    res = res.fetchall()
    return res
 
# async def read_appraisal_form(db:Session):
#     res = db.execute("""SELECT department, grade, positions, appraisal_form_id, date, staff_id FROM public.appraisal_form;""")
#     res = res.fetchall()
#     return res

# async def read_annual_plan(db:Session):
#     res = db.execute("""SELECT result_areas, target, resources, appraisal_form_id, annual_plan_id, status, form_hash FROM public.annual_plan;""")
#     res = res.fetchall()
#     return res

# async def read_annual_appraisal(db:Session):
#     res = db.execute("""SELECT grade, comment, field, appraisal_form_id, status, annual_appraisal_id FROM public.annual_appraisal;""")
#     res = res.fetchall()
#     return res

# async def verify_hash_form(hash_:str, db:Session):
#     res = db.execute(""" SELECT public.get_hash_verification(:hash_) """,{'hash_':hash_})
#     res = res.fetchall()
#     return res

# async def read_hash_form(db:Session):
#     res = db.execute("""SELECT hash, email, hash_table_id
# 	FROM public.hash_table;""")
#     res = res.fetchall()
#     return res


async def create_mid_year_review(progress_review, remarks, mid_status, appraisal_form_id, annual_plan_id, db: Session):
    res = db.execute("""INSERT INTO public.midyear_review( progress_review, remarks, mid_status, appraisal_form_id, annual_plan_id, staff_id)
    values(:progress_review, :remarks, :mid_status, :appraisal_form_id, :annual_plan_id, :staff_id);""",
    {'progress_review':progress_review, 'remarks':remarks, 'mid_status':mid_status, 'appraisal_form_id':appraisal_form_id, 'annual_plan_id':annual_plan_id})
    db.commit()
    return JSONResponse(status_code=200, content={"message": "mid-year review has been created"})

# async def create_appraisal_form(deadline, department, positions, grade, date, staff_id, progress_review, remarks, assessment, score, weight, comment, db:Session):
#     res = db.execute("""insert into public.appraisal_form(deadline, department, positions, grade, date, staff_id, progress_review, remarks, assessment, score, weight, comment)
#     values(:deadline, :department, :positions, :grade, :date, :staff_id, :progress_review, :remarks, :assessment, :score, :weight, :comment);""",
#     {'deadline':deadline, 'department':department, 'positions':positions, 'grade':grade, 'date':date, 'staff_id':staff_id, 'progress_review':progress_review, 'remarks':remarks, 'assessment':assessment, 'score':score, 'weight':weight, 'comment':comment})
#     db.commit()
#     return res

# async def appraisal_form(department, grade, positions, date, staff_id, db:Session):
#     res = db.execute("""insert into public.appraisal_form(department, grade, positions, date, staff_id)
#     values(:department, :grade, :positions, :date, :staff_id);""",
#     {'department':department, 'grade':grade, 'positions':positions, 'date':date, 'staff_id':staff_id})
#     db.commit()
#     return res

# async def create_annual_plan(result_areas, target, resources, appraisal_form_id, form_hash, dfb:Session):
#     res = db.execute("""insert into public.annual_plan(result_areas, target, resources, appraisal_form_id, form_hash)
#     values(:result_areas, :target, :resources, :appraisal_form_id, :form_hash);""",
#     {'result_areas':result_areas, 'target':target,'resources':resources, 'appraisal_form_id':appraisal_form_id, 'form_hash':form_hash})
#     db.commit()
#     return res

# async def create_annual_appraisal(grade, comment, field, appraisal_form_id, db:Session):
#     res = db.execute("""insert into public.annual_appraisal(grade, comment, field, appraisal_form_id)
#     values(:grade, :comment, :field, :appraisal_form_id);""",
#     {'grade':grade, 'comment':comment,'field':field, 'appraisal_form_id':appraisal_form_id})
#     db.commit()
#     return res


async def update_mid_year_review(mid_year_review: schemas.update_mid_year_review, db: Session):
    res = db.execute("""UPDATE public.midyear_review
	SET midyear_review_id = :midyear_review_id, progress_review = :progress_review, remarks = :remarks, mid_status = :mid_status, appraisal_form_id = :appraisal_form_id, annual_plan_id = :annual_plan_id
	WHERE midyear_review_id = :midyear_review_id;""",
    {'midyear_review_id':mid_year_review.midyear_review_id, 'progress_review':mid_year_review.progress_review, 'remarks':mid_year_review.remarks, 'mid_status':mid_year_review.mid_status, 'appraisal_form_id':mid_year_review.appraisal_form_id, 'annual_plan_id':mid_year_review.annual_plan_id})
    db.commit()
    return JSONResponse(status_code=200, content={"message": "mid-year review has been updated"})

# async def update_appraisal_form(appraisal_form: schemas.update_appraisal_form, db: Session):
#     res = db.execute("""UPDATE public.appraisal_form
# 	SET appraisal_form_id = :appraisal_form_id, department = :department, grade = :grade, position = :positions, date = :date, staff_id = :staff_id
# 	WHERE appraisal_form_id = :appraisal_form_id;""",
#     {'appraisal_form_id':appraisal_form.appraisal_form_id, 'department': appraisal_form.department, 'grade': appraisal_form.grade, 'positions': appraisal_form.positions, 'date': appraisal_form.date, 'staff_id': appraisal_form.staff_id})
#     db.commit()
#     return res

# async def update_annual_plan(annual_plan: schemas.update_annual_plan, db: Session):
#     res = db.execute("""UPDATE public.annual_plan 
#     SET result_areas = :result_areas, target = :target, resources = :resources, annual_plan_id = :annual_plan_id, status = :status, form_hash = :form_hash
# 	WHERE annual_plan_id = :annual_plan_id;""", 
#     {'result_areas':annual_plan.result_areas, 'target':annual_plan.target,'resources':annual_plan.resources, 'annual_plan_id':annual_plan.annual_plan_id, 'status':annual_plan.status, 'form_hash':annual_plan.form_hash})
#     db.commit()
#     return res

# async def update_annual_appraisal(annual_appraisal: schemas.create_annual_appraisal, db: Session):
#     res = db.execute("""UPDATE public.annual_appraisal
# 	SET grade = :grade, comment = :comment, field = :field, appraisal_form_id = :appraisal_form_id, annual_appraisal_id = :annual_appraisal_id
# 	WHERE annual_appraisal_id = :annual_appraisal_id;""",
#     {'grade':annual_appraisal.grade, 'comment':annual_appraisal.comment, 'field':annual_appraisal.field, 'appraisal_form_id': annual_appraisal.appraisal_form_id, 'annual_appraisal_id':annual_appraisal.annual_appraisal_id})
#     db.commit()
#     return res 


async def delete_mid_year_review(midyear_review_id: int, db: Session):
    res = db.execute("""DELETE FROM public.midyear_review
	WHERE midyear_review_id = :midyear_review_id;""",
    {'midyear_review_id':midyear_review_id})
    db.commit()
    return JSONResponse(status_code=200, content={"message": "mid-year review has been deleted"})

# async def delete_appraisal_form(appraisal_form_id: int, db:Session):
#     res = db.execute("""DELETE FROM public.appraisal_form
# 	WHERE appraisal_form_id = :appraisal_form_id;""",
#     {'appraisal_form_id': appraisal_form.appraisal_form_id})
#     db.commit()
#     return res

# async def delete_annual_plan(annual_plan_id: int, db: Session):
#     res = db.execute("""DELETE FROM public.annual_plan
# 	WHERE annual_plan_id = :annual_plan_id;""",
#     {'annual_plan_id': annual_plan.annual_plan_id})
#     db.commit()
#     return res

# async def delete_annual_appraisal(annual_appraisal_id: int, db: Session):
#     res = db.execute("""DELETE FROM public.annual_appraisal
# 	WHERE annual_appraisal_id = :annual_appraisal.annual_appraisal_id;""",
#     {'annual_appraisal_id':annual_appraisal.annual_appraisal_id})
#     db.commit()
#     return res



# async def create_review_start( db: Session, phase1: schemas.create_review_start ):
#     for item in phase1:
#         phase1 = models.phase1(kra=str(item.kra.dict()), target=str(item.target.dict()), resource_required=str(item.resource_required.dict()) )
#         db.add(phase1)
#     db.commit()
#     return 'success'
    
# async def read_phase_1(db: Session, skip:int, limit:int, search:str, value:str):
#     base = db.query(models.phase1)
#     if search and value:
#         try:
#             base = base.filter(models.phase1.__table__.c[search].like("%" + value + "%"))
#         except KeyError:
#             return base.offset(skip).limit(limit).all()
#     return base.offset(skip).limit(limit).all()

# async def update_hash_form(db: Session, hash:str):
#     pass