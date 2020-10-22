import requests, os, time#, sqlite3
from bs4 import BeautifulSoup
#from sqlite3 import Error

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

#connection = None
#global db_connection_status
#
#try:
#    connection = sqlite3.connect("database.db")
#    db_connection_status = True
#except Error as e:
#    db_connection_status = False

def clear():
    clear = lambda: os.system('cls')
    clear()

def setupCheck():
    setup_file = open("setup.txt", "r")
    setup_status = setup_file.read()
    setup_file.close()
    return setup_status

def setup(
    #c
    ):
    setup_file = open("setup.txt", "w")
    setup_file.write("yes")
    setup_file.close()
    #c.execute("""CREATE TABLE products (
    #             name text,
    #             price float
    #             )""")
    #connection.commit()

def title():
    print("Amazon Price Checker")
    print(
        #"Database Connected: ",db_connection_status,
        "\n")

def productLookup(HEADERS):
    clear()
    title()
    URL = input("Amazon URL: ")
    page = requests.get(URL,headers=HEADERS)
    soup = BeautifulSoup(page.content,"lxml")

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
                name = str(name[0])
            except:
                pass

    try:
        price = soup.find(id='priceblock_ourprice').get_text()
    except:
        try:
            price = soup.find(id='priceblock_dealprice').get_text()
        except:
            try:
                price = soup.find(class_="a-size-medium a-color-price offer-price a-text-normal").get_text()
            except:
                pass

    return name, price 

#def newTrack(HEADERS,c):
#    clear()
#    title()
#    name, price = productLookup(HEADERS)
#
#    c.execute("INSERT INTO products (name,price) values (?,?)",(name,price))
#
#    return c


def main(HEADERS
    #,c
    ):
    clear()
    title()
    print("A) Price Lookup (from URL)")
    #print("B) Start Tracking Product (from URL)")
    print("\n")
    mode = input("Mode Select: ")
    mode = mode.upper()
    if mode == "A":
        name, price = productLookup(HEADERS)
        clear()
        title()
        print("Product:\t",name)
        print("Price:\t\t",price)
        time.sleep(2)
    #elif mode == "B":
        #c = newTrack(HEADERS,c)
    else:
        clear()
        print("Invalid Mode Selection")
        time.sleep(2)

while True:
    setup_check = setupCheck()
    #c = connection.cursor()
    if setup_check == "yes":
        pass
    elif setup_check == "":
        setup(
            #c
            )
    main(HEADERS,
        #c
        )
    #connection.commit