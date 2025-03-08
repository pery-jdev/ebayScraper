

from spider.ebay import EbaySpider


def main():
    spider: EbaySpider = EbaySpider()
    spider.get_products("laptop")

if __name__ == "__main__":
    main()