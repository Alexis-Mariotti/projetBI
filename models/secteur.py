from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.database import Base

class Secteur(Base):
    __tablename__ = "secteur"

    id = Column(Integer, primary_key=True, index=True)
    nom_secteur = Column(String(255), nullable=True)

    actions = relationship("Action", back_populates="secteur_rel")