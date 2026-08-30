from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60 * 24  

pwd_context = CryptContext(schemes=["bcrypt"])