from TestAddigy.main import *
# from TestAddigy.info import *
# from selenium.webdriver import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait


class OnBoarding(unittest.TestCase):

    def setUpClass(self):
        self.driver = driver
        self.driver.get(landingPage)
        signin()

    def tearDownClass(self):
        getlogs()
        self.driver.close()
