from fastapi import BackgroundTasks, APIRouter, Depends, APIRouter
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import timedelta
from starlette.responses import JSONResponse
from database import SessionLocal
from sqlalchemy.orm import Session
from main import settings

# IMPORT EMAILTENPLATES
from static.email_templates.template_2 import template2
from static.email_templates.template_4 import template4
from static.email_templates.template_12 import template12
from static.email_templates.template_13 import template13
from static.email_templates.template_14 import template14
from static.email_templates.template_15 import template15
from static.email_templates.template_16 import template16
from static.email_templates.template_21 import template21
from static.email_templates.template_22 import template22
from static.email_templates.template_23 import template23
from static.email_templates.template_24 import template24
from static.email_templates.template_25 import template25
from static.email_templates.template_27 import template27


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# SETUP MAILTRAP CONNECTION
fm = FastMail(
    ConnectionConfig(
        MAIL_USERNAME = settings.MAIL_USERNAME,
        MAIL_PASSWORD = settings.MAIL_PASSWORD,
        MAIL_FROM = settings.MAIL_FROM,
        MAIL_PORT = settings.MAIL_PORT,
        MAIL_SERVER = settings.MAIL_SERVER,
        MAIL_TLS = settings.MAIL_TLS,
        MAIL_SSL = settings.MAIL_SSL
    )
)

# DEFINE BACKGROUND TASKS
background_tasks = BackgroundTasks()


# BACKGROUND TASKS(WITHOUT SCHEDULER)



# START MID-YEAR REVIEW
async def background_send_2(user_hash_list, background_tasks) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Mid-Year Review Form",
            recipients=[item[1]],
            body=template2.format(url=settings.MID_URL,hash=item[0]),
            subtype="html"
        )        
        background_tasks.add_task(fm.send_message,message)

# APPROVE MID-YEAR REVIEW
async def background_send_39(user_hash_list, background_tasks) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Approve Appraisee Forms",
            recipients=[item["supervisor_email"]],
            body=template23.format( email=[item["email"]], progress_review=[item["progress_review"]], lastname=[item["lastname"]], staff_id=[item["staff_id"]], firstname=[item["firstname"]], remarks=[item["remarks"]], middlename=[item["middlename"]], supervisor=[item["supervisor"]], competency=[item["competency"]], supervisor_email=[item["supervisor_email"]], appraisal_form_id=[item["appraisal_form_id"]]),
            subtype="html"
        )        
        background_tasks.add_task(fm.send_message,message)

# START MID-YEAR REVIEW(INDIVIDUAL)
async def background_send_37(user_hash_list, background_tasks) -> JSONResponse:
    for item in user_hash_list: # CREATE VARIABLES FOR EMAIL TEMPLATES
        message = MessageSchema(
            subject="Start Mid-Year Review",
            recipients=[item[0]], # INDEX OF EMAIL FROM DB QUERY
            body=template2.format(url=settings.MID_URL,hash=item[1]), # VARIABLES IN TEMPLATES STORING URL AND HASH
            subtype="html"
        )        
        background_tasks.add_task(fm.send_message,message)

# SEND MID-YEAR REVIEW DETAILS TO APPROVED
async def background_send_41(user_hash_list, background_tasks) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Mid-Year Review Details",
            recipients=[item["email"]],
            body=template27.format( email=[item["email"]], progress_review=[item["progress_review"]], lastname=[item["lastname"]], staff_id=[item["staff_id"]], firstname=[item["firstname"]], remarks=[item["remarks"]], middlename=[item["middlename"]], supervisor=[item["supervisor"]], competency=[item["competency"]], supervisor_email=[item["supervisor_email"]], appraisal_form_id=[item["appraisal_form_id"]]),
            subtype="html"
        )        
        background_tasks.add_task(fm.send_message,message)


# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# BACKGROUND TASKS(WITH SCHEDULER)
async def background_send_20(user_hash_list) -> JSONResponse:
    for item in user_hash_list: #CREATE VARIABLES FOR EMAIL TEMPLATES
        message = MessageSchema(
            subject="Mid-Year Review (Three Days To Start Reminder)",
            recipients=[item[1]], #INDEX OF EMAIL FROM DB
            body=template4,
            subtype="html"
        )       
        await fm.send_message(message)      

# LAST DAYS FOR MID-YEAR REVIEW
async def background_send_21(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Mid-Year Review (Last Five Days Reminder)",
            recipients=[item["email"]],
            body=template13,
            subtype="html"
        )       
        await fm.send_message(message)

async def background_send_22(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Mid-Year Review (Last Four Days Reminder)",
            recipients=[item["email"]],
            body=template14,
            subtype="html"
        )       
        await fm.send_message(message)

async def background_send_23(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Mid-Year Review (Last Three Days Reminder)",
            recipients=[item["email"]],
            body=template15,
            subtype="html"
        )       
        await fm.send_message(message)

async def background_send_24(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Mid-Year Review (Last Two Days Reminder)",
            recipients=[item["email"]],
            body=template16,
            subtype="html"
        )       
        await fm.send_message(message)

async def background_send_25(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Mid-Year Review (Last Day Reminder)",
            recipients=[item["email"]],
            body=template24,
            subtype="html"
        )       
        await fm.send_message(message)


# START MID-YEAR REVIEW
async def background_send_26(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Start Mid-Year Review",
            recipients=[item[1]],
            body=template12.format(url=settings.START_URL,hash=item[0]),
            subtype="html"
        )        
        await fm.send_message(message)


# LAST DAYS TO APPROVE MID-YEAR REVIEW
async def background_send_27(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Approve Mid-Year Review (Last Five Days Reminder)",
            recipients=[item["supervisor_email"]],
            body=template25.format( email=[item["email"]], progress_review=[item["progress_review"]], lastname=[item["lastname"]], staff_id=[item["staff_id"]], firstname=[item["firstname"]], remarks=[item["remarks"]], middlename=[item["middlename"]], competency=[item["competency"]], supervisor_email=[item["supervisor_email"]], appraisal_form_id=[item["appraisal_form_id"]]),
            subtype="html"
        )        
        background_tasks.add_task(fm.send_message,message)

async def background_send_28(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Approve Mid-Year Review (Last Four Days Reminder)",
            recipients=[item["supervisor_email"]],
            body=template25.format( email=[item["email"]], progress_review=[item["progress_review"]], lastname=[item["lastname"]], staff_id=[item["staff_id"]], firstname=[item["firstname"]], remarks=[item["remarks"]], middlename=[item["middlename"]], competency=[item["competency"]], supervisor_email=[item["supervisor_email"]], appraisal_form_id=[item["appraisal_form_id"]]),
            subtype="html"
        )        
        background_tasks.add_task(fm.send_message,message)

async def background_send_29(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Approve Mid-Year Review (Last Three Days Reminder)",
            recipients=[item["supervisor_email"]],
            body=template25.format( email=[item["email"]], progress_review=[item["progress_review"]], lastname=[item["lastname"]], staff_id=[item["staff_id"]], firstname=[item["firstname"]], remarks=[item["remarks"]], middlename=[item["middlename"]], competency=[item["competency"]], supervisor_email=[item["supervisor_email"]], appraisal_form_id=[item["appraisal_form_id"]]),
            subtype="html"
        )        
        background_tasks.add_task(fm.send_message,message)

async def background_send_30(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Approve Mid-Year Review (Last Two Days Reminder)",
            recipients=[item["supervisor_email"]],
            body=template25.format( email=[item["email"]], progress_review=[item["progress_review"]], lastname=[item["lastname"]], staff_id=[item["staff_id"]], firstname=[item["firstname"]], remarks=[item["remarks"]], middlename=[item["middlename"]], competency=[item["competency"]], supervisor_email=[item["supervisor_email"]], appraisal_form_id=[item["appraisal_form_id"]]),
            subtype="html"
        )        
        background_tasks.add_task(fm.send_message,message)

