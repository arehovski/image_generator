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
        self.driver = webdriver.Chrome(options=options)
        self.driver.get('https://google.com')
        form = self.driver.find_element_by_xpath("//input[@title='Поиск']")
        form.send_keys(search_text)
        form.send_keys(Keys.ENTER)
        self.driver.find_element_by_xpath("//a[@class='hide-focus-ring'][1]").click()
        time.sleep(2)
        self._scroll_down(self.driver)

    def parse(self, response, **kwargs):
        image_thumbnails = self.driver.find_elements_by_xpath(
            "//img[contains(@class,'Q4LuWd')]")
        for img_thumb in image_thumbnails:
            try:
                img_thumb.click()
                time.sleep(0.3)
            except Exception:
                continue
            full_images = self.driver.find_elements_by_xpath("//img[contains(@class,'n3VNCb')]")
            for image in full_images:
                source = image.get_attribute('src')
                if source and 'http' in source:
                    yield ImageScraperItem(folder=self.search_text, image_urls=[source])
        self.driver.close()

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
