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

    def test_rank_booking(self):
        self.selenium.get(self.live_server_url) #  front_page
        self.selenium.find_element_by_xpath('/html/body/div[5]/div/div/div/table/tbody/tr/td[2]/a').click() #  one_book
        time.sleep(1)
        self.selenium.find_element_by_xpath('/html/body/div[6]/div/div[3]/table/tbody/tr/td[5]/button').click()  # booking
        self.selenium.find_element_by_xpath('//*[@id="ording-button"]').click()  # confirm
        time.sleep(2)
        self.selenium.find_element_by_xpath(
            '/html/body/div[3]/div/div[2]/ul[3]/li[2]/a').click()  # click_register
        time.sleep(0.2)
        username_input = self.selenium.find_element_by_name('rUsername')  # input_username
        username_input.send_keys('myuser')
        password_input = self.selenium.find_element_by_name('rPassword')  # input_password
        password_input.send_keys('secret')
        confirm_input = self.selenium.find_element_by_name('rPassword2')  # input_confirm
        confirm_input.send_keys('secret')
        email_input = self.selenium.find_element_by_name('rEmail')  # input_email
        email_input.send_keys('secret@qq.com')
        name_input = self.selenium.find_element_by_name('rName')  # input_name
        name_input.send_keys('secret')
        self.selenium.find_element_by_xpath(
            '/html/body/div[2]/div/div/div[3]/button[2]').click()  # click_register
        time.sleep(2)
        self.selenium.find_element_by_xpath('/html/body/div[6]/div/div[3]/table/tbody/tr/td[5]/button').click()  # booking_first_book
        time.sleep(0.2)
        self.selenium.find_element_by_xpath('//*[@id="ording-button"]').click()  # confirm
        time.sleep(2)
        self.selenium.find_element_by_xpath('/html/body/div[6]/div/div[3]/table/tbody/tr[2]/td[5]/button').click()  # booking_second_book
        time.sleep(0.2)
        self.selenium.find_element_by_xpath('//*[@id="ording-button"]').click()  # confirm
        time.sleep(2)
        self.selenium.find_element_by_xpath('/html/body/div[6]/div/div[3]/table/tbody/tr/td[5]/button').click()  # booking_first_book
        time.sleep(0.2)
        self.selenium.find_element_by_xpath('//*[@id="ording-button"]').click()  # confirm
        self.selenium.find_element_by_xpath('/html/body/div[3]/div/div[2]/ul[3]/li[2]/a').click()  # logout
        time.sleep(0.1)
        self.selenium.find_element_by_xpath('/html/body/div[3]/div/div/a').click()  # go_to_frontpage
        self.selenium.find_element_by_xpath(
            '/html/body/div[3]/div/div[2]/ul[2]/li/a').click()
        time.sleep(0.2)
        self.selenium.find_element_by_xpath(
            '/html/body/div/div/div/div[3]/button[2]').click()  # login
        username_input = self.selenium.find_element_by_xpath(
            '/html/body/div/div/div/div[2]/div/div[3]/input')
        username_input.send_keys('bookmanager')
        password_input = self.selenium.find_element_by_xpath(
            '/html/body/div/div/div/div[2]/div[2]/div[3]/input')
        password_input.send_keys('admin')
        self.selenium.find_element_by_xpath(
            '/html/body/div/div/div/div[3]/button[2]').click()  # submit
        time.sleep(1.5)
        self.selenium.find_element_by_xpath(
            '/html/body/div[3]/div/div[2]/ul[2]/li/a').click()  # go_to_manage_page
        time.sleep(0.5)
        self.selenium.find_element_by_xpath(
            '/html/body/div[4]/div[2]/ul/li[3]/a').click()  # bookmanage
        time.sleep(0.2)
        chooseuser_input = self.selenium.find_element_by_xpath('//*[@id="find-user-input2"]')  # input_booking_user
        chooseuser_input.send_keys('myuser')
        self.selenium.find_element_by_xpath('//*[@id="magic2"]').click()  # confirm
        time.sleep(0.2)
        self.selenium.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[2]/div/div[3]/table/tbody/tr/td[6]/button').click()  # choose_booking_user
        time.sleep(0.1)
        choosebook_input = self.selenium.find_element_by_xpath('//*[@id="borrow-book-bid2"]')  # input_booking_book
        choosebook_input.send_keys('1')
        self.selenium.find_element_by_xpath('//*[@id="magic-borrow2"]').click()  # click_submit_book
        time.sleep(0.4)
        choosebook_input = self.selenium.find_element_by_xpath('//*[@id="borrow-book-bid2"]')  # input_booking_book_again
        choosebook_input.send_keys('2')
        self.selenium.find_element_by_xpath('//*[@id="magic-borrow2"]').click()  # click_submit_book
        time.sleep(0.4)
        choosebook_input = self.selenium.find_element_by_xpath('//*[@id="borrow-book-bid2"]')  # input_booking_book_again
        choosebook_input.send_keys('8')
        self.selenium.find_element_by_xpath('//*[@id="magic-borrow2"]').click()  # click_submit_book
        
