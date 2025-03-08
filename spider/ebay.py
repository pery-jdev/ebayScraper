from spider.parser import EbayParser
from spider.response import SpiderResponse


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

        products = self.parser.parse_products(soup=response)
        print(products)
