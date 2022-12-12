from fastapi import FastAPI, File, Query, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse, PlainTextResponse
import uvicorn
import joblib
import numpy as np
from pydantic import BaseModel

from typing import Union
from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext 

# ______________________________________________________

# JWT Authentication

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_users_db = {
    "moksha": {
        "username": "moksha",
        "full_name": "Moksha Doshi",
        "email": "md@gmail.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": True,
    },
    "vyshnavi": {
        "username": "vyshnavi",
        "full_name": "Vyshnavi Pendru",
        "email": "vp@gmail.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
}

class creditCardFraudDetection(BaseModel):
    distance_from_home:int
    distance_from_last_transaction:int
    ratio_to_median_purchase_price:float	
    repeat_retailer:float	
    used_chip:float	
    used_pin_number:float	
    online_order:float	
    


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None

class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


app = FastAPI(
    title="Credit Card Fraud Detection API",
    description="""An API that utilises a Machine Learning model that detects if a credit card transaction is fraudulent or not based on the following features: distance_from_home, distance_from_last_transaction,
       ratio_to_median_purchase_price, repeat_retailer, used_chip, used_pin_number, online_order.""",
    version="1.0.0", debug=True)



def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user



async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/", response_class=PlainTextResponse)
async def running():
  note = """
Credit Card Fraud Detection API
  """
  return note

# write to an in-memory BytesIO object, which acts like a file but doesn't actually touch a disk
from io import BytesIO
import boto3
import pickle

s3 = boto3.resource('s3')
with BytesIO() as data:
    s3.Bucket("damg-model").download_fileobj("pickle_model.pkl", data)
    data.seek(0)    # move back to the beginning after writing
    model = pickle.load(data)

@app.post('/predict')
def predict(data : creditCardFraudDetection,current_user: User = Depends(get_current_user)):
    # model = joblib.load('model.pkl')                                                                                                                                                                                                                          
    features = np.array([[data.distance_from_home, data.distance_from_last_transaction, data.ratio_to_median_purchase_price, data.repeat_retailer, 
                data.used_chip, data.used_pin_number, data.online_order]])
    

    predictions = model.predict(features)
    if predictions == 1:
        return {"predictions":"fraudulent"}
    elif predictions == 0:
        return {"predictions":"not fraudulent"}

# uvicorn model-as-a-service:app --reload

# run using - http://127.0.0.1:8000