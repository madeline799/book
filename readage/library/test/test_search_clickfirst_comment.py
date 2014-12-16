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

    def test_search_clickfirst_comment(self):
        self.selenium.get(self.live_server_url)  # front_page
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
            '/html/body/div[2]/div/div/div[3]/button[2]').click()  # click_register
        time.sleep(2)
        search_input = self.selenium.find_element_by_xpath(
            '/html/body/div[4]/form/div/div[2]/input')  # input_search
        search_input.send_keys('network')
        self.selenium.find_element_by_xpath(
            '/html/body/div[4]/form/div[2]/div[2]/button').click()  # click_search
        time.sleep(1)
        self.selenium.find_element_by_xpath(
            '/html/body/div[5]/div/div[2]/div/table/tbody/tr/td[2]/a'
            ).click()  # choose_book
        time.sleep(1)
        self.selenium.find_element_by_xpath('/html/body/div[8]/div/div[2]/div/div[2]/a').click() #  CommentLoadMore
        time.sleep(2)
        self.selenium.find_element_by_xpath(
            '/html/body/div[5]/div/div/button').click()  # findbug
        time.sleep(0.2)
        author_input = self.selenium.find_element_by_xpath(
            '/html/body/div[10]/div/div/div[2]/form/div/div/input')
        author_input.send_keys('hehe')
        self.selenium.find_element_by_xpath(
            '/html/body/div[10]/div/div/div[3]/button').click()  # close
        time.sleep(1)
        self.selenium.find_element_by_xpath(
            '/html/body/div[8]/div/div/button').click()  # add_comment
        time.sleep(0.2)
        self.selenium.find_element_by_xpath(
            '//*[@id="makemycomment-submit"]').click()  # click_submit
        self.selenium.find_element_by_xpath(
            '//*[@id="isSpoiler"]').click()  # select_jutou
        time.sleep(0.2)
        title_input = self.selenium.find_element_by_xpath(
            '//*[@id="input-comment-title"]')  # input_title
        title_input.send_keys('AoWu')
        self.selenium.find_element_by_xpath('//*[@id="inlineRadio5"]').click()  #score
        comment_input = self.selenium.find_element_by_xpath(
            '//*[@id="input-comment"]')  # input_comment
        comment_input.send_keys('bilibili')
        self.selenium.find_element_by_xpath(
            '//*[@id="makemycomment-submit"]').click()  # submit
        time.sleep(1)
