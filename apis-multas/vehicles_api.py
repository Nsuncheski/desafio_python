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


@app.get("/vehicles/")
def read_vehicles(vehicles_crud: VehicleCRUD = Depends(get_vehicles_crud)):
    # import pdb; pdb.set_trace()
    vehicles = vehicles_crud.get()
    if vehicles is None:
        raise HTTPException(status_code=404, detail="VehiclePydantic not found")
    # 
    
    # import pdb; pdb.set_trace()
    return vehicles

@app.post("/vehicles/")
def create_vehicles(vehicles: VehiclePydantic, vehicles_crud: VehicleCRUD = Depends(get_vehicles_crud)):

    # import pdb; pdb.set_trace()
    
    return vehicles_crud.create(vehicles.dict())

@app.delete("/vehicles/{vehicles_id}")
def delete_vehicles(vehicles_id: int, vehicles_crud: VehicleCRUD = Depends(get_vehicles_crud)):
    # import pdb; pdb.set_trace()
    deleted_vehicles = vehicles_crud.delete(id=vehicles_id)
    if deleted_vehicles is None:
        raise HTTPException(status_code=404, detail="VehiclePydantic not found")
    return deleted_vehicles

@app.put("/vehicles/{vehicles_id}")
def update_vehicles(vehicles_id: int, vehicles: dict, vehicles_crud: VehicleCRUD = Depends(get_vehicles_crud)):
    # import pdb; pdb.set_trace()
    updated_vehicles = vehicles_crud.update(vehicles_id, **vehicles)
    if updated_vehicles is None:
        raise HTTPException(status_code=404, detail="VehiclePydantic not found")
    return updated_vehicles



# Ruta para cargar una infracción
@app.post("/cargar_infraccion/")
def cargar_infraccion(infraccion: InfraccionCreate, infringement_crud: VehicleCRUD = Depends(get_infringement_crud)):
    # Verificar si el vehículo existe
    # import pdb; pdb.set_trace()
    
    return infringement_crud.create(infraccion.dict())


@app.get("/generar_informe/")
def generar_informe(email: str, person_crud: PersonCRUD = Depends(get_person_crud)):
    # import pdb; pdb.set_trace()
    person = person_crud.get(email)
    # import pdb; pdb.set_trace()
    infringements_list = []
    for per in person:
        for vehicle in per.vehicles:
            for infringement in vehicle.infringements:

                infringement_data = {
                    "patente": infringement.license_plate,
                    "fecha": infringement.timestamp,
                    "comentarios": infringement.comments
                }
                infringements_list.append(infringement_data)
    
    return infringements_list

    
