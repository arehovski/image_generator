import time
import random
import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from image_scraper.items import ImageScraperItem


class GoogleSpider(scrapy.Spider):
    name = 'google'
    start_urls = ['https://google.com']

    def __init__(self, search_text, **kwargs):
        super().__init__(**kwargs)
        self.search_text = search_text
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        driver.get('https://google.com')
        form = driver.find_element_by_xpath("//input[@title='Поиск']")
        form.send_keys(search_text)
        form.send_keys(Keys.ENTER)
        driver.find_element_by_xpath("//a[@class='hide-focus-ring'][1]").click()
        time.sleep(2)
        # self._scroll_down(driver)
        page = driver.page_source
        self.response = Selector(text=page)
        driver.close()

    def parse(self, response, **kwargs):
        yield ImageScraperItem(folder=self.search_text, image_urls=self.response.xpath(
            "//img[contains(@alt, 'Картинки')]"))

    def _scroll_down(self, driver):
        last_height = driver.execute_script("return document.documentElement.scrollHeight")

        while True:
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(random.uniform(2, 3.1))
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                if driver.find_element_by_xpath('//input[@jsaction]').is_displayed():
                    driver.find_element_by_xpath('//input[@jsaction]').click()
                    self._scroll_down(driver)
                break
            last_height = new_height
