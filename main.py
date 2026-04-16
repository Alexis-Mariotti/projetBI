import os

from dotenv import load_dotenv

import StockPricesScraper
import asyncio

from playwright.async_api import async_playwright

from db.database_repository import get_or_create_indice_reference
from models import init_db

# Cette methode est faite pour Nils !
# Cette methode permet de tester les differentes fonctionalités du projet, et de fournir des données à la base
# N'oubliez pas de bien lire le readme pour ne pas oublier des étapes nescessaires au fonctionement du projet
# notament l'instalation des dépendances ainsi que le lancement de le contner de la BD
# vous pouvez consulter la BD sur php my admin : http://localhost:8080
async def sampleForNils(scraper):
    # données live de l'action AIRBUS
    await scraper.getLiveDataStock("AIR")
    # données de l'action SAFRAN
    await scraper.getLiveDataStock("SAF")
    # Les données de l'action RICARD
    await scraper.getLiveDataStock("RI")

     # données historique de l'action AIRBUS sur 6 mois
    await scraper.getHistoricalDataStock("AIR", "6M")
    # données historique de l'action SAFRAN sur 6 mois
    await scraper.getHistoricalDataStock("SAF", "6M")
    # Données historique de l'action RICARD sur 10 ans
    await scraper.getHistoricalDataStock("1rPRI", "10A")

    # on répuere les données de AIRBUS sur 5 jours, 5 ans et sur le live pour tester les chevauchements
    await scraper.getHistoricalDataStock("AIR", "5J")
    await scraper.getHistoricalDataStock("AIR", "5A")
    await scraper.getLiveDataStock("AIR")


async def main():
    async with async_playwright() as playwright:
        scraper = StockPricesScraper.StockPricesScraper(playwright, is_headless=False)
        #ricardStockData = await scraper.getLiveDataStock("1rPRI")
        #print(ricardStockData)

        #ricardStockDataHistory = await scraper.getHistoricalDataStock("SAF", "6M")
        #await scraper.getLiveDataStock("AIR")
        #scraper.saveHistoricalDataStockFromCSV("1rPRI_10A_2026-04-07_historical_data.csv")

        await sampleForNils(scraper)


if __name__ == "__main__":
    init_db()
    asyncio.run(main())