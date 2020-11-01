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
    print("Amazon Price Checker\n")


def productLookup(HEADERS, url):
    now = datetime.now()
    dt = now.strftime("%Y-%m-%d-%H-%M-%S")

    page = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(page.content, "lxml")

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
            except:
                name = "Name could not be parsed"

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
                    price = "Price could not be parsed"

    return name, price, dt


def startTracking(HEADERS):
    clear()
    title()
    url = input("Amazon URL: ")
    check = 0
    products = os.scandir("products/")
    for product in products:
        file = open("products/" + product.name, "r")
        lines = file.read().splitlines()
        firstline = lines[0]
        if url == firstline:
            check = 1
        else:
            pass
    if check == 1:
        clear()
        title()
        print("This product is already being tracked.")
        time.sleep(1)
        home(HEADERS)
    else:
        name, price, dt = productLookup(HEADERS, url)
        clear()
        title()
        name = input(name + "\n\n" + "Please choose a suitable name: ")
        name = name.replace("\\", "")
        name = name.replace("/", "")
        name = name.replace(":", "")
        name = name.replace("*", "")
        name = name.replace("?", "")
        name = name.replace("\"", "")
        name = name.replace("<", "")
        name = name.replace(">", "")
        name = name.replace("|", "")
        file = open("products/" + name + ".txt", "a")
        file.write(url + "\n" + dt + "-" + price + "\n")
        file.close()
        clear()
        title()
        print("\n" + name + " is now being tracked with a starting price of " + price)
        home(HEADERS)


def updatePrices(HEADERS):
    clear()
    title()
    print("Updating product prices, please wait (this may take a while depending on how many products you have saved and your internet speed.)")
    products = os.scandir("products/")
    for product in products:
        file = open(product, "r")
        lines = file.read().splitlines()
        url = lines[0]
        name, price, dt = productLookup(HEADERS, url)
        lastline = lines[-1]
        line = lastline.split("-")
        lastprice = line[6]
        if price != lastprice:
            file = open(product, "a")
            file.write(dt + "-" + price + "\n")
            file.close()
            price = price.replace("£", "")
            price = float(price)
            lastprice = lastprice.replace("£", "")
            lastprice = float(lastprice)
            name = product.name.split(".txt")
            name = name[0]
            if price < lastprice:
                pricechange = lastprice - price
                percentage = (pricechange / lastprice) * 100
                percentage = round(percentage)
                print(name, "has dropped from", lastprice, "to", price, "(", percentage, "%)")
            elif price > lastprice:
                pricechange = lastprice - price
                percentage = (pricechange / lastprice) * -100
                percentage = round(percentage)
                print(name, "has increased from", lastprice, "to", price, "(", percentage, "%)")
            input("\nPress [ENTER] to continue... ")
        else:
            pass


def showPrices(HEADERS):
    clear()
    title()
    print("Saved Price\tProduct\n")
    products = os.scandir("products/")
    for product in products:
        file = open(product)
        lines = file.read().splitlines()
        lastline = lines[-1]
        line = lastline.split("-")
        price = line[6]
        name = product.name.split(".txt")
        print(price + "\t\t" + name[0])
    input("\nPress [ENTER] to return to home... ")
    home(HEADERS)


def stopTracking(HEADERS):
    clear()
    title()
    print("Product ID\tProduct\n")
    num = 0
    names = []
    products = os.scandir("products/")
    for product in products:
        num = num + 1
        name = product.name.split(".txt")
        names.append(name[0])
        print(num, "\t\t", name[0])
    delete = int(input("\nEnter the number of a product to delete it: "))
    delete = delete - 1
    os.remove("products/" + names[delete] + ".txt")
    home(HEADERS)


def home(HEADERS):
    clear()
    title()
    print("A) Start Tracking a New Product")
    print("B) Update and Show Prices")
    print("C) Stop Tracking a Product")
    mode = input("\nChoose a Function: ")
    mode = mode.upper()
    if mode == "A":
        startTracking(HEADERS)
    elif mode == "B":
        updatePrices(HEADERS)
        showPrices(HEADERS)
    elif mode == "C":
        stopTracking(HEADERS)
    else:
        home(HEADERS)


def start(HEADERS):
    updatePrices(HEADERS)
    home(HEADERS)


start(HEADERS)
