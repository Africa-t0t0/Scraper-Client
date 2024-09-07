import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

CHROMEDRIVER_PATH = os.getenv("PATH_TO_CHROMEDRIVER", None)

class Scraper(object):
    _chrome_driver_path = None
    _service = None
    _chrome_options = None
    _driver = None
    _url = None

    def __init__(self):
        self._chrome_driver_path = CHROMEDRIVER_PATH

    def _set_chrome_options(self) -> None:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self._chrome_options = chrome_options

    def _set_service(self) -> None:
        service = Service(self._chrome_driver_path)
        self._service = service

    def _set_driver(self) -> None:
        self._driver = webdriver.Chrome(service=self._service, options=self._chrome_options)

    def _set_url(self, url: str) -> None:
        self._url = url

    def _get_service(self) -> Service:
        if self._service is None:
            self._set_service()
        return self._service

    def _get_chrome_options(self) -> Options:
        if self._chrome_options is None:
            self._set_chrome_options()
        return self._chrome_options

    def _get_driver(self) -> webdriver.Chrome:
        if self._driver is None:
            self._get_service()
            self._get_chrome_options()
            self._set_driver()
        return self._driver

    def _get_url(self) -> str:
        return self._url

    def _get_page_title(self, url: str) -> str:
        driver = self._get_driver()
        driver.get(url)
        page_title = driver.title
        return page_title

    def scrap_full_site(self, url):
        driver = self._get_driver()
        driver.get(url)
        page_source = driver.page_source
        return page_source

    def find_word(self, url: str, word: str):
        full_site = self.scrap_full_site(url=url)
        if word.lower() in full_site.lower():
            print("word found!")
        else:
            print("word not found")

    def scrap_site(self, url: str):
        driver = self._get_driver()
        driver.get(url)
        page_source = driver.page_source

