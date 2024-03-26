from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase
from sqlalchemy import BigInteger
from database_connection import engine

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
    
    