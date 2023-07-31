from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from typing import List

#to mysql connector thing

# Replace the database_url with your actual MySQL connection URL
database_url = "mysql+mysqlconnector://root:1234@localhost/app"

app = FastAPI()

# Create the MySQL database engine and session
engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the base class for declarative models
Base = declarative_base()


# Define the Transaction model
class user(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255))
    pswd = Column(String(255))
    
class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, index=True)
    date = Column(String(10))
    description = Column(String(255))
    amount = Column(Float)


# Create the table in the database (run this once to create the table)
Base.metadata.create_all(bind=engine)


# Pydantic model for input validation
class TransactionCreate(BaseModel):
    transaction_id: int
    date: str
    description: str
    amount: float

class userCreate(BaseModel):
    username: str
    pswd: str

@app.get("/transactions/", response_model=List[TransactionCreate])
def get_transactions(skip: int = 0, limit: int = 10, db: Session = Depends(SessionLocal)):
    transactions = db.query(Transaction).offset(skip).limit(limit).all()
    return transactions

@app.get("/user/", response_model=List[userCreate])
def get_user(skip: int = 0, limit: int = 10, db: Session = Depends(SessionLocal)):
    user = db.query(user).offset(skip).limit(limit).all()
    return user

@app.post("/transactions/", response_model=TransactionCreate)
def add_transaction(transaction: TransactionCreate, db: Session = Depends(SessionLocal)):
    db_transaction = Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@app.post("/user/", response_model=userCreate)
def add_user(user: userCreate, db: Session = Depends(SessionLocal)):
    db_user = user(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

'''
@app.put("/transactions/{transaction_id}/", response_model=TransactionCreate)
def edit_transaction(transaction_id: int, transaction: TransactionCreate, db: Session = Depends(SessionLocal)):
    db_transaction = db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()

    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    for key, value in transaction.dict().items():
        setattr(db_transaction, key, value)

    db.commit()
    db.refresh(db_transaction)
    return db_transaction
'''
