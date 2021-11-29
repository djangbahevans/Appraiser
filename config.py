from pydantic import BaseSettings
import os


class Settings(BaseSettings):  # STORE VARIABLES IN ENV TO BE EXPORTED TO MAIN.PY
    SECRET_KEY: str = os.environ.get(
        'SECRET_KEY') or "fsdfsdfsdfsdflhiugysadf87w940e-=r0werpolwe$16$5*dfsdfsdf&&#$rrr$$)7a9563OO93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = os.environ.get('ALGORITHM') or "HS256"
    MAIL_USERNAME: str = os.environ.get('MAIL_USERNAME') or "9bf9dd29ed49a9"
    MAIL_PASSWORD: str = os.environ.get('MAIL_PASSWORD') or "eb28ce2abf91e5"
    MAIL_FROM: str = os.environ.get(
        'MAIL_FROM') or "appraisalmanagement2021@gmail.com"
    MAIL_PORT: int = os.environ.get('MAIL_PORT') or 587
    MAIL_SERVER: str = os.environ.get('MAIL_SERVER') or "smtp.mailtrap.io"
    MAIL_TLS: bool = os.environ.get('MAIL_TLS') or True
    MAIL_SSL: bool = os.environ.get('MAIL_SSL') or False
    USE_CREDENTIALS: bool = os.environ.get('USE_CREDENTIALS') or True
    ACCESS_TOKEN_DURATION_IN_MINUTES: float = os.environ.get(
        'ACCESS_TOKEN_DURATION_IN_MINUTES') or 30.5
    REFRESH_TOKEN_DURATION_IN_MINUTES: float = os.environ.get(
        'REFRESH_TOKEN_DURATION_IN_MINUTES') or 87000.5
    RESET_PASSWORD_SESSION_DURATION_IN_MINUTES: float = os.environ.get(
        'RESET_PASSWORD_SESSION_DURATION_IN_MINUTES') or 1
    STATIC_DIR: str = os.environ.get('STATIC_DIR') or None
    API_BASE_URL: str = os.environ.get('API_BASE_URL') or 'http://0.0.0.0:8000'
    COMPANY_URL: str = os.environ.get(
        'COMPANY_URL') or 'https://www.aiti-kace.com.gh'
    START_URL: str = os.environ.get(
        'START_URL') or 'http://196.43.196.108:5445/forms/start'
    MID_URL: str = os.environ.get(
        'MID_URL') or 'http://196.43.196.108:5445/forms/mid-year'
    END_URL: str = os.environ.get(
        'END_URL') or 'http://196.43.196.108:5445/forms/end-year'
    PASSWORD_URL: str = os.environ.get(
        'PASSWORD_URL') or 'http://196.43.196.108:5445/forms/start'

    class Config:
        title = 'Base Settings'
