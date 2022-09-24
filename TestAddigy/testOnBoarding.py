from TestAddigy.main import *
# from TestAddigy.info import *
# from selenium.webdriver import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait


def neworgenv():
    if env == '-dev':
        a = 'https://dev.addigy.com/signup'
        return a
    elif env == '-stage':
        a = 'https://stage.addigy.com/signup'
        return a
    elif env == '':
        a = 'https://prod.addigy.com/signup'
        return a
    else:
        print('ERROR: No environment selected!')


def onboard():
    print('Organization creation started. Please input the information below.\n')
    while True:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.ID, 'signup_firstname'))).clear()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.ID, 'signup_lastname'))).clear()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.ID, 'signup_email'))).clear()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.ID, 'signup_phone'))).clear()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.ID, 'signup_company'))).clear()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.ID, 'signup_firstname'))).send_keys(input("First Name?: "))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.ID, 'signup_lastname'))).send_keys(input("First Last?: "))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.ID, 'signup_email'))).send_keys(input("Business Email?: "))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.ID, 'signup_phone'))).send_keys(input("Business Phone?: "))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.ID, 'signup_company'))).send_keys(input("Company Name?: "))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@class='btn btn-primary btn-block btn-lg' and @type='submit']"))).click()
        try:
            WebDriverWait(driver, 10).until(EC.url_changes(driver.current_url))
            break
        except TimeoutException:
            print('Incorrect input. Please try again.\n')
            continue
    print('Organization created. Email sent.\n')


class OnBoarding(unittest.TestCase):

    def setUp(self):
        self.driver = driver
        self.driver.get(neworgenv())

    def test_OnBoarding(self):
        onboard()
        self.assertTrue('https://addigy.com/thank-you/' in driver.current_url)

    def tearDown(self):
        getlogs()
        self.driver.close()
