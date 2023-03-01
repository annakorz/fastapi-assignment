
from fastapi import FastAPI, Depends, HTTPException
from starlette import status
from models import User, Base
from forms import UserCreateForm
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from crud import get_user_by_email, get_user_by_id

# create_all 
# This method will issue queries that first check for the existence 
# of each individual table, and if not found will issue the CREATE statements

Base.metadata.create_all(bind=engine)


app = FastAPI()


# to have an independent database session/connection (SessionLocal) per request, 
# use the same session through all the request and then close it after the request is finished.

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# The parameter db is actually of type SessionLocal, but this class (created with sessionmaker()) 
# is a "proxy" of a SQLAlchemy Session, so, the editor doesn't really know what methods are 
# provided.
# But by declaring the type as Session, the editor now can know the available methods 
# (.add(), .query(), .commit(), etc) and can provide better support (like completion). 
# The type declaration doesn't affect the actual object.

@app.get("/users/{user_id}", response_model=UserCreateForm, name='user: get by id')
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return db_user

@app.post('/users', name='user:create')
def create_user(user: UserCreateForm, db=Depends(get_db)):
    exists_user = get_user_by_email(db, user=user)
    if exists_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already exists')
    
    new_user = User(
        name=user.name,
        email=user.email,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {new_user}


