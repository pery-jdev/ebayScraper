from selenium.webdriver import ChromeOptions, FirefoxOptions, EdgeOptions

class SeleniumOptions(object):
    def __init__(self):  
        self.chrome_options = ChromeOptions()
        self.firefox_options = FirefoxOptions()
        self.edge_options = EdgeOptions()

    def get_chrome_options(self):
        options = self.chrome_options
        options.add_argument('--no-sandbox')
        options.page_load_strategy = 'eager'
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--enable-logging")
        options.add_argument("--v=1")
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        return options
    
    def get_firefox_options(self):
        options = self.firefox_options
        return options
    
    def get_edge_options(self):
        options = self.edge_options
        return options