from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from crud import VehicleCRUD, OfficerCRUD, PersonCRUD, InfringementCRUD
from database.model import SessionLocal, engine, Vehicle, Officer, Person, Infringement
from fastapi import FastAPI, HTTPException, Depends, Header
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from model_pydantic_multas import (
    OfficerPydantic,
    VehiclePydantic,
    PersonPydantic,
    InfraccionCreate,
)
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


@app.post("/persons/")
def create_person(
    person: PersonPydantic, person_crud: PersonCRUD = Depends(get_person_crud)
):


    return person_crud.create(person.dict())


@app.get("/persons/")
def read_person(person_crud: PersonCRUD = Depends(get_person_crud)):
    person = person_crud.get()
    if person is None:
        raise HTTPException(status_code=404, detail="PersonPydantic not found")
    return person


@app.put("/persons/{person_id}")
def update_person(
    person_id: int, person: dict, person_crud: PersonCRUD = Depends(get_person_crud)
):
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


@app.get("/officers/")
def read_officer(oficce_crud: OfficerCRUD = Depends(get_office_crud)):
    oficce = oficce_crud.get()
    if oficce is None:
        raise HTTPException(status_code=404, detail="officerPydantic not found")
    #

    return oficce


@app.post("/officers/")
def create_officer(
    oficce: OfficerPydantic, oficce_crud: OfficerCRUD = Depends(get_office_crud)
):


    return oficce_crud.create(oficce.dict())


@app.delete("/officers/{officer_id}")
def delete_officer(
    officer_id: int, oficce_crud: OfficerCRUD = Depends(get_office_crud)
):
    deleted_officer = oficce_crud.delete(id=officer_id)
    if deleted_officer is None:
        raise HTTPException(status_code=404, detail="officerPydantic not found")
    return deleted_officer


@app.put("/officers/{officer_id}")
def update_officer(
    officer_id: int, officer: dict, oficce_crud: OfficerCRUD = Depends(get_office_crud)
):
    updated_officer = oficce_crud.update(officer_id, **officer)
    if updated_officer is None:
        raise HTTPException(status_code=404, detail="officerPydantic not found")
    return updated_officer


################################### vehicles ###################
@app.get("/vehicles/")
def read_vehicles(vehicles_crud: VehicleCRUD = Depends(get_vehicles_crud)):
    vehicles = vehicles_crud.get()
    if vehicles is None:
        raise HTTPException(status_code=404, detail="VehiclePydantic not found")
    #

    return vehicles


@app.post("/vehicles/")
def create_vehicles(
    vehicles: VehiclePydantic, vehicles_crud: VehicleCRUD = Depends(get_vehicles_crud)
):


    return vehicles_crud.create(vehicles.dict())


@app.delete("/vehicles/{vehicles_id}")
def delete_vehicles(
    vehicles_id: int, vehicles_crud: VehicleCRUD = Depends(get_vehicles_crud)
):
    deleted_vehicles = vehicles_crud.delete(id=vehicles_id)
    if deleted_vehicles is None:
        raise HTTPException(status_code=404, detail="VehiclePydantic not found")
    return deleted_vehicles


@app.put("/vehicles/{vehicles_id}")
def update_vehicles(
    vehicles_id: int,
    vehicles: dict,
    vehicles_crud: VehicleCRUD = Depends(get_vehicles_crud),
):
    updated_vehicles = vehicles_crud.update(vehicles_id, **vehicles)
    if updated_vehicles is None:
        raise HTTPException(status_code=404, detail="VehiclePydantic not found")
    return updated_vehicles


# Ruta para cargar una infracción
@app.post("/cargar_infraccion/")
def cargar_infraccion(
    infraccion: InfraccionCreate,
    infringement_crud: VehicleCRUD = Depends(get_infringement_crud),
):
    # Verificar si el vehículo existe

    return infringement_crud.create(infraccion.dict())


@app.get("/generar_informe/")
def generar_informe(email: str, person_crud: PersonCRUD = Depends(get_person_crud)):
    person = person_crud.get(email)
    infringements_list = []
    for per in person:
        for vehicle in per.vehicles:
            for infringement in vehicle.infringements:

                infringement_data = {
                    "patente": infringement.license_plate,
                    "fecha": infringement.timestamp,
                    "comentarios": infringement.comments,
                }
                infringements_list.append(infringement_data)

    return infringements_list
