
from db.database import SessionLocal
from models import Reponse, Action

# methode uttilisé pour ajouter une reponse spécifique à un sujet de forum en base de donnée
def add_reponse(reponse: Reponse):
    session = SessionLocal()
    try:
        session.add(reponse)
        session.commit()
    finally:
        session.close()

# methode uttilisé pour ajouter une action en base de donnée
# L'action represente l'action en elle meme et pas les information liés
def add_action(action: Action):
    session = SessionLocal()
    try:
        session.add(action)
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


def add_historique_fin_journee(historique):
    session = SessionLocal()
    try:
        session.add(historique)
        session.commit()
    finally:
        session.close()