from sqlalchemy.orm import Session
from database.model import Person, Vehicle, Officer, Infringement


class CRUD:
    def __init__(self, db: Session, model):
        self.db = db
        self.model = model

    def create(self, dict1: dict,):

        instance = self.model(dict1)
        self.db.add(instance)

        self.db.commit()
        self.db.refresh(instance)
        return instance

    def get(self, id=None):
        if id:
            result = self.db.query(self.model).filter(self.model.email == id).all()
        else:
            result = self.db.query(self.model).all()
        return result

    def update(self, id, **kwargs):
        instance = self.get(id)     
        if instance:
            for key, value in kwargs.items():
                setattr(instance, key, value)
            self.db.commit()
            self.db.refresh(instance)
        return instance

    def delete(self, id):
        instance = self.get(id)
        if instance:
    
            self.db.delete(instance)
            self.db.commit()
        return instance

class PersonCRUD(CRUD):
    def __init__(self, db: Session):
        super().__init__(db, Person)

class VehicleCRUD(CRUD):
    def __init__(self, db: Session):
        super().__init__(db, Vehicle)

class OfficerCRUD(CRUD):
    def __init__(self, db: Session):
        super().__init__(db, Officer)

class InfringementCRUD(CRUD):
    def __init__(self, db: Session):
        super().__init__(db, Infringement)
