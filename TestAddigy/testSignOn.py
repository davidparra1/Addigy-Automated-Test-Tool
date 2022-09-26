from TestAddigy.main import *
# from TestAddigy.info import *
# from selenium.webdriver import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait


class SignOn(MainTestCase):

    def test_a_SignOn(self):
        self.assertEqual(mainPage, driver.current_url)

    def test_b_SignOut(self):
        if driver.current_url == landingPage:
            signin()
        signout()
        self.assertTrue(newSignInPage in driver.current_url or oldSignInPage in driver.current_url)
