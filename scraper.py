import requests
import pandas as pd
from bs4 import BeautifulSoup
import json

# https://heynode.com/tutorial/create-packagejson-file
# how to cerate a package.json

websiteName = "https://www.apple.com"

# parses the website name you parametarize...


def getSoup(websiteName):
    websiteName = websiteName
    applePage = requests.get(websiteName)
    soup = BeautifulSoup(applePage.content, 'html.parser')
    return soup

# in this case will find a specific tag and make it into an href array
# and into a name array for each one
# this href is the reference to either the product type or the product itself


def findItems(Container, lim="null"):
    if lim == "null":
        productsContainer = Container.find_all('li')
    else:
        productsContainer = Container.find_all('li', limit=lim)
    name = [product.find('a').find('span').get_text()
            for product in productsContainer]

    ref = [link.find('a').get('href')
           for link in productsContainer]

    return {"name": name, "ref": ref}

# this function will return all the text contained inside of the page we are looking for


def getText(Container):
    return Container.get_text("|", strip=True)


Container = getSoup(websiteName).find(class_='ac-gn-list')
responce = findItems(Container, 7)
responce["ref"].remove("/")
responce["name"].remove("Apple")

product_class = responce["name"]

# this array will contain a json strings of each type of product along with each of their descriptions,
# all of the products are inside an array for each product type
prod = []
hashprod = dict()

# for name in responce["name"]:
#     hashprod[name] = {}


print("------------------")


# this for loop will looop through each href for the type of product
index = 0
for res in responce["ref"]:
    prodType = res[1:len(res)-1]
    hashprod[prodType] = {}

    prodTy = []

    NewWebName = websiteName+res

    Container = getSoup(NewWebName).find(class_='chapternav-items')
    responce = findItems(Container)
    product_type = responce["name"]

    # for prodType in product_type:
    #     hashprod[]
    # print(product_type)

    for res2 in responce["ref"]:
        prodName = res2[1:len(res2)-1]
        hashprod[prodType][prodName] = []

        prodDes = []
        Container = getSoup(NewWebName).find(class_='main')
        responce = getText(Container)
        hashprod[prodType][prodName] = responce
        prodDes = responce
        prodTy.append(prodDes)

    prod.append(json.dumps(prodTy))
index = index+1
print("-------------")


apple_product_info = pd.DataFrame({
    'product_class': hashprod,

})
print(apple_product_info)
