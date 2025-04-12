from bs4 import BeautifulSoup
from services.spider.parser import EbayParser
from services.spider.response import SpiderResponse
from core.config import config as cfg


class EbaySpider(object):
    def __init__(self):
        self.base_url: list[str] = ["https://www.ebay.com.au/", "https://www.ebay.com"]
        self.response: SpiderResponse = SpiderResponse()
        self.parser: EbayParser = EbayParser()

    def get_products(self, query: str):
        response = self.response.get_response(
            url=f"{self.base_url[0]}sch/i.html?" ,
            params={
                "_nkw": query,
                "_sacat": 0,
                "_from": "R40",
                "_trksid": "p2334524.m570.l1313",
                "_odkw": "laptop",
                "_osacat": 0,
            }, mode="selenium",
        )
        # f = open(cfg.TEMP_DIR / "response.html", "r")
        # soup = BeautifulSoup(f.read(), "html.parser")

        products = self.parser.parse_products(soup=response)

        return products
    
    def get_product_details(self, url: str):
        # response = self.response.get_response(url=url, mode="selenium")
        f = open(cfg.TEMP_DIR / "response.html", "r")
        soup = BeautifulSoup(f.read(), "html.parser")
        product = self.parser.parse_product_details(soup=soup)
        return product
    
    def generate_products(self, query: str):
        products = self.get_products(query=query)
        return products