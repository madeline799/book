from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
import time


class MySeleniumTests(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(MySeleniumTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(MySeleniumTests, cls).tearDownClass()

    def test_book_onboard_miss(self):
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
        self.selenium.find_element_by_xpath(
            '/html/body/div[4]/div[2]/ul/li[4]/a').click()  # click_onboard
        time.sleep(0.1)
        choosebook_input = self.selenium.find_element_by_xpath(
            '//*[@id="return-book-bid2"]')
        choosebook_input.send_keys('1')
        self.selenium.find_element_by_xpath(
            '//*[@id="magic-return2"]').click()  #click_submit
        time.sleep(0.1)
        choosebook_input = self.selenium.find_element_by_xpath(
            '//*[@id="return-book-bid2"]')
        choosebook_input.send_keys('3')
        self.selenium.find_element_by_xpath(
            '//*[@id="magic-return2"]').click()  #click_submit
        time.sleep(0.1)
        choosebook_input = self.selenium.find_element_by_xpath(
            '//*[@id="return-book-bid2"]')
        choosebook_input.send_keys('5')
        self.selenium.find_element_by_xpath(
            '//*[@id="magic-return2"]').click()  #click_submit
        time.sleep(0.1)
        choosebook_input = self.selenium.find_element_by_xpath(
            '//*[@id="return-book-bid2"]')
        choosebook_input.send_keys('6')
        self.selenium.find_element_by_xpath(
            '//*[@id="magic-return2"]').click()  #click_submit
        time.sleep(0.1)
        choosebook_input = self.selenium.find_element_by_xpath(
            '//*[@id="return-book-bid2"]')
        choosebook_input.send_keys('10')
        self.selenium.find_element_by_xpath(
            '//*[@id="magic-return2"]').click()  #click_submit
        time.sleep(0.1)
        self.selenium.find_element_by_xpath(
            '/html/body/div[4]/div[2]/ul/li[5]/a').click()  # click_bookmiss
        time.sleep(0.1)
        choosebook_input = self.selenium.find_element_by_xpath(
            '//*[@id="return-book-bid3"]')
        choosebook_input.send_keys('1')
        self.selenium.find_element_by_xpath(
            '//*[@id="magic-return3"]').click()  #click_submit
        time.sleep(0.1)
        choosebook_input = self.selenium.find_element_by_xpath(
            '//*[@id="return-book-bid3"]')
        choosebook_input.send_keys('3')
        self.selenium.find_element_by_xpath(
            '//*[@id="magic-return3"]').click()  #click_submit
        time.sleep(0.1)
        choosebook_input = self.selenium.find_element_by_xpath(
            '//*[@id="return-book-bid3"]')
        choosebook_input.send_keys('5')
        self.selenium.find_element_by_xpath(
            '//*[@id="magic-return3"]').click()  #click_submit
        time.sleep(0.1)
        choosebook_input = self.selenium.find_element_by_xpath(
            '//*[@id="return-book-bid3"]')
        choosebook_input.send_keys('6')
        self.selenium.find_element_by_xpath(
            '//*[@id="magic-return3"]').click()  #click_submit
        time.sleep(0.1)
        choosebook_input = self.selenium.find_element_by_xpath(
            '//*[@id="return-book-bid3"]')
        choosebook_input.send_keys('10')
        self.selenium.find_element_by_xpath(
            '//*[@id="magic-return3"]').click()  #click_submit
        time.sleep(0.1)
        
