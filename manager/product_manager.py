from services.spider.ebay import EbaySpider
class EbayProductManager:
    def __init__(self):
        self.ebay_spider = EbaySpider()

    def get_products(self):
        # products = self.ebay_spider.get_product_details(url="https://www.ebay.com.au/itm/396276693896?_skw=lure+fishing&itmmeta=01JR0SA1V95H9PF6MJ3HCRF59Q&hash=item5c43ee7b88:g:OJ4AAOSwH8pnxwrZ&itmprp=enc%3AAQAKAAAA4FkggFvd1GGDu0w3yXCmi1d5CZW3WPA3N30fgZQvnvltFOvbkBFJv%2BSez4DTMylbx0wPpZpj01VVhXFGc%2B0Ziv8SZt8z%2BZkoRD65%2B9hfq0D0pFg7IowUplBonsgF%2BtKQdTfYrcwSClAl1nAHmcHlM3j9SSYrIiRKiO49Q%2FtjrqmoWuJvR2YErF09mqTsWdcpZ2CPzJpAiEDqZfYDbR02gFJ5O2VTMVYXS7T%2B%2BrPnBPf0kFTg6UvbBEevwvPUHJypYzofl3sUxXYRmeaOX0kpRmrB0dX6opmpBbMXRkKCIoOA%7Ctkp%3ABFBM-p2omcBl")
        # return products
        products = self.ebay_spider.generate_products(query="Fishing Lures")
        print(products)