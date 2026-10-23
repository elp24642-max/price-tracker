import argparse

from report import find_changes, load_history, save_history, write_excel
from scraper import fetch_books


def main():
    parser = argparse.ArgumentParser(description="Парсер цен books.toscrape.com в Excel")
    parser.add_argument("--pages", type=int, default=3, help="сколько страниц каталога (по 20 книг)")
    parser.add_argument("--output", default="prices.xlsx", help="имя Excel-файла")
    args = parser.parse_args()

    books = fetch_books(args.pages)
    changes = find_changes(books, load_history())
    write_excel(books, changes, args.output)
    save_history(books)

    print(f"Собрано книг: {len(books)}. Изменилась цена у: {len(changes)}. Файл: {args.output}")


if __name__ == "__main__":
    main()
