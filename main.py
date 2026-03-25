import os

from dotenv import load_dotenv

import StockPricesScraper
import asyncio

from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as playwright:
        scraper = StockPricesScraper.StockPricesScraper(playwright)
        await scraper.connect_to_boursorama()

if __name__ == "__main__":
    asyncio.run(main())