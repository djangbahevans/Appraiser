from fastapi import BackgroundTasks, APIRouter, Depends, APIRouter
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import timedelta
from starlette.responses import JSONResponse
from database import SessionLocal
from sqlalchemy.orm import Session
from main import settings

# IMPORT EMAILTENPLATES
from static.email_templates.template_3 import template3
from static.email_templates.template_29 import template29
from static.email_templates.template_30 import template30
from static.email_templates.template_31 import template31
from static.email_templates.template_32 import template32
from static.email_templates.template_33 import template33
from static.email_templates.template_34 import template34
from static.email_templates.template_35 import template35
from static.email_templates.template_36 import template36
from static.email_templates.template_37 import template37
from static.email_templates.template_38 import template38
from static.email_templates.template_39 import template39
from static.email_templates.template_40 import template40
from static.email_templates.template_41 import template41
from static.email_templates.template_42 import template42
from static.email_templates.template_43 import template43
from static.email_templates.template_44 import template44
from static.email_templates.template_45 import template45
from static.email_templates.template_46 import template46


USE_CREDENTIALS = settings.USE_CREDENTIALS
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
        MAIL_USERNAME=settings.MAIL_USERNAME,
        MAIL_PASSWORD=settings.MAIL_PASSWORD,
        MAIL_FROM=settings.MAIL_FROM,
        MAIL_PORT=settings.MAIL_PORT,
        MAIL_SERVER=settings.MAIL_SERVER,
        MAIL_TLS=settings.MAIL_TLS,
        MAIL_SSL=settings.MAIL_SSL,
        USE_CREDENTIALS=settings.USE_CREDENTIALS
    )
)

# DEFINE BACKGROUND TASKS
background_tasks = BackgroundTasks()


# BACKGROUND TASKS(WITHOUT SCHEDULER)


# START END-YEAR REVIEW
async def background_send_2(user_hash_list, background_tasks) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="End-Year Review Form",
            recipients=[item[1]],
            body=template3.format(url=settings.END_URL, hash=item[0]),
            subtype="html"
        )
        background_tasks.add_task(fm.send_message, message)


# APPROVE END-YEAR REVIEW
async def background_send_39(user_hash_list, background_tasks) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Approve Appraisee Forms",
            recipients=[item["supervisor_email"]],
            body=template37.format(email=item["email"], lastname=item["lastname"], staff_id=item["staff_id"], firstname=item["firstname"],
                                   middlename=item["middlename"], supervisor_email=item["supervisor_email"], appraisal_form_id=item["appraisal_form_id"]),
            subtype="html"
        )
        background_tasks.add_task(fm.send_message, message)


# START END-YEAR REVIEW(INDIVIDUAL)
async def background_send_37(user_hash_list, background_tasks) -> JSONResponse:
    for item in user_hash_list:  # CREATE VARIABLES FOR EMAIL TEMPLATES
        message = MessageSchema(
            subject="Start End-Year Review",
            recipients=[item[0]],  # INDEX OF EMAIL FROM DB QUERY
            # VARIABLES IN TEMPLATES STORING URL AND HASH
            body=template3.format(url=settings.END_URL, hash=item[1]),
            subtype="html"
        )
        background_tasks.add_task(fm.send_message, message)


# SEND END-YEAR REVIEW DETAILS TO APPROVED
async def background_send_19(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Form Approved",
            recipients=[item[0]],
            body=template37.format(email=item[0], lastname=item[1], staff_id=item[2], firstname=item[3],
                                   middlename=item[4], appraisal_form_id=item[5], supervisor_email=item[6], core_assessments=item[7], non_core_assessments=item[8], total_score=item[9], overall_rating=item[10], hash=item[11]),
            subtype="html"
        )
        await fm.send_message(message)


