from passlib.context import CryptContext

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(pwd: str):
    return pwd_ctx.hash(pwd)


def verify(hashed_password: str, plain_pwd):
    return hash_password(plain_pwd) == hashed_password
