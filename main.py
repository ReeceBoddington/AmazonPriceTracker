import requests
import os
import time
from bs4 import BeautifulSoup
from datetime import datetime

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})


def clear():
    clear = lambda: os.system('cls')
    clear()


def title():
    print("Amazon Price Checker")
    print("\n")


def productLookup(HEADERS, URL):
    page = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(page.content, "lxml")

    name = "Name could not be found"
    price = "Price could not be found"

    try:
        name = soup.find(id='productTitle').get_Text()
    except:
        try:
            name = soup.find(class_="a-size-extra-large").get_Text()
        except:
            try:
                name = soup.find('title')
                name = name.string
                name = name.split(": Amazon",)
                name = name[0]
                name = name.replace("\\", "")
                name = name.replace("/", "")
                name = name.replace(":", "")
                name = name.replace("*", "")
                name = name.replace("?", "")
                name = name.replace("\"", "")
                name = name.replace("<", "")
                name = name.replace(">", "")
                name = name.replace("|", "")
            except:
                pass

    try:
        price = soup.find(id='priceblock_ourprice').get_text()
    except:
        try:
            price = soup.find(id='priceblock_dealprice').get_text()
        except:
            try:
                price = soup.find(id='priceblock_saleprice').get_text()
            except:
                try:
                    price = soup.find(class_="a-size-medium a-color-price offer-price a-text-normal").get_text()
                except:
                    pass

    url = str(URL)
    name = str(name)
    price = str(price)

    return url, name, price


def newTrack(url, name, price):
    now = datetime.now()
    dt = now.strftime("%Y-%m-%d-%H-%M-%S")
    if os.path.isfile("products/" + name + ".txt") == False:
        file = open("products/" + name + ".txt", "a")
        file.write(url + "\n")
        file.write(dt + "-" + price + "\n")
        file.close()
    else:
        updatePrice(name, price, dt)


def updatePrice(name, price, dt):
    file = open("products/" + name + ".txt", "r")
    lines = file.read().splitlines()
    lastline = lines[-1]
    line = lastline.split("-")
    lastprice = line[6]

    if price != lastprice:
        file = open("products/" + name + ".txt", "a")
        file.write(dt + "-" + price + "\n")
        file.close()
    else:
        pass

    return lastprice


def autoUpdate(HEADERS):
    now = datetime.now()
    dt = now.strftime("%Y-%m-%d-%H-%M-%S")
    products = os.scandir("products/")
    print("Previous Price\tCurrent Price\tProduct\n")
    for product in products:
        file = open(product)
        URL = file.readline()
        url, name, price = productLookup(HEADERS, URL)
        lastprice = updatePrice(name, price, dt)
        print(lastprice + "\t\t" + price + "\t\t" + name + "\n")
    time.sleep(2)


def main(HEADERS):
    clear()
    title()
    print("A) Price Lookup (from URL)")
    print("B) Start Price Tracking (from URL)")
    print("C) Update Prices (from saved)")
    print("\n")
    mode = input("Mode Select: ")
    mode = mode.upper()
    if mode == "A":
        clear()
        title()
        URL = input("Amazon URL: ")
        url, name, price = productLookup(HEADERS, URL)
        clear()
        title()
        print("Product:\t", name)
        print("Price:\t\t", price)
        time.sleep(2)
    elif mode == "B":
        clear()
        title()
        URL = input("Amazon URL: ")
        url, name, price = productLookup(HEADERS, URL)
        newTrack(url, name, price)
    elif mode == "C":
        clear()
        title()
        autoUpdate(HEADERS)
    else:
        clear()
        print("Invalid Mode Selection")
        time.sleep(2)


while True:
    main(HEADERS)
