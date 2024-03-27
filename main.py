from fastapi import FastAPI, Header, status, Security
from fastapi.security import APIKeyHeader
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, EmailStr
from models import User, get_password_hash, verify_password
from database_connection import session
from sqlalchemy import Select
from sqlalchemy.exc import IntegrityError
import base64


apikeyHeader= APIKeyHeader(name='X-API-Key')

app = FastAPI(title="API Key Validation")

SIMPLE_SALT="HelloWORLD"
class SignupModel(BaseModel):
    username:str
    password:str
    email:EmailStr
    contact:int|None=None

def create_APIkey(username:str,password:str):
    return base64.urlsafe_b64encode((f"username:{username}, password:{password}, salt:{SIMPLE_SALT}").encode()).decode()

def decode_APIkey(apiKey:str):
    # return base64.urlsafe_b64decode(apiKey.encode()).decode()
    decoded_api_key = (base64.urlsafe_b64decode(apiKey.encode()).decode())
    pairs = decoded_api_key.split(", ")
    result = {}
    for pair in pairs:
        key, value = pair.split(':', 1)
        key = key.strip()
        value = value
        result[key] = value
    
    # username = result['username']
    username = result.get('username')
    statement = Select(User).where(User.username==username)
    user_found = session.execute(statement).one_or_none()

    if user_found:
        if user_found[0].api_key == apiKey:
            return True
    return False

    

@app.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(signupModel:SignupModel):
    api_key = create_APIkey(signupModel.username,signupModel.password)
    user_object_to_add = User(
        username = signupModel.username,
        password = get_password_hash(signupModel.password),
        email = signupModel.email,
        contact = signupModel.contact,
        api_key=api_key)
    session.add(user_object_to_add)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already exsist",
        )
    return{
        'info':'Please save this api key',
        'api_key':api_key
    }

@app.get('/info')
def get_api_info(api_key:str=Header(title='X-API-key')):
    return (decode_APIkey(api_key))



    