from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase
from sqlalchemy import BigInteger
from database_connection import engine
from passlib.context import CryptContext
from decouple import config
SALT = config('salt')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    plain_password = plain_password+ SALT
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password:str):
    password = password+SALT
    return pwd_context.hash(password)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__='users'
    id:Mapped[int] = mapped_column(primary_key=True)
    username:Mapped[str]= mapped_column(unique=True)
    password:Mapped[str] = mapped_column(nullable=False)
    email:Mapped[str]= mapped_column(unique=True, nullable=False)
    contact= mapped_column(BigInteger, nullable=True)
    api_key:Mapped[str]

# Base.metadata.create_all(bind=engine)
    
    