from pydantic import BaseSettings
import os

class Settings(BaseSettings): # STORE VARIABLES IN ENV TO BE EXPORTED TO MAIN.PY
    SECRET_KEY : str = os.environ.get('SECRET_KEY') or "fsdfsdfsdfsdflhiugysadf87w940e-=r0werpolwe$16$5*dfsdfsdf&&#$rrr$$)7a9563OO93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = os.environ.get('ALGORITHM') or "HS256"
    MAIL_USERNAME : str = os.environ.get('MAIL_USERNAME') or "b1bbdb302533a8"
    MAIL_PASSWORD : str = os.environ.get('MAIL_PASSWORD') or "c39e9a21e72915"
    MAIL_FROM : str = os.environ.get('MAIL_FROM') or "admin@aiti.com"
    MAIL_PORT : int = os.environ.get('MAIL_PORT') or 587
    MAIL_SERVER : str = os.environ.get('MAIL_SERVER') or "smtp.mailtrap.io"
    MAIL_TLS : bool = os.environ.get('MAIL_TLS') or False
    MAIL_SSL : bool = os.environ.get('MAIL_SSL') or False
    ACCESS_TOKEN_DURATION_IN_MINUTES: float = os.environ.get('ACCESS_TOKEN_DURATION_IN_MINUTES') or 30.5
    REFRESH_TOKEN_DURATION_IN_MINUTES: float = os.environ.get('REFRESH_TOKEN_DURATION_IN_MINUTES') or 87000.5
    RESET_PASSWORD_SESSION_DURATION_IN_MINUTES: float = os.environ.get('RESET_PASSWORD_SESSION_DURATION_IN_MINUTES') or 1
    STATIC_DIR:str = os.environ.get('STATIC_DIR') or None
    API_BASE_URL:str = os.environ.get('API_BASE_URL') or 'http://0.0.0.0:8000'
    COMPANY_URL:str = os.environ.get('COMPANY_URL') or 'https://www.aiti-kace.com.gh'
    START_URL: str = os.environ.get('START_URL') or 'http://localhost:4200/forms/start'
    MID_URL: str = os.environ.get('MID_URL') or 'http://localhost:4200/forms/mid-year'
    PASSWORD_URL: str = os.environ.get('PASSWORD_URL') or 'http://localhost:4200/forms/start'

    class Config:
        title = 'Base Settings'
