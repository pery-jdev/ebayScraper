import requests
import os

from typing import Any
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager
from urllib.parse import urlencode


from core.config import config as cfg
from services.spider.utils.selenium_page_loader import PageLoader


class SpiderResponse(object):
    def __init__(self):
        self.session: requests.Session = requests.Session()
        self.modes = ["selenium", "requests", "httpx"]

    def get_response(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, Any] = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        },
        use_session: bool = False,
        mode: str = "selenium",
    ) -> BeautifulSoup:
        if mode not in self.modes:
            raise ValueError(f"Mode {mode} is not supported. Choise from: {self.modes}")

        if mode == "requests":
            if use_session:
                res = self.session.get(url, params=params, headers=headers)
                print(f"Using session to request url: {res.url}")
            else:
                res = requests.get(url, params=params, headers=headers)
                print("Requesting url: %s" % (res.url))

            if res.status_code != 200:
                # looging error with response
                try:
                    os.makedirs(cfg.TEMP_DIR, exist_ok=True)
                except FileExistsError:
                    pass

                with open(cfg.TEMP_DIR / "error.html", "w") as f:
                    f.write(res.text)
                    f.close()
                raise Exception("Request failed with status code: %s" % res.status_code)
            else:
                if cfg.DEBUG:
                    with open(cfg.TEMP_DIR / "response.html", "w") as f:
                        f.write(res.text)
                        return BeautifulSoup(f.read(), "html.parser")

                return BeautifulSoup(res.text, "html.parser")
        elif mode == "selenium":
            # formatted url here

            try:
                url = f"{url}{urlencode(params)}"
            except:
                pass
            print(f"Requesting url use selenium: {url}")
            driver = webdriver.Chrome(
                service=ChromeService(
                    ChromeDriverManager(
                        cache_manager=DriverCacheManager(cfg.DRIVER_PATH)
                    ).install()
                )
            )
            try:
                driver.get(url)
                loader = PageLoader(driver)
                if loader.wait_for_page_load():
                    print("Page fully loaded")
                    # Perform actions on loaded page
                else:
                    print("Page load timeout")

                if cfg.DEBUG:
                    with open(cfg.TEMP_DIR / "response.html", "w+") as f:
                        f.write(driver.page_source)

                        return BeautifulSoup(f.read(), "html.parser")
            except Exception as e:
                print(e)
                raise

            return BeautifulSoup(driver.page_source, "html.parser")
