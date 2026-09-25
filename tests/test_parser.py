import pytest
from src.parser import Parser
from src.dto import Book
from dataclasses import asdict

def test_parser():

    with open("tests/book1.html", "r", encoding="utf-8") as file:
        html_string = file.read()

    z = Parser(html_string)
    book = z.parse()
    assert book is not None

    test_book = Book(
        title="A Light in the Attic",
        price=(51.77, "£"),
        tax=(0, "£"),
        availability=22,
        upc="a897fe39b1053632"
    )

    assert asdict(book) == asdict(test_book)
