from bs4 import BeautifulSoup
import re
from src.dto import Book

class Parser:

    def __init__(self, html: str):
        self._html: str = html
        self._soup: BeautifulSoup | None = None


    def parse(self) -> Book | None:
        """Main entrypoint for parser"""
        is_success = self._load_to_bs4()
        if not is_success or not self._soup:
            return None

        book = Book(
            title=self._parse_title(),
            price=self._parse_price(),
            tax=self._parse_tax(),
            availability=self._parse_availability(),
            upc=self._parse_upc(),
        )
        if book.is_valid():
            return book
        return None


    # Internals -------------------------------------------------------------------------------------------------------

    def _parse_title(self) -> str | None:
        """Parses title and returns a string"""
        return self._parse_string("div.product_main > h1")


    def _parse_price(self) -> tuple[float, str] | None:
        """Parses price and returns a tuple where a first element is the price and the second is a currency symbol"""
        return self._parse_amount(".table > tr:nth-child(3) > td")


    def _parse_tax(self) -> tuple[float, str] | None:
        """Parses tax and returns a tuple where a first element is the tax and the second is a currency symbol"""
        return self._parse_amount(".table > tr:nth-child(5) > td")


    def _parse_availability(self) -> int | None:
        """Parses availability and returns an int"""
        return self._parse_int(".table > tr:nth-child(6) > td")


    def _parse_upc(self) -> str | None:
        """Parses UPC and returns a string"""
        return self._parse_string(".table > tr:nth-child(1) > td")


    # General methods------------------------------------------------------------------------------------------------

    def _parse_string(self, css_selector: str) -> str | None:
        """Takes as argument a CSS selector path as string, parses and returns a single string"""
        str_object = self._soup.select_one(css_selector)
        if str_object is None:
            print(f"Error occurred while parsing, selector did not match any objects")
            return None
        return str_object.text.strip()


    def _parse_amount(self, css_selector: str) -> tuple[float, str] | None:
        """Takes as argument a CSS selector path as string, parses and returns a float and currency symbol as string"""
        amount_object = self._soup.select_one(css_selector)
        if amount_object is None:
            print(f"Error occurred while parsing, selector did not match any objects")
            return None

        amount_text = amount_object.text.strip()

        # Regex breakdown:
        # (^[^0-9.]+) -> Group 1: Matches any non-numeric characters at the start (e.g., '£')
        # ([0-9.]+)   -> Group 2: Matches the numeric price digits and the decimal point (e.g., '51.77')
        match = re.match(r"(^[^0-9.]+)?([0-9.]+)", amount_text)
        # This Regex could be improved more

        if match and match.group(1) and match.group(2):
            currency_symbol = match.group(1)
            amount_value = float(match.group(2))
            return amount_value, currency_symbol
        return None


    def _parse_int(self, css_selector: str) -> int | None:
        """Takes as argument a CSS selector path as string, parses and returns an int"""
        availability_object = self._soup.select_one(css_selector)
        if availability_object is None:
            print(f"Error occurred while parsing, selector did not match any objects")
            return None

        availability_text = availability_object.text.strip()
        match = re.search(r"\d+", availability_text)
        return int(match.group()) if match else None


    def _load_to_bs4(self) -> bool:
        """Loads HTML to a BeautifulSoup object, returns True if successful"""
        try:
            self._soup = BeautifulSoup(self._html, "html.parser")
            return True
        except Exception as e:
            print(f"Error occurred while parsing - {e}")
            return False

