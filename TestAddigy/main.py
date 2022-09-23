import time
import unittest
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

PATH = '/Users/dparra/PycharmProjects/pythonProject/chromedriver'
s = Service(PATH)
driver = webdriver.Chrome(service=s)


def testenv():
    while True:
        a = input("Which environment to test? (dev/stage/prod)?: ")
        if a.casefold() == 'dev':
            a = '-dev'
            print('Test environment selected: DEV\n')
            return a
        elif a.casefold() == 'stage':
            a = '-stage'
            print('Test environment selected: STAGE\n')
            return a
        elif a.casefold() == 'prod':
            a = ''
            print('Test environment selected: PROD\n')
            return a
        else:
            print('Error: Invalid Value\n')
            continue


env = testenv()
mfaPage = 'https://login' + env + '.addigy.com/u/mfa'
oldSignInPage = 'https://prod.addigy.com/login'
newSignInPage = 'https://login' + env + '.addigy.com/u/login'
landingPage = 'https://app' + env + '.addigy.com/signin'
mainPage = 'https://app' + env + '.addigy.com/dashboard/system'
devicesPage = 'https://app' + env + '.addigy.com/devices'
addDevicesPage = 'https://app' + env + '.addigy.com/downloads'
policiesPage = 'https://app' + env + '.addigy.com/policies'
catalogPage = 'https://app' + env + '.addigy.com/catalog'
monitoringPage = 'https://app' + env + '.addigy.com/monitoring'
dashSystemPage = 'https://app' + env + '.addigy.com/dashboard/system'
dashExecutivePage = 'https://app' + env + '.addigy.com/dashboard/executive'
dashApplicationsPage = 'https://app' + env + '.addigy.com/dashboard/applications'
dashEventsPage = 'https://app' + env + '.addigy.com/dashboard/events'
communityFactsPage = 'https://app' + env + '.addigy.com/community/facts'
communityScriptsPage = 'https://app' + env + '.addigy.com/community/scripts'


def askforemail():
    email = input("Account email?: ")
    return email


def askforpassword():
    password = input("Account password?: ")
    return password


# make another function for new login experience #DONE
# add conditional statement to MainTestCase that checks for old login experience vs new #DONE, NOT NEEDED
# make changes to signOnTest if using new login experience? (potentially not needed) #DONE
# figure out how to run individual test cases inside of test suites #DONE
# deal with 2FA if using new login experience #DONE
# deal with CAPTCHA if using new login experience #DONE
# different environments? dev / stage / prod # DONE
# detect errors in browser console # DONE, but need to improve error logs

# figure out how to make test suites not run setUp again completely. To avoid logging in multiple times. Maybe keep a
#   for multiple tests? Until the user wishes to terminate the sessions?
#   can utilize class setups with unittest (could expand to session initializations). tearDown script could lead to home
#   page instead of shutting down selenium window

# tests should likely be run on legacy login experience by default (saves times)
# SSO login options?
# different browsers?


def getlogs():
    for log in driver.get_log('browser'):
        print(log)


def signin():
    while True:
        email = askforemail()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'email-input'))).clear()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'email-input'))).send_keys(email)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, "//button[@data-v-757e2e4a='' and @type='submit']"))).click()
        time.sleep(2)
        if driver.current_url == landingPage:
            print('Incorrect email. Please try again.\n')
            continue
        else:
            break
    if WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.ID, 'username'))).get_attribute("value") != email:
        driver.find_element(By.ID, 'username').clear()
        driver.find_element(By.ID, 'username').send_keys(email)
    while True:
        password = askforpassword()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'password'))).clear()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'password'))).send_keys(password, Keys.ENTER)
        time.sleep(2)
        if newSignInPage in driver.current_url:
            try:
                driver.find_element(By.ID, 'captcha')
                print('CAPTCHA detected. Please input CAPTCHA. (60s)')
                WebDriverWait(driver, 60).until_not(EC.url_contains(newSignInPage))
                break
            except NoSuchElementException:
                print('Incorrect password. Please try again.\n')
                continue
        elif oldSignInPage in driver.current_url:
            print('Incorrect password. Please try again.\n')
            continue
        else:
            break
    if mfaPage in driver.current_url:
        print('New login experience detected. Waiting for MFA authentication. (80s)\n')
        WebDriverWait(driver, 80).until(EC.url_contains(mainPage))
    else:
        WebDriverWait(driver, 10).until(EC.url_contains(mainPage))
    print('Successfully signed in!')


