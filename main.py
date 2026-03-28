import os

from dotenv import load_dotenv

import StockPricesScraper
import asyncio

from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as playwright:
        scraper = StockPricesScraper.StockPricesScraper(playwright)
        #ricardStockData = await scraper.getLiveDataStock("1rPRI")
        #print(ricardStockData)

        ricardStockDataHistory = await scraper.getHistoricalDataStock("1rPRI", "27/03/2025")


if __name__ == "__main__":
    asyncio.run(main())