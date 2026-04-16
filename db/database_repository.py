import pandas as pd
import datetime

from sqlalchemy import TIMESTAMP, DateTime

from db.database import SessionLocal
from models import Reponse, Action, Sujet, IndiceReference, Secteur, HistoriqueFinJournee, HistoriqueLive


# methode uttilisé pour ajouter une reponse spécifique à un sujet de forum en base de donnée
def add_reponse(reponse: Reponse):
    session = SessionLocal()
    try:
        session.add(reponse)
        session.commit()
        # refresh pour recuperer l'id
        session.refresh(reponse)
    finally:
        session.close()

# methode uttilisé pour ajouter une action en base de donnée
# L'action represente l'action en elle meme et pas les information liés
def add_action(action: Action):
    session = SessionLocal()
    try:
        session.add(action)
        session.commit()
        # refresh pour recuperer l'id
        session.refresh(action)
    finally:
        session.close()

# methode pour recharger une action depuis la base de donnée et la synchroniser
# tres uttile pour obtenir l'id apres un commit
def refresh_action(action: Action):
    session = SessionLocal()
    try:
        session.refresh(action)
    finally:
        session.close()

# methode pour recharger un secteur depuis la base de donnée et la synchroniser
# tres uttile pour obtenir l'id apres un commit
def refresh_secteur(secteur: Secteur):
    session = SessionLocal()
    try:
        session.refresh(secteur)
    finally:
        session.close()

# methode pour recharger un indice de reference depuis la base de donnée et la synchroniser
# tres uttile pour obtenir l'id apres un commit
def refresh_indice_reference(indice: IndiceReference):
    session = SessionLocal()
    try:
        session.refresh(indice)
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


def add_historique_fin_journee(historique : HistoriqueFinJournee):
    session = SessionLocal()
    try:
        session.add(historique)
        session.commit()
        # refresh pour recuperer l'id
        session.refresh(historique)
    finally:
        session.close()

def add_historique_live(historique : HistoriqueLive):
    session = SessionLocal()
    try:
        session.add(historique)
        session.commit()
        # refresh pour recuperer l'id
        session.refresh(historique)
    finally:
        session.close()


# methode uttilisé pour ajouter un sujet de forum en base de donnée
def add_sujet(sujet: Sujet):
    session = SessionLocal()
    try:
        session.add(sujet)
        session.commit()
        # refresh pour recuperer l'id
        session.refresh(sujet)
    finally:
        session.close()


# fonction qui recherche si un indice existant ou le crée s'il n'existe pas et le renvoie
def get_or_create_indice_reference(nom_indice: str) -> IndiceReference:
    session = SessionLocal()
    indice_reference = None
    try:
        query = session.query(IndiceReference).filter(IndiceReference.nom_indice == nom_indice)
        if query.first() is None:
            indice_reference = IndiceReference()
            indice_reference.nom_indice = nom_indice
            session.add(indice_reference)
            session.commit()
            # refresh pour recuperer l'id
            session.refresh(indice_reference)
        else:
            indice_reference = query.first()
    finally:
        session.close()
    return indice_reference


# fonction qui cherche si un secteur existant ou le crée s'il n'existe pas et le renvoie
def get_or_create_secteur(nom_secteur: str) -> Secteur:
    session = SessionLocal()
    secteur = None
    try:
        query = session.query(Secteur).filter(Secteur.nom_secteur == nom_secteur)
        if  query.first() is None:
            secteur = Secteur()
            secteur.nom_secteur = nom_secteur
            session.add(secteur)
            session.commit()
            # refresh pour recuperer l'id
            session.refresh(secteur)
        else:
            secteur = query.first()
    finally:
        session.close()
    return secteur

# fonction qui crée ou renvoie une action si elle existe déja en base
def get_or_create_action(symbole_boursier: str, indice_label : str, secteur_label : str, nom_action : str) -> Action:
    # on cherche si recupere ou crée l'action si elle n'existe pas en BD
    action = get_action_by_symbole_boursier(symbole_boursier)
    if action is None:
        # crée l'action en base si elle n'existe pas
        # recupere l'incide et le secteur
        indice_reference = None
        secteur = None
        if indice_label is not None:
            indice_reference = get_or_create_indice_reference(indice_label)

        if secteur_label is not None:
            secteur = get_or_create_secteur(secteur_label)

        # crée l'action avec les objets que l'on viens de charger
        action = Action(nom_action=nom_action, symbole_boursier=symbole_boursier, secteur=secteur.id if secteur else None,
                        indice_reference=indice_reference.id if indice_reference else None)
        add_action(action)

    return action


# Fonction uttilisé pour enregistrer les données d'un historique d'action telechargé depuis Boursorama en base de donnée
# La bibliotheque pandas est uttilisée
# fileName : seulement le nom du ficher avec son extension, il doit etre present dans le répertoire "./temp/historique/"
def save_historical_data_stock_from_CSV( fileName: str, stockSymbol: str, stockName : str, secteur_label, indice_label) -> None:

    df = pd.read_csv("./temp/historique/" + fileName, sep='\t')


    print(df.axes)
    print(df['date'])

    # on cherche si recupere ou crée l'action si elle n'existe pas en BD
    action = get_or_create_action(stockSymbol, indice_label, secteur_label, stockName)


    # on ajoute les historiques de fin de journee en base de donnée
    action_id = action.id
    for index, row in df.iterrows():
        historique = HistoriqueFinJournee(date=datetime.datetime.strptime(row['date'], '%d/%m/%Y %H:%M'), ouverture=row['ouv'], haut=row['haut'], bas=row['bas'], cloture=row['clot'], volume=row['vol'], devise=row['devise'], action=action_id)
        add_historique_fin_journee(historique)


# Fonction uttilisé pour enregister les données recupére sur une action en live
def save_live_data_stock(stockSymbol: str, stockName : str, secteur_label: str, indice_label: str, prix_actuel: float, ouverture: float, haut: float, bas: float, volume: int, devise : str, timestamp : DateTime) -> None:
    # on cherche si recupere ou crée l'action si elle n'existe pas en BD
    action = get_or_create_action(stockSymbol, indice_label, secteur_label, stockName)

    # on enregistre en base
    historique_live = HistoriqueLive(prix_actuel=prix_actuel, ouverture=ouverture, haut=haut, bas=bas, volume=volume, devise=devise, action=action.id, timestamp=timestamp)
    add_historique_live(historique_live)