async def background_send_31(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Approve Mid-Year Review (Last Day Reminder)",
            recipients=[item["supervisor_email"]],
            body=template25.format( email=[item["email"]], progress_review=[item["progress_review"]], lastname=[item["lastname"]], staff_id=[item["staff_id"]], firstname=[item["firstname"]], remarks=[item["remarks"]], middlename=[item["middlename"]], competency=[item["competency"]], supervisor_email=[item["supervisor_email"]], appraisal_form_id=[item["appraisal_form_id"]]),
            subtype="html"
        )        
        background_tasks.add_task(fm.send_message,message)

# MID-YEAR REVIEW APPROVED
async def background_send_32(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Mid-Year Review Approved",
            recipients=[item[0]],
            body=template23.format( email=[item[0]], progress_review=[item[1]], lastname=[item[2]], staff_id=[item[3]], firstname=[item[4]], remarks=[item[5]], middlename=[item[6]], competency=[item[7]], appraisal_form_id=[item[8]], supervisor_email=[item[9]]),
            subtype="html"
        )        
        await fm.send_message(message)


# MID-YEAR REVIEW DISAPPROVED
async def background_send_38(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Form Disaproved",
            recipients=[item[0]],
            body=template22.format( email=[item[0]], progress_review=[item[1]], lastname=[item[2]], staff_id=[item[3]], firstname=[item[4]], remarks=[item[5]], middlename=[item[6]], competency=[item[7]], appraisal_form_id=[item[8]], supervisor_email=[item[9]], midyear_review_comment=[item[10]]),
            subtype="html"
        )        
        await fm.send_message(message)

# APPROVE MID-YEAR REVIEW
async def background_send_36(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Approve Mid-Year Review",
            recipients=[item[9]],
            body=template21.format( email=[item[0]], progress_review=[item[1]], lastname=[item[2]], staff_id=[item[3]], firstname=[item[4]], remarks=[item[5]], middlename=[item[6]], competency=[item[7]], appraisal_form_id=[item[8]], supervisor_email=[item[9]]),
            subtype="html"
        )        
        await fm.send_message(message)

# EMAIL ENDPOINTS FOR MANUALLY SENT EMAILS

# SEND MID-YEAR LINK TO ALL STAFF
@router.post("/midyearreviewemail/")
async def start_midyear_review_(background_tasks:BackgroundTasks, db:Session=Depends(get_db)):
    res = db.execute("""SELECT * FROM public.hash_table""")
    res = res.fetchall()
    return await background_send_2(res, background_tasks)

# SEND MID-YEAR LINK TO INDIVIDUAL STAFF
@router.post("/midyearreviewemailstaff/")
async def mid_year_review_staff(email:str, background_tasks:BackgroundTasks, db:Session=Depends(get_db)):
    res = db.execute("""SELECT email, hash FROM public.hash_table where email=:email""", {'email':email}) # SELECT EMAIL AND HASH PAIR FROM HASH TABLE 
    res = res.fetchall()
    return await background_send_37(res, background_tasks)

# SEND REMINDER TO SUPERVISORS TO APPROVE SUBMITTED MIDYEAR REVIEW FORMS
@router.post("/approvemidyearreview/")
async def approve_completed_mid_year_review(background_tasks:BackgroundTasks, db:Session=Depends(get_db)):
    res = db.execute("""SELECT public.get_list_of_waiting_approval('Mid', 1)""") # SELECT EMAIL FROM WAITING APPROVAL FUNCTION
    res = res.first()[0]
    return await background_send_39(res, background_tasks)

# SEND MID-YEAR DETAILS TO APPROVED
@router.post("/midformdetails/")
async def send_midyear_review_details_to_approved(background_tasks:BackgroundTasks, db:Session=Depends(get_db)): # SEND FORM DETAILS TO APPROVED STAFF
    res = db.execute("""SELECT public.get_list_of_approved_form('Mid', 1)""") # SELECT EMAIL FROM LIST OF APPROVED FUNCTION IN DB
    res = res.first()[0]
    return await background_send_41(res, background_tasks)

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# SCHEDULED REMINDERS FOR APPRAISEE


