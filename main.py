from services.pricing.alphavantage_converter import AlphaVantageConverter
from services.pricing.currency_converter import CurrencyConverter
from services.spider.xe import XeSpider


def main():
    # alpha = AlphaVantageConverter()
    # xe_spider = XeSpider()
    # rates = alpha.get_rates()
    # # print(rates)

    # # rates = xe_spider.scrape_rate(10, "USD", "JPY", )
    # print(rates)
    converter = CurrencyConverter()
    convert = converter.convert_currency("USD", "JPY", 10)
    print(convert)


if __name__ == "__main__":
    main()
