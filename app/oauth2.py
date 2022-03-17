from fastapi.security import OAuth2PasswordBearer

# INITIATE AUTHENTICATION SCHEME
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/authenticate")
