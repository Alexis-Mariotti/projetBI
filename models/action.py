from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base


class Action(Base):
    __tablename__ = "action"

    id = Column(Integer, primary_key=True, index=True)
    nom_action = Column(String(255), nullable=True)
    symbole_boursier = Column(String(255), nullable=True)

    secteur = Column(Integer, ForeignKey("secteur.id"))
    indice_reference = Column(Integer, ForeignKey("indice_reference.id"))

    secteur_rel = relationship("Secteur", back_populates="actions")
    indice_rel = relationship("IndiceReference", back_populates="actions")

    historiques_fj = relationship("HistoriqueFinJournee", back_populates="action_rel")
    historiques_live = relationship("HistoriqueLive", back_populates="action_rel")
    sujets = relationship("Sujet", back_populates="action_rel")