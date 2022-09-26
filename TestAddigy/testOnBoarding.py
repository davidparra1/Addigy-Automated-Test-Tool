import secrets
import string

from selenium.common import InvalidArgumentException

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


def generatepassword():
    letter_choices = string.ascii_letters
    num_letters = secrets.choice(range(10, 15))  # between 10 and 14 letters
    password = [secrets.choice(letter_choices) for _ in range(num_letters)]

    symbol = secrets.choice("!@#$%^&*")
    password.insert(secrets.randbelow(len(password) + 1), symbol)

    digit = secrets.choice("0123456789")
    password.insert(secrets.randbelow(len(password) + 1), digit)

    return ''.join(password)


def signup():
    print('Organization creation started.\n')
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.ID, 'signup_firstname'))).send_keys('Automated')
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.ID, 'signup_lastname'))).send_keys('Test')
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.ID, 'signup_phone'))).send_keys('1112223333')
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.ID, 'signup_company'))).send_keys('Automated Test')
    while True:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.ID, 'signup_email'))).clear()
        a = input("Business Email?: ")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.ID, 'signup_email'))).send_keys(a)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@class='btn btn-primary btn-block btn-lg' and @type='submit']"))).click()
        try:
            WebDriverWait(driver, 10).until(EC.url_changes(driver.current_url))
            break
        except TimeoutException:
            print('Incorrect input. Please try again.\n')
            continue
    print('Organization created. Email sent to: ' + a + '\n')


def onboard():
    while True:
        try:
            driver.get(input("Please input confirmation link from email: "))
        except InvalidArgumentException:
            print('Invalid link. Please try again.')
            continue
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'ula-agree')))
            break
        except TimeoutException:
            print('Wrong link. Please try again.\n')
            continue
    print('Generating random password...')
    a = generatepassword()
    print('Random password generated! Password: ' + a)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'password'))).send_keys(a)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'repassword'))).send_keys(a)
    while True:
        a = input('Agree to the Master Subscription Agreement? (Y/N): ')
        if a.upper() == 'Y' or a.lower() == 'y':
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'ula-agree'))).click()
            break
        else:
            print('Error: Cannot create account without agreeing.\n')
            continue
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "/html/body/div[3]/div[1]/div[2]/div/div/form[2]/div[6]/button"))).click()
    WebDriverWait(driver, 15).until(EC.url_contains(newSignInPage))
    print('Organization successfully created!\n')


class OnBoarding(unittest.TestCase):
    driver = driver

    @classmethod
    def setUpClass(cls):
        cls.driver = driver

    def test_a_SignUp(self):
        self.driver.get(neworgenv())
        signup()
        self.assertTrue('https://addigy.com/thank-you/' in driver.current_url)

    def test_b_OnBoard(self):
        onboard()
        self.assertTrue(newSignInPage in driver.current_url)

    @classmethod
    def tearDownClass(cls):
        getlogs()
        cls.driver.close()
