import random
from TestAddigy.main import *
# from TestAddigy.info import *
# from selenium.webdriver import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait


def addpolicies():
    parent = 'Auto Tester' + str(random.randint(1, 9999))
    child = 'Auto Tester' + str(random.randint(1, 9999))
    grandchild = 'Auto Tester' + str(random.randint(1, 9999))
    gotopoliciespage()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "/html/body/div[1]/div[2]/div/div/div[1]/header/div/div/span/button"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "//input[@placeholder='Policy Name, required' and @class='input m-l-half']"))).send_keys(parent)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "/html/body/div[1]/div[2]/div/div/div[1]/header/div/div/div/div[2]/div/section/form/footer/button")
    )).click()
    a = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[1]/div[2]/div/div/div/div[2]/div/section[1]/div[2]/strong")
    )).get_attribute("innerHTML")
    print('Parent policy created with Policy ID: ' + a)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "/html/body/div[1]/div[2]/div/div/header/div[2]/div[2]/span/button"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "//input[@placeholder='Policy Name, required' and @class='input m-l-half']"))).send_keys(child)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "//input[@type='text' and @class='vue-treeselect__input']"))).send_keys(parent)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@type='submit' and @class='button is-primary']"))).click()
    b = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[1]/div[2]/div/div/div/div[2]/div/section[1]/div[2]/strong")
    )).get_attribute("innerHTML")
    print('Child policy created with Policy ID: ' + b)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "/html/body/div[1]/div[2]/div/div/header/div[2]/div[2]/span/button"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "//input[@placeholder='Policy Name, required' and @class='input m-l-half']"))).send_keys(grandchild)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "//input[@type='text' and @class='vue-treeselect__input']"))).send_keys(child)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@type='submit' and @class='button is-primary']"))).click()
    c = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[1]/div[2]/div/div/div/div[2]/div/section[1]/div[2]/strong")
    )).get_attribute("innerHTML")
    print('Grandchild policy created with Policy ID: ' + c)
    gotopoliciespage()


class AddInitialPolicies(MainTestCase):

    def test_a_AddInitialPolicies(self):
        addpolicies()
        self.assertEqual(policiesPage, driver.current_url)
