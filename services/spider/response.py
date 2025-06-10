import logging
import requests
import httpx
import os
import time
import asyncio
from typing import Any
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager
from urllib.parse import urlencode
from core.config import config as cfg
from services.spider.utils.selenium_page_loader import PageLoader
from services.spider.utils.selenium_options import SeleniumOptions
from concurrent.futures import ThreadPoolExecutor


class SpiderResponse(object):
    def __init__(self):
        self.session: requests.Session = requests.Session()
        self.modes = ["selenium", "requests", "httpx"]
        self.options: SeleniumOptions = SeleniumOptions()
        self._executor = ThreadPoolExecutor(max_workers=10)

    async def get_response_async(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, Any] = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        },
        use_session: bool = False,
        mode: str = "httpx",
    ) -> BeautifulSoup:
        """Async version of get_response"""
        if mode not in self.modes:
            raise ValueError(f"Mode {mode} is not supported. Choose from: {self.modes}")

        if mode == "httpx":
            try:
                print(f"Requesting url use httpx: {url}")
                # Add 2 second delay before making request
                await asyncio.sleep(2)
                # Configure httpx client to follow redirects
                async with httpx.AsyncClient(follow_redirects=True) as client:
                    res = await client.get(url, params=params)
                    print(f"Requesting url use httpx: {res.url}")
            except Exception as e:
                print(e)
                raise

            if res.status_code != 200:
                # logging error with response
                try:
                    os.makedirs(cfg.TEMP_DIR, exist_ok=True)
                except FileExistsError:
                    pass

                with open(cfg.TEMP_DIR / "error.html", "w") as f:
                    f.write(res.text)
                    f.close()
                raise Exception(f"Request failed with status code: {res.status_code}")
            else:
                if cfg.DEBUG:
                    with open(cfg.TEMP_DIR / "response.html", "w") as f:
                        f.write(res.text)
                        return BeautifulSoup(f.read(), "html.parser")

                return BeautifulSoup(res.text, "html.parser")
        else:
            # For other modes, run in thread pool
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(
                self._executor,
                lambda: self.get_response(url, params, headers, use_session, mode)
            )

    def get_response(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, Any] = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        },
        use_session: bool = False,
        mode: str = "httpx",
    ) -> BeautifulSoup:
        """Original synchronous version of get_response"""
        if mode not in self.modes:
            raise ValueError(f"Mode {mode} is not supported. Choose from: {self.modes}")

        if mode == "requests":
            if use_session:
                res = self.session.get(url, params=params, headers=headers)
                print(f"Using session to request url: {res.url}")
            else:
                res = requests.get(url, params=params, headers=headers)
                print("Requesting url: %s" % (res.url))

            if res.status_code != 200:
                # logging error with response
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

        elif mode == "httpx":
            try:
                print(f"Requesting url use httpx: {url}")
                # Add 2 second delay before making request
                time.sleep(2)
                # Configure httpx client to follow redirects
                with httpx.Client(follow_redirects=True) as client:
                    res = client.get(url, params=params)
                    print(f"Requesting url use httpx: {res.url}")
            except Exception as e:
                print(e)
                raise

            if res.status_code != 200:
                # logging error with response
                try:
                    os.makedirs(cfg.TEMP_DIR, exist_ok=True)
                except FileExistsError:
                    pass

                with open(cfg.TEMP_DIR / "error.html", "w") as f:
                    f.write(res.text)
                    f.close()
                raise Exception(f"Request failed with status code: {res.status_code}")
            else:
                if cfg.DEBUG:
                    with open(cfg.TEMP_DIR / "response.html", "w") as f:
                        f.write(res.text)
                        return BeautifulSoup(f.read(), "html.parser")

                return BeautifulSoup(res.text, "html.parser")

        elif mode == "selenium":
            # formatted url here
            options = self.options.get_chrome_options()

            try:
                url = f"{url}{urlencode(params)}"
            except:
                pass
            print(f"Requesting url use selenium: {url}")
            driver = webdriver.Chrome(
                options=options,
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

    def __del__(self):
        """Cleanup thread pool on deletion"""
        self._executor.shutdown(wait=False)


class XeResponse(object):
    def __init__(self):
        self.session: requests.Session = requests.Session()

    def get_response(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, Any] = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        },
    ):
        try:
            response = self.session.get(
                url=url, params=params, headers=headers, timeout=10
            )
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except requests.exceptions.RequestException as e:
            logging.error(f"XE scraping failed: {str(e)}")
