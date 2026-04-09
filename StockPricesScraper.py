import datetime
from time import sleep

import  Scraper
from playwright.async_api import async_playwright, Playwright

import os
from dotenv import load_dotenv

# on uttilise panda dans ce script pour parser les historiques csv
import pandas as pd

class StockPricesScraper (Scraper.Scraper):
    def __init__(self, playwright: Playwright, is_headless: bool = False):
        super().__init__(playwright, is_headless)

        # On recupere les indentifiants de connexion à boursorama depuis le fichier .env.local
        # pensez à renseigner les votres en copiant le .env
        dotenv_file = ".env.local"
        load_dotenv(dotenv_file)
        self.boursoLogin = os.getenv("BOURSO_LOGIN")
        self.boursoPassword = os.getenv("BOURSO_PASSWORD")

    # methode pour se connecter à boursorama, elle ouvre la page de connexion, remplit les champs de connexion et valide le formulaire
    async def connect_to_boursorama(self):
        await self.run("https://www.boursorama.com/connexion/")
        loginForm = self.current_page.locator("#login")

        mailField = loginForm.locator("#login_member_login")
        pswdField = loginForm.locator("#login_member_password")
        loginSubmitButton = loginForm.locator("#login_member_connect")

        # si le mur de coockies s'ouvre, on l'accepte
        await self.acceptBoursoramaCookies();

        # on rempli les credentials
        await mailField.fill(self.boursoLogin)
        await pswdField.fill(self.boursoPassword)

        # on valide le formulaire de connexion
        await loginSubmitButton.click()

        # debug
        # si il y a une erreur de redirection, on redirige nous même
        '''
        sleep(2) # attend chargement
        errorPage = self.current_page.locator(".neterror .error-code").get_by_text("ERR_TOO_MANY_REDIRECTS")
        if await errorPage.count() > 0:
            await self.current_page.goto("https://www.boursorama.com/")
        '''

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

    # Fonctionnalité permettant de collecter à partir de la page d’une action du site Boursorama, toutes les
    # informations sur le cours du jour (date/heure de collecte, cours, cours d’ouverture, cours haut, cours bas, volumes)
    async def getLiveDataStock(self, stockCode: str):
        # on se rend sur la page correspondante à l'action dont on veut les données
        await self.run("https://www.boursorama.com/cours/" + stockCode)

        # on récupere la date
        currentDate = datetime.datetime.now()
        actualStockPrice = await self.current_page.locator(".c-faceplate__price .c-instrument--last").text_content()
        openingStockPrice = await self.current_page.locator(".c-instrument--open").text_content()
        highStockPrice = await self.current_page.locator(".c-instrument--high").text_content()
        lowStockPrice = await self.current_page.locator(".c-instrument--low").text_content()
        volumeStockPrice = await self.current_page.locator(".c-instrument--totalvolume").text_content()

        # on ferme le navigateur
        await self.close()


        # on renvoie un dictionaire avec les information
        return {"currentDate": currentDate, "actualStockPrice": actualStockPrice, "opening": openingStockPrice, "high": highStockPrice, "low": lowStockPrice, "volume": volumeStockPrice}

    # Fonctionnalité permettant de collecter à partir de la page d’une action du site Boursorama, toutes les
    # informations sur l'historique du cours de l’action (date/heure de collecte, cours, cours d’ouverture, cours haut, cours bas, volumes) pour une période donnée
    # period : permet de determiner la taille de la plage de donnée. Accepte uniquement les valeurs du formulaire sur le site Boursorama
    async def getHistoricalDataStock(self, stockCode: str, startDate: str, period: str = "10A"):
        # on se connecte à boursorama et se rend sur la page correspondante à l'action dont on veut les données
        await self.connect_to_boursorama()
        await self.current_page.goto("https://www.boursorama.com/cours/" + stockCode)

        # Recupere les boutons de navigation
        # secondaryNav = self.current_page.locator("[aria-label=\"Menu secondaire\"]")
        # historyButton = secondaryNav.locator("[title=\"Historique\"]")

        sleep(1)

        # Recupere le menu de durée du graphique pour selectioner la durée voulue
        durationMenu = self.current_page.locator(".c-quote-chart__durations")
        # recupere le bouton de la durée voulu
        durationButton = durationMenu.locator(".c-quote-chart__length").get_by_text(period)
        # bouton de telechargement
        downloadButton = durationMenu.locator("[data-original-title=\"Télécharger les cotations\"]")

        #print(await downloadButton.all())
        #sleep(100)
        await durationButton.click()

        # on previens playwright qu'un telechargement est attendu pour pouvoir le sauvegarder dans le repertoire ovulu
        async with self.current_page.expect_download() as download_info:
            # lance le telechargement
            await downloadButton.click(button="left")
        download = await download_info.value
        # sauvegarde le fichier dans le repertoire voulu
        fileName = "./temp/historique/" + stockCode + "_" + period + "_" + datetime.datetime.now().strftime("%Y-%m-%d") + "_historical_data.csv"
        await download.save_as(fileName)

        # sauvegarde en BD les données contenue dans le fichier qui viens d'etre telechargé
        self.saveHistoricalDataStockFromCSV(fileName.replace("./temp/historique/", ""))

    # Fonction uttilisé pour enregistrer les données d'un historique d'action telechargé depuis Boursorama en base de donnée
    # La bibliotheque pandas est uttilisée
    # fileName : seulement le nom du ficher avec son extension, il doit etre present dans le répertoire "./temp/historique/"
    def saveHistoricalDataStockFromCSV(self, fileName: str):

        df = pd.read_csv("./temp/historique/" + fileName, sep='\t')


        print(df.axes)
        print(df['date'])


