import pytest
from src.book_writer import BookWriter
from src.dto import Book
import json
from dataclasses import asdict

def test_book_writer(tmp_path):
    path = f"{tmp_path}/book_writer"

    book1 = Book(
        title="A Light in the Attic",
        price=(51.77, "£"),
        tax=(0, "£"),
        availability=22,
        upc="a897fe39b1053632"
    )
    book2 = Book(
        title="Tipping the Velvet",
        price=(53.74, "£"),
        tax=(0, "£"),
        availability=20,
        upc="90fa61229261140a"
    )

    writer = BookWriter(path)
    writer.write(book1)
    writer.write(book2)

    with open(path, "r") as file:
        lines = list(file)
        assert len(lines) == 2
        assert json.loads(lines[0]) == json.loads(json.dumps(asdict(book1)))
        assert json.loads(lines[1]) == json.loads(json.dumps(asdict(book2)))


def test_book_writer_rejects_duplicates(tmp_path):
    path = f"{tmp_path}/book_writer"
    book1 = Book(
        title="A Light in the Attic",
        price=(51.77, "£"),
        tax=(0, "£"),
        availability=22,
        upc="a897fe39b1053632"
    )
    writer = BookWriter(path)
    writer.write(book1)
    with pytest.raises(SystemExit):
        writer.write(book1)