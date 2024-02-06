from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from crud import VehicleCRUD, OfficerCRUD, PersonCRUD, InfringementCRUD
from database.model import SessionLocal, engine, Vehicle, Officer, Person, Infringement
from fastapi import FastAPI, HTTPException, Depends, Header
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from model_pydantic_multas import OfficerPydantic, VehiclePydantic, PersonPydantic, InfraccionCreate
import jwt

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
# Crear la tabla en la base de datos si no existe
Vehicle.metadata.create_all(bind=engine)
Officer.metadata.create_all(bind=engine)
Person.metadata.create_all(bind=engine)

app = FastAPI()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_person_crud(db: Session = Depends(get_db)) -> PersonCRUD:
    return PersonCRUD(db)
def get_office_crud(db: Session = Depends(get_db)) -> OfficerCRUD:
    return OfficerCRUD(db)
def get_vehicles_crud(db: Session = Depends(get_db)) -> VehicleCRUD:
    return VehicleCRUD(db)
def get_infringement_crud(db: Session = Depends(get_db)) -> InfringementCRUD:
    return InfringementCRUD(db)



@app.get("/officers/")
def read_officer(oficce_crud: OfficerCRUD = Depends(get_office_crud)):
    oficce = oficce_crud.get()
    if oficce is None:
        raise HTTPException(status_code=404, detail="officerPydantic not found")
    # 
    
    return oficce

@app.post("/officers/")
def create_officer(oficce: OfficerPydantic, oficce_crud: OfficerCRUD = Depends(get_office_crud)):
    return oficce_crud.create(oficce.dict())

@app.delete("/officers/{officer_id}")
def delete_officer(officer_id: int, oficce_crud: OfficerCRUD = Depends(get_office_crud)):
    deleted_officer = oficce_crud.delete(id=officer_id)
    if deleted_officer is None:
        raise HTTPException(status_code=404, detail="officerPydantic not found")
    return deleted_officer

@app.put("/officers/{officer_id}")
def update_officer(officer_id: int, officer: dict, oficce_crud: OfficerCRUD = Depends(get_office_crud)):
    updated_officer = oficce_crud.update(officer_id, **officer)
    if updated_officer is None:
        raise HTTPException(status_code=404, detail="officerPydantic not found")
    return updated_officer