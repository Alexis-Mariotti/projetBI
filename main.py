import ForumScraper
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
async def sampleForNils(stock_scraper, forum_scraper):
    # données live de l'action AIRBUS
    await stock_scraper.getLiveDataStock("AIR")
    # données de l'action SAFRAN
    await stock_scraper.getLiveDataStock("SAF")
    # Les données de l'action RICARD
    await stock_scraper.getLiveDataStock("RI")

     # données historique de l'action AIRBUS sur 6 mois
    await stock_scraper.getHistoricalDataStock("AIR", "6M")
    # données historique de l'action SAFRAN sur 6 mois
    await stock_scraper.getHistoricalDataStock("SAF", "6M")
    # Données historique de l'action RICARD sur 10 ans
    await stock_scraper.getHistoricalDataStock("RI", "10A")

    # on répuere les données de AIRBUS sur 5 jours, 5 ans et sur le live pour tester les chevauchements
    await stock_scraper.getHistoricalDataStock("AIR", "5J")
    await stock_scraper.getHistoricalDataStock("AIR", "5A")
    await stock_scraper.getLiveDataStock("AIR")

    # scraping de l'un des forums (uniquement 1 par défault parce que ça prend énormement de temps)

    await forum_scraper.scarpe_forum("RI")
    #await forum_scraper.scarpe_forum("SAF")

    # AIRBUS ne possède pas de forum sur boursorama


async def main():
    async with async_playwright() as playwright:
        stock_scraper = StockPricesScraper.StockPricesScraper(playwright, is_headless=False)
        forum_scraper = ForumScraper.ForumScraper(playwright)

        await sampleForNils(stock_scraper, forum_scraper)


if __name__ == "__main__":
    init_db()
    asyncio.run(main())