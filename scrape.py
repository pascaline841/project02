import os

import requests
from requests import get

from bs4 import BeautifulSoup

import csv

import re


def get_categories_urls(url):
    """takes content of home page and returns a list  categories' urls"""
    categories_urls = []
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    li = soup.find(class_="nav nav-list").find("ul").find_all("li")
    for item in li:
        category_url = url + item.find("a", href=True).get("href").replace(
            "http", "https"
        )
        categories_urls.append(category_url)
    return categories_urls


def get_category_title(category_url):
    """parses the title of the category and returns it """
    page = requests.get(category_url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup.find(class_="page-header action").get_text().strip()


def get_category_folder(path, category_title):
    """creates a folder by category's name and return the path"""
    cat_path = os.path.join(path, category_title)
    os.makedirs(cat_path, exist_ok=True)
    return cat_path


def get_products_urls(category_url):
    """takes content of a category and return a list of products'url."""
    products_urls = []
    page = requests.get(category_url)
    soup = BeautifulSoup(page.content, "html.parser")
    book_div = soup.find_all(class_="product_pod")
    for container in book_div:
        product_page_url = "http://books.toscrape.com/catalogue/" + container.h3.a.get(
            "href"
        ).replace("../", "")
        products_urls.append(product_page_url)
    start_page, max_end_page = 2, 10
    for i in range(start_page, max_end_page):
        url = category_url.replace("index.html", f"page-{i}.html")
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        book_div = soup.find_all("article", class_="product_pod")
        for container in book_div:
            product_page_url = (
                "http://books.toscrape.com/catalogue/"
                + container.h3.a.get("href").replace("../", "")
            )
            products_urls.append(product_page_url)
    return products_urls


def get_products_details(category_url, cat_path, category_title):
    """takes content of a product's page, parses it and returns details about the product"""
    books = []
    products_urls = get_products_urls(category_url)
    for product_page_url in products_urls:
        book = {}
        page = requests.get(product_page_url)
        soup = BeautifulSoup(page.content, "html.parser")
        book["product_page_url"] = product_page_url
        title = soup.h1.string
        book["title"] = title
        td = soup.find(class_="table table-striped").find_all("td")
        book["universal_product_code"] = td[0].string
        book["price_including_tax"] = td[3].string
        book["price_excluding_tax"] = td[2].string
        s = td[5].string
        number_available = re.findall("(\d+?)\s", s)
        book["number_available"] = number_available[0]
        paragraph = soup.find_all("p")
        book["product_description"] = paragraph[3].string
        link = soup.find(class_="breadcrumb").find_all("a")
        book["category"] = link[2].string
        book["review_rating"] = len(
            soup.find(class_="col-sm-6 product_main").find_all(class_="icon-star")
        )
        image = soup.find("img")
        image_url = "https://books.toscrape.com" + image["src"].replace(
            "../..", ""
        ).replace("../../../..", "")
        book["image_url"] = image_url
        images = requests.get(image_url)
        cleaned_title = "".join(char for char in title if char.isalnum())
        with open(f"{cat_path}/{category_title}{cleaned_title}.jpg", "wb") as file:
            file.write(images.content)
        books.append(book)
    return books


def get_file(path, category_url):
    """stores the books' informations from the same category"""
    category_title = get_category_title(category_url)
    cat_path = get_category_folder(path, category_title)
    books = get_products_details(category_url, cat_path, category_title)
    with open(
        f"{cat_path}/{category_title}books.csv", "w", newline="", encoding="utf8"
    ) as csvfile:
        header = [
            "product_page_url",
            "universal_product_code",
            "title",
            "price_including_tax",
            "price_excluding_tax",
            "number_available",
            "product_description",
            "category",
            "review_rating",
            "image_url",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=header, delimiter=";")
        writer.writeheader()
        writer.writerows(books)
