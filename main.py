from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from services.email import background_send, fm, MessageSchema, template, background_send_2, background_send3
from database import SessionLocal, engine
from routers.phase1_router import models
# from routers.staff_router import models
from routers.auth_router import models
from routers.appraiser import models
# from fastapi import BackgroundTasks
# from fastapi import FastAPI
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, FastAPI
from sqlalchemy.orm import Session

api = FastAPI(docs_url="/api/docs")

origins = ["*"]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.triggers.cron import CronTrigger
import pytz

jobstores = { 'default': SQLAlchemyJobStore(url='sqlite:///./sql_app.db')}
executors = { 'default': ThreadPoolExecutor(20), 'processpool': ProcessPoolExecutor(5)}
job_defaults = { 'coalesce': False, 'max_instances': 3}
scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=pytz.utc, misfire_grace_time=1)

def send_email():
    
    # return 'df'
    print("fill in your forms")

from datetime import datetime, timedelta

@api.post("/testemail")
def send_hash_email():
    tasks=BackgroundTasks()
    db = SessionLocal()
    res = db.execute("""SELECT * FROM public.hash_table""")
    res = res.fetchall()

    for item in res:
        message = MessageSchema(
            subject="REVIEW FORMS",
            recipients=[item[1]],
            body=template.format(url="http://localhost:4200/forms/start",hash=item[0]),
            subtype="html"
        ) 
        # background_tasks.add_task(fm.send_message,message)
        tasks.add_task(fm.send_message, message)   
    print('success')
    print(res)
scheduler.add_job(send_hash_email, trigger='interval', minutes=1)
# scheduler.add_job(send_hash_email, 'cron', month='1-2, 6-7,11-12', day='1st mon, 3rd fri', hour='0-2')

# async def background_send(user_hash_list, background_tasks) -> JSONResponse:
#     # print(user_hash_list)
#     for item in user_hash_list:
        # message = MessageSchema(
        #     subject="Fastapi-Mail module",
        #     recipients=[item[1]],
        #     body=template.format(url="http://localhost:4200/forms/start/harsh",hash=item[0]),
        #     subtype="html"
        # )        
#         background_tasks.add_task(fm.send_message,message)

#         print('sd')
#         await background_send(res.fetchall(), background_tasks)
#     print('success')

# scheduler.add_job(send_hash_email, trigger='interval', minutes=1)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#models.Base.metadata.create_all(bind=engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/authenticate")

from routers.phase1_router import main as phase1
from routers.appraiser import main as appraiser
# from routers.staff_router import main as staff
from routers.auth_router import main as auth
from routers.phase2_router import main as phase2

api.include_router(appraiser.router,prefix="/api/appraiser", tags=["Appraiser"])
api.include_router(phase1.router,prefix="/api/review",tags=["Start Review"])
# api.include_router(staff.router,prefix="/api/staff",tags=["staff"])
api.include_router(auth.router,prefix="/api/staff",tags=["Staff"])
api.include_router(phase2.router, prefix="/api/midyearreview", tags=["Mid-Year Review"])

@api.get("/")
def welcome():
    return "Reminders started"

@api.on_event("startup")
async def startup_event():
    scheduler.start()

@api.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()


# background_tasks = BackgroundTasks()

@api.post("/startreviewemail/")
async def send_start_review_email(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    res = db.execute("""SELECT * FROM public.hash_table""")
    res = res.fetchall()

    return await background_send(res, background_tasks)

@api.post("/midyearreviewemail/")
async def send_midyear_review_email(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    res = db.execute("""SELECT * FROM public.hash_table""")
    res = res.fetchall()

    return await background_send3(res, background_tasks)

# @api.post("/test/test")
# async def b():
#     print('b')
#     print(dir(background_tasks))
#     return await background_send([{'email':'a@a.com','hash':'34242assdd'}], background_tasks)