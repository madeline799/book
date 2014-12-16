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

    def test_login_failure(self):
        self.selenium.get(self.live_server_url)
        self.selenium.find_element_by_xpath(
            '/html/body/div[3]/div/div[2]/ul[2]/li/a').click()  # click_login
        time.sleep(0.2)
        self.selenium.find_element_by_xpath(
            '/html/body/div/div/div/div[3]/button[2]').click()  # click_submit
        username_input = self.selenium.find_element_by_xpath(
            '/html/body/div/div/div/div[2]/div/div[3]/input')  # input_username
        username_input.send_keys('myuser')
        password_input = self.selenium.find_element_by_xpath(
            '/html/body/div/div/div/div[2]/div[2]/div[3]/input')  # input_password
        password_input.send_keys('secret')
        self.selenium.find_element_by_xpath(
            '/html/body/div/div/div/div[3]/button[2]').click()  # click_submit
