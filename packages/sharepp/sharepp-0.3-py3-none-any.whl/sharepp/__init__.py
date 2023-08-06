"""SharePriceProvider is a small application that provides the current price in EUR for a given ISIN."""
import requests
from bs4 import BeautifulSoup

LANG_UND_SCHWARZ_URL = "https://www.ls-tc.de/de/etf/"


def parse_price(isin):
    if isinstance(isin, str):
        response = requests.get(LANG_UND_SCHWARZ_URL + isin)
        parsed_html = BeautifulSoup(response.text, "html.parser")
        price_span = parsed_html.find("div", class_="mono").find("span")
        price_string = price_span.text.replace(".", "").replace(",", ".")
        return float(price_string)
    else:
        raise ValueError("You must provide a string object representing a valid ISIN!")
