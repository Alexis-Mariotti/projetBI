import os

from dotenv import load_dotenv

import StockPricesScraper
import asyncio

from playwright.async_api import async_playwright

from db.database_repository import get_or_create_indice_reference
from models import init_db

async def main():
    async with async_playwright() as playwright:
        scraper = StockPricesScraper.StockPricesScraper(playwright)
        #ricardStockData = await scraper.getLiveDataStock("1rPRI")
        #print(ricardStockData)

        #ricardStockDataHistory = await scraper.getHistoricalDataStock("SAF", "6M")
        await scraper.getLiveDataStock("SABE")
        #scraper.saveHistoricalDataStockFromCSV("1rPRI_10A_2026-04-07_historical_data.csv")


if __name__ == "__main__":
    init_db()
    asyncio.run(main())