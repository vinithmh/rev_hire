from passlib.context import CryptContext

jobseek_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    def hash(password):
        return jobseek_pwd.hash(password)

    def verify(hashed_password, plain_password):
        return jobseek_pwd.verify(plain_password, hashed_password)