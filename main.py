from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import asyncio
from datetime import datetime
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SQLALCHEMY_DATABASE_URL = "sqlite:///./weather.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserInteraction(Base):
    __tablename__ = "user_interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    city = Column(String, default="")
    check_weather = Column(String, nullable=False)
    response = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserData(BaseModel):
    name: str
    check_weather: str
    city: str = ""

class WeatherResponse(BaseModel):
    message: str
    progress_complete: bool = False

class UserInteractionResponse(BaseModel):
    id: int
    name: str
    city: str
    check_weather: str
    response: str
    timestamp: datetime
    
    class Config:
        from_attributes = True

def get_weather_response(check_weather: str, city: str = ""):
    check_weather = check_weather.lower().strip()
    
    if check_weather == "yes":
        return "look out of your fucking window you fucking Dumbass, You need an application for weather."
    elif check_weather == "no":
        return "why the fuck are you here then, you fucking piece of shit."
    else:
        return "are you fucking retarted you fucking pig, can't you see yes or no, are you fucking blind."

@app.post("/weather", response_model=WeatherResponse)
async def weather_endpoint(user_data: UserData, db: Session = Depends(get_db)):
    try:
        response = get_weather_response(user_data.check_weather, user_data.city)
        
        db_interaction = UserInteraction(
            name=user_data.name,
            city=user_data.city,
            check_weather=user_data.check_weather,
            response=response
        )
        db.add(db_interaction)
        db.commit()
        db.refresh(db_interaction)
        
        return WeatherResponse(message=response, progress_complete=True)
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/interactions", response_model=list[UserInteractionResponse])
async def get_all_interactions(db: Session = Depends(get_db)):
    """Get all user interactions from database"""
    interactions = db.query(UserInteraction).all()
    return interactions

@app.get("/interactions/{user_name}", response_model=list[UserInteractionResponse])
async def get_user_interactions(user_name: str, db: Session = Depends(get_db)):
    """Get interactions for a specific user"""
    interactions = db.query(UserInteraction).filter(UserInteraction.name == user_name).all()
    return interactions

@app.get("/progress")
async def progress_endpoint():
    # Simulate the 10-second progress bar
    for i in range(101):
        await asyncio.sleep(0.1)
        yield f"data: {i}\n\n"

app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.get("/")
async def read_root():
    return FileResponse('static/index.html')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
