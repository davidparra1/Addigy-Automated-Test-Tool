import secrets
import string
from selenium.common import InvalidArgumentException
from TestAddigy.main import *
# from TestAddigy.info import *
# from selenium.webdriver import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait

email = ''
password = ''


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
    a = [secrets.choice(letter_choices) for _ in range(num_letters)]

    symbol = secrets.choice("!@#$%^&*")
    a.insert(secrets.randbelow(len(a) + 1), symbol)

    digit = secrets.choice("0123456789")
    a.insert(secrets.randbelow(len(a) + 1), digit)

    return ''.join(a)


def signup():
    global email
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
        email = input("Business Email?: ")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.ID, 'signup_email'))).send_keys(email)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@class='btn btn-primary btn-block btn-lg' and @type='submit']"))).click()
        try:
            WebDriverWait(driver, 10).until(EC.url_changes(driver.current_url))
            break
        except TimeoutException:
            print('Incorrect input. Please try again.\n')
            continue
    print('Organization created. Email sent to: ' + email + '\n')


def onboard():
    global password
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
    password = generatepassword()
    print('Random password generated! Password: ' + password)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'password'))).send_keys(password)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'repassword'))).send_keys(password)
    print('Automatically agreeing to the Master Subscription Agreement...')
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'ula-agree'))).click()
    # while True:
    #     a = input('Agree to the Master Subscription Agreement? (Y/N): ')
    #     if a.upper() == 'Y' or a.lower() == 'y':
    #         WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'ula-agree'))).click()
    #         break
    #     else:
    #         print('Error: Cannot create account without agreeing.\n')
    #         continue
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "/html/body/div[3]/div[1]/div[2]/div/div/form[2]/div[6]/button"))).click()
    WebDriverWait(driver, 15).until(EC.url_contains(newSignInPage))
    print('Organization successfully created!')


def neworgsignin():
    driver.get(landingPage)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'email-input'))).clear()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'email-input'))).send_keys(email)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@data-v-757e2e4a='' and @type='submit']"))).click()
    if WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.ID, 'username'))).get_attribute("value") != email:
        driver.find_element(By.ID, 'username').clear()
        driver.find_element(By.ID, 'username').send_keys(email)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'password'))).clear()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'password'))).send_keys(password, Keys.ENTER)
    try:
        WebDriverWait(driver, 5).until(EC.url_changes(driver.current_url))
    except TimeoutException:
        if newSignInPage in driver.current_url:
            try:
                driver.find_element(By.ID, 'captcha')
                print('CAPTCHA detected. Please input CAPTCHA. (60s)\n')
                WebDriverWait(driver, 60).until(EC.url_changes(driver.current_url))
            except NoSuchElementException:
                print('Error occurred. Please try again.\n')
    if mfaPage in driver.current_url:
        print('New login experience detected. Waiting for MFA setup. (120s)\n')
        WebDriverWait(driver, 120).until(EC.url_contains(setUpPage))
    else:
        WebDriverWait(driver, 10).until(EC.url_contains(setUpPage))
    print('Successfully signed in!\n'
          'Environment: ' + env +
          '\nAccount Email: ' + email)


# def createorg():
    

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

    def test_c_SignIn(self):
        neworgsignin()
        self.assertTrue(setUpPage in driver.current_url)

    @classmethod
    def tearDownClass(cls):
        getlogs()
