from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from datetime import timedelta

from app.config import settings
from app.database import SessionLocal
# IMPORT EMAILTENPLATES
from app.static.email_templates.template_1 import template1
from app.static.email_templates.template_2 import template2
from app.static.email_templates.template_3 import template3
from app.static.email_templates.template_4 import template4
from app.static.email_templates.template_5 import template5
from app.static.email_templates.template_6 import template6
from app.static.email_templates.template_7 import template7
from app.static.email_templates.template_8 import template8
from app.static.email_templates.template_9 import template9
from app.static.email_templates.template_10 import template10
from app.static.email_templates.template_11 import template11
from app.static.email_templates.template_12 import template12
from app.static.email_templates.template_13 import template13
from app.static.email_templates.template_14 import template14
from app.static.email_templates.template_15 import template15
from app.static.email_templates.template_16 import template16
from app.static.email_templates.template_17 import template17
from app.static.email_templates.template_18 import template18
from app.static.email_templates.template_19 import template19
from app.static.email_templates.template_20 import template20
from app.static.email_templates.template_21 import template21
from app.static.email_templates.template_22 import template22
from app.static.email_templates.template_23 import template23
from app.static.email_templates.template_24 import template24
from app.static.email_templates.template_25 import template25
from app.static.email_templates.template_26 import template26
from app.static.email_templates.template_27 import template27
from app.static.email_templates.template_28 import template28
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

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
        MAIL_SSL = settings.MAIL_SSL,
        USE_CREDENTIALS = settings.USE_CREDENTIALS
    )
)

# DEFINE BACKGROUND TASKS
background_tasks = BackgroundTasks()


# BACKGROUND TASKS(WITHOUT SCHEDULER)

# START ANNUAL PLAN
async def background_send(user_hash_list, background_tasks) -> JSONResponse:
    for item in user_hash_list: # CREATE VARIABLES FOR EMAIL TEMPLATES
        message = MessageSchema(
            subject="Start Appraisal Form",
            recipients=[item[1]], # INDEX OF EMAIL FROM DB QUERY
            body=template1.format(url=settings.START_URL,hash=item[0]), # VARIABLES IN TEMPLATES STORING URL AND HASH
            subtype="html"
        )        
        background_tasks.add_task(fm.send_message,message)

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

# START END OF YEAR REVIEW
async def background_send_3(user_hash_list, background_tasks) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="End of Year Review Form",
            recipients=[item[1]],
            body=template3.format(url=settings.START_URL,hash=item[0]),
            subtype="html"
        )        
        background_tasks.add_task(fm.send_message,message)

# ANNUAL PLAN DETAILS
async def background_send_4(user_hash_list, background_tasks) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Appraisal Form Details",
            recipients=[item["email"]],
            body=template5.format( email=[item["email"]], target=[item["target"]], lastname=[item["lastname"]], staff_id=[item["staff_id"]], firstname=[item["firstname"]], resources=[item["resources"]], middlename=[item["middlename"]], supervisor=[item["supervisor"]], result_areas=[item["result_areas"]], supervisor_email=[item["supervisor_email"]], appraisal_form_id=[item["appraisal_form_id"]]),
            subtype="html"
        )        
        background_tasks.add_task(fm.send_message,message)

# APPROVE ANNUAL PLAN
async def background_send_5(user_hash_list, background_tasks) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Approve Appraisee Forms",
            recipients=[item["supervisor_email"]],
            body=template5.format( email=[item["email"]], target=[item["target"]], lastname=[item["lastname"]], staff_id=[item["staff_id"]], firstname=[item["firstname"]], resources=[item["resources"]], middlename=[item["middlename"]], supervisor=[item["supervisor"]], result_areas=[item["result_areas"]], supervisor_email=[item["supervisor_email"]], appraisal_form_id=[item["appraisal_form_id"]]),
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

# REMIND STAFF TO FILL ANNUAL PLAN (NO LINK)
async def background_send_35(user_hash_list, background_tasks) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Reminder To Start Annual Plan",
            recipients=[item[0]],
            body=template19.format( target=[item[1]], resources=[item[2]],result_areas=[item[3]]),
            subtype="html"
        )        
        background_tasks.add_task(fm.send_message,message)

