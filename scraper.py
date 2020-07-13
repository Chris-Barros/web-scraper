import requests
import pandas as pd
from bs4 import BeautifulSoup
import json

# https://heynode.com/tutorial/create-packagejson-file
# how to cerate a package.json

websiteName = "https://www.apple.com"


def getSoup(websiteName):
    websiteName = websiteName
    applePage = requests.get(websiteName)
    soup = BeautifulSoup(applePage.content, 'html.parser')
    return soup


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


def getText(Container):
    return Container.get_text("|", strip=True)


Container = getSoup(websiteName).find(class_='ac-gn-list')
responce = findItems(Container, 7)
responce["ref"].remove("/")
responce["name"].remove("Apple")
product_class = responce["name"]
print(product_class)
prod = []
print(responce["ref"])
print("--------main page----------^^^")
for res in responce["ref"]:
    prodTy = []
    NewWebName = websiteName+res

    Container = getSoup(NewWebName).find(class_='chapternav-items')
    responce = findItems(Container)
    product_type = responce["name"]
    # print(product_type)
    for res2 in responce["ref"]:
        prodDes = []
        Container = getSoup(NewWebName).find(class_='main')
        responce = getText(Container)

        prodDes = responce
        prodTy.append(prodDes)

    prod.append(json.dumps(prodTy))

    print("-------------")


apple_product_info = pd.DataFrame({
    'product_class': product_class,
    'product_type': prod,
})
print(apple_product_info)
