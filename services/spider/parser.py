from bs4 import BeautifulSoup

from core.config import Config as cfg

class EbayParser:
    def __init__(self):
        pass

    def parse_products(self, soup: BeautifulSoup):
        
        products_container = soup.find('ul', attrs={'class': 'srp-results srp-list clearfix'}).find_all('li', attrs={'class': 's-item'})
        for product in products_container:
            title = product.find('div', attrs={'class': 's-item__title'}).text.strip()
            print(title)
        # print(products_container)