from sqlalchemy import Column, Integer, String, Float, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from db.database import Base


class HistoriqueLive(Base):
    __tablename__ = "historique_live"

    id = Column(Integer, primary_key=True, index=True)
    prix_actuel = Column(Float, nullable=True)
    ouverture = Column(Float, nullable=True)
    haut = Column(Float, nullable=True)
    bas = Column(Float, nullable=True)
    volume = Column(Integer, nullable=True)
    devise = Column(String(255), nullable=True)
    timestamp = Column(TIMESTAMP, nullable=True)

    action = Column(Integer, ForeignKey("action.id"))

    action_rel = relationship("Action", back_populates="historiques_live")