# REMIND STAFF TO FILL MID-YEAR REVIEW (NO LINK)
async def background_send_46(user_hash_list, background_tasks) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Reminder To Start Mid-Year Review",
            recipients=[item[0]],
            body=template28.format( progress_review=[item[1]], remarks=[item[2]],competency=[item[3]]),
            subtype="html"
        )        
        background_tasks.add_task(fm.send_message,message)

# START ANNUAL PLAN(INDIVIDUAL)
async def background_send_34(user_hash_list, background_tasks) -> JSONResponse:
    for item in user_hash_list: # CREATE VARIABLES FOR EMAIL TEMPLATES
        message = MessageSchema(
            subject="Start Appraisal Form",
            recipients=[item[0]], # INDEX OF EMAIL FROM DB QUERY
            body=template1.format(url=settings.START_URL,hash=item[1]), # VARIABLES IN TEMPLATES STORING URL AND HASH
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

# START END OF YEAR REVIEW(INDIVIDUAL)
async def background_send_45(user_hash_list, background_tasks) -> JSONResponse:
    for item in user_hash_list: # CREATE VARIABLES FOR EMAIL TEMPLATES
        message = MessageSchema(
            subject="Start End of Year Review",
            recipients=[item[0]], # INDEX OF EMAIL FROM DB QUERY
            body=template3.format(url=settings.END_URL,hash=item[1]), # VARIABLES IN TEMPLATES STORING URL AND HASH
            subtype="html"
        )        
        background_tasks.add_task(fm.send_message,message)

# SEND ANNUAL PLAN DETAILS TO APPROVED
async def background_send_40(user_hash_list, background_tasks) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Appraisal Form Details",
            recipients=[item["email"]],
            body=template26.format( email=[item["email"]], target=[item["target"]], lastname=[item["lastname"]], staff_id=[item["staff_id"]], firstname=[item["firstname"]], resources=[item["resources"]], middlename=[item["middlename"]], supervisor=[item["supervisor"]], result_areas=[item["result_areas"]], supervisor_email=[item["supervisor_email"]], appraisal_form_id=[item["appraisal_form_id"]]),
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

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# BACKGROUND TASKS(WITH SCHEDULER)

async def background_send_6(user_hash_list) -> JSONResponse:
    for item in user_hash_list: #CREATE VARIABLES FOR EMAIL TEMPLATES
        message = MessageSchema(
            subject="Appraisal Form (Three Days To Start Reminder)",
            recipients=[item[1]], #INDEX OF EMAIL FROM DB
            body=template6,
            subtype="html"
        )       
        await fm.send_message(message)      

# LAST DAYS TO END START OF YEAR REVIEW
async def background_send_7(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Appraisal Form (Last Five Days Reminder)",
            recipients=[item["email"]],
            body=template7,
            subtype="html"
        )       
        await fm.send_message(message)

async def background_send_8(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Appraisal Form (Last Four Days Reminder)",
            recipients=[item["email"]],
            body=template8,
            subtype="html"
        )       
        await fm.send_message(message)

async def background_send_9(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Appraisal Form (Last Three Days Reminder)",
            recipients=[item["email"]],
            body=template9,
            subtype="html"
        )       
        await fm.send_message(message)

async def background_send_10(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Appraisal Form (Last Two Days Reminder)",
            recipients=[item["email"]],
            body=template10,
            subtype="html"
        )       
        await fm.send_message(message)

async def background_send_11(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Appraisal Form (Last Day Reminder)",
            recipients=[item["email"]],
            body=template11,
            subtype="html"
        )       
        await fm.send_message(message)

# START ANNUAL PLAN
async def background_send_12(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Start Appraisal Form",
            recipients=[item[1]],
            body=template1.format(url=settings.START_URL,hash=item[0]),
            subtype="html"
        )        
        await fm.send_message(message)

# LAST DAYS TO APPROVE START OF YEAR REVIEW
async def background_send_13(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Approve Appraisee Forms(Last Five Days Reminder)",
            recipients=[item["supervisor_email"]],
            body=template5.format( email=[item["email"]], target=[item["target"]], lastname=[item["lastname"]], staff_id=[item["staff_id"]], firstname=[item["firstname"]],  resources=[item["resources"]], middlename=[item["middlename"]], result_areas=[item["result_areas"]], supervisor_email=[item["supervisor_email"]], appraisal_form_id=[item["appraisal_form_id"]]),
            subtype="html"
        )        
        background_tasks.add_task(fm.send_message,message)

async def background_send_14(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Approve Appraisee Forms(Last Four Days Reminder)",
            recipients=[item["supervisor_email"]],
            body=template5.format( email=[item["email"]], target=[item["target"]], lastname=[item["lastname"]], staff_id=[item["staff_id"]], firstname=[item["firstname"]], resources=[item["resources"]], middlename=[item["middlename"]], result_areas=[item["result_areas"]], supervisor_email=[item["supervisor_email"]], appraisal_form_id=[item["appraisal_form_id"]]),
            subtype="html"
        )        
        background_tasks.add_task(fm.send_message,message)

async def background_send_15(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Approve Appraisee Forms(Last Three Days Reminder)",
            recipients=[item["supervisor_email"]],
            body=template5.format( email=[item["email"]], target=[item["target"]], lastname=[item["lastname"]], staff_id=[item["staff_id"]], firstname=[item["firstname"]], resources=[item["resources"]], middlename=[item["middlename"]], result_areas=[item["result_areas"]], supervisor_email=[item["supervisor_email"]], appraisal_form_id=[item["appraisal_form_id"]]),
            subtype="html"
        )        
        background_tasks.add_task(fm.send_message,message)

async def background_send_16(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Approve Appraisee Forms(Last Two Days Reminder)",
            recipients=[item["supervisor_email"]],
            body=template5.format( email=[item["email"]], target=[item["target"]], lastname=[item["lastname"]], staff_id=[item["staff_id"]], firstname=[item["firstname"]], resources=[item["resources"]], middlename=[item["middlename"]], result_areas=[item["result_areas"]], supervisor_email=[item["supervisor_email"]], appraisal_form_id=[item["appraisal_form_id"]]),
            subtype="html"
        )        
        background_tasks.add_task(fm.send_message,message)

async def background_send_17(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Approve Appraisee Forms(Last Day Reminder)",
            recipients=[item["supervisor_email"]],
            body=template5.format( email=[item["email"]], target=[item["target"]], lastname=[item["lastname"]], staff_id=[item["staff_id"]], firstname=[item["firstname"]], resources=[item["resources"]], middlename=[item["middlename"]], result_areas=[item["result_areas"]], supervisor_email=[item["supervisor_email"]], appraisal_form_id=[item["appraisal_form_id"]]),
            subtype="html"
        )        
        background_tasks.add_task(fm.send_message,message)


# APPROVE START OF YEAR REVIEW
async def background_send_18(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Approve Appraisee Forms (Alert)",
            recipients=[item[9]],
            body=template17.format( email=[item[0]], target=[item[1]], lastname=[item[2]], staff_id=[item[3]], firstname=[item[4]], resources=[item[5]], middlename=[item[6]], result_areas=[item[7]], appraisal_form_id=[item[8]], supervisor_email=[item[9]]),
            subtype="html"
        )        
        await fm.send_message(message)

async def background_send_19(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Form Approved",
            recipients=[item[0]],
            body=template18.format( email=[item[0]], target=[item[1]], lastname=[item[2]], staff_id=[item[3]], firstname=[item[4]], resources=[item[5]], middlename=[item[6]], result_areas=[item[7]], appraisal_form_id=[item[8]], supervisor_email=[item[9]]),
            subtype="html"
        )        
        await fm.send_message(message)

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

# START OF YEAR REVIEW DISAPPROVED
async def background_send_33(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Form Disaproved",
            recipients=[item[0]],
            body=template20.format( email=[item[0]], target=[item[1]], lastname=[item[2]], staff_id=[item[3]], firstname=[item[4]], resources=[item[5]], middlename=[item[6]], result_areas=[item[7]], appraisal_form_id=[item[8]], supervisor_email=[item[9]], annual_plan_comment=[item[10]]),
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

# START ANNUAL PLAN
@router.post("/startreviewemail/")
async def start_annual_plan(background_tasks:BackgroundTasks, db:Session=Depends(get_db)):
    res = db.execute("""SELECT * FROM public.hash_table""") # SELECT EMAIL AND HASH PAIR FROM HASH TABLE 
    res = res.fetchall()
    return await background_send(res, background_tasks)

# SEND START LINK TO INDIVIDUAL STAFF
@router.post("/startreviewemailstaff/")
async def start_annual_plan_staff(email:str, background_tasks:BackgroundTasks, db:Session=Depends(get_db)):
    res = db.execute("""SELECT email, hash FROM public.hash_table where email=:email""", {'email':email}) # SELECT EMAIL AND HASH PAIR FROM HASH TABLE 
    res = res.fetchall()
    return await background_send_34(res, background_tasks)

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

# SEND END OF YEAR LINK TO ALL STAFF
@router.post("/endofyearreviewemail/")
async def start_end_0f_year_review_(background_tasks:BackgroundTasks, db:Session=Depends(get_db)):
    res = db.execute("""SELECT * FROM public.hash_table""")
    res = res.fetchall()
    return await background_send_3(res, background_tasks)

# SEND END OF YEAR LINK TO INDIVIDUAL STAFF
@router.post("/endofyearreviewmailstaff/")
async def end_of_year_review_staff(email:str, background_tasks:BackgroundTasks, db:Session=Depends(get_db)):
    res = db.execute("""SELECT email, hash FROM public.hash_table where email=:email""", {'email':email}) # SELECT EMAIL AND HASH PAIR FROM HASH TABLE 
    res = res.fetchall()
    return await background_send_45(res, background_tasks)

# SEND ANNUAL PLAN DETAILS TO APPROVED
@router.post("/startformdetails/")
async def send_annual_plan_details_to_approved(background_tasks:BackgroundTasks, db:Session=Depends(get_db)): # SEND FORM DETAILS TO APPROVED STAFF
    res = db.execute("""SELECT public.get_list_of_approved_form('Start', 1)""") # SELECT EMAIL FROM LIST OF APPROVED FUNCTION IN DB
    res = res.first()[0]
    return await background_send_40(res, background_tasks)

# SEND MID-YEAR DETAILS TO APPROVED
@router.post("/midformdetails/")
async def send_midyear_review_details_to_approved(background_tasks:BackgroundTasks, db:Session=Depends(get_db)): # SEND FORM DETAILS TO APPROVED STAFF
    res = db.execute("""SELECT public.get_list_of_approved_form('Mid', 1)""") # SELECT EMAIL FROM LIST OF APPROVED FUNCTION IN DB
    res = res.first()[0]
    return await background_send_41(res, background_tasks)

# SEND REMINDER TO SUPERVISORS TO APPROVE SUBMITTED ANNUAL PLAN FORMS
@router.post("/approvestartreview/")
async def approve_completed_annual_plan(background_tasks:BackgroundTasks, db:Session=Depends(get_db)):
    res = db.execute("""SELECT public.get_list_of_waiting_approval('Start', 1)""") # SELECT EMAIL FROM WAITING APPROVAL FUNCTION
    res = res.first()[0]
    return await background_send_5(res, background_tasks)

# SEND REMINDER TO SUPERVISORS TO APPROVE SUBMITTED MIDYEAR REVIEW FORMS
@router.post("/approvemidyearreview/")
async def approve_completed_mid_year_review(background_tasks:BackgroundTasks, db:Session=Depends(get_db)):
    res = db.execute("""SELECT public.get_list_of_waiting_approval('Mid', 1)""") # SELECT EMAIL FROM WAITING APPROVAL FUNCTION
    res = res.first()[0]
    return await background_send_39(res, background_tasks)

# REMIND APPRAISEE TO CHECK EMAIL WITH LINK FOR START OF YEAR REVIEW
@router.post("/startannualplanreminder/{supervisor}/")
async def start_annual_plan_reminder(background_tasks:BackgroundTasks, supervisor:int, db:Session=Depends(get_db)):
    res = db.execute("""select email, target, resources, result_areas from public.view_users_form_details where supervisor=:supervisor and start_status=0 and target is null and result_areas is null and resources is null""", {'supervisor':supervisor}) # SELECT EMAIL AND HASH PAIR FROM HASH TABLE 
    res = res.fetchall()
    return await background_send_35(res, background_tasks)

# REMIND APPRAISEE TO CHECK EMAIL WITH LINK FOR MID-YEAR REVIEW
@router.post("/midyearreviewreminder/{supervisor}/")
async def start_midyear_review_reminder(background_tasks:BackgroundTasks, supervisor:int, db:Session=Depends(get_db)):
    res = db.execute("""select email, progress_review, remarks, competency from public.view_users_form_details where supervisor=:supervisor and mid_status=0 and progress_review is null and remarks is null and competency is null""", {'supervisor':supervisor}) # SELECT EMAIL AND HASH PAIR FROM HASH TABLE 
    res = res.fetchall()
    return await background_send_46(res, background_tasks)

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# SCHEDULED REMINDERS FOR APPRAISEE

# START OF YEAR

# @router.post("/threedaysreminder/")
async def three_days_to_start_reminder():
    res = db.execute("""SELECT * FROM public.hash_table""") # SELECT EMAIL FROM HASH TABLE
    res = res.fetchall()
    return await background_send_6(res)   

# @router.post("/startday/")
async def start_annual_plan():
    res = db.execute("""SELECT * FROM public.hash_table""") # SELECT EMAIL FROM HASH TABLE
    res = res.fetchall()
    return await background_send_12(res)  

# @router.post("/lastfivedaysreminder/")
async def last_five_days_reminder():
    res = db.execute("""SELECT public.get_list_of_incompleted_form('Start', 1)""")
    res = res.first()[0]
    return await background_send_7(res)

# @router.post("/lastfourdaysreminder/")
async def last_four_days_reminder():
    res = db.execute("""SELECT public.get_list_of_incompleted_form('Start', 1)""")
    res = res.first()[0]
    return await background_send_8(res)

# @router.post("/lastthreedaysreminder/")
async def last_three_days_reminder():
    res = db.execute("""SELECT public.get_list_of_incompleted_form('Start', 1)""")
    res = res.first()[0]
    return await background_send_9(res)

# @router.post("/lasttwodaysreminder/")
async def last_two_days_reminder():
    res = db.execute("""SELECT public.get_list_of_incompleted_form('Start', 1)""")
    res = res.first()[0]
    return await background_send_10(res)

# @router.post("/lastdayreminder/")
async def last_day_reminder():
    res = db.execute("""SELECT public.get_list_of_incompleted_form('Start', 1)""")
    res = res.first()[0]
    return await background_send_11(res)    


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


# END OF YEAR

# @router.post("/threedaysreminder/")
async def three_days_to_end_reminder():
    res = db.execute("""SELECT * FROM public.hash_table""") # SELECT EMAIL FROM HASH TABLE
    res = res.fetchall()
    return await background_send_20(res)   

# @router.post("/startday/")
async def start_end_year_review():
    res = db.execute("""SELECT * FROM public.hash_table""") # SELECT EMAIL FROM HASH TABLE
    res = res.fetchall()
    return await background_send_26(res)  

# @router.post("/lastfivedaysreminder/")
async def last_five_days_to_end_reminder():
    res = db.execute("""SELECT public.get_list_of_incompleted_form('End', 1)""")
    res = res.first()[0]
    return await background_send_21(res)

# @router.post("/lastfourdaysreminder/")
async def last_four_days_to_end_reminder():
    res = db.execute("""SELECT public.get_list_of_incompleted_form('End', 1)""")
    res = res.first()[0]
    return await background_send_22(res)

# @router.post("/lastthreedaysreminder/")
async def last_three_days_to_end_reminder():
    res = db.execute("""SELECT public.get_list_of_incompleted_form('End', 1)""")
    res = res.first()[0]
    return await background_send_23(res)

# @router.post("/lasttwodaysreminder/")
async def last_two_days_to_end_reminder():
    res = db.execute("""SELECT public.get_list_of_incompleted_form('End', 1)""")
    res = res.first()[0]
    return await background_send_24(res)

# @router.post("/lastdayreminder/")
async def last_day_to_end_reminder():
    res = db.execute("""SELECT public.get_list_of_incompleted_form('End', 1)""")
    res = res.first()[0]
    return await background_send_25(res)    


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# SCHEDULED REMINDERS FOR APPRAISER

# START OF YEAR

# @router.post("/approveannualplan/")
async def approve_annual_plan(appraisal_form_id): # TAKE APPRAISAL FORM ID FROM "create_annual_plan" FUNCTION IN phase_1 Router, crud.py 
    res = db.execute(""" SELECT email, target, lastname, staff_id, firstname, resources, middlename, result_areas, appraisal_form_id, supervisor_email FROM view_users_form_details where appraisal_form_id=:appraisal_form_id  """, {'appraisal_form_id':appraisal_form_id}) # SELECT EMAIL OF SUPERVISOR FROM DB USING APPRAISAL FORM ID IN ANNUAL PLAN FORM  
    res = res.fetchall()
    return await background_send_18(res)

# @router.post("/annualplanapproved/")
async def annual_plan_approved(appraisal_form_id): # TAKE APPRAISAL FORM ID FROM "approve_form" FUNCTION IN appraiser Router, crud.py 
    res = db.execute(""" SELECT email, target, lastname, staff_id, firstname, resources, middlename, result_areas, appraisal_form_id, supervisor_email FROM view_users_form_details where appraisal_form_id=:appraisal_form_id  """, {'appraisal_form_id':appraisal_form_id}) # SELECT EMAIL FROM DB USING APPRAISAL FORM ID IN APPROVE FORM  
    res = res.fetchall()
    return await background_send_19(res)

# @router.post("/annualplandisapproved/")
async def annual_plan_disapproved(appraisal_form_id): # TAKE APPRAISAL FORM ID FROM "approve_form" FUNCTION IN appraiser Router, crud.py 
    res = db.execute(""" SELECT email, target, lastname, staff_id, firstname, resources, middlename, result_areas, appraisal_form_id, supervisor_email, annual_plan_comment FROM view_users_form_details where appraisal_form_id=:appraisal_form_id  """, {'appraisal_form_id':appraisal_form_id}) # SELECT EMAIL FROM DB USING APPRAISAL FORM ID IN APPROVE FORM  
    res = res.fetchall()
    return await background_send_33(res)

# @router.post("/lastfivedaystoapprovereminder/")
async def last_five_days_to_approve_reminder():
    res = db.execute("""SELECT public.get_list_of_waiting_approval('Start', 1)""")
    res = res.first()[0]
    return await background_send_13(res)

# @router.post("/lastfourdaystoapprovereminder/")
async def last_four_days_to_approve_reminder():
    res = db.execute("""SELECT public.get_list_of_waiting_approval('Start', 1)""")
    res = res.first()[0]
    return await background_send_14(res)

# @router.post("/lastthreedaystoapprovereminder/")
async def last_three_days_to_approve_reminder():
    res = db.execute("""SELECT public.get_list_of_waiting_approval('Start', 1)""")
    res = res.first()[0]
    return await background_send_15(res)

# @router.post("/lasttwodaystoapprovereminder/")
async def last_two_days_to_approve_reminder():
    res = db.execute("""SELECT public.get_list_of_waiting_approval('Start', 1)""")
    res = res.first()[0]
    return await background_send_16(res)

# @router.post("/lastdaytoapprovereminder/")
async def last_day_to_approve_reminder():
    res = db.execute("""SELECT public.get_list_of_waiting_approval('Start', 1)""")
    res = res.first()[0]
    return await background_send_17(res)


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


# END OF YEAR

# @router.post("/approveendyearreview/")
async def approve_end_year_review(appraisal_form_id): # TAKE APPRAISAL FORM ID FROM "create_mid_year_review" FUNCTION IN phase_2 Router, crud.py 
    res = db.execute(""" SELECT email, progress_review, lastname, staff_id, firstname, remarks, middlename, competency, appraisal_form_id, supervisor_email FROM public.view_users_form_details where appraisal_form_id=:appraisal_form_id  """, {'appraisal_form_id':appraisal_form_id}) # SELECT EMAIL OF SUPERVISOR FROM DB USING APPRAISAL FORM ID IN ANNUAL PLAN FORM  
    res = res.fetchall()
    return await background_send_36(res)

# @router.post("/midyearreviewapproved/")
async def end_year_review_approved(appraisal_form_id): # TAKE APPRAISAL FORM ID FROM "approve_form" FUNCTION IN appraiser Router, crud.py 
    res = db.execute(""" SELECT email, progress_review, lastname, staff_id, firstname, remarks, middlename, competency, appraisal_form_id, supervisor_email FROM public.view_users_form_details where appraisal_form_id=:appraisal_form_id  """, {'appraisal_form_id':appraisal_form_id}) # SELECT EMAIL FROM DB USING APPRAISAL FORM ID IN APPROVE FORM  
    res = res.fetchall()
    return await background_send_32(res)

# @router.post("/endyearreviewdisapproved/")
async def end_year_review_disapproved(appraisal_form_id): # TAKE APPRAISAL FORM ID FROM "approve_form" FUNCTION IN appraiser Router, crud.py 
    res = db.execute(""" SELECT email, progress_review, lastname, staff_id, firstname, remarks, middlename, competency, appraisal_form_id, supervisor_email, midyear_review_comment FROM public.view_users_form_details where appraisal_form_id=:appraisal_form_id  """, {'appraisal_form_id':appraisal_form_id}) # SELECT EMAIL FROM DB USING APPRAISAL FORM ID IN APPROVE FORM  
    res = res.fetchall()
    return await background_send_38(res)

# @router.post("/lastfivedaystoapprovereminder/")
async def last_five_days_to_approve_end_reminder():
    res = db.execute("""SELECT public.get_list_of_waiting_approval('End', 1)""")
    res = res.first()[0]
    return await background_send_27(res)

# @router.post("/lastfourdaystoapprovereminder/")
async def last_four_days_to_approve_end_reminder():
    res = db.execute("""SELECT public.get_list_of_waiting_approval('End', 1)""")
    res = res.first()[0]
    return await background_send_28(res)

# @router.post("/lastthreedaystoapprovereminder/")
async def last_three_days_to_approve_end_reminder():
    res = db.execute("""SELECT public.get_list_of_waiting_approval('End', 1)""")
    res = res.first()[0]
    return await background_send_29(res)

# @router.post("/lasttwodaystoapprovereminder/")
async def last_two_days_to_approve_end_reminder():
    res = db.execute("""SELECT public.get_list_of_waiting_approval('End', 1)""")
    res = res.first()[0]
    return await background_send_30(res)

# @router.post("/lastdaytoapprovereminder/")
async def last_day_to_approve_end_reminder():
    res = db.execute("""SELECT public.get_list_of_waiting_approval('End', 1)""")
    res = res.first()[0]
    return await background_send_31(res)


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

jobstores = { 'default': SQLAlchemyJobStore(url='sqlite:///./sql_app.db')}
executors = { 'default': ThreadPoolExecutor(20), 'processpool': ProcessPoolExecutor(5)}
job_defaults = { 'coalesce': False, 'max_instances': 3}

#  DEADLINES
db=SessionLocal()

deadline=db.execute(""" SELECT * FROM deadline WHERE deadline_type = 'Start' """)
deadline=deadline.fetchall()

mid_deadline=db.execute(""" SELECT * FROM deadline WHERE deadline_type = 'Mid' """)
mid_deadline=mid_deadline.fetchall()

end_deadline=db.execute(""" SELECT * FROM deadline WHERE deadline_type = 'End' """)
end_deadline=end_deadline.fetchall()


# DATES 

start_date=deadline[0][1]
mid_start_date=mid_deadline[0][1]
end_start_date=end_deadline[0][1]

end_date=deadline[0][2]
mid_end_date=mid_deadline[0][2]
end_end_date=end_deadline[0][2]

send_date=start_date-timedelta(3) # THREE DAYS TO START
mid_send_date=mid_start_date-timedelta(3)
end_send_date=end_start_date-timedelta(3)

send_date_2=end_date-timedelta(5) # LAST FIVE DAYS REMINDER
mid_send_date_2=mid_end_date-timedelta(5)
end_send_date_2=end_end_date-timedelta(5)

send_date_3=end_date-timedelta(4) # LAST FOUR DAYS REMINDER
mid_send_date_3=mid_end_date-timedelta(4)
end_send_date_3=end_end_date-timedelta(4)

send_date_4=end_date-timedelta(3) # LAST THREE DAYS REMINDER
mid_send_date_4=mid_end_date-timedelta(3)
end_send_date_4=end_end_date-timedelta(3)

send_date_5=end_date-timedelta(2) # LAST TWO DAYS REMINDER
mid_send_date_5=mid_end_date-timedelta(2)
end_send_date_5=end_end_date-timedelta(2)

send_date_6=end_date # LAST DAY REMINDER
mid_send_date_6=mid_end_date
end_send_date_6=end_end_date

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# JOB SCHEDULER

# START
scheduler = AsyncIOScheduler()  
scheduler.add_job(func=three_days_to_start_reminder, trigger='date', run_date=send_date)
scheduler.add_job(func=start_annual_plan, trigger='date', run_date=start_date)
scheduler.add_job(func=last_five_days_reminder, trigger='date', run_date=send_date_2)
scheduler.add_job(func=last_four_days_reminder, trigger='date', run_date=send_date_3)
scheduler.add_job(func=last_three_days_reminder, trigger='date', run_date=send_date_4)
scheduler.add_job(func=last_two_days_reminder, trigger='date', run_date=send_date_5)
scheduler.add_job(func=last_day_reminder, trigger='date', run_date=send_date_6)
scheduler.add_job(func=last_five_days_to_approve_reminder, trigger='date', run_date=send_date_2)
scheduler.add_job(func=last_four_days_to_approve_reminder, trigger='date', run_date=send_date_3)
scheduler.add_job(func=last_three_days_to_approve_reminder, trigger='date', run_date=send_date_4)
scheduler.add_job(func=last_two_days_to_approve_reminder, trigger='date', run_date=send_date_5)
scheduler.add_job(func=last_day_to_approve_reminder, trigger='date', run_date=send_date_6)

# MID
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

# END
scheduler.add_job(func=three_days_to_end_reminder, trigger='date', run_date=end_send_date)
scheduler.add_job(func=start_end_year_review, trigger='date', run_date=end_start_date)
scheduler.add_job(func=last_five_days_to_end_reminder, trigger='date', run_date=end_send_date_2)
scheduler.add_job(func=last_four_days_to_end_reminder, trigger='date', run_date=end_send_date_3)
scheduler.add_job(func=last_three_days_to_end_reminder, trigger='date', run_date=end_send_date_4)
scheduler.add_job(func=last_two_days_to_end_reminder, trigger='date', run_date=end_send_date_5)
scheduler.add_job(func=last_day_to_end_reminder, trigger='date', run_date=end_send_date_6)
scheduler.add_job(func=last_five_days_to_approve_end_reminder, trigger='date', run_date=end_send_date_2)
scheduler.add_job(func=last_four_days_to_approve_end_reminder, trigger='date', run_date=end_send_date_3)
scheduler.add_job(func=last_three_days_to_approve_end_reminder, trigger='date', run_date=end_send_date_4)
scheduler.add_job(func=last_two_days_to_approve_end_reminder, trigger='date', run_date=end_send_date_5)
scheduler.add_job(func=last_day_to_approve_end_reminder, trigger='date', run_date=end_send_date_6)

scheduler.start() 
