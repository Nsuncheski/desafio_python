# # SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# # Base = declarative_base()

# # def get_person_crud(db: Session = Depends(get_db)) -> PersonCRUD:
# #     return PersonCRUD(db)


# # def get_office_crud(db: Session = Depends(get_db)) -> OfficerCRUD:
# #     return OfficerCRUD(db)


# # def get_vehicles_crud(db: Session = Depends(get_db)) -> VehicleCRUD:
# #     return VehicleCRUD(db)


# # def get_infringement_crud(db: Session = Depends(get_db)) -> InfringementCRUD:
#     return InfringementCRUD(db)