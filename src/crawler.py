import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import AsyncIterator, AsyncIterable
import asyncio


class Crawler:

    def __init__(self, domain: str):
        self._domain: str = domain
        self._soup: BeautifulSoup | None = None


    async def paginate(self) -> AsyncIterator[str]:
        """Crawls books.toscrape.com page, yields strings of book urls, one by one"""
        current_page = self._domain
        async with aiohttp.ClientSession() as session:
            while current_page:
                if not self._load_to_bs4(await self._get_html(current_page, session)):
                    break
                book_links = self._find_books(current_page)
                for book_link in book_links:
                    yield book_link
                current_page = self._find_next(current_page)


    async def request_html(self, book_urls: AsyncIterable[str]) -> AsyncIterator[str]:
        """Retrieves and returns a list of HTMLs from a list of book urls"""
        coroutines = []
        async with aiohttp.ClientSession() as session:
            async for url in book_urls:
                coroutines.append(self._get_html(url, session))
            book_htmls = await asyncio.gather(*coroutines)
        for book_html in book_htmls:
            if book_html is not None:
                yield book_html


    # Internals -----------------------------------------------------------------------------------------------


    def _find_books(self, current_page: str) -> list[str]:
        """Finds and returns book urls as a list of strings"""
        book_links = self._soup.select("article.product_pod > h3 > a")
        full_links = list()
        for link in book_links:
            if not link.get("href"):
                continue
            full_links.append(
                urljoin(current_page, str(link.get("href")))
            )
        return full_links


    def _find_next(self, current_page: str) -> str | None:
        """Finds and returns next page link of books as a string"""
        next_page = self._soup.select_one(".next > a")
        return urljoin(current_page, str(next_page.get("href"))) if next_page else None


    @staticmethod
    async def _get_html(url: str, session: aiohttp.ClientSession) -> str | None:
        """Gets and returns HTML from url as a string"""
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                response.raise_for_status()
                return await response.text()
        except aiohttp.ClientError as e:
            print(f"Client Error: {e}")
            return None
    # Non-200 status codes, timeouts, connection errors, non-HTML content types (PDFs, images).


    def _load_to_bs4(self, html: str | None) -> bool:
        """Loads HTML to a BeautifulSoup object, returns True if successful"""
        if html is None:
            return False
        try:
            self._soup = BeautifulSoup(html, 'html.parser')
            return True
        except Exception as e:
            print(f"Error occurred while loading to bs4 - {e}")
            return False