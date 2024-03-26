from fastapi import FastAPI, status, Security
from fastapi.security import APIKeyHeader
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, EmailStr
import base64

apikeyHeader= APIKeyHeader(name='X-API-Key')

app = FastAPI(title="API Key Validation")

fake_db={
    'admin': {'username': 'admin', 'password': 'admin', 'email': 'admin@example.com', 'contact': 123456, 'api_key': 'YWRtaW5hZG1pbkhlbGxvV09STEQ='}, 
    'rohan': {'username': 'rohan', 'password': 'rohan1', 'email': 'rohan@example.com', 'contact': 123456789, 'api_key': 'cm9oYW5yb2hhbjFIZWxsb1dPUkxE'}
    }



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
    
    username = result['username']
    user_found = fake_db.get(username)
    
    if user_found:
        if user_found['api_key'] == apiKey:
            return True
    return False
    

@app.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(signupModel:SignupModel):
    if signupModel.username in fake_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exsist",
        )
    payload = {
        "username":signupModel.username,
        "password": signupModel.password,
        "email": signupModel.email,
        }
    if signupModel.contact:
        payload.update({'contact':signupModel.contact})
    api_key = create_APIkey(signupModel.username,signupModel.password)
    payload.update({'api_key':api_key})
    fake_db[signupModel.username] = payload
    print(fake_db)
    return{
        'info':'Please save this api key',
        'api_key':api_key
    }

@app.get('/info')
def get_api_info(api_key:str=Security(apikeyHeader)):
    return (decode_APIkey(api_key))



    