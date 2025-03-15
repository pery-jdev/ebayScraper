from services.spider.ebay import EbaySpider
class ProductManager:
    def __init__(self):
        self.ebay_spider = EbaySpider()

    def get_products(self):
        products = self.ebay_spider.get_product_details(url="https://www.ebay.com.au/itm/334297884748?_skw=fishing+tackle&itmmeta=01JPC6BV5WVS041V4C7SC1K37M&hash=item4dd5b4e84c:g:fr8AAOSwcZxh6LVE&itmprp=enc%3AAQAKAAAA0FkggFvd1GGDu0w3yXCmi1cEtL%2FSUwtIyX9I5WDhXP25uUxZZR0mNH1sdMhBwq%2FxeQT2hcPQAyt3Ofb63wTFxnGJVBh7PdyqCTOm9Lxwom8F1LSYWTimYhBQopBuZfbJ0EuJUSwpgbz2TrEP4t%2BUGkqUYPeDsONHKw0qNaRr3z2EcAt5mihLcyN%2FHGM8jTcM2P0RdBP%2FGTjJ6KMT5oDiAeGVrPX88FqVdu%2BJFF8AcOsLLZV4muuPPph%2F10eeFDmN7rPss69u0KXWfD9c%2BySyekU%3D%7Ctkp%3ABlBMUJSzr4azZQ")
        print(products)
        return products