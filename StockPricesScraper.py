from time import sleep

import  Scraper
from playwright.async_api import async_playwright, Playwright

import os
from dotenv import load_dotenv

class StockPricesScraper (Scraper.Scraper):
    def __init__(self, playwright: Playwright, is_headless: bool = False):
        super().__init__(playwright, is_headless)

        # On recupere les indentifiants de connexion à boursorama depuis le fichier .env
        # pensez à renseigner les votres
        load_dotenv()
        self.boursoLogin = os.getenv("BOURSO_LOGIN")
        self.boursoPassword = os.getenv("BOURSO_PASSWORD")

    # methode pour se connecter à boursorama, elle ouvre la page de connexion, remplit les champs de connexion et valide le formulaire
    async def connect_to_boursorama(self):
        await self.run("https://www.boursorama.com/connexion/?org=/membre/inscription-succes")
        loginForm = self.current_page.locator("#login")

        mailField = loginForm.locator("#login_member_login")
        pswdField = loginForm.locator("#login_member_password")
        loginSubmitButton = loginForm.locator("#login_member_connect")

        # si le mur de coockies s'ouvre, on l'accepte
        await self.acceptBoursoramaCookies(True);

        # on rempli les credentials
        await mailField.fill(self.boursoLogin)
        await pswdField.fill(self.boursoPassword)

        # on valide le formulaire de connexion
        await loginSubmitButton.click()


    # methode pour accepter les cookies sur le site de boursorama, si le mur de cookies s'affiche
    # le parametre withoutAgree permet de choisir si on accepte les cookies ou pas, par défaut on les accepte
    async def acceptBoursoramaCookies(self, withoutAgree: bool = False):
        cookiesWall = self.current_page.locator("#didomi-popup")
        if cookiesWall and await cookiesWall.is_visible():
            # on definit le bouton à cliquer differement selon si on veut accepter les cookies ou pas
            if not withoutAgree:
                button = cookiesWall.locator(".didomi-notice-agree-button")
            else:
                button = cookiesWall.locator(".didomi-continue-without-agreeing")
            await button.click()
