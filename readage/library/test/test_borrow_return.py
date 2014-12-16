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

    def test_borrow_return(self):
        self.selenium.get(self.live_server_url)  # open_front_page
        self.selenium.find_element_by_xpath(
            '/html/body/div[3]/div/div[2]/ul[2]/li/a').click()  # click_login
        time.sleep(0.2)
        username_input = self.selenium.find_element_by_xpath(
            '/html/body/div/div/div/div[2]/div/div[3]/input')  # username
        username_input.send_keys('bookmanager')
        password_input = self.selenium.find_element_by_xpath(
            '/html/body/div/div/div/div[2]/div[2]/div[3]/input')  # password
        password_input.send_keys('admin')
        self.selenium.find_element_by_xpath(
            '/html/body/div/div/div/div[3]/button[2]').click()  # click_finish
        time.sleep(0.2)
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/book/'))  # open_manager_page
        time.sleep(2)
        borrower_input = self.selenium.find_element_by_xpath('//*[@id="find-user-input"]')  # input_borrow_user
        borrower_input.send_keys('zhangjiao')
        self.selenium.find_element_by_xpath('//*[@id="magic"]').click()  # search
        time.sleep(0.2)
        self.selenium.find_element_by_xpath(
            '/html/body/div[4]/div[2]/div/div/div/div[3]/table/tbody/tr/td[6]/button').click()  # select_user
        time.sleep(0.1)
        borrowbook_input = self.selenium.find_element_by_xpath(
            '//*[@id="borrow-book-bid"]')  # input_borrow_book
        borrowbook_input.send_keys('5')
        self.selenium.find_element_by_xpath(
            '//*[@id="magic-borrow"]').click()  # click_borrow
        time.sleep(0.1)
        borrowbook_input = self.selenium.find_element_by_xpath(
            '//*[@id="borrow-book-bid"]')  # input_borrow_book
        borrowbook_input.send_keys('11')
        self.selenium.find_element_by_xpath(
            '//*[@id="magic-borrow"]').click()  # click_borrow
        time.sleep(0.1)
        borrowbook_input = self.selenium.find_element_by_xpath(
            '//*[@id="borrow-book-bid"]')
        borrowbook_input.send_keys('11')  # input_borrow_book
        self.selenium.find_element_by_xpath(
            '//*[@id="magic-borrow"]').click()  # click_borrow
        time.sleep(0.2)
        self.selenium.find_element_by_xpath('/html/body/div[4]/div[2]/ul/li[2]/a').click()  # click_return_book
        time.sleep(0.2)
        return_input = self.selenium.find_element_by_xpath('//*[@id="return-book-bid"]')  # input_return_book
        return_input.send_keys('11')
        self.selenium.find_element_by_xpath('//*[@id="magic-return"]').click()  # click_return
        time.sleep(0.2)
        return_input = self.selenium.find_element_by_xpath('//*[@id="return-book-bid"]')  # input_return_book
        return_input.send_keys('5')
        self.selenium.find_element_by_xpath('//*[@id="magic-return"]').click()  # click_return
        
