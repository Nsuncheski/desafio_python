from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from typing import Optional

# SQLAlchemy setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, index=True)
    email = Column(String, index=True)

    vehicles = relationship("Vehicle", back_populates="owner")

    def __init__(self, persons_dict) -> None:
        super().__init__()

        self.name = persons_dict["name"]
        self.email = persons_dict["email"]

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    license_plate = Column(String, index=True, unique=True)
    brand = Column(String)
    color = Column(String)
    owner_name = Column(String, ForeignKey("persons.name"))

    owner = relationship("Person", back_populates="vehicles")
    infringements = relationship("Infringement", back_populates="vehicle")

    def __init__(self, vehicles_dict) -> None:
        super().__init__()

        self.license_plate = vehicles_dict["license_plate"]
        self.brand = vehicles_dict["brand"]    
        self.color = vehicles_dict["color"]
        self.owner_name = vehicles_dict["owner_name"]          

class Officer(Base):
    __tablename__ = "officers"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String)
    badge_number = Column(String, unique=True)

    def __init__(self, officers_dict) -> None:
        super().__init__()

        self.name = officers_dict["name"]
        self.badge_number = officers_dict["badge_number"]

class Infringement(Base):
    __tablename__ = "infringements"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    license_plate = Column(String, ForeignKey("vehicles.license_plate"))
    timestamp = Column(String)
    comments = Column(String)

    vehicle = relationship("Vehicle", back_populates="infringements")

    def __init__(self, infringement_dict) -> None:
        super().__init__()

        self.license_plate = infringement_dict["placa_patente"]
        self.timestamp = infringement_dict["timestamp"]
        self.comments = infringement_dict["comentarios"]
