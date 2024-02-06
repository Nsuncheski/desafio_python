from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import VehicleCRUD, OfficerCRUD, PersonCRUD, InfringementCRUD
from database.model import SessionLocal, engine, Vehicle, Officer, Person
from fastapi import FastAPI, HTTPException, Depends, Header
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from model_pydantic_multas import  PersonPydantic


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

@app.post("/persons/")
def create_person(person: PersonPydantic, person_crud: PersonCRUD = Depends(get_person_crud)): 
    return person_crud.create(person.dict())

@app.get("/persons/")
def read_person(person_crud: PersonCRUD = Depends(get_person_crud)):
    person = person_crud.get()
    if person is None:
        raise HTTPException(status_code=404, detail="PersonPydantic not found")
    return person

@app.put("/persons/{person_id}")
def update_person(person_id: int, person: dict, person_crud: PersonCRUD = Depends(get_person_crud)):
    updated_person = person_crud.update(person_id, **person)
    if updated_person is None:
        raise HTTPException(status_code=404, detail="PersonPydantic not found")
    return updated_person

@app.delete("/persons/{person_id}")
def delete_person(person_id: int, person_crud: PersonCRUD = Depends(get_person_crud)):
    deleted_person = person_crud.delete(id=person_id)
    if deleted_person is None:
        raise HTTPException(status_code=404, detail="PersonPydantic not found")
    return deleted_person