async def background_send_63(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="View Comments On Work-Plan",
            recipients=[item[6]],
            body=template45.format(email=item[0], lastname=item[1], staff_id=item[2], firstname=item[3],
                                   middlename=item[4], appraisal_form_id=item[5], supervisor_email=item[6], core_assessments=item[7], non_core_assessments=item[8], total_score=item[9], overall_rating=item[10], appraisees_comments_and_plan=item[11], hash=item[12]),
            subtype="html"
        )
        await fm.send_message(message)


async def background_send_64(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="View Appraiser's Comments On Work-Plan",
            recipients=[item[6]],
            body=template46.format(email=item[0], lastname=item[1], staff_id=item[2], firstname=item[3],
                                   middlename=item[4], appraisal_form_id=item[5], supervisor_email=item[6], core_assessments=item[7], non_core_assessments=item[8], total_score=item[9], overall_rating=item[10], appraisees_comments_and_plan=item[11], appraisal_comment_on_workplan=item[12]),
            subtype="html"
        )
        await fm.send_message(message)


async def background_send_41(user_hash_list, background_tasks) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="End-Year Review Details",
            recipients=[item["email"]],
            body=template40.format(email=item["email"], progress_review=item["progress_review"], lastname=item["lastname"], staff_id=item["staff_id"], firstname=item["firstname"], remarks=item["remarks"],
                                   middlename=item["middlename"], supervisor=item["supervisor"], competency=item["competency"], supervisor_email=item["supervisor_email"], appraisal_form_id=item["appraisal_form_id"]),
            subtype="html"
        )
        background_tasks.add_task(fm.send_message, message)


# REMIND STAFF TO FILL END-YEAR REVIEW (NO LINK)
async def background_send_46(user_hash_list, background_tasks) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Reminder To Start End-Year Review",
            recipients=[item[0]],
            body=template41.format(
                progress_review=item[1], remarks=item[2], competency=item[3]),
            subtype="html"
        )
        background_tasks.add_task(fm.send_message, message)

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


# BACKGROUND TASKS(WITH SCHEDULER)
async def background_send_20(user_hash_list) -> JSONResponse:
    for item in user_hash_list:  # CREATE VARIABLES FOR EMAIL TEMPLATES
        message = MessageSchema(
            subject="End-Year Review (Three Days To Start Reminder)",
            recipients=[item[1]],  # INDEX OF EMAIL FROM DB
            body=template29,
            subtype="html"
        )
        await fm.send_message(message)


# LAST DAYS FOR END-YEAR REVIEW
async def background_send_21(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="End-Year Review (Last Five Days Reminder)",
            recipients=[item["email"]],
            body=template31,
            subtype="html"
        )
        await fm.send_message(message)


async def background_send_22(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="End-Year Review (Last Four Days Reminder)",
            recipients=[item["email"]],
            body=template32,
            subtype="html"
        )
        await fm.send_message(message)


async def background_send_23(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="End-Year Review (Last Three Days Reminder)",
            recipients=[item["email"]],
            body=template33,
            subtype="html"
        )
        await fm.send_message(message)


async def background_send_24(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="End-Year Review (Last Two Days Reminder)",
            recipients=[item["email"]],
            body=template34,
            subtype="html"
        )
        await fm.send_message(message)


async def background_send_25(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="End-Year Review (Last Day Reminder)",
            recipients=[item["email"]],
            body=template38,
            subtype="html"
        )
        await fm.send_message(message)


# START END-YEAR REVIEW
async def background_send_26(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Start End-Year Review",
            recipients=[item[1]],
            body=template30.format(url=settings.END_URL, hash=item[0]),
            subtype="html"
        )
        await fm.send_message(message)


# LAST DAYS TO APPROVE END-YEAR REVIEW
async def background_send_27(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Approve End-Year Review (Last Five Days Reminder)",
            recipients=[item["supervisor_email"]],
            body=template39.format(email=item["email"], progress_review=item["progress_review"], lastname=item["lastname"], staff_id=item["staff_id"], firstname=item["firstname"],
                                   remarks=item["remarks"], middlename=item["middlename"], competency=item["competency"], supervisor_email=item["supervisor_email"], appraisal_form_id=item["appraisal_form_id"]),
            subtype="html"
        )
        background_tasks.add_task(fm.send_message, message)


