from datetime import datetime
from typing import Any

from playwright.async_api import Playwright

import Scraper
from db.database_repository import add_sujet
from models import Sujet


class ForumScraper (Scraper.Scraper):
    def __init__(self, playwright: Playwright, is_headless: bool = False):
        super().__init__(playwright, is_headless)

    async def get_all_sujets(self):

        #TODO : récupération de chaque page de sujet du forum
        return

    async def get_all_sujets_by_page(self):
        list_a: list = await self.current_page.get_by_title("Voir le sujet").all()
        for a in list_a:
            href: str = a.get_attribute("href")
            await self.get_all_responses(href)
        return

    async def get_all_responses_by_page(self, page):
        sujet_container = page.locator('ul[data-load-more-content]')

        #TODO : récupération de chaque réponses + save response
        return

    async def get_all_responses(self, url: str):
        new_page: Any = await self.browser.new_page()
        await new_page.goto(url)

        await self.save_sujet(new_page)

        await self.get_all_responses_by_page(new_page)

        #TODO : véfifier le nombre de page de réponses + get all response par page


        return

    async def save_sujet(self, page: Any) -> None :
        sujet_container: Any = page.locator("div .c-message")

        titre: str = page.locator("h1 .c-title").text_content()
        message: str = sujet_container.locator("p .c-message__text").text_content()
        auteur: str = sujet_container.locator(".c-profile-card__name").locator("button").text_content()

        source_time: list = sujet_container.locator(".c-source__time")

        date_string: str = source_time[0].text_content()
        heure_string: str = source_time[1].text_content()

        date: datetime = parse_french_date(date_string, heure_string)

        sujet: Sujet = Sujet(titre=titre, message=message, auteur=auteur, date=date)

        add_sujet(sujet)

        return None

    async def save_reponse(self):

        #TODO : enregistrer la reponse en base
        return None

    async def scarpe_forum(self, symbole_boursier: str):
        await self.run("https://www.boursorama.com/cours/" + symbole_boursier)
        await self.current_page.get_by_title("Forum").click()

        return


def parse_french_date(d_str, h_str):

    mois_fr = {
        "janv.": "01", "févr.": "02", "mars": "03", "avr.": "04",
        "mai": "05", "juin": "06", "juil.": "07", "août": "08",
        "sept.": "09", "oct.": "10", "nov.": "11", "déc.": "12"
    }

    parts = d_str.split()
    day = parts[0]
    month = mois_fr.get(parts[1], "01")
    year = parts[2]

    clean_string = f"{day}/{month}/{year} {h_str}"

    return datetime.strptime(clean_string, "%d/%m/%Y %H:%M")
