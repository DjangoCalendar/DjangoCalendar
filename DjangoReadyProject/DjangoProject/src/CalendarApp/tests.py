# -*- coding: utf-8 -*-
from selenium import webdriver
from django.test import Client
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
from selenium.common.exceptions import NoSuchElementException,\
    NoAlertPresentException

from CalendarApp.views import index
from django.test.client import RequestFactory
from CalendarApp.models import Entry
from django.test.testcases import TestCase
import time

class Tests(TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://localhost:8000"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_A(self):
        driver = self.driver
            #u = User.objects.create_user("tester1234", "test@o2.pl", "Master1234")
            #u.save()
        driver.get(self.base_url + "/calendar/")
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_id("id_Login").clear()
        driver.find_element_by_id("id_Login").send_keys("tester1234")
        driver.find_element_by_id("id_Password").clear()
        driver.find_element_by_id("id_Password").send_keys("tester1234")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_link_text("Options").click()
        driver.find_element_by_link_text("Yearly Calendar").click()
        driver.find_element_by_link_text("February").click()
        nyear, nmonth, nday = time.localtime()[:3]
        driver.find_element_by_xpath("//td[@onclick=\"parent.location='/calendar/day/"+str(nyear)+"/"+str(nmonth)+"/" +str(nday) +"/'\"]").click()
        driver.find_element_by_id("id_form-0-title").clear()
        driver.find_element_by_id("id_form-0-title").send_keys("Testowy")
        driver.find_element_by_id("id_form-0-snippet").clear()
        driver.find_element_by_id("id_form-0-snippet").send_keys("Krotki Opis")
        driver.find_element_by_id("id_form-0-remind").click()
        driver.find_element_by_id("id_form-0-body").clear()
        driver.find_element_by_id("id_form-0-body").send_keys("Wiecej Szczegolow")
        driver.find_element_by_xpath("//button[@value='Save']").click()
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "div.alert.alert-success"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_css_selector("a > img").click()
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "div.alert.alert-success"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("February").click()
        driver.find_element_by_css_selector("td.current").click()
        driver.find_element_by_id("id_form-0-DELETE").click()
        driver.find_element_by_xpath("//button[@value='Save']").click()

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

class Tests1(TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://localhost:8000"
        self.verificationErrors = []
        self.accept_next_alert = True


    def test_B(self):
        driver = self.driver
        #try:
         #   user = User.objects.get(username="testowytester1990")
         #   user.delete()
         #   User.save()
        #except Exception,e:
        #    h=""
        driver.get(self.base_url + "/calendar/")
        driver.find_element_by_link_text("Register").click()
        driver.find_element_by_id("id_Login").clear()
        driver.find_element_by_id("id_Login").send_keys("testowytester1990")
        driver.find_element_by_id("id_Email").clear()
        driver.find_element_by_id("id_Email").send_keys("testowytester1990@o2.pl")
        driver.find_element_by_id("id_GGNumber").clear()
        driver.find_element_by_id("id_GGNumber").send_keys("1108347")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        self.assertEqual(driver.title != "Django Calendar 2013-2014",True )

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


class Tests2(TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://localhost:8000"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_C(self):
        driver = self.driver
        driver.get(self.base_url + "/calendar/")
        try: self.assertTrue(self.is_element_present(By.LINK_TEXT, "DjangoCalendar Project"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.LINK_TEXT, "Login"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.LINK_TEXT, "Register"))
        except AssertionError as e: self.verificationErrors.append(str(e))
    
    def test_D(self):
        driver = self.driver
        driver.get(self.base_url + "/calendar/")
        driver.find_element_by_link_text("Login").click()
        self.assertEqual("Login", driver.title)
        self.assertEqual("Please log in", driver.find_element_by_css_selector("h2.form-signin-heading").text)
        try: self.assertTrue(self.is_element_present(By.ID, "id_Login"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_Password"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.XPATH, "//button[@type='submit']"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.LINK_TEXT, "Register"))
        except AssertionError as e: self.verificationErrors.append(str(e))
 
    def test_E(self):
        driver = self.driver
        driver.get(self.base_url + "/calendar/")
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_xpath("//button[@type='submit']").click()
        try: self.assertTrue(self.is_element_present(By.ID, "id_Login"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_Password"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_id("id_Login").clear()
        driver.find_element_by_id("id_Login").send_keys("tester1234")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        try: self.assertTrue(self.is_element_present(By.ID, "id_Login"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_Password"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.XPATH, "//button[@type='submit']"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.LINK_TEXT, "Register"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        
    def test_F(self):
        driver = self.driver
        driver.get(self.base_url + "/calendar/")
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_id("id_Password").clear()
        driver.find_element_by_id("id_Password").send_keys("tester1234")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        try: self.assertTrue(self.is_element_present(By.ID, "id_Login"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_Password"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("tester1234", driver.find_element_by_id("id_Password").get_attribute("value"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.XPATH, "//button[@type='submit']"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.LINK_TEXT, "Register"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertEqual("Login", driver.title)
        
    def test_G(self):
        driver = self.driver
        driver.get(self.base_url + "/calendar/")
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_id("id_Login").clear()
        driver.find_element_by_id("id_Login").send_keys("ttttttttttttttttt")
        driver.find_element_by_id("id_Password").clear()
        driver.find_element_by_id("id_Password").send_keys("tester1234")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "div.alert"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_Login"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_Password"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.XPATH, "//button[@type='submit']"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.LINK_TEXT, "Register"))
        except AssertionError as e: self.verificationErrors.append(str(e))

    def test_H(self):
        driver = self.driver
        driver.get(self.base_url + "/calendar/")
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_id("id_Login").clear()
        driver.find_element_by_id("id_Login").send_keys("tester1234")
        driver.find_element_by_id("id_Password").clear()
        driver.find_element_by_id("id_Password").send_keys("tttttttttttttt")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "div.alert"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_Login"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_Password"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.XPATH, "//button[@type='submit']"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.LINK_TEXT, "Register"))
        except AssertionError as e: self.verificationErrors.append(str(e))

    def test_I(self):
        driver = self.driver
        driver.get(self.base_url + "/calendar/")
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_id("id_Login").clear()
        driver.find_element_by_id("id_Login").send_keys("tt")
        driver.find_element_by_id("id_Password").clear()
        driver.find_element_by_id("id_Password").send_keys("tester1234")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        try: self.assertEqual("You login is too short - at least 6 characters", driver.find_element_by_css_selector("li").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_Login"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_Password"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.XPATH, "//button[@type='submit']"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.LINK_TEXT, "Register"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_id("id_Login").clear()
        driver.find_element_by_id("id_Login").send_keys("tester1234")
        driver.find_element_by_id("id_Password").clear()
        driver.find_element_by_id("id_Password").send_keys("tt")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        try: self.assertEqual("You password is too short - at least 10 characters", driver.find_element_by_css_selector("li").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_Login"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_Password"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.XPATH, "//button[@type='submit']"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.LINK_TEXT, "Register"))
        except AssertionError as e: self.verificationErrors.append(str(e))

    def test_J(self):
        driver = self.driver
        driver.get(self.base_url + "/calendar/")
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_id("id_Login").clear()
        driver.find_element_by_id("id_Login").send_keys("tester1234")
        driver.find_element_by_id("id_Password").clear()
        driver.find_element_by_id("id_Password").send_keys("tester1234")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        try: self.assertEqual("Logged In: tester1234", driver.find_element_by_css_selector("li.navbar-brand").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertEqual("Django Calendar 2013-2014", driver.title)
        try: self.assertTrue(self.is_element_present(By.LINK_TEXT, "Options"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("Options").click()
        driver.find_element_by_link_text("Logout").click()

    def test_K(self):
        driver = self.driver
        driver.get(self.base_url + "/calendar/")
        driver.find_element_by_link_text("Register").click()
        self.assertEqual("Register", driver.title)
        try: self.assertTrue(self.is_element_present(By.ID, "id_Login"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_Email"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_FirstName"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_LastName"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_GGNumber"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_FacebookId"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.XPATH, "//button[@type='submit']"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        
    def test_L(self):
        driver = self.driver
        driver.get(self.base_url + "/calendar/")
        driver.find_element_by_link_text("Register").click()
        driver.find_element_by_id("id_Login").clear()
        driver.find_element_by_id("id_Login").send_keys("tester1234")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        try: self.assertTrue(self.is_element_present(By.ID, "id_Login"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("tester1234", driver.find_element_by_id("id_Login").get_attribute("value"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_Email"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_FirstName"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_LastName"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_GGNumber"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_FacebookId"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.XPATH, "//button[@type='submit']"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        
    def test_M(self):
        driver = self.driver
        driver.get(self.base_url + "/calendar/")
        driver.find_element_by_link_text("Register").click()
        driver.find_element_by_id("id_Login").clear()
        driver.find_element_by_id("id_Login").send_keys("tester1234")
        driver.find_element_by_id("id_Email").clear()
        driver.find_element_by_id("id_Email").send_keys("mateusz.bacal@o2.pl")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        try: self.assertEqual("mateusz.bacal@o2.pl", driver.find_element_by_id("id_Email").get_attribute("value"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("tester1234", driver.find_element_by_id("id_Login").get_attribute("value"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_FirstName"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_LastName"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_GGNumber"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_FacebookId"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.XPATH, "//button[@type='submit']"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        
    def test_N(self):
        driver = self.driver
        driver.get(self.base_url + "/calendar/")
        driver.find_element_by_link_text("Register").click()
        driver.find_element_by_id("id_Login").clear()
        driver.find_element_by_id("id_Login").send_keys("tester1234")
        driver.find_element_by_id("id_Email").clear()
        driver.find_element_by_id("id_Email").send_keys("bonzai1990@o2.pl")
        driver.find_element_by_id("id_GGNumber").clear()
        driver.find_element_by_id("id_GGNumber").send_keys("1108347")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "div.alert"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("tester1234", driver.find_element_by_id("id_Login").get_attribute("value"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("bonzai1990@o2.pl", driver.find_element_by_id("id_Email").get_attribute("value"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("1108347", driver.find_element_by_id("id_GGNumber").get_attribute("value"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_id("id_Login").clear()
        driver.find_element_by_id("id_Login").send_keys("t")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        try: self.assertEqual("You login is too short - at least 6 characters", driver.find_element_by_css_selector("li").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("bonzai1990@o2.pl", driver.find_element_by_id("id_Email").get_attribute("value"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("1108347", driver.find_element_by_id("id_GGNumber").get_attribute("value"))
        except AssertionError as e: self.verificationErrors.append(str(e))

    def test_O(self):
        driver = self.driver
        driver.get(self.base_url + "/calendar/")
        driver.find_element_by_link_text("Register").click()
        driver.find_element_by_id("id_Login").clear()
        driver.find_element_by_id("id_Login").send_keys("testowytester")
        driver.find_element_by_id("id_Email").clear()
        driver.find_element_by_id("id_Email").send_keys("djangocalendar")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_id("id_GGNumber").clear()
        driver.find_element_by_id("id_GGNumber").send_keys("1108347")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        try: self.assertEqual("Enter a valid email address.", driver.find_element_by_css_selector("li").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_id("id_Email").clear()
        driver.find_element_by_id("id_Email").send_keys("bonzai1990@o2.pl")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "div.alert"))
        except AssertionError as e: self.verificationErrors.append(str(e))


    def test_P(self):
        driver = self.driver
        driver.get(self.base_url + "/calendar/")
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_id("id_Login").clear()
        driver.find_element_by_id("id_Login").send_keys("tester1234")
        driver.find_element_by_id("id_Password").clear()
        driver.find_element_by_id("id_Password").send_keys("tester1234")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_link_text("Options").click()
        driver.find_element_by_link_text("Account details").click()
        self.assertEqual("User Account Details", driver.title)
        driver.find_element_by_css_selector("img[alt=\"Back to Main Page\"]").click()
        driver.find_element_by_link_text("Options").click()
        driver.find_element_by_link_text("Logout").click()

    def test_R(self):
        driver = self.driver
        driver.get(self.base_url + "/calendar/")
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_id("id_Login").clear()
        driver.find_element_by_id("id_Login").send_keys("tester1234")
        driver.find_element_by_id("id_Password").clear()
        driver.find_element_by_id("id_Password").send_keys("tester1234")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_link_text("Options").click()
        driver.find_element_by_link_text("Account details").click()
        self.assertEqual("User Account Details", driver.title)
        try: self.assertTrue(self.is_element_present(By.ID, "ui-id-1"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "ui-id-2"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "ui-id-3"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "ui-id-4"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("tester1234", driver.find_element_by_id("id_Login").get_attribute("value"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("bonzai1990@o2.pl", driver.find_element_by_id("id_Email").get_attribute("value"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Jan", driver.find_element_by_id("id_FirstName").get_attribute("value"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Kowalsky", driver.find_element_by_id("id_LastName").get_attribute("value"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("1108347", driver.find_element_by_id("id_GGNumber").get_attribute("value"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("mateusz.bacal", driver.find_element_by_id("id_FacebookId").get_attribute("value"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_id("ui-id-2").click()
        try: self.assertTrue(self.is_element_present(By.ID, "id_OldPassword"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_NewPassword"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_RepeatNewPassword"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.XPATH, "(//button[@type='submit'])[2]"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_id("ui-id-3").click()
        try: self.assertTrue(self.is_element_present(By.XPATH, "(//button[@type='submit'])[3]"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_id("ui-id-4").click()
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "img[alt=\"Avatar1\"]"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "img[alt=\"Avatar2\"]"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "img[alt=\"Avatar3\"]"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "img[alt=\"Avatar4\"]"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "img[alt=\"Avatar5\"]"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "img[alt=\"Avatar6\"]"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "img[alt=\"Avatar5\"]"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "img[alt=\"Avatar7\"]"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.XPATH, "(//button[@type='submit'])[4]"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "img[alt=\"Back to Main Page\"]"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_css_selector("img[alt=\"Back to Main Page\"]").click()
        driver.find_element_by_link_text("Options").click()
        driver.find_element_by_link_text("Logout").click()
    


    def test_S(self):
        driver = self.driver
        #try:
        #    user = User.objects.get(username="testowytester")
        #    Entry.objects.all().delete()
        #except Exception,e:
        #    u = User.objects.create_user("testowytester", "test@o2.pl", "Master1234")
        #    u.save()
        driver.get(self.base_url + "/calendar/")
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_id("id_Login").clear()
        driver.find_element_by_id("id_Login").send_keys("tester1234")
        driver.find_element_by_id("id_Password").clear()
        driver.find_element_by_id("id_Password").send_keys("tester1234")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_link_text("Options").click()
        driver.find_element_by_link_text("Account details").click()
        driver.find_element_by_id("ui-id-2").click()
        driver.find_element_by_id("id_OldPassword").clear()
        driver.find_element_by_id("id_OldPassword").send_keys("M")
        driver.find_element_by_xpath("(//button[@type='submit'])[2]").click()
        try: self.assertTrue(self.is_element_present(By.ID, "id_NewPassword"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_RepeatNewPassword"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.XPATH, "(//button[@type='submit'])[2]"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_id("id_OldPassword").clear()
        driver.find_element_by_id("id_OldPassword").send_keys("")
        driver.find_element_by_css_selector("img[alt=\"Back to Main Page\"]").click()
        driver.find_element_by_css_selector("b.caret").click()
        driver.find_element_by_link_text("Logout").click()
        
    def test_T(self):
        driver = self.driver
        #try:
        #    user = User.objects.get(username="testowytester")
        #    Entry.objects.all().delete()
        #except Exception,e:
        #    u = User.objects.create_user("testowytester", "test@o2.pl", "Master1234")
        #    u.save()
        driver.get(self.base_url + "/calendar/")
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_id("id_Login").clear()
        driver.find_element_by_id("id_Login").send_keys("tester1234")
        driver.find_element_by_id("id_Password").clear()
        driver.find_element_by_id("id_Password").send_keys("tester1234")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_link_text("Options").click()
        driver.find_element_by_link_text("Account details").click()
        driver.find_element_by_id("ui-id-2").click()
        driver.find_element_by_id("id_OldPassword").clear()
        driver.find_element_by_id("id_OldPassword").send_keys("tester1234")
        driver.find_element_by_id("id_NewPassword").clear()
        driver.find_element_by_id("id_NewPassword").send_keys("Master")
        driver.find_element_by_id("id_RepeatNewPassword").clear()
        driver.find_element_by_id("id_RepeatNewPassword").send_keys("Master")
        driver.find_element_by_xpath("(//button[@type='submit'])[2]").click()
        try: self.assertTrue(self.is_element_present(By.ID, "id_OldPassword"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_NewPassword"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_RepeatNewPassword"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("You password is too short - at least 10 characters", driver.find_element_by_css_selector("ul.errorlist > li").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("You password is too short - at least 10 characters", driver.find_element_by_xpath("//div[@id='tabs-2']/form/ul[2]/li").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_css_selector("img[alt=\"Back to Main Page\"]").click()
        driver.find_element_by_link_text("Options").click()
        driver.find_element_by_link_text("Logout").click()
        
    def test_W(self):
        driver = self.driver
        #try:
        #    user = User.objects.get(username="tester1234")
        #    Entry.objects.all().delete()
        #    user.set_password("tester1234")
        #    user.save()
        #except Exception,e:
        #    u = User.objects.create_user("tester1234", "test@o2.pl", "tester1234")
        #    u.save()
        driver.get(self.base_url + "/calendar/")
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_id("id_Login").clear()
        driver.find_element_by_id("id_Login").send_keys("tester1234")
        driver.find_element_by_id("id_Password").clear()
        driver.find_element_by_id("id_Password").send_keys("tester1234")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_link_text("Options").click()
        driver.find_element_by_link_text("Account details").click()
        driver.find_element_by_id("ui-id-2").click()
        driver.find_element_by_id("id_OldPassword").clear()
        driver.find_element_by_id("id_OldPassword").send_keys("tester1234")
        driver.find_element_by_id("id_NewPassword").clear()
        driver.find_element_by_id("id_NewPassword").send_keys("Master123456")
        driver.find_element_by_id("id_RepeatNewPassword").clear()
        driver.find_element_by_id("id_RepeatNewPassword").send_keys("Master1234567890")
        driver.find_element_by_xpath("(//button[@type='submit'])[2]").click()
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "div.alert.alert-success"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_css_selector("img[alt=\"Back to Main Page\"]").click()
        driver.find_element_by_link_text("Options").click()
        driver.find_element_by_link_text("Logout").click()

    def test_U(self):
        driver = self.driver
        #try:
        #    user = User.objects.get(username="testowytester")
        #    Entry.objects.all().delete()
        #except Exception,e:
        #    u = User.objects.create_user("testowytester", "test@o2.pl", "Master1234")
        #    u.save()
        driver.get(self.base_url + "/calendar/")
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_id("id_Login").clear()
        driver.find_element_by_id("id_Login").send_keys("tester1234")
        driver.find_element_by_id("id_Password").clear()
        driver.find_element_by_id("id_Password").send_keys("tester1234")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_link_text("Options").click()
        driver.find_element_by_link_text("Account details").click()
        driver.find_element_by_id("ui-id-2").click()
        driver.find_element_by_id("id_OldPassword").clear()
        driver.find_element_by_id("id_OldPassword").send_keys("tester1234")
        driver.find_element_by_id("id_NewPassword").clear()
        driver.find_element_by_id("id_NewPassword").send_keys("Master1234")
        driver.find_element_by_id("id_RepeatNewPassword").clear()
        driver.find_element_by_id("id_RepeatNewPassword").send_keys("Master1234")
        driver.find_element_by_xpath("(//button[@type='submit'])[2]").click()
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "div.alert.alert-success"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_OldPassword"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_NewPassword"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_RepeatNewPassword"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.XPATH, "(//button[@type='submit'])[2]"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_id("id_OldPassword").clear()
        driver.find_element_by_id("id_OldPassword").send_keys("Master1234")
        driver.find_element_by_id("id_NewPassword").clear()
        driver.find_element_by_id("id_NewPassword").send_keys("tester1234")
        driver.find_element_by_id("id_RepeatNewPassword").clear()
        driver.find_element_by_id("id_RepeatNewPassword").send_keys("tester1234")
        driver.find_element_by_xpath("(//button[@type='submit'])[2]").click()
        driver.find_element_by_css_selector("img[alt=\"Back to Main Page\"]").click()
        driver.find_element_by_link_text("Options").click()
        driver.find_element_by_link_text("Logout").click()
        
    def test_X(self):
        driver = self.driver
        #try:
        #    user = User.objects.get(username="tester1234")
        #    Entry.objects.all().delete()
        #    user.set_password("tester1234")
        #    user.save()
        #except Exception,e:
        #    u = User.objects.create_user("tester1234", "test@o2.pl", "tester1234")
        #    u.save()
        driver.get(self.base_url + "/calendar/")
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_id("id_Login").clear()
        driver.find_element_by_id("id_Login").send_keys("tester1234")
        driver.find_element_by_id("id_Password").clear()
        driver.find_element_by_id("id_Password").send_keys("tester1234")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_link_text("Options").click()
        driver.find_element_by_link_text("Account details").click()
        driver.find_element_by_id("ui-id-2").click()
        driver.find_element_by_id("id_OldPassword").clear()
        driver.find_element_by_id("id_OldPassword").send_keys("Master1234567")
        driver.find_element_by_id("id_NewPassword").clear()
        driver.find_element_by_id("id_NewPassword").send_keys("Master1234")
        driver.find_element_by_id("id_RepeatNewPassword").clear()
        driver.find_element_by_id("id_RepeatNewPassword").send_keys("Master1234")
        driver.find_element_by_xpath("(//button[@type='submit'])[2]").click()
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "div.alert.alert-success"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_OldPassword"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_NewPassword"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_RepeatNewPassword"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.XPATH, "(//button[@type='submit'])[2]"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertEqual("User Account Details", driver.title)
        driver.find_element_by_css_selector("img[alt=\"Back to Main Page\"]").click()
        driver.find_element_by_link_text("Options").click()
        driver.find_element_by_link_text("Logout").click()

        
    def test_Y(self):
        driver = self.driver
        #try:
        #    user = User.objects.get(username="testowytester")
        #    Entry.objects.all().delete()
        #    user.set_password("tester1234")
        #    user.save()
        #except Exception,e:
        #    u = User.objects.create_user("testowytester", "test@o2.pl", "Master1234")
        #    u.save()
        driver.get(self.base_url + "/calendar/")
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_id("id_Login").clear()
        driver.find_element_by_id("id_Login").send_keys("tester1234")
        driver.find_element_by_id("id_Password").clear()
        driver.find_element_by_id("id_Password").send_keys("tester1234")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_link_text("Options").click()
        driver.find_element_by_link_text("Account details").click()
        driver.find_element_by_id("id_Login").clear()
        driver.find_element_by_id("id_Login").send_keys("test666")
        try: self.assertTrue(self.is_element_present(By.ID, "id_Login"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_xpath("//button[@type='submit']").click()
        try: self.assertEqual("test666", driver.find_element_by_id("id_Login").get_attribute("value"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_css_selector("img[alt=\"Back to Main Page\"]").click()
        driver.find_element_by_link_text("Options").click()
        driver.find_element_by_link_text("Account details").click()
        try: self.assertEqual("test666", driver.find_element_by_id("id_Login").get_attribute("value"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_id("id_Login").clear()
        driver.find_element_by_id("id_Login").send_keys("tester1234")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_css_selector("img[alt=\"Back to Main Page\"]").click()
        driver.find_element_by_link_text("Options").click()
        driver.find_element_by_link_text("Logout").click()

    def test_ZA(self):
        driver = self.driver
        #try:
        #    user = User.objects.get(username="testowytester")
         #   Entry.objects.all().delete()
            
        #except Exception,e:
        #    u = User.objects.create_user("testowytester", "test@o2.pl", "Master1234")
        #    u.save()
        driver.get(self.base_url + "/calendar/")
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_id("id_Login").clear()
        driver.find_element_by_id("id_Login").send_keys("tester1234")
        driver.find_element_by_id("id_Password").clear()
        driver.find_element_by_id("id_Password").send_keys("tester1234")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_link_text("Options").click()
        driver.find_element_by_link_text("Account details").click()
        driver.find_element_by_id("id_Login").clear()
        driver.find_element_by_id("id_Login").send_keys("tester12345")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "div.alert.alert-success"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_css_selector("img[alt=\"Back to Main Page\"]").click()
        driver.find_element_by_link_text("Options").click()
        driver.find_element_by_link_text("Account details").click()
        try: self.assertEqual("tester12345", driver.find_element_by_id("id_Login").get_attribute("value"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_id("id_Login").clear()
        driver.find_element_by_id("id_Login").send_keys("tester1234")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_css_selector("img[alt=\"Back to Main Page\"]").click()
        driver.find_element_by_link_text("Options").click()
        driver.find_element_by_link_text("Logout").click()
        
    def test_ZB(self):
        driver = self.driver
        #try:
        #    user = User.objects.get(username="testowytester")
        #    Entry.objects.all().delete()
        #except Exception,e:
        #    u = User.objects.create_user("testowytester", "test@o2.pl", "Master1234")
        #    u.save()
        driver.get(self.base_url + "/calendar/")
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_id("id_Login").clear()
        driver.find_element_by_id("id_Login").send_keys("tester1234")
        driver.find_element_by_id("id_Password").clear()
        driver.find_element_by_id("id_Password").send_keys("tester1234")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_link_text("Options").click()
        driver.find_element_by_link_text("Account details").click()
        driver.find_element_by_id("id_Login").clear()
        driver.find_element_by_id("id_Login").send_keys("testowytester123")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "div.alert.alert-success"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_css_selector("img[alt=\"Back to Main Page\"]").click()
        self.assertEqual("Logged In: testowytester123", driver.find_element_by_css_selector("li.navbar-brand").text)
        driver.find_element_by_link_text("Options").click()
        driver.find_element_by_link_text("Account details").click()
        driver.find_element_by_id("id_Login").clear()
        driver.find_element_by_id("id_Login").send_keys("tester1234")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_css_selector("img[alt=\"Back to Main Page\"]").click()
        driver.find_element_by_link_text("Options").click()
        driver.find_element_by_link_text("Logout").click()
        
    def test_ZC(self):
        driver = self.driver
        driver.get(self.base_url + "/calendar/")
        driver.find_element_by_link_text("Register").click()
        driver.find_element_by_id("id_Login").clear()
        driver.find_element_by_id("id_Login").send_keys("testowytester123")
        driver.find_element_by_id("id_Email").clear()
        driver.find_element_by_id("id_Email").send_keys("mateusz.bacal@uj.edu.pl")
        driver.find_element_by_id("id_GGNumber").clear()
        driver.find_element_by_id("id_GGNumber").send_keys("1108347")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_id("id_Login").clear()
        driver.find_element_by_id("id_Login").send_keys("testowytester123")
        driver.find_element_by_id("id_Password").clear()
        driver.find_element_by_id("id_Password").send_keys("Master1234")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_link_text("Options").click()
        driver.find_element_by_link_text("Account details").click()
        driver.find_element_by_id("ui-id-3").click()
        try: self.assertTrue(self.is_element_present(By.XPATH, "(//button[@type='submit'])[3]"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_xpath("(//button[@type='submit'])[3]").click()
        self.assertRegexpMatches(self.close_alert_and_get_its_text(), r"^Are you sure you want to delete account [\s\S]$")
        self.assertEqual("Django Calendar 2013-2014", driver.title)
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_id("id_Login").clear()
        driver.find_element_by_id("id_Login").send_keys("testowytester123")
        driver.find_element_by_id("id_Password").clear()
        driver.find_element_by_id("id_Password").send_keys("Master1234")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        try: self.assertTrue(self.is_element_present(By.ID, "id_Login"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_Password"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.XPATH, "//button[@type='submit']"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        
    def test_ZD(self):
        driver = self.driver
        driver.get(self.base_url + "/calendar/")
        driver.get(self.base_url + "/calendar/year")
        self.assertEqual("Login", driver.title)
        
    def test_ZE(self):
        driver = self.driver
        driver.get(self.base_url + "/calendar/")
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_id("id_Login").clear()
        driver.find_element_by_id("id_Login").send_keys("tester1234")
        driver.find_element_by_id("id_Password").clear()
        driver.find_element_by_id("id_Password").send_keys("tester1234")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_link_text("Options").click()
        driver.find_element_by_link_text("Yearly Calendar").click()
        driver.find_element_by_link_text("February").click()
        driver.find_element_by_xpath("//td[2]/a/img").click()
        try: self.assertEqual("March 2014", driver.find_element_by_css_selector("h2").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_xpath("//td[2]/a/img").click()
        try: self.assertEqual("April 2014", driver.find_element_by_css_selector("h2").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_xpath("//tr[2]/td/a/img").click()
        driver.find_element_by_xpath("//tr[2]/td/a/img").click()
        driver.find_element_by_xpath("//tr[2]/td/a/img").click()
        driver.find_element_by_xpath("//tr[2]/td/a/img").click()
        try: self.assertEqual("December 2013", driver.find_element_by_css_selector("h2").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("Options").click()

    def test_ZF(self):
        driver = self.driver
        driver.get(self.base_url + "/calendar/")
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_id("id_Login").clear()
        driver.find_element_by_id("id_Login").send_keys("tester1234")
        driver.find_element_by_id("id_Password").clear()
        driver.find_element_by_id("id_Password").send_keys("tester1234")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_link_text("Options").click()
        driver.find_element_by_link_text("Yearly Calendar").click()
        try: self.assertEqual("2014", driver.find_element_by_css_selector("h2").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_xpath("//a[2]/img").click()
        try: self.assertEqual("2017", driver.find_element_by_css_selector("h2").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_xpath("//a[2]/img").click()
        try: self.assertEqual("2020", driver.find_element_by_css_selector("h2").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_css_selector("a > img").click()
        driver.find_element_by_css_selector("a > img").click()
        driver.find_element_by_css_selector("a > img").click()
        try: self.assertEqual("2011", driver.find_element_by_css_selector("h2").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_css_selector("a > img").click()
        try: self.assertEqual("2008", driver.find_element_by_css_selector("h2").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("Options").click()

    def test_ZG(self):
        driver = self.driver
        #try:
        #    user = User.objects.get(username="testowytester")
        #    Entry.objects.all().delete()
        #except Exception,e:
        #    u = User.objects.create_user("testowytester", "test@o2.pl", "Master1234")
        #    u.save()
        driver.get(self.base_url + "/calendar/")
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_id("id_Login").clear()
        driver.find_element_by_id("id_Login").send_keys("tester1234")
        driver.find_element_by_id("id_Password").clear()
        driver.find_element_by_id("id_Password").send_keys("tester1234")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_link_text("Options").click()
        driver.find_element_by_link_text("Account details").click()
        driver.find_element_by_id("id_FirstName").clear()
        driver.find_element_by_id("id_FirstName").send_keys("Jan")
        driver.find_element_by_id("id_LastName").clear()
        driver.find_element_by_id("id_LastName").send_keys("Kowalsky")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "div.alert.alert-success"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_css_selector("img[alt=\"Back to Main Page\"]").click()
        driver.find_element_by_link_text("Options").click()
        driver.find_element_by_link_text("Account details").click()
        try: self.assertEqual("Jan", driver.find_element_by_id("id_FirstName").get_attribute("value"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Kowalsky", driver.find_element_by_id("id_LastName").get_attribute("value"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_id("id_FacebookId").clear()
        driver.find_element_by_id("id_FacebookId").send_keys("mateusz.bacal")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "div.alert.alert-success"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_css_selector("img[alt=\"Back to Main Page\"]").click()
        driver.find_element_by_link_text("Options").click()
        driver.find_element_by_link_text("Account details").click()
        try: self.assertEqual("mateusz.bacal", driver.find_element_by_id("id_FacebookId").get_attribute("value"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_css_selector("img[alt=\"Back to Main Page\"]").click()
        driver.find_element_by_link_text("Options").click()
        
    def test_ZH(self):
        driver = self.driver
        driver.get(self.base_url + "/calendar/accountdetails")
        self.assertEqual("Login", driver.title)
        try: self.assertEqual("Please log in", driver.find_element_by_css_selector("h2.form-signin-heading").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        
    def test_ZI(self):
        driver = self.driver
        #try:
        #    user = User.objects.get(username="testowytester")
        #    Entry.objects.all().delete()
        #except Exception,e:
        #    u = User.objects.create_user("testowytester", "test@o2.pl", "Master1234")
        #    u.save()
        driver.get(self.base_url + "/calendar/")
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_id("id_Login").clear()
        driver.find_element_by_id("id_Login").send_keys("tester1234")
        driver.find_element_by_id("id_Password").clear()
        driver.find_element_by_id("id_Password").send_keys("tester1234")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.get(self.base_url + "/calendar/accountdetails/")
        #driver.find_element_by_link_text("Account details").click()
        driver.find_element_by_id("ui-id-2").click()
        driver.find_element_by_id("id_OldPassword").clear()
        driver.find_element_by_id("id_OldPassword").send_keys("tester1234")
        driver.find_element_by_id("id_NewPassword").clear()
        driver.find_element_by_id("id_NewPassword").send_keys("tester12345")
        driver.find_element_by_id("id_RepeatNewPassword").clear()
        driver.find_element_by_id("id_RepeatNewPassword").send_keys("tester12345")
        driver.find_element_by_xpath("(//button[@type='submit'])[2]").click()
        driver.find_element_by_css_selector("img[alt=\"Back to Main Page\"]").click()
        driver.find_element_by_link_text("Options").click()
        driver.find_element_by_link_text("Logout").click()
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_id("id_Login").clear()
        driver.find_element_by_id("id_Login").send_keys("tester1234")
        driver.find_element_by_id("id_Password").clear()
        driver.find_element_by_id("id_Password").send_keys("tester12345")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        self.assertEqual("Django Calendar 2013-2014", driver.title)
        try: self.assertTrue(self.is_element_present(By.LINK_TEXT, "Options"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("Options").click()
        driver.find_element_by_link_text("Account details").click()
        driver.find_element_by_id("ui-id-2").click()
        driver.find_element_by_id("id_OldPassword").clear()
        driver.find_element_by_id("id_OldPassword").send_keys("tester12345")
        driver.find_element_by_id("id_NewPassword").clear()
        driver.find_element_by_id("id_NewPassword").send_keys("tester1234")
        driver.find_element_by_id("id_RepeatNewPassword").clear()
        driver.find_element_by_id("id_RepeatNewPassword").send_keys("tester1234")
        driver.find_element_by_xpath("(//button[@type='submit'])[2]").click()
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "div.alert.alert-success"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        

        
    def test_ZJ(self):
        driver = self.driver
        driver.get(self.base_url + "/calendar/")
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_id("id_Login").clear()
        driver.find_element_by_id("id_Login").send_keys("tester1234")
        driver.find_element_by_id("id_Password").clear()
        driver.find_element_by_id("id_Password").send_keys("tester1234")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_link_text("Options").click()
        driver.find_element_by_link_text("Yearly Calendar").click()
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "a > img"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.XPATH, "//a[2]/img"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("2014", driver.find_element_by_css_selector("h2").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("2015", driver.find_element_by_xpath("//table[2]/thead/tr/th/h2").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("2016", driver.find_element_by_xpath("//table[3]/thead/tr/th/h2").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("Options").click()
        driver.find_element_by_link_text("Logout").click()
        

    def test_ZK(self):
        driver = self.driver
        driver.get(self.base_url + "/calendar")
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_id("id_Login").clear()
        driver.find_element_by_id("id_Login").send_keys("tester1234")
        driver.find_element_by_id("id_Password").clear()
        driver.find_element_by_id("id_Password").send_keys("tester1234")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_link_text("Options").click()
        driver.find_element_by_link_text("Yearly Calendar").click()
        driver.find_element_by_link_text("February").click()
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "a > img"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.XPATH, "//tr[2]/td/a/img"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.XPATH, "//td[2]/a/img"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("February 2014", driver.find_element_by_css_selector("h2").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.XPATH, "//td[@onclick=\"parent.location='/calendar/day/2014/2/4/'\"]"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("Options").click()

    def test_ZL(self):
        driver = self.driver
        driver.get(self.base_url + "/calendar/")
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_id("id_Login").clear()
        driver.find_element_by_id("id_Login").send_keys("tester1234")
        driver.find_element_by_id("id_Password").clear()
        driver.find_element_by_id("id_Password").send_keys("tester1234")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_link_text("Options").click()
        driver.find_element_by_link_text("Yearly Calendar").click()
        driver.find_element_by_link_text("February").click()
        driver.find_element_by_xpath("//td[@onclick=\"parent.location='/calendar/day/2014/2/22/'\"]").click()
        try: self.assertTrue(self.is_element_present(By.ID, "id_form-0-DELETE"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_form-0-title"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_form-0-snippet"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_form-0-remind"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.ID, "id_form-0-body"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(self.is_element_present(By.XPATH, "//button[@value='Save']"))
        except AssertionError as e: self.verificationErrors.append(str(e))

    def test_ZM(self):
        driver = self.driver
        #try:
        #    user = User.objects.get(username="tester1234")
            #user = user.entry.objects.all().delete()
        #    Entry.objects.all().delete()
        #     Entry.save()
        #except Exception,e:
        #    u = User.objects.create_user("tester1234", "test@o2.pl", "tester1234")
        #    u.save()
        driver.get(self.base_url + "/calendar/")
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_id("id_Login").clear()
        driver.find_element_by_id("id_Login").send_keys("tester1234")
        driver.find_element_by_id("id_Password").clear()
        driver.find_element_by_id("id_Password").send_keys("tester1234")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_link_text("Options").click()
        driver.find_element_by_link_text("Yearly Calendar").click()
        driver.find_element_by_link_text("February").click()
        driver.find_element_by_css_selector("td.current").click()
        driver.find_element_by_id("id_form-0-title").clear()
        driver.find_element_by_id("id_form-0-title").send_keys("Test Tittle")
        driver.find_element_by_id("id_form-0-snippet").clear()
        driver.find_element_by_id("id_form-0-snippet").send_keys("Test Snippet")
        driver.find_element_by_id("id_form-0-remind").click()
        driver.find_element_by_id("id_form-0-body").clear()
        driver.find_element_by_id("id_form-0-body").send_keys("qwaesdrtfgyhuj")
        driver.find_element_by_xpath("//button[@value='Save']").click()
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "div.alert.alert-success"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_css_selector("font > b").click()
        driver.find_element_by_id("id_form-0-DELETE").click()
        driver.find_element_by_xpath("//button[@value='Save']").click()
    
    
    def test_ZN(self):
        self.client = Client()
        response = self.client.get('/calendar/')
        try:
            self.assertEqual(response.status_code, 200)
        except AssertionError as e: self.verificationErrors.append(str(e))
    
    def test_ZO(self):
        self.client = Client()
        response = self.client.get('/calendar/testowe/')
        try:
            self.assertEqual(response.status_code, 404)
        except AssertionError as e: self.verificationErrors.append(str(e))
    
    def test_ZP(self):
        self.client = Client()
        user = User.objects.create_user('tester1234', 'lennon@thebeatles.com', 'tester1234')
        user.save()
        response = self.client.post('/calendar/login/',{'Login':'tester1234','Password':'tester1234'},follow=True)
        try:
            self.assertEqual(response.status_code, 200)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try:
            self.assertEqual("Django Calendar 2013-2014" in response.content, True)
        except AssertionError as e: self.verificationErrors.append(str(e))
        user.delete()

    def  test_ZR(self):
        factory = RequestFactory()
        request = factory.get('/calendar/',follow=True)
        user = User.objects.create_user('tester1234', 'lennon@thebeatles.com', 'tester1234')
        user.save()
        request.user = user
        response = index(request)
        try:
            self.assertEqual("Django Calendar 2013-2014" in response.content, True)
        except AssertionError as e: self.verificationErrors.append(str(e))
        user.delete()

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)
