# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver

class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['www.linkedin.com']
    start_urls = ['http://www.linkedin.com/']

    def parse(self, response):

        driver = webdriver.Chrome('/home/tomas/Documents/scrapy/chromedriver')
        driver.get('https://www.linkedin.com')
        driver.find_element_by_name("session_key")

        user_name = driver.find_element_by_name("session_key")
        user_name.send_keys("foobaa@gmail.com")

        password = driver.find_element_by_name("session_password")
        password.send_keys('test')

        submit_button = driver.find_element_by_class_name("sign-in-form__submit-btn")
