import json
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from crud import PersonCRUD


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()


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


# Person routes
def create_person(event, context):
    body = event["body"]
    person_data = json.loads(body)
    with get_db() as db:
        person_crud = get_person_crud(db)
        created_person = person_crud.create(person_data)
    return {
        "statusCode": 200,
        "body": json.dumps(created_person)
    }


def read_person(event, context):
    with get_db() as db:
        person_crud = get_person_crud(db)
        person = person_crud.get()
    if person is None:
        raise HTTPException(status_code=404, detail="PersonPydantic not found")
    return {
        "statusCode": 200,
        "body": json.dumps(person)
    }


def update_person(event, context):
    path_params = event["pathParameters"]
    person_id = int(path_params["person_id"])
    body = event["body"]
    person_data = json.loads(body)
    with get_db() as db:
        person_crud = get_person_crud(db)
        updated_person = person_crud.update(person_id, **person_data)
    if updated_person is None:
        raise HTTPException(status_code=404, detail="PersonPydantic not found")
    return {
        "statusCode": 200,
        "body": json.dumps(updated_person)
    }


def delete_person(event, context):
    path_params = event["pathParameters"]
    person_id = int(path_params["person_id"])
    with get_db() as db:
        person_crud = get_person_crud(db)
        deleted_person = person_crud.delete(id=person_id)
    if deleted_person is None:
        raise HTTPException(status_code=404, detail="PersonPydantic not found")
    return {
        "statusCode": 200,
        "body": json.dumps(deleted_person)
    }
