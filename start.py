from flask import Flask
from flask import render_template

from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

PATH = r"C:\Users\huari\Documents\Projects\flaskTest\chromedriver.exe"

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>YES</p>"
@app.route("/main-test")
def testing():
    return "<h1>TESTING</h1>"

@app.route("/nike-test")
def nike():
    sample_shoes = ["https://www.nike.com/ca/t/air-zoom-alphafly-next-flyknit-road-racing-shoe-xDM1Lj/DJ5455-100"]
    master_result = all_shoes(sample_shoes)
    return render_template("index.html", item = master_result[0], price = master_result[1], colour = master_result[2], sizes = master_result[3:len(master_result)])

def find_shoe(web_address):
    # list of a shoe's info by price, color, size
    final_shoeINFO = []

    # web drivers
    driver = webdriver.Chrome(PATH)
    driver.get(web_address)

    # selenium HTML 
    ind_shoes_page_source = driver.page_source
    ind_shoes_soup = BeautifulSoup(ind_shoes_page_source, 'lxml')

    # find shoe name
    shoes_nameINFO = ind_shoes_soup.find('h1', id = 'pdp_product_title')
    final_shoeINFO.append(shoes_nameINFO.text.strip())

    # find shoe price
    shoes_priceINFO = ind_shoes_soup.find('div', class_ = 'product-price css-11s12ax is--current-price')
    alternate_priceINFO = ind_shoes_soup.find('div', class_ = 'product-price is--current-price css-s56yt7')
    if (shoes_priceINFO):
        final_shoeINFO.append(shoes_priceINFO.text.strip())
    elif (alternate_priceINFO):
        final_shoeINFO.append(alternate_priceINFO.text.strip())

    # find shoe colors
    shoes_colorsINFO = ind_shoes_soup.find('li', class_ = 'description-preview__color-description ncss-li')
    if (shoes_colorsINFO):
        final_shoeINFO.append(shoes_colorsINFO.text.strip())

    # find shoe sizes
    shoes_sizesINFO = ind_shoes_soup.find_all('fieldset', class_ = 'mt5-sm mb3-sm body-2 css-1pj6y87')
    for available_sizes in shoes_sizesINFO:
        shoes_avail = available_sizes.find_all('div')
        for avail in shoes_avail:
            instock_sizes_checker = avail.select('input:disabled')
            if (not instock_sizes_checker):
                instock_size = avail.find('label') 
                if (instock_size):
                    final_shoeINFO.append(instock_size.text.strip())

    return final_shoeINFO    

def all_shoes(web_address_list):
    for web_address in web_address_list:
        result = find_shoe(web_address)
        print(result)
        return result
    