async def background_send_28(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Approve End-Year Review (Last Four Days Reminder)",
            recipients=[item["supervisor_email"]],
            body=template39.format(email=item["email"], progress_review=item["progress_review"], lastname=item["lastname"], staff_id=item["staff_id"], firstname=item["firstname"],
                                   remarks=item["remarks"], middlename=item["middlename"], competency=item["competency"], supervisor_email=item["supervisor_email"], appraisal_form_id=item["appraisal_form_id"]),
            subtype="html"
        )
        background_tasks.add_task(fm.send_message, message)


async def background_send_29(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Approve End-Year Review (Last Three Days Reminder)",
            recipients=[item["supervisor_email"]],
            body=template39.format(email=item["email"], progress_review=item["progress_review"], lastname=item["lastname"], staff_id=item["staff_id"], firstname=item["firstname"],
                                   remarks=item["remarks"], middlename=item["middlename"], competency=item["competency"], supervisor_email=item["supervisor_email"], appraisal_form_id=item["appraisal_form_id"]),
            subtype="html"
        )
        background_tasks.add_task(fm.send_message, message)


async def background_send_30(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Approve End-Year Review (Last Two Days Reminder)",
            recipients=[item["supervisor_email"]],
            body=template39.format(email=item["email"], progress_review=item["progress_review"], lastname=item["lastname"], staff_id=item["staff_id"], firstname=item["firstname"],
                                   remarks=item["remarks"], middlename=item["middlename"], competency=item["competency"], supervisor_email=item["supervisor_email"], appraisal_form_id=item["appraisal_form_id"]),
            subtype="html"
        )
        background_tasks.add_task(fm.send_message, message)


async def background_send_31(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Approve End-Year Review (Last Day Reminder)",
            recipients=[item["supervisor_email"]],
            body=template39.format(email=item["email"], progress_review=item["progress_review"], lastname=item["lastname"], staff_id=item["staff_id"], firstname=item["firstname"],
                                   remarks=item["remarks"], middlename=item["middlename"], competency=item["competency"], supervisor_email=item["supervisor_email"], appraisal_form_id=item["appraisal_form_id"]),
            subtype="html"
        )
        background_tasks.add_task(fm.send_message, message)


# END-YEAR REVIEW APPROVED
async def background_send_32(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Competency Details Approved",
            recipients=[item[0]],
            body=template37.format(email=item[0], lastname=item[1], staff_id=item[2], firstname=item[3],
                                   middlename=item[4], appraisal_form_id=item[5], supervisor_email=item[6]),
            subtype="html"
        )
        await fm.send_message(message)


# END-YEAR REVIEW DISAPPROVED
async def background_send_38(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Competency Details Disapproved",
            recipients=[item[0]],
            body=template36.format(email=item[0], lastname=item[1], staff_id=item[2], firstname=item[3],
                                   middlename=item[4], appraisal_form_id=item[5], supervisor_email=item[6], comments=item[7]),
            subtype="html"
        )
        await fm.send_message(message)


async def background_send_33(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Form Disaproved",
            recipients=[item[0]],
            body=template44.format(email=item[0], lastname=item[1], staff_id=item[2], firstname=item[3],
                                   middlename=item[4], appraisal_form_id=item[5], supervisor_email=item[6]),
            subtype="html"
        )
        await fm.send_message(message)


# APPROVE END-YEAR REVIEW
async def background_send_36(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Approve End-Year Review",
            recipients=[item[6]],
            body=template35.format(email=item[0], lastname=item[1], staff_id=item[2], firstname=item[3],
                                   middlename=item[4], appraisal_form_id=item[5], supervisor_email=item[6]),
            subtype="html"
        )
        await fm.send_message(message)


