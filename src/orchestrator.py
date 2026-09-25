from src.crawler import Crawler
from src.parser import Parser
from src.book_writer import BookWriter
import asyncio

async def main():
    domain_url = "https://books.toscrape.com/"
    filename = "books.json"

    crawler = Crawler(domain_url)
    writer = BookWriter(filename)

    urls = crawler.paginate()

    async for html in crawler.request_html(urls):
        parser = Parser(html)
        book = parser.parse()
        if book is not None:
            writer.write(book)


if __name__ == "__main__":
    asyncio.run(main())