from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv


dotenv_file = ".env.local"
load_dotenv(dotenv_file)
url = os.getenv("DATABASE_URL")

# Création de l'engine
engine = create_engine(url, echo=True)

@event.listens_for(Engine, "connect")
def set_mariadb_charset(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci")
    cursor.execute("SET CHARACTER SET utf8mb4")
    cursor.close()

# Configuration de la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base déclarative pour les modèles
Base = declarative_base()


