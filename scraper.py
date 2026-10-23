import re
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
HEADERS = {"User-Agent": "price-tracker-demo/1.0 (learning project)"}  # только латиница: HTTP-заголовки не принимают кириллицу
DELAY_SECONDS = 1  # пауза между запросами, чтобы не нагружать сайт


def parse_price(text):
    """'£51.77' -> 51.77. Берём число из строки, символ валюты не важен."""
    match = re.search(r"\d+(?:\.\d+)?", text)
    if not match:
        raise ValueError(f"Не нашёл цену в {text!r}")
    return float(match.group())


def parse_page(html, page_url):
    """Достаёт книги из HTML одной страницы каталога."""
    soup = BeautifulSoup(html, "html.parser")
    books = []
    for card in soup.select("article.product_pod"):
        link = card.select_one("h3 a")
        books.append(
            {
                # В тексте ссылки название обрезано ('A Light in the ...'), полное в title
                "title": link["title"],
                "price": parse_price(card.select_one("p.price_color").text),
                "in_stock": "in stock" in card.select_one("p.availability").text.lower(),
                "url": urljoin(page_url, link["href"]),
            }
        )
    return books


def fetch_books(pages):
    """Скачивает первые `pages` страниц каталога. Возвращает список книг."""
    books = []
    for number in range(1, pages + 1):
        url = BASE_URL.format(number)
        response = requests.get(url, headers=HEADERS, timeout=15)
        if response.status_code == 404:
            break  # страницы закончились
        response.raise_for_status()
        response.encoding = "utf-8"  # иначе символ £ портится
        books.extend(parse_page(response.text, url))
        time.sleep(DELAY_SECONDS)
    return books