# MID YEAR

# @router.post("/threedaysreminder/")
async def three_days_to_mid_reminder():
    res = db.execute("""SELECT * FROM public.hash_table""") # SELECT EMAIL FROM HASH TABLE
    res = res.fetchall()
    return await background_send_20(res)   

# @router.post("/startday/")
async def start_mid_year_review():
    res = db.execute("""SELECT * FROM public.hash_table""") # SELECT EMAIL FROM HASH TABLE
    res = res.fetchall()
    return await background_send_26(res)  

# @router.post("/lastfivedaysreminder/")
async def last_five_days_to_mid_reminder():
    res = db.execute("""SELECT public.get_list_of_incompleted_form('Mid', 1)""")
    res = res.first()[0]
    return await background_send_21(res)

# @router.post("/lastfourdaysreminder/")
async def last_four_days_to_mid_reminder():
    res = db.execute("""SELECT public.get_list_of_incompleted_form('Mid', 1)""")
    res = res.first()[0]
    return await background_send_22(res)

# @router.post("/lastthreedaysreminder/")
async def last_three_days_to_mid_reminder():
    res = db.execute("""SELECT public.get_list_of_incompleted_form('Mid', 1)""")
    res = res.first()[0]
    return await background_send_23(res)

# @router.post("/lasttwodaysreminder/")
async def last_two_days_to_mid_reminder():
    res = db.execute("""SELECT public.get_list_of_incompleted_form('Mid', 1)""")
    res = res.first()[0]
    return await background_send_24(res)

# @router.post("/lastdayreminder/")
async def last_day_to_mid_reminder():
    res = db.execute("""SELECT public.get_list_of_incompleted_form('Mid', 1)""")
    res = res.first()[0]
    return await background_send_25(res)    


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# SCHEDULED REMINDERS FOR APPRAISER


# MID YEAR

# @router.post("/approvemidyearreview/")
async def approve_mid_year_review(appraisal_form_id): # TAKE APPRAISAL FORM ID FROM "create_mid_year_review" FUNCTION IN phase_2 Router, crud.py 
    res = db.execute(""" SELECT email, progress_review, lastname, staff_id, firstname, remarks, middlename, competency, appraisal_form_id, supervisor_email FROM public.view_users_form_details where appraisal_form_id=:appraisal_form_id  """, {'appraisal_form_id':appraisal_form_id}) # SELECT EMAIL OF SUPERVISOR FROM DB USING APPRAISAL FORM ID IN ANNUAL PLAN FORM  
    res = res.fetchall()
    return await background_send_36(res)

# @router.post("/midyearreviewapproved/")
async def mid_year_review_approved(appraisal_form_id): # TAKE APPRAISAL FORM ID FROM "approve_form" FUNCTION IN appraiser Router, crud.py 
    res = db.execute(""" SELECT email, progress_review, lastname, staff_id, firstname, remarks, middlename, competency, appraisal_form_id, supervisor_email FROM public.view_users_form_details where appraisal_form_id=:appraisal_form_id  """, {'appraisal_form_id':appraisal_form_id}) # SELECT EMAIL FROM DB USING APPRAISAL FORM ID IN APPROVE FORM  
    res = res.fetchall()
    return await background_send_32(res)

# @router.post("/midyearreviewdisapproved/")
async def mid_year_review_disapproved(appraisal_form_id): # TAKE APPRAISAL FORM ID FROM "approve_form" FUNCTION IN appraiser Router, crud.py 
    res = db.execute(""" SELECT email, progress_review, lastname, staff_id, firstname, remarks, middlename, competency, appraisal_form_id, supervisor_email, midyear_review_comment FROM public.view_users_form_details where appraisal_form_id=:appraisal_form_id  """, {'appraisal_form_id':appraisal_form_id}) # SELECT EMAIL FROM DB USING APPRAISAL FORM ID IN APPROVE FORM  
    res = res.fetchall()
    return await background_send_38(res)

