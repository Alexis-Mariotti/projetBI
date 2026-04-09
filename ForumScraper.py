from playwright.async_api import Playwright

from Scraper import Scraper


class ForumScraper (Scraper.Scraper):
    def __init__(self, playwright: Playwright, is_headless: bool = False):
        super().__init__(playwright, is_headless)

    #async def get_all_sujets(self):
