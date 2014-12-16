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

    def test_registers_success(self):
        self.selenium.get(self.live_server_url)
        self.selenium.find_element_by_xpath(
            '/html/body/div[3]/div/div[2]/ul[2]/li[2]/a').click()  # click_register
        time.sleep(0.2)
        username_input = self.selenium.find_element_by_name('rUsername')
        print(username_input.is_displayed())
        username_input.send_keys('myuser')
        password_input = self.selenium.find_element_by_name('rPassword')
        password_input.send_keys('secret')
        confirm_input = self.selenium.find_element_by_name('rPassword2')
        confirm_input.send_keys('secret')
        email_input = self.selenium.find_element_by_name('rEmail')
        email_input.send_keys('secret@qq.com')
        name_input = self.selenium.find_element_by_name('rName')
        name_input.send_keys('secret')
        self.selenium.find_element_by_xpath(
            '/html/body/div[2]/div/div/div[3]/button[2]').click()  # register
        time.sleep(2)
        self.selenium.find_element_by_xpath(
            '/html/body/div[3]/div/div[2]/ul[2]/li[2]/a').click()  # logout
        time.sleep(1)
        self.selenium.find_element_by_xpath(
            '/html/body/div[3]/div/div[2]/ul[2]/li[2]/a').click()  # click_register
        time.sleep(0.2)
        password_input = self.selenium.find_element_by_name('rPassword')
        password_input.send_keys('secret')
        confirm_input = self.selenium.find_element_by_name('rPassword2')
        confirm_input.send_keys('secret')
        self.selenium.find_element_by_xpath(
            '/html/body/div[2]/div/div/div[3]/button[2]').click()  # register
        username_input = self.selenium.find_element_by_name('rUsername')
        username_input.send_keys('11')
        self.selenium.find_element_by_xpath(
            '/html/body/div[2]/div/div/div[3]/button[2]').click()  # register
        time.sleep(2)
        self.selenium.find_element_by_xpath(
            '/html/body/div[3]/div/div[2]/ul[2]/li[2]/a').click()  # logout
        time.sleep(1)
        self.selenium.find_element_by_xpath(
            '/html/body/div[3]/div/div[2]/ul[2]/li/a').click()  # click_login
        time.sleep(0.2)
        username_input2 = self.selenium.find_element_by_xpath(
            '/html/body/div/div/div/div[2]/div/div[3]/input')
        username_input2.send_keys('myuser')
        password_input2 = self.selenium.find_element_by_xpath(
            '/html/body/div/div/div/div[2]/div[2]/div[3]/input')
        password_input2.send_keys('secret')
        self.selenium.find_element_by_xpath(
            '/html/body/div/div/div/div[3]/button[2]').click()  # login
