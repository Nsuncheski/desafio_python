from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from crud import VehicleCRUD, OfficerCRUD, PersonCRUD, InfringementCRUD
from model_pydantic_multas import OfficerPydantic, VehiclePydantic, PersonPydantic, InfraccionCreate
import json

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_person_crud(db: Session) -> PersonCRUD:
    return PersonCRUD(db)


def get_office_crud(db: Session) -> OfficerCRUD:
    return OfficerCRUD(db)


def get_vehicles_crud(db: Session) -> VehicleCRUD:
    return VehicleCRUD(db)


def get_infringement_crud(db: Session) -> InfringementCRUD:
    return InfringementCRUD(db)


def lambda_handler(event, context):
    path = event["path"]
    method = event["httpMethod"]
    body = event["body"]
    query_params = event["queryStringParameters"]

    # Determinar la ruta y ejecutar la función Lambda correspondiente
    if method == "GET":
        if path == "/officers/":
            return read_officer(query_params)
        # Agregar otras rutas GET aquí

    elif method == "POST":
        if path == "/officers/":
            return create_officer(body)
        # Agregar otras rutas POST aquí

    elif method == "DELETE":
        if path.startswith("/officers/"):
            officer_id = int(path.split("/")[2])
            return delete_officer(officer_id)
        # Agregar otras rutas DELETE aquí

    elif method == "PUT":
        if path.startswith("/officers/"):
            officer_id = int(path.split("/")[2])
            return update_officer(officer_id, body)
        # Agregar otras rutas PUT aquí

    return {"statusCode": 404, "body": json.dumps("Ruta no encontrada")}


def read_officer(query_params):
    # Obtener datos de la base de datos
    with get_db() as db:
        office_crud = get_office_crud(db)
        officers = office_crud.get()

    # Convertir datos a formato JSON
    officers_json = [officer.json() for officer in officers]

    return {"statusCode": 200, "body": json.dumps(officers_json)}


def create_officer(body):
    # Decodificar el cuerpo JSON
    officer_data = json.loads(body)

    # Crear el oficial en la base de datos
    with get_db() as db:
        office_crud = get_office_crud(db)
        new_officer = office_crud.create(officer_data)

    return {"statusCode": 200, "body": json.dumps(new_officer)}


def delete_officer(officer_id):
    # Eliminar el oficial de la base de datos
    with get_db() as db:
        office_crud = get_office_crud(db)
        deleted_officer = office_crud.delete(id=officer_id)

    return {"statusCode": 200, "body": json.dumps(deleted_officer)}


def update_officer(officer_id, body):
    # Decodificar el cuerpo JSON
    officer_data = json.loads(body)

    # Actualizar el oficial en la base de datos
    with get_db() as db:
        office_crud = get_office_crud(db)
        updated_officer = office_crud.update(officer_id, **officer_data)

    return {"statusCode": 200, "body": json.dumps(updated_officer)}
