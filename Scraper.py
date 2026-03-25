
import asyncio
import asyncio
from playwright.async_api import async_playwright, Playwright

# La classe Scraper permet d'encapsuler l'usage de Playright pour avoir la même configuration de playright sur tous les usages de scraping du projet
# Elle permet aussi de centraliser des methodes uttiles pour l'usage de Playwright
class Scraper:
    # Constructeur de la classe Scraper
    def __init__(self, playwright: Playwright, is_headless: bool = False):
        self.is_headless = is_headless
        # on initialise les variables vides qui seront innitialisées au lancement du navigateur
        self.playwright = playwright
        self.browser = None
        self.current_page = None

    # Méthode pour lancer le navigateur et accéder à l'url spécifié
    async def run(self, url: str):
        self.browser = await self.playwright.chromium.launch(headless=self.is_headless)
        self.current_page = await self.browser.new_page()
        await self.current_page.goto(url)

    # Méthode pour fermer le navigateur
    async def close(self):
        await self.browser.close()