def signout():
    checkformainpage()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
        (By.XPATH, "//button[@class='button is-link' and @data-v-1995d9b0='']"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "//a[@href='/logout']"))).click()
    time.sleep(2)


def checkformainpage():
    if driver.current_url != mainPage:
        driver.get(mainPage)


def gotodashsystem():
    if driver.current_url != mainPage:
        # dumb workaround
        driver.get(catalogPage)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@class='nav-item trigger' and @title='Dashboards']"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "//a[@class='nav-item' and @href='/dashboard/system' and @role='menuitem']"))).click()
        WebDriverWait(driver, 10).until(EC.url_contains(dashSystemPage))
    else:
        return


def gotodashexecutive():
    checkformainpage()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@class='nav-item trigger' and @title='Dashboards']"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "//a[@class='nav-item' and @href='/dashboard/executive' and @role='menuitem']"))).click()
    WebDriverWait(driver, 10).until(EC.url_contains(dashExecutivePage))


def gotodashapplications():
    checkformainpage()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@class='nav-item trigger' and @title='Dashboards']"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "//a[@class='nav-item' and @href='/dashboard/applications' and @role='menuitem']"))).click()
    WebDriverWait(driver, 10).until(EC.url_contains(dashApplicationsPage))


def gotodashevents():
    checkformainpage()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@class='nav-item trigger' and @title='Dashboards']"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "//a[@class='nav-item' and @href='/dashboard/events' and @role='menuitem']"))).click()
    WebDriverWait(driver, 10).until(EC.url_contains(dashEventsPage))


def gotodevicespage():
    checkformainpage()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@class='nav-item trigger' and @title='Devices']"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "//a[@class='nav-item' and @href='/devices' and @role='menuitem']"))).click()
    WebDriverWait(driver, 10).until(EC.url_contains(devicesPage))


def gotoadddevicespage():
    checkformainpage()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "//a[@class='nav-item' and @href='/downloads']"))).click()
    WebDriverWait(driver, 10).until(EC.url_contains(addDevicesPage))


def gotopoliciespage():
    checkformainpage()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "//a[@class='nav-item' and @href='/policies']"))).click()
    WebDriverWait(driver, 10).until(EC.url_contains(policiesPage))


def gotocatalogpage():
    checkformainpage()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "//a[@class='nav-item' and @href='/catalog']"))).click()
    WebDriverWait(driver, 10).until(EC.url_contains(catalogPage))


def gotomonitoringpage():
    checkformainpage()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "//a[@class='nav-item' and @href='/monitoring']"))).click()
    WebDriverWait(driver, 10).until(EC.url_contains(monitoringPage))


def gotocommunityfactspage():
    checkformainpage()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@class='nav-item trigger' and @title='Community']"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "//a[@class='nav-item' and @href='/community/facts' and @role='menuitem']"))).click()
    WebDriverWait(driver, 10).until(EC.url_contains(communityFactsPage))


def gotocommunityscriptspage():
    checkformainpage()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@class='nav-item trigger' and @title='Community']"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "//a[@class='nav-item' and @href='/community/scripts' and @role='menuitem']"))).click()
    WebDriverWait(driver, 10).until(EC.url_contains(communityScriptsPage))


class MainTestCase(unittest.TestCase):
    driver = driver

    @classmethod
    def setUpClass(cls):
        cls.driver = driver
        cls.driver.get(landingPage)
        signin()

    @classmethod
    def tearDownClass(cls):
        getlogs()
        cls.driver.close()


if __name__ == "__main__":
    unittest.main()
