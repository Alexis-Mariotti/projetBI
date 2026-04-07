from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base


class Reponse(Base):
    __tablename__ = "reponse"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text(length=65535), nullable=True)
    auteur = Column(String(255), nullable=True)
    date = Column(DateTime, nullable=True)

    sujet = Column(Integer, ForeignKey("sujet.id"))

    sujet_rel = relationship("Sujet", back_populates="reponses")