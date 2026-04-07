from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.database import Base

class IndiceReference(Base):
    __tablename__ = "indice_reference"

    id = Column(Integer, primary_key=True, index=True)
    nom_indice = Column(String(255), nullable=True)

    actions = relationship("Action", back_populates="indice_rel")