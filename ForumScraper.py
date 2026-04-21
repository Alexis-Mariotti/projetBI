from datetime import datetime
from typing import Any

from playwright.async_api import Playwright

import Scraper
from db.database_repository import add_sujet, add_reponse, get_action_by_symbole_boursier
from models import Sujet, Reponse, Action


class ForumScraper (Scraper.Scraper):
    def __init__(self, playwright: Playwright, is_headless: bool = False):
        super().__init__(playwright, is_headless)

    async def get_all_sujets(self, symbole_boursier: str):

        #TODO : récupération de chaque page de sujet du forum
        return

    async def get_all_sujets_by_page(self, symbole_boursier: str):
        list_a: list = await self.current_page.get_by_title("Voir le sujet").all()
        for a in list_a:
            href: str = a.get_attribute("href")
            await self.get_all_responses(href, symbole_boursier)
        return

    async def get_all_responses_by_page(self, page: Any, sujet: Sujet):
        all_reponse_container = page.locator('ul[data-load-more-content]')
        reponses = all_reponse_container.locator('li').all()

        for reponse in reponses:
            await self.save_reponse(reponse, sujet)

        return

    async def get_all_responses(self, url: str, symbole_boursier: str):
        new_page: Any = await self.browser.new_page()
        await new_page.goto(url)

        sujet: Sujet = await self.save_sujet(new_page, symbole_boursier)

        div_main_page = new_page.locator("div .l-basic-page__main")

        await self.get_all_responses_by_page(new_page, sujet)

        pagination = div_main_page.locator("div .c-pagination")

        if pagination.count() > 0:
            page_suivante = pagination.get_by_role("link", name="Page suivante")
            if page_suivante > 0:
                while page_suivante > 0:
                    page_suivante.click()
                    await self.get_all_responses_by_page(new_page, sujet)
                    page_suivante = pagination.get_by_role("link", name="Page suivante")
            else:
                liste_page = pagination.get_by_role("link").all()
                liste_page.pop(0)

                for page in liste_page:
                    page.click()
                    await self.get_all_responses_by_page(new_page, sujet)
        return

    async def save_sujet(self, page: Any, symbole_boursier: str) -> Sujet :
        sujet_container: Any = page.locator("div .c-message")

        titre: str = page.locator("h1 .c-title").text_content()
        message: str = sujet_container.locator("p .c-message__text").text_content()
        auteur: str = sujet_container.locator(".c-profile-card__name").locator("button").text_content()

        source_time: list = sujet_container.locator(".c-source__time")

        date_string: str = source_time[0].text_content()
        heure_string: str = source_time[1].text_content()

        date: datetime = parse_french_date(date_string, heure_string)

        action: Action|None = get_action_by_symbole_boursier(symbole_boursier)
        action_id = None

        if action:
            action_id = action.id

        sujet: Sujet = Sujet(titre=titre, message=message, auteur=auteur, date=date, action=action_id)

        add_sujet(sujet)

        return sujet

    async def save_reponse(self, reponse_container: Any, sujet: Sujet) -> None:
        reponse_container: Any = reponse_container.locator("div .c-message")

        message: str = reponse_container.locator("p .c-message__text").text_content()
        auteur: str = reponse_container.locator(".c-profile-card__name").locator("button").text_content()

        source_time: list = reponse_container.locator(".c-source__time")

        date_string: str = source_time[0].text_content()
        heure_string: str = source_time[1].text_content()

        date: datetime = parse_french_date(date_string, heure_string)

        reponse: Reponse = Reponse(message=message, auteur=auteur, date=date, sujet=sujet.id)

        add_reponse(reponse)

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
