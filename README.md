# Book Scraper

An async web scraper that crawls books.toscrape.com, parses every book's detail
page and saves the results to a JSON file.

---

## How it works

1. `Crawler.paginate()` starts on the home page, collects every book link on the page, follows the
   "next" button and repeats until there are no more pages. It yields book URLs one by one.
2. `Crawler.request_html()` downloads all book pages concurrently with `asyncio.gather()` and yields
   their HTMLs.
3. `Parser.parse()` parses a given HTML and returns a Book dataclass (title, price, tax, availability, UPC).
   It returns None if any field could not be parsed.
4. `BookWriter.write()` appends the book as one JSON line to books.json. If a book with the same UPC is
   already in the file, the program stops (`sys.exit()`). This relies on the site having the books sorted from newest
   to oldest, so when the first duplicate is found, that means that everything from here is already saved and we can close the program.
5. `orchestrator.main()` ties the individual classes together.

## Running the app

Requires Python 3.11+.

Run these commands from the project root:
```bash
python -m venv .venv
pip install -r requirements.txt
python -m src.orchestrator
```

Results are written to `books.json` in the current working directory.

## Known issues and points to consider for improvement

1. `book_writer.py`, `write()` calls `sys.exit()` on a duplicate.

Instead of writer handling this case, an error could be raised and handled on an upper level. 

2. Consider updating method for duplicity checking

Currently the application works under assumption that the books in books.toscrape.com are sorted from newest to oldest.
Exits early if a duplicate is spotted.

3. Seperating HTTP response codes

All errors are treated the same. It's worth considering separating the errors and handling each type differently.

4. Duplicate functions/methods

Class methods `_load_to_bs4()` in `crawler.py` and `parser.py` are doing practically the same thing with minimal
difference. It is worth considering equalizing them and moving to a helper function module.

5. `parser.py` selectors depend on row position in the table.

Selectors could be improved. Currently works, since books.toscrape.com page and its HTMLs are tidy.
Other webpages could be written in a less orderly manner.

## Bonus tasks

### 1.1 Splitting the app

I would start by writing a .proto file. It would define a service for parsing data with a function like `ParseBook()`.
Request would send a raw HTML string and response would send a Book type object (as defined in dto.py)

Separation of concerns: Parser would be responsible for parsing the raw data and checking if any fields are missing.

I would also need to rethink duplicate book checking. Since currently `sys.exit()` gets called in `book_writer.py`,
that might be bad practice.