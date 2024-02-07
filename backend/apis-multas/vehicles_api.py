import json
from fastapi import HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from crud import VehicleCRUD, PersonCRUD, InfringementCRUD


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD Dependencies
def get_person_crud(db: Session = Depends(get_db)) -> PersonCRUD:
    return PersonCRUD(db)

def get_vehicles_crud(db: Session = Depends(get_db)) -> VehicleCRUD:
    return VehicleCRUD(db)

def get_infringement_crud(db: Session = Depends(get_db)) -> InfringementCRUD:
    return InfringementCRUD(db)

def lambda_handler(event, context):
    path = event["path"]
    method = event["httpMethod"]
    body = event.get("body", None)

    if method == "GET":
        if path == "/vehicles/":
            return read_vehicles()
        # Add other GET routes here

    elif method == "POST":
        if path == "/vehicles/":
            return create_vehicles(body)
        elif path == "/cargar_infraccion/":
            return cargar_infraccion(body)
        # Add other POST routes here

    elif method == "DELETE":
        if path.startswith("/vehicles/"):
            vehicles_id = int(path.split("/")[2])
            return delete_vehicles(vehicles_id)
        # Add other DELETE routes here

    elif method == "PUT":
        if path.startswith("/vehicles/"):
            vehicles_id = int(path.split("/")[2])
            return update_vehicles(vehicles_id, body)
        # Add other PUT routes here

    elif method == "GET" and path == "/generar_informe/":
        query_params = event["queryStringParameters"]
        email = query_params.get("email", None)
        return generar_informe(email)

    return {
        "statusCode": 404,
        "body": json.dumps("Route not found")
    }

def read_vehicles():
    with get_db() as db:
        vehicles_crud = get_vehicles_crud(db)
        vehicles = vehicles_crud.get()
    if vehicles is None:
        raise HTTPException(status_code=404, detail="VehiclePydantic not found")
    return {
        "statusCode": 200,
        "body": json.dumps(vehicles)
    }

def create_vehicles(body):
    vehicle_data = json.loads(body)
    with get_db() as db:
        vehicles_crud = get_vehicles_crud(db)
        created_vehicle = vehicles_crud.create(vehicle_data)
    return {
        "statusCode": 200,
        "body": json.dumps(created_vehicle)
    }

def delete_vehicles(vehicles_id):
    with get_db() as db:
        vehicles_crud = get_vehicles_crud(db)
        deleted_vehicle = vehicles_crud.delete(id=vehicles_id)
    if deleted_vehicle is None:
        raise HTTPException(status_code=404, detail="VehiclePydantic not found")
    return {
        "statusCode": 200,
        "body": json.dumps(deleted_vehicle)
    }

def update_vehicles(vehicles_id, body):
    vehicle_data = json.loads(body)
    with get_db() as db:
        vehicles_crud = get_vehicles_crud(db)
        updated_vehicle = vehicles_crud.update(vehicles_id, **vehicle_data)
    if updated_vehicle is None:
        raise HTTPException(status_code=404, detail="VehiclePydantic not found")
    return {
        "statusCode": 200,
        "body": json.dumps(updated_vehicle)
    }

def cargar_infraccion(body):
    infringement_data = json.loads(body)
    with get_db() as db:
        infringement_crud = get_infringement_crud(db)
        created_infringement = infringement_crud.create(infringement_data)
    return {
        "statusCode": 200,
        "body": json.dumps(created_infringement)
    }

def generar_informe(email):
    with get_db() as db:
        person_crud = get_person_crud(db)
        person = person_crud.get(email)
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")
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
    return {
        "statusCode": 200,
        "body": json.dumps(infringements_list)
    }