# @router.post("/lastfivedaystoapprovereminder/")
async def last_five_days_to_approve_mid_reminder():
    res = db.execute("""SELECT public.get_list_of_waiting_approval('Mid', 1)""")
    res = res.first()[0]
    return await background_send_27(res)

# @router.post("/lastfourdaystoapprovereminder/")
async def last_four_days_to_approve_mid_reminder():
    res = db.execute("""SELECT public.get_list_of_waiting_approval('Mid', 1)""")
    res = res.first()[0]
    return await background_send_28(res)

# @router.post("/lastthreedaystoapprovereminder/")
async def last_three_days_to_approve_mid_reminder():
    res = db.execute("""SELECT public.get_list_of_waiting_approval('Mid', 1)""")
    res = res.first()[0]
    return await background_send_29(res)

# @router.post("/lasttwodaystoapprovereminder/")
async def last_two_days_to_approve_mid_reminder():
    res = db.execute("""SELECT public.get_list_of_waiting_approval('Mid', 1)""")
    res = res.first()[0]
    return await background_send_30(res)

# @router.post("/lastdaytoapprovereminder/")
async def last_day_to_approve_mid_reminder():
    res = db.execute("""SELECT public.get_list_of_waiting_approval('Mid', 1)""")
    res = res.first()[0]
    return await background_send_31(res)




# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

jobstores = { 'default': SQLAlchemyJobStore(url='sqlite:///./sql_app.db')}
executors = { 'default': ThreadPoolExecutor(20), 'processpool': ProcessPoolExecutor(5)}
job_defaults = { 'coalesce': False, 'max_instances': 3}

#  DEADLINES
db=SessionLocal()


mid_deadline=db.execute(""" SELECT * FROM deadline WHERE deadline_type = 'Mid' """)
mid_deadline=mid_deadline.fetchall()

# DATES 

mid_start_date=mid_deadline[0][1]
mid_end_date=mid_deadline[0][2]
mid_send_date=mid_start_date-timedelta(3)
mid_send_date_2=mid_end_date-timedelta(5)
mid_send_date_3=mid_end_date-timedelta(4)
mid_send_date_4=mid_end_date-timedelta(3)
mid_send_date_5=mid_end_date-timedelta(2)
mid_send_date_6=mid_end_date


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# JOB SCHEDULER


# MID
scheduler = AsyncIOScheduler()  
scheduler.add_job(func=three_days_to_mid_reminder, trigger='date', run_date=mid_send_date)
scheduler.add_job(func=start_mid_year_review, trigger='date', run_date=mid_start_date)
scheduler.add_job(func=last_five_days_to_mid_reminder, trigger='date', run_date=mid_send_date_2)
scheduler.add_job(func=last_four_days_to_mid_reminder, trigger='date', run_date=mid_send_date_3)
scheduler.add_job(func=last_three_days_to_mid_reminder, trigger='date', run_date=mid_send_date_4)
scheduler.add_job(func=last_two_days_to_mid_reminder, trigger='date', run_date=mid_send_date_5)
scheduler.add_job(func=last_day_to_mid_reminder, trigger='date', run_date=mid_send_date_6)
scheduler.add_job(func=last_five_days_to_approve_mid_reminder, trigger='date', run_date=mid_send_date_2)
scheduler.add_job(func=last_four_days_to_approve_mid_reminder, trigger='date', run_date=mid_send_date_3)
scheduler.add_job(func=last_three_days_to_approve_mid_reminder, trigger='date', run_date=mid_send_date_4)
scheduler.add_job(func=last_two_days_to_approve_mid_reminder, trigger='date', run_date=mid_send_date_5)
scheduler.add_job(func=last_day_to_approve_mid_reminder, trigger='date', run_date=mid_send_date_6)


scheduler.start() 