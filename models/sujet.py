from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base


class Sujet(Base):
    __tablename__ = "sujet"

    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String(255), nullable=True)
    message = Column(Text(length=65535), nullable=True)
    auteur = Column(String(255), nullable=True)
    date = Column(DateTime, nullable=True)

    action = Column(Integer, ForeignKey("action.id"))

    action_rel = relationship("Action", back_populates="sujets")
    reponses = relationship("Reponse", back_populates="sujet_rel")