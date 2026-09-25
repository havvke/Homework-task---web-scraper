from src.dto import Book
from dataclasses import asdict
from sys import exit
import json


class BookWriter:

    def __init__(self, filename: str):
        self._filename: str = filename


    def write(self, book: Book):
        """Main entrypoint for BookWriter"""
        new_book = asdict(book)

        if self._book_exists(new_book["upc"]):
            exit()

        self._write_book(new_book)


    # Internals -----------------------------------------------------------------------------------------------------


    def _write_book(self, book: dict):
        """Write book and a new line to file"""
        with open(self._filename, "a") as f:
            json.dump(book, f)
            f.write("\n")


    def _book_exists(self, upc: str) -> bool:
        """ Check if current upc exists in open file """
        try:
            with open(self._filename, "r") as f:
                for line in f:
                    data = json.loads(line)
                    if data["upc"] == upc:
                        return True
        except FileNotFoundError:
            pass
        return False