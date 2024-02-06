from typing import List, Optional
from pydantic import BaseModel

class PersonPydantic(BaseModel):
    name: str
    email: str

class Person(PersonPydantic):
    id: int

    class Config:
        orm_mode = True

class VehiclePydantic(BaseModel):
    license_plate: str
    brand: str
    color: str
    owner_name: str

class Vehicle(VehiclePydantic):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class OfficerPydantic(BaseModel):
    name: str
    badge_number: str

class Officer(OfficerPydantic):
    id: int

    class Config:
        orm_mode = True
        
class InfraccionCreate(BaseModel):
    placa_patente: str
    timestamp: str
    comentarios: str