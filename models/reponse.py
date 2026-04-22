from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base


class Reponse(Base):
    __tablename__ = "reponse"

    __table_args__ = {
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
    }

    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text(length=65535), nullable=True)
    auteur = Column(String(255), nullable=True)
    date = Column(DateTime, nullable=True)

    sujet = Column(Integer, ForeignKey("sujet.id"))

    sujet_rel = relationship("Sujet", back_populates="reponses")