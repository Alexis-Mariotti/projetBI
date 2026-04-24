import re
from datetime import datetime
from typing import Any

from playwright.async_api import Playwright

import Scraper
from db.database_repository import add_sujet, add_reponse, get_action_by_symbole_boursier
from models import Sujet, Reponse, Action


class ForumScraper (Scraper.Scraper):
    def __init__(self, playwright: Playwright, is_headless: bool = False):
        super().__init__(playwright, is_headless)

    async def get_all_sujets(self, action_id: int):
        url_forum = self.current_page.url
        last_url_forum = await self.current_page.get_by_role("link", name="Dernière page").first.get_attribute("href")

        resultat = re.search(r"page-(\d+)", last_url_forum)

        if resultat:
            last_page_number = int(resultat.group(1))
        else:
            return None

        page_number = 1
        while page_number <= last_page_number:
            await self.current_page.goto(url_forum + "page-" + str(page_number))
            await self.get_all_sujets_by_page(action_id)
            page_number += 1

        return None

    async def get_all_sujets_by_page(self, action_id: int):
        list_a: list = await self.current_page.get_by_title("Voir le sujet").all()
        for a in list_a:
            href: str = await a.get_attribute("href")
            await self.get_all_responses(href, action_id)
        return

    async def get_all_responses_by_page(self, page: Any, sujet: Sujet):
        reponses = await page.locator('ul[data-load-more-content] > li').all()

        for reponse in reponses:
            await self.save_reponse(reponse, sujet)

        return

    async def get_all_responses(self, url: str, action_id: int):
        new_page: Any = await self.browser.new_page()

        if url.startswith("/"):
            url = "https://www.boursorama.com" + url

        await new_page.goto(url)

        await self.acceptBoursoramaCookies(new_page)

        sujet: Sujet = await self.save_sujet(new_page, action_id)

        div_main_page = new_page.locator("div.l-basic-page__main")

        await self.get_all_responses_by_page(new_page, sujet)

        pagination = div_main_page.locator("div.c-pagination").first

        if await pagination.count() > 0:
            page_suivante = pagination.get_by_role("link", name="Page suivante")
            if await page_suivante.count() > 0:
                while await page_suivante.count() > 0:
                    await page_suivante.click()
                    await self.get_all_responses_by_page(new_page, sujet)
                    div_main_page = new_page.locator("div.l-basic-page__main")
                    pagination = div_main_page.locator("div.c-pagination").first
                    page_suivante = pagination.get_by_role("link", name="Page suivante")
            else:
                liste_page = await pagination.get_by_role("link").all()
                liste_page.pop(0)

                for page in liste_page:
                    new_page_pagination: Any = await self.browser.new_page()
                    await self.acceptBoursoramaCookies(new_page_pagination)

                    url_pagination = await page.get_attribute("href")

                    if url_pagination.startswith("/"):
                        url_pagination = "https://www.boursorama.com" + url_pagination

                    await new_page_pagination.goto(url_pagination)
                    await self.get_all_responses_by_page(new_page_pagination, sujet)
                    await new_page_pagination.close()

        await new_page.close()

        return

    async def save_sujet(self, page: Any, action_id: int) -> Sujet :
        sujet_container: Any = page.locator("div.c-message").first

        titre_brut: str = await page.locator("h1.c-title").text_content()

        texte_locator = sujet_container.locator("p.c-message__text")

        lignes_brutes = await texte_locator.all_text_contents()
        message_brut = "\n".join(lignes_brutes)

        auteur_brut: str = await sujet_container.locator(".c-profile-card__name").first.locator("button").text_content()

        titre: str = titre_brut.strip() if titre_brut else ""
        message: str = message_brut.strip() if message_brut else ""
        auteur: str = auteur_brut.strip() if auteur_brut else ""

        source_time: Any = sujet_container.locator(".c-source__time")
        nb_date_elements = await source_time.count()

        if nb_date_elements == 1:
            date_string = ""
            heure_string = await source_time.nth(0).text_content()
        elif nb_date_elements >= 2:
            date_string = await source_time.nth(0).text_content()
            heure_string = await source_time.nth(1).text_content()
        else:
            date_string = ""
            heure_string = "00:00"

        date_string = date_string.strip() if date_string else ""
        heure_string = heure_string.strip() if heure_string else "00:00"

        date: datetime = parse_french_date(date_string, heure_string)

        sujet: Sujet = Sujet(titre=titre, message=message, auteur=auteur, date=date, action=action_id)

        add_sujet(sujet)

        return sujet

    async def save_reponse(self, reponse_container: Any, sujet: Sujet) -> None:
        reponse_container: Any = reponse_container.locator("div.c-message")

        texte_locator = reponse_container.locator("p.c-message__text")

        if await texte_locator.count() == 0:
            return None

        lignes_brutes = await texte_locator.all_text_contents()
        message_brut = "\n".join(lignes_brutes)

        auteur_brut: str = await reponse_container.locator(".c-profile-card__name").first.locator("button").text_content()

        message: str = message_brut.strip() if message_brut else ""
        auteur: str = auteur_brut.strip() if auteur_brut else ""

        source_time: Any = reponse_container.locator(".c-source__time")
        nb_date_elements = await source_time.count()

        if nb_date_elements == 1:
            date_string = ""
            heure_string = await source_time.nth(0).text_content()
        elif nb_date_elements >= 2:
            date_string = await source_time.nth(0).text_content()
            heure_string = await source_time.nth(1).text_content()
        else:
            date_string = ""
            heure_string = "00:00"

        date_string = date_string.strip() if date_string else ""
        heure_string = heure_string.strip() if heure_string else "00:00"

        date: datetime = parse_french_date(date_string, heure_string)

        reponse: Reponse = Reponse(message=message, auteur=auteur, date=date, sujet=sujet.id)

        add_reponse(reponse)

        return None

    async def scarpe_forum(self, symbole_boursier: str):
        await self.run("https://www.boursorama.com/cours/" + symbole_boursier)
        await self.acceptBoursoramaCookies()
        await self.current_page.get_by_role("navigation", name="Menu secondaire").get_by_title("Forum").click()

        action: Action | None = get_action_by_symbole_boursier(symbole_boursier)
        action_id = None

        if action:
            action_id = action.id

        await self.get_all_sujets(action_id)
        await self.close()
        return


def parse_french_date(d_str, h_str):
    now = datetime.now()

    if not d_str:
        clean_string = f"{now.day:02d}/{now.month:02d}/{now.year} {h_str}"
        return datetime.strptime(clean_string, "%d/%m/%Y %H:%M")

    mois_fr = {
        "janv.": "01", "févr.": "02", "mars": "03", "avr.": "04",
        "mai": "05", "juin": "06", "juil.": "07", "août": "08",
        "sept.": "09", "oct.": "10", "nov.": "11", "déc.": "12"
    }

    parts = d_str.split()

    if len(parts) >= 3:
        day = parts[0]
        month = mois_fr.get(parts[1], "01")
        year = parts[2]
        clean_string = f"{day}/{month}/{year} {h_str}"
    else:
        clean_string = f"{now.day:02d}/{now.month:02d}/{now.year} {h_str}"

    return datetime.strptime(clean_string, "%d/%m/%Y %H:%M")
