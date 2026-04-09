from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

from models import Action
from models.sujet import Sujet
from models.reponse import Reponse

dotenv_file = ".env.local"
load_dotenv(dotenv_file)
url = os.getenv("DATABASE_URL")

# Création de l'engine
engine = create_engine(url, echo=True)

# Configuration de la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base déclarative pour les modèles
Base = declarative_base()

def add_sujet(sujet: Sujet):
    session = SessionLocal()
    try:
        session.add(sujet)
        session.commit()
    finally:
        session.close()

def add_reponse(reponse: Reponse):
    session = SessionLocal()
    try:
        session.add(reponse)
        session.commit()
    finally:
        session.close()

def get_action_by_symbole_boursier(symbole_boursier: str) -> Action | None:
    session = SessionLocal()
    action = None
    try:
        action = session.query(Action).filter(Action.symbole_boursier == symbole_boursier).first()
    finally:
        session.close()
        return action
