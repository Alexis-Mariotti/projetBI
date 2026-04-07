from db.database import engine, Base

from models.secteur import Secteur
from models.indice_reference import IndiceReference
from models.action import Action
from models.historique_fin_journee import HistoriqueFinJournee
from models.historique_live import HistoriqueLive
from models.sujet import Sujet
from models.reponse import Reponse

def init_db():
    print("Création des tables dans la base de données MariaDB")
    Base.metadata.create_all(bind=engine)
    print("Création terminée avec succès !")

