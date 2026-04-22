
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

    # methode pour accepter les cookies sur le site de boursorama, si le mur de cookies s'affiche
    # le parametre withoutAgree permet de choisir si on accepte les cookies ou pas, par défaut on les accepte
    async def acceptBoursoramaCookies(self, withoutAgree: bool = False):
        cookiesWall = self.current_page.locator("#didomi-popup")
        if cookiesWall and await cookiesWall.is_visible():
            # on definit le bouton à cliquer differement selon si on veut accepter les cookies ou pas
            if not withoutAgree:
                button = cookiesWall.locator("#didomi-notice-agree-button")
            else:
                button = cookiesWall.locator(".didomi-continue-without-agreeing")
            await button.click()





