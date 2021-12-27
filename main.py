"""Crawls all book from http://books.toscrape.com/ and stores their informations in csv files and their pictures."""
import os

import requests

from requests import get

from bs4 import BeautifulSoup

import csv

import re

import scrape 


def main() :
    """Main function that coordinates the whole crawling task"""

    print("\n\n" +"WELCOME TO BOOKS To SCRAPE"+ "\n\n")

    url = "http://books.toscrape.com/"
    path = "BooksToScrape"
    
    os.makedirs(path, exist_ok=True)
    categories_urls = scrape.get_categories_urls(url)
    for category_url in categories_urls :
        scrape.get_file(path, category_url)

    print("Crawling done !")

if __name__ == "__main__" :
    main()



