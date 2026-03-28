import datetime
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

        # debug
        # si il y a une erreur de redirection, on redirige nous même
        sleep(2) # attend chargement
        errorPage = self.current_page.locator(".neterror .error-code").get_by_text("ERR_TOO_MANY_REDIRECTS")
        if await errorPage.count() > 0:
            await self.current_page.goto("https://www.boursorama.com/")


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
    async def getHistoricalDataStock(self, stockCode: str, startDate: str, period: str = "2 mois"):
        # on se connecte à boursorama et se rend sur la page correspondante à l'action dont on veut les données
        await self.connect_to_boursorama()
        await self.current_page.goto("https://www.boursorama.com/cours/" + stockCode)

        # Recupere les boutons de navigation
        secondaryNav = self.current_page.locator("[aria-label=\"Menu secondaire\"]")
        historyButton = secondaryNav.locator("[title=\"Historique\"]")

        # navigue vers l'historique
        await historyButton.click()

        # Recupere les boutons de recherche de l'historique
        historic_search = self.current_page.locator("#historic_search")
        startDateInput = historic_search.locator("#historic_search_startDate")
        periodInputUl = historic_search.locator("#historic_search_duration-listbox")
        periodInput = periodInputUl.locator("xpath=..")
        searchButton = historic_search.locator("#historic_search_filter")

        # repli et lance la recherche
        await startDateInput.press_sequentially(startDate)
        # clique sur la periode voulu sur le combobox de periode
        await periodInput.click()
        await periodInputUl.get_by_text(period).click()
        # lance la recherche
        await searchButton.click()

        sleep(1)

        # Recupere le menu de pagination pour naviguer et recuperer toutes les données
        paginationElements = self.current_page.locator(".c-pagination a")
        pageCount = len(await paginationElements.all())

        print(await paginationElements.all())

        for i in range(pageCount):
            # on recupere le numero de page dans la pagination et on clqiue dessus
            await self.current_page.locator(".c-pagination a").nth(i).click()
            resultTable = self.current_page.locator("[data-refreshable-id=\"historical-period\"] table")
            resultTableRows = resultTable.locator("tbody tr")
            print(await resultTableRows.all())

        sleep(20)



        print(secondaryNav)