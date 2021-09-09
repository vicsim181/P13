# from applications import authentication
# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from django.db import models
# from selenium import webdriver
# from applications import authentication


# firefox_options = webdriver.FirefoxOptions()
# firefox_options.headless = False


# class UserStoriesTests(StaticLiveServerTestCase):
#     """
#     Serie of tests to simulate the actions of a user on the application.
#     """
#     fixtures = ['data_tests.json']

#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.browser = webdriver.Firefox(options=firefox_options)
#         cls.browser.implicitly_wait(10)
#         cls.browser.maximize_window()

#     @classmethod
#     def tearDownClass(cls):
#         super().tearDownClass()
#         cls.browser.quit()

#     def test_1_register_and_login_user(self):
#         """
#         User registers and logs in
#         """
#         self.browser.get('http://127.0.0.1:3000/')
#         self.browser.find_element_by_xpath('//*[@id="nav-collapse"]/ul/li[4]/a/b').click()
#         self.browser.find_element_by_xpath('//*[@id="__layout"]/div/div[1]/div[3]/a').click()
#         first_name_input = self.browser.find_element_by_xpath('//*[@id="input-3"]')
#         first_name_input.send_keys("Essai")
#         last_name_input = self.browser.find_element_by_xpath('//*[@id="input-4"]')
#         last_name_input.send_keys("TEST")
#         email_input = self.browser.find_element_by_xpath('//*[@id="input-1"]')
#         email_input.send_keys("essai@email.fr")
#         password_input = self.browser.find_element_by_xpath('//*[@id="input-2"]')
#         password_input.send_keys("sup€rP@ssw0rd")
#         self.browser.find_element_by_xpath('//*[@id="__layout"]/div/body/div/div[2]/form/button[1]').click()
#         self.browser.find_element_by_xpath('//*[@id="nav-collapse"]/ul/li[4]/a/b').click()
#         email_login_input = self.browser.find_element_by_xpath('//*[@id="input-1"]')
#         email_login_input.send_keys('essai@email.fr')
#         password_login_input = self.browser.find_element_by_xpath('//*[@id="input-2"]')
#         password_login_input.send_keys('sup€rP@ssw0rd')
#         self.browser.find_element_by_xpath('//*[@id="__layout"]/div/div[1]/div[2]/form/button[1]').click()
#         self.browser.implicitly_wait(3)
#         print("assert 'MON COMPTE' in self.browser.page_source")
#         assert 'MON COMPTE' in self.browser.page_source
#         print('ASSERT DONE')

#     def test_2_login_participate_consultation(self):
#         """
#         User logs in and participates to a consultation
#         """
#         users = authentication.models.CustomUser.objects.all()
#         print(users)
#         self.browser.get('http://127.0.0.1:3000/')
#         self.browser.find_element_by_xpath('//*[@id="nav-collapse"]/ul/li[4]/a/b').click()
#         email_login_input = self.browser.find_element_by_xpath('//*[@id="input-1"]')
#         email_login_input.send_keys('dony@duck.us')
#         password_login_input = self.browser.find_element_by_xpath('//*[@id="input-2"]')
#         password_login_input.send_keys('blabla85')
#         self.browser.find_element_by_xpath('//*[@id="__layout"]/div/div[1]/div[2]/form/button[1]').click()
#         self.browser.implicitly_wait(2)
#         self.browser.find_element_by_xpath('//*[@id="nav-collapse"]/ul/li[1]/a/b').click()
#         self.browser.implicitly_wait(4)
#         project = self.browser.find_element_by_xpath('//*[@id="__layout"]/div/div[1]/div[3]/div/div/div/article/div/div/a').click()
#         self.browser.execute_script("arguments[0].setAttribute('style','display:none;');", project)
#         self.browser.implicitly_wait(2)
#         self.browser.find_element_by_xpath('//*[@id="form"]/div/div/button').click()
#         self.browser.find_element_by_xpath('//*[@id="__BVID__57"]').click()


# Problème pour faire fonctionner les tests dans un mode isolé de tests.
# Les requêtes envoyées par Selenium via le front vont impacter la base de données de développement et non une base test créée spécialement.
