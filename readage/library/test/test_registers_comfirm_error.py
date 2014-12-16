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

    def test_registers_comfirm_error(self):
        self.selenium.get(self.live_server_url)
        self.selenium.find_element_by_xpath(
            '/html/body/div[3]/div/div[2]/ul[2]/li[2]/a').click()  # click_register
        time.sleep(0.2)
        username_input = self.selenium.find_element_by_name('rUsername')
        username_input.send_keys('myuser')
        self.selenium.find_element_by_xpath(
            '/html/body/div[2]/div/div/div[3]/button[2]').click()
        password_input = self.selenium.find_element_by_name('rPassword')
        password_input.send_keys('secret')
        email_input = self.selenium.find_element_by_name('rEmail')
        email_input.send_keys('secrets')
        self.selenium.find_element_by_xpath(
            '/html/body/div[2]/div/div/div[3]/button[2]').click()
        confirm_input = self.selenium.find_element_by_name('rPassword2')
        confirm_input.send_keys('secrets')
        email_input.send_keys('@qq.com')
        name_input = self.selenium.find_element_by_name('rName')
        name_input.send_keys('secret')
        self.selenium.find_element_by_xpath(
            '/html/body/div[2]/div/div/div[3]/button[2]').click()  # click_submit
