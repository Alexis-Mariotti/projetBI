from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

dotenv_file = ".env.local"
load_dotenv(dotenv_file)
url = os.getenv("DATABASE_URL")

# Création de l'engine
engine = create_engine(url, echo=True)

# Configuration de la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base déclarative pour les modèles
Base = declarative_base()