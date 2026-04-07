from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base


class HistoriqueFinJournee(Base):
    __tablename__ = "historique_fin_journee"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=True)
    ouverture = Column(Float, nullable=True)
    haut = Column(Float, nullable=True)
    bas = Column(Float, nullable=True)
    cloture = Column(Float, nullable=True)
    volume = Column(Integer, nullable=True)
    devise = Column(String(255), nullable=True)

    action = Column(Integer, ForeignKey("action.id"))

    action_rel = relationship("Action", back_populates="historiques_fj")