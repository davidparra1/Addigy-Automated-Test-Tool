from TestAddigy.main import *
# from TestAddigy.info import *
# from selenium.webdriver import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait


class Pages(MainTestCase):

    def test_a_DevicesPage(self):
        gotodevicespage()
        self.assertEqual(devicesPage, driver.current_url)

    def test_b_AddDevicesPage(self):
        gotoadddevicespage()
        self.assertEqual(addDevicesPage, driver.current_url)

    def test_c_PoliciesPage(self):
        gotopoliciespage()
        self.assertEqual(policiesPage, driver.current_url)

    def test_d_CatalogPage(self):
        gotocatalogpage()
        self.assertEqual(catalogPage, driver.current_url)

    def test_e_MonitoringPage(self):
        gotomonitoringpage()
        self.assertEqual(monitoringPage, driver.current_url)

    def test_f_DashSystemPage(self):
        gotodashsystem()
        self.assertEqual(dashSystemPage, driver.current_url)

    def test_g_DashExecutivePage(self):
        gotodashexecutive()
        self.assertEqual(dashExecutivePage, driver.current_url)

    def test_h_DashApplicationsPage(self):
        gotodashapplications()
        self.assertEqual(dashApplicationsPage, driver.current_url)

    def test_i_DashEventsPage(self):
        gotodashevents()
        self.assertEqual(dashEventsPage, driver.current_url)

    def test_j_CommunityFactsPage(self):
        gotocommunityfactspage()
        self.assertEqual(communityFactsPage, driver.current_url)

    def test_k_CommunityScriptsPage(self):
        gotocommunityscriptspage()
        self.assertEqual(communityScriptsPage, driver.current_url)
