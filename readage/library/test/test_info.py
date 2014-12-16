from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
import time


class MySeleniumTests(LiveServerTestCase):
    fixtures = ['user-data.json']

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(MySeleniumTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(MySeleniumTests, cls).tearDownClass()

    def test_info(self):
        self.selenium.get(self.live_server_url)
        self.selenium.find_element_by_xpath(
            '/html/body/div[3]/div/div[2]/ul/li[3]/a').click()  # Info
        self.selenium.find_element_by_xpath(
            '/html/body/div[3]/div/div[2]/ul/li/a').click()  # Home
        self.selenium.find_element_by_xpath(
            '/html/body/div[5]/div/div[2]/div/table/tbody/tr/td[2]/a'
            ).click()  # Mark
        self.selenium.find_element_by_xpath(
            '/html/body/div[5]/div/div[2]/div/div/div/div/div/div/h4/a'
            ).click()  # Mark Nov.14
        self.selenium.find_element_by_xpath(
            '/html/body/div[5]/div/div[2]/div/ul/li[2]/a').click()  # UserGuide
        time.sleep(0.2)
        self.selenium.find_element_by_xpath(
            '/html/body/div[5]/div/div[2]/div/div/div[2]/div/div/div/h4/a'
            ).click()  # guide!
        self.selenium.find_element_by_xpath(
            '/html/body/div[3]/div/div/a').click()  # ReadTogether
