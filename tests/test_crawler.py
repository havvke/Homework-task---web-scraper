from src.crawler import Crawler
import csv


def main():

    url = "https://books.toscrape.com/"
    crawler = Crawler(url)

    with open("links.csv", "w", newline="") as file:
        writer = csv.writer(file)
        for row in crawler.paginate():
            print(row)
            writer.writerow([row])

if __name__ == "__main__":
    main()