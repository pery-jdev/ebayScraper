from services.pricing.alphavantage_converter import AlphaVantageConverter
from services.spider.xe import XeSpider


def main():
    # alpha = AlphaVantageConverter()
    xe_spider = XeSpider()
    # rates = alpha.get_rates()
    # print(rates)

    rates = xe_spider.scrape_rate(10, "USD", "JPY", )
    print(rates)


if __name__ == "__main__":
    main()
