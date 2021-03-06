from pydantic import BaseSettings, root_validator


class Settings(BaseSettings):  # STORE VARIABLES IN ENV TO BE EXPORTED TO MAIN.PY
    SECRET_KEY: str = "fsdfsdfsdfsdflhiugysadf87w940e-=r0werpolwe$16$5*dfsdfsdf&&#$rrr$$)7a9563OO93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    MAIL_USERNAME: str = "9bf9dd29ed49a9"
    MAIL_PASSWORD: str = "eb28ce2abf91e5"
    MAIL_FROM: str = "appraisalmanagement2021@gmail.com"
    MAIL_PORT: int = 465
    MAIL_SERVER: str = "smtp.mailtrap.io"
    MAIL_TLS: bool = True
    MAIL_SSL: bool = False
    USE_CREDENTIALS: bool = True
    ACCESS_TOKEN_DURATION_IN_MINUTES: float = 30.5
    REFRESH_TOKEN_DURATION_IN_MINUTES: float = 87000.5
    RESET_PASSWORD_SESSION_DURATION_IN_MINUTES: float = 1
    STATIC_DIR: str = None
    API_BASE_URL: str = 'http://0.0.0.0:8000'
    COMPANY_URL: str = 'https://www.aiti-kace.com.gh'
    START_URL: str = '/forms/start'
    MID_URL: str = '/forms/mid-year'
    END_URL: str = '/forms/end-year'
    PASSWORD_URL: str = '/forms/start'
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_DOMAIN: str
    FRONTEND_URI: str

    @root_validator
    def prepend_base_url(cls, values):
        FRONTEND_URI = values.get("FRONTEND_URI")
        values["START_URL"] = FRONTEND_URI + values.get("START_URL")
        values["MID_URL"] = FRONTEND_URI + values.get("MID_URL")
        values["END_URL"] = FRONTEND_URI + values.get("END_URL")
        values["PASSWORD_URL"] = FRONTEND_URI + values.get("PASSWORD_URL")
        return values

    class Config:
        title = 'Base Settings'
        env_file = '.env'


# DEFINE SETTINGS
# SETTINGS FROM CONFIG.PY WHERE VARIABLES ARE STORED IN ONE ENVIRONMENT
settings = Settings()
