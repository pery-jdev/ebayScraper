from typing import Any
from bs4 import BeautifulSoup

class EbayParser:
    def __init__(self):
        self.product_lists = []

    def parse_products(self, soup: BeautifulSoup):
        
        products_container = soup.find('ul', attrs={'class': 'srp-results srp-list clearfix'}).find_all('li', attrs={'class': 's-item'})
        for product in products_container:
            title = product.find('div', attrs={'class': 's-item__title'}).find('span', attrs={'role': 'heading'}).text.strip()
            price_with_discount = product.find('span', attrs={'class': 's-item__price'}).text.strip()
            logistic_cost = product.find('span', attrs={'class': 's-item__logisticsCost'}).text.strip()
            product_url = product.find('a', attrs={'class': 's-item__link'})['href']
            try:
                product_location = product.find('span', attrs={'class': 's-item__location'})
            except:
                product_location = None
            print(product_location)

            self.product_lists.append({
                'title': title,
                'price_with_discount': price_with_discount,
                'logistic_cost': logistic_cost,
                'product_url': product_url,
                'product_location': product_location,
            })

        return self.product_lists
    
    def parse_product_details(self, soup: BeautifulSoup):
        products: dict[str, Any] = {}
        product_image_lists: list[dict[str, str]] = []

        body = soup.find('div', attrs={'class': 'tabs__content'})
        
        # images
        images = soup.find('div', attrs={'data-testid': 'x-photos'}).find_all('button', attrs={'class': 'ux-image-grid-item'})
        for image in images:
            try:
                image_url = image.find('img')['src']
            except:
                image_url = image.find('img')['data-src']
                
            image_alt = image.find('img')['alt']
            if image_alt and image_url != None:
                product_image_lists.append({
                    'image_url': image_url,
                    'image_alt': image_alt
                })
            print(product_image_lists)
        product_sku = soup.find('div', attrs=['class', 'ux-layout-section__textual-display ux-layout-section__textual-display--itemId']).find('span', attrs={'class': 'ux-textspans ux-textspans--BOLD'}).text.strip()


        items = soup.find('div', attrs={'class': 'ux-layout-section-evo ux-layout-section--features'}).find_all('div',attrs={'class': 'ux-layout-section-evo__row'})
        for item in items:
            item_cols = item.find_all('div', attrs={'class':'ux-layout-section-evo__col'})
            for item_col in item_cols:
                item_col_label = item_col.find('dt', attrs={'class':'ux-labels-values__labels'})
                item_col_value = item_col.find('dd', attrs={'class':'ux-labels-values__values'})
                if item_col_label and item_col_value != None:
                    products[item_col_label.text.strip()] = item_col_value.text.strip()
            
            # print(item_label, item_value)
        return products