async def background_send_99(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Approve Competence Details",
            recipients=[item[6]],
            body=template42.format(email=item[0], lastname=item[1], staff_id=item[2], firstname=item[3],
                                   middlename=item[4], appraisal_form_id=item[5], supervisor_email=item[6]),
            subtype="html"
        )
        await fm.send_message(message)


async def background_send_98(user_hash_list) -> JSONResponse:
    for item in user_hash_list:
        message = MessageSchema(
            subject="Approve Performance Details",
            recipients=[item[6]],
            body=template43.format(email=item[0], lastname=item[1], staff_id=item[2], firstname=item[3],
                                   middlename=item[4], appraisal_form_id=item[5], supervisor_email=item[6]),
            subtype="html"
        )
        await fm.send_message(message)


# EMAIL ENDPOINTS FOR MANUALLY SENT EMAILS


# SEND END-YEAR LINK TO ALL STAFF
@ router.post("/endyearreviewemail/")
async def start_endyear_review_(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    res = db.execute("""SELECT * FROM public.hash_table""")
    res = res.fetchall()
    return await background_send_2(res, background_tasks)


# SEND END-YEAR LINK TO INDIVIDUAL STAFF
@ router.post("/endyearreviewemailstaff/")
async def end_year_review_staff(email: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    res = db.execute("""SELECT email, hash FROM public.hash_table where email=:email""", {
        'email': email})  # SELECT EMAIL AND HASH PAIR FROM HASH TABLE
    res = res.fetchall()
    return await background_send_37(res, background_tasks)


# SEND REMINDER TO SUPERVISORS TO APPROVE SUBMITTED END-YEAR REVIEW FORMS
@ router.post("/approveendyearreview/")
async def approve_completed_end_year_review(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    res = db.execute(
        """SELECT public.get_list_of_waiting_approval('End', 1)""")  # SELECT EMAIL FROM WAITING APPROVAL FUNCTION
    res = res.first()[0]
    return await background_send_39(res, background_tasks)


# SEND END-YEAR DETAILS TO APPROVED
@ router.post("/endformdetails/")
# SEND FORM DETAILS TO APPROVED STAFF
async def send_endyear_review_details_to_approved(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    res = db.execute(
        """SELECT public.get_list_of_approved_form('End', 1)""")  # SELECT EMAIL FROM LIST OF APPROVED FUNCTION IN DB
    res = res.first()[0]
    return await background_send_41(res, background_tasks)


# REMIND APPRAISEE TO CHECK EMAIL WITH LINK FOR END-YEAR REVIEW
@ router.post("/endyearreviewreminder/{supervisor}/")
async def start_endyear_review_reminder(background_tasks: BackgroundTasks, supervisor: int, db: Session = Depends(get_db)):
    res = db.execute("""select email, progress_review, remarks, competency from public.view_users_form_details where supervisor=:supervisor and end_status=0 and progress_review is null and remarks is null and competency is null""", {
        'supervisor': supervisor})  # SELECT EMAIL AND HASH PAIR FROM HASH TABLE
    res = res.fetchall()
    return await background_send_46(res, background_tasks)

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# SCHEDULED REMINDERS FOR APPRAISEE


# END YEAR

# @router.post("/threedaysreminder/")
async def three_days_to_end_reminder():
    res = db.execute(
        """SELECT * FROM public.hash_table""")  # SELECT EMAIL FROM HASH TABLE
    res = res.fetchall()
    return await background_send_20(res)


# @router.post("/startday/")
async def start_end_year_review():
    res = db.execute(
        """SELECT * FROM public.hash_table""")  # SELECT EMAIL FROM HASH TABLE
    res = res.fetchall()
    return await background_send_26(res)


# @router.post("/lastfivedaysreminder/")
async def last_five_days_to_end_reminder():
    res = db.execute(
        """SELECT public.get_list_of_incompleted_form('End', 1)""")
    res = res.first()[0]
    return await background_send_21(res)


# @router.post("/lastfourdaysreminder/")
async def last_four_days_to_end_reminder():
    res = db.execute(
        """SELECT public.get_list_of_incompleted_form('End', 1)""")
    res = res.first()[0]
    return await background_send_22(res)


# @router.post("/lastthreedaysreminder/")
async def last_three_days_to_end_reminder():
    res = db.execute(
        """SELECT public.get_list_of_incompleted_form('End', 1)""")
    res = res.first()[0]
    return await background_send_23(res)


# @router.post("/lasttwodaysreminder/")
async def last_two_days_to_end_reminder():
    res = db.execute(
        """SELECT public.get_list_of_incompleted_form('End', 1)""")
    res = res.first()[0]
    return await background_send_24(res)


# @router.post("/lastdayreminder/")
async def last_day_to_end_reminder():
    res = db.execute(
        """SELECT public.get_list_of_incompleted_form('End', 1)""")
    res = res.first()[0]
    return await background_send_25(res)


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# SCHEDULED REMINDERS FOR APPRAISER


# END YEAR

# @router.post("/approveendyearreview/")
# TAKE APPRAISAL FORM ID FROM "create_end_year_review" FUNCTION IN phase_2 Router, crud.py
async def approve_end_year_review(appraisal_form_id):
    res = db.execute("""select  email, lastname, staff_id, firstname, middlename, appraisal_form_id, supervisor_email from public.view_end
                        where appraisal_form_id=:appraisal_form_id and comments is  not null and weight is not  null and final_score is not  null and submit=1  """,
                     {
                         'appraisal_form_id': appraisal_form_id})  # SELECT EMAIL OF SUPERVISOR FROM DB USING APPRAISAL FORM ID IN ANNUAL PLAN FORM
    res = res.fetchall()
    return await background_send_36(res)


async def add_comment_on_workplan(appraisal_form_id):
    res = db.execute("""select  view_users_form_details.email, view_users_form_details.lastname, view_users_form_details.staff_id, view_users_form_details.firstname, view_users_form_details.middlename, view_users_form_details.appraisal_form_id, view_users_form_details.supervisor_email,round((core_assessments*0.6)::decimal,1) as core_assessments, round((non_core_assessments*0.6)::decimal,1) as non_core_assessments, round((((core_assessments+non_core_assessments)*0.6)*0.6)::decimal,1) as total_score, ((((core_assessments+non_core_assessments)*0.6)*0.6))*100 as overall_rating, view_users_form_details.appraisees_comments_and_plan, public.hash_table.hash
from public.view_users_form_details
inner join public.hash_table
on view_users_form_details.email=hash_table.email where appraisal_form_id=:appraisal_form_id """,
                     {
                         'appraisal_form_id': appraisal_form_id})  # SELECT EMAIL OF SUPERVISOR FROM DB USING APPRAISAL FORM ID IN ANNUAL PLAN FORM
    res = res.fetchall()
    return await background_send_63(res)


async def add_head_of_division_comments(appraisal_form_id):
    res = db.execute("""select  email, lastname, staff_id, firstname, middlename, appraisal_form_id, supervisor_email,round((core_assessments*0.6)::decimal,1) as core_assessments, round((non_core_assessments*0.6)::decimal,1) as non_core_assessments, round((((core_assessments+non_core_assessments)*0.6)*0.6)::decimal,1) as total_score, ((((core_assessments+non_core_assessments)*0.6)*0.6))*100 as overall_rating, appraisees_comments_and_plan,appraisal_comment_on_workplan from public.view_users_form_details
                        where appraisal_form_id=:appraisal_form_id """,
                     {
                         'appraisal_form_id': appraisal_form_id})  # SELECT EMAIL OF SUPERVISOR FROM DB USING APPRAISAL FORM ID IN ANNUAL PLAN FORM
    res = res.fetchall()
    return await background_send_64(res)


async def approve_competence_details(appraisal_form_id):
    res = db.execute(""" SELECT email, lastname, staff_id, firstname, middlename, appraisal_form_id, supervisor_email FROM public.view_users_form_details where appraisal_form_id=:appraisal_form_id  """, {
        'appraisal_form_id': appraisal_form_id})  # SELECT EMAIL OF SUPERVISOR FROM DB USING APPRAISAL FORM ID IN ANNUAL PLAN FORM
    res = res.fetchall()
    return await background_send_99(res)


async def approve_performance_details(appraisal_form_id):
    res = db.execute(""" SELECT email, lastname, staff_id, firstname, middlename, appraisal_form_id, supervisor_email FROM public.view_users_form_details where appraisal_form_id=:appraisal_form_id  """, {
        'appraisal_form_id': appraisal_form_id})  # SELECT EMAIL OF SUPERVISOR FROM DB USING APPRAISAL FORM ID IN ANNUAL PLAN FORM
    res = res.fetchall()
    return await background_send_98(res)


# @router.post("/endyearreviewapproved/")
async def end_of_year_approved(appraisal_form_id):
    res = db.execute(""" SELECT view_users_form_details.email, view_users_form_details.lastname, view_users_form_details.staff_id, view_users_form_details.firstname, view_users_form_details.middlename, view_users_form_details.appraisal_form_id, view_users_form_details.supervisor_email,  round((core_assessments*0.6)::decimal,1) as core_assessments, round((non_core_assessments*0.6)::decimal,1) as non_core_assessments, round((((core_assessments+non_core_assessments)*0.6)*0.6)::decimal,1) as total_score, ((((core_assessments+non_core_assessments)*0.6)*0.6))*100 as overall_rating, public.hash_table.hash FROM view_users_form_details 
inner join public.hash_table
on view_users_form_details.email=hash_table.email where appraisal_form_id=:appraisal_form_id  """, {
                     'appraisal_form_id': appraisal_form_id})  # SELECT EMAIL FROM DB USING APPRAISAL FORM ID IN APPROVE FORM
    res = res.fetchall()
    return await background_send_19(res)


async def end_of_year_disapproved(appraisal_form_id):
    res = db.execute(""" SELECT email, lastname, staff_id, firstname, middlename, appraisal_form_id, supervisor_email FROM view_users_form_details where appraisal_form_id=:appraisal_form_id  """, {
                     'appraisal_form_id': appraisal_form_id})  # SELECT EMAIL FROM DB USING APPRAISAL FORM ID IN APPROVE FORM
    res = res.fetchall()
    return await background_send_33(res)


# TAKE APPRAISAL FORM ID FROM "approve_form" FUNCTION IN appraiser Router, crud.py
async def competency_details_approved(appraisal_form_id):
    res = db.execute(""" SELECT email, lastname, staff_id, firstname, middlename, appraisal_form_id, supervisor_email FROM public.view_users_form_details where appraisal_form_id=:appraisal_form_id  """, {
        'appraisal_form_id': appraisal_form_id})  # SELECT EMAIL FROM DB USING APPRAISAL FORM ID IN APPROVE FORM
    res = res.fetchall()
    return await background_send_32(res)


# @router.post("/endyearreviewdisapproved/")
# TAKE APPRAISAL FORM ID FROM "approve_form" FUNCTION IN appraiser Router, crud.py
async def competency_details_disapproved(appraisal_form_id):
    res = db.execute(""" SELECT email, lastname, staff_id, firstname, middlename, appraisal_form_id, supervisor_email FROM public.view_users_form_details where appraisal_form_id=:appraisal_form_id  """, {
        'appraisal_form_id': appraisal_form_id})  # SELECT EMAIL FROM DB USING APPRAISAL FORM ID IN APPROVE FORM
    res = res.fetchall()
    com = db.execute("""SELECT competency_details FROM public.supervisor_comment where appraisal_form_id=:appraisal_form_id """, {
        'appraisal_form_id': appraisal_form_id})
    com = com.fetchall()
    return await background_send_38(res)


# @router.post("/lastfivedaystoapprovereminder/")
async def last_five_days_to_approve_end_reminder():
    res = db.execute(
        """SELECT public.get_list_of_waiting_approval('End', 1)""")
    res = res.first()[0]
    return await background_send_27(res)


# @router.post("/lastfourdaystoapprovereminder/")
async def last_four_days_to_approve_end_reminder():
    res = db.execute(
        """SELECT public.get_list_of_waiting_approval('End', 1)""")
    res = res.first()[0]
    return await background_send_28(res)


# @router.post("/lastthreedaystoapprovereminder/")
async def last_three_days_to_approve_end_reminder():
    res = db.execute(
        """SELECT public.get_list_of_waiting_approval('End', 1)""")
    res = res.first()[0]
    return await background_send_29(res)


# @router.post("/lasttwodaystoapprovereminder/")
async def last_two_days_to_approve_end_reminder():
    res = db.execute(
        """SELECT public.get_list_of_waiting_approval('End', 1)""")
    res = res.first()[0]
    return await background_send_30(res)


# @router.post("/lastdaytoapprovereminder/")
async def last_day_to_approve_end_reminder():
    res = db.execute(
        """SELECT public.get_list_of_waiting_approval('End', 1)""")
    res = res.first()[0]
    return await background_send_31(res)


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

jobstores = {'default': SQLAlchemyJobStore(url='sqlite:///./sql_app.db')}
executors = {'default': ThreadPoolExecutor(
    20), 'processpool': ProcessPoolExecutor(5)}
job_defaults = {'coalesce': False, 'max_instances': 3}

#  DEADLINES
db = SessionLocal()


end_deadline = db.execute(
    """ SELECT * FROM deadline WHERE deadline_type = 'End' """)
end_deadline = end_deadline.fetchall()


# DATES
end_start_date = end_deadline[0][1]
end_end_date = end_deadline[0][2]
end_send_date = end_start_date-timedelta(3)
end_send_date_2 = end_end_date-timedelta(5)
end_send_date_3 = end_end_date-timedelta(4)
end_send_date_4 = end_end_date-timedelta(3)
end_send_date_5 = end_end_date-timedelta(2)
end_send_date_6 = end_end_date


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# JOB SCHEDULER


# END
scheduler = AsyncIOScheduler()
scheduler.add_job(func=three_days_to_end_reminder,
                  trigger='date', run_date=end_send_date)
scheduler.add_job(func=start_end_year_review,
                  trigger='date', run_date=end_start_date)
scheduler.add_job(func=last_five_days_to_end_reminder,
                  trigger='date', run_date=end_send_date_2)
scheduler.add_job(func=last_four_days_to_end_reminder,
                  trigger='date', run_date=end_send_date_3)
scheduler.add_job(func=last_three_days_to_end_reminder,
                  trigger='date', run_date=end_send_date_4)
scheduler.add_job(func=last_two_days_to_end_reminder,
                  trigger='date', run_date=end_send_date_5)
scheduler.add_job(func=last_day_to_end_reminder,
                  trigger='date', run_date=end_send_date_6)
scheduler.add_job(func=last_five_days_to_approve_end_reminder,
                  trigger='date', run_date=end_send_date_2)
scheduler.add_job(func=last_four_days_to_approve_end_reminder,
                  trigger='date', run_date=end_send_date_3)
scheduler.add_job(func=last_three_days_to_approve_end_reminder,
                  trigger='date', run_date=end_send_date_4)
scheduler.add_job(func=last_two_days_to_approve_end_reminder,
                  trigger='date', run_date=end_send_date_5)
scheduler.add_job(func=last_day_to_approve_end_reminder,
                  trigger='date', run_date=end_send_date_6)


scheduler.start()
