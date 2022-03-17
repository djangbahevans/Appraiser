# IMPORT DEPENDENCIES
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from app.database import engine
from app.routers.appraiser import main as appraiser
from app.routers.auth_router import main as auth
from app.routers.email import end as end
from app.routers.email import mid as mid
from app.routers.email import start as start
from app.routers.phase1_router import main as phase1
from app.routers.phase2_router import main as phase2
from app.routers.phase3_router import main as phase3
from app.routers.phase4_router import main as phase4
from app.routers.staff_router import main as staff
from app.routers.user_router import main as user
from app.routers.user_router import models

api = FastAPI(docs_url="/api/docs")
# INITIATE AUTHENTICATION SCHEME
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/authenticate")

# GIVE PERMISSION TO FRONTEND
origins = ["*", "http://localhost"]
api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

# CUSTOMIZE ALL ENDPOINT HEADERS
api.include_router(auth.router, prefix="/auth", tags=["User Login"])
api.include_router(user.router, prefix="/user", tags=["User"])
api.include_router(staff.router, prefix="/api/staff", tags=["Staff"])
api.include_router(
    appraiser.router, prefix="/api/appraiser", tags=["Appraiser"])
api.include_router(phase1.router, prefix="/api/review", tags=["Start Review"])
api.include_router(phase2.router, prefix="/api/midyearreview",
                   tags=["Mid-Year Review"])
api.include_router(phase3.router, prefix="/api/endofyearreview",
                   tags=["End of Year Review"])
api.include_router(phase4.router, prefix="/api/finalremarks",
                   tags=["Final Remarks"])
# api.include_router(email.router, prefix="/email", tags=["E-mails"])
api.include_router(start.router, prefix="/email",
                   tags=["Start of Year Review Emails"])
api.include_router(mid.router, prefix="/email",
                   tags=["Mid-Year Review Emails"])
api.include_router(end.router, prefix="/email", tags=["End of Year Emails"])

# DEFAULT ENDPOINT


@api.get("/")
def welcome():
    return "BACKEND OF APPRAISAL MANAGEMENT APP (url/api/docs)"
