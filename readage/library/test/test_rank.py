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

    def test_rank(self):
        self.selenium.get(self.live_server_url)
        self.selenium.find_element_by_xpath('/html/body/div[3]/div/div[2]/ul/li[2]/a').click()  # click_head_rank
        time.sleep(1)
        self.selenium.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/ul/li[2]/a').click()  # click_comment_rank
        self.selenium.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/ul/li/a').click()  # click_borrow_rank
        time.sleep(0.2)
        self.selenium.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div/div/div/div/div/h4/a').click()  # click_one_book
        time.sleep(0.2)
        self.selenium.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/a').click() #  detail_book_information
