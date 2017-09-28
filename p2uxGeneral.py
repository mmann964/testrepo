import unittest
import time
import base64
import xml.etree.ElementTree as ET
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import logging


# to run, type one of these commands at the bash prompt:
# python p2uxlogin.py
# nosetests --nocapture p2uxlogin.py
# nosetests --verbosity=3 --nocapture p2uxlogin.py

tree = ET.parse('ConfigSettings.xml')
root = tree.getroot()
browserType = root.find('browserType').text
url = root.find('url').text
uname = root.find('uname').text
passwordEnc = root.find('passwordEnc').text
headless = int(root.find('headless').text)

print "browserType: " + browserType
print "url: " + url
print "uname: " + uname
print "passwordEnc: " + passwordEnc
print "headless: " + str(headless)
passwordDec = base64.b64decode(passwordEnc)

def check_browser_errors(driver):
    """
    Checks browser for errors, returns a list of errors
    :param driver:
    :return:
    """
    try:
        browserlogs = driver.get_log('browser')
    except (ValueError, WebDriverException) as e:
        # Some browsers does not support getting logs
        logging.debug("Could not get browser logs for driver %s due to exception: %s",
                     driver, e)
        return []

    errors = []
    for entry in browserlogs:
        if entry['level'] == 'SEVERE':
            errors.append(entry)
    return errors



class P2uxBaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if browserType == "1":
            print "Browser = Chrome"
            if headless > 0:
                options = webdriver.ChromeOptions()
                options.add_argument('headless')
                cls.driver = webdriver.Chrome(chrome_options=options)
            else:
                cls.driver = webdriver.Chrome()
        elif browserType == "2":
            print "Browser = Firefox"
            fp = webdriver.FirefoxProfile()
            fp.set_preference('webdriver_enable_native_events', True)
            cls.driver = webdriver.Firefox(firefox_profile=fp)
        elif browserType == "3":
            print "Browser = Safari"
            cls.driver = webdriver.Safari()
        else:
            print "Invalid entry for browser.  Exiting."
            exit()
        cls.driver.implicitly_wait(3)
        cls.driver.get(url)

    def setUp(self):
        # hack -- waiting allows Safari to load the javascript so we can do a click
        if browserType == "3":
            time.sleep(.5)

    def tearDown(self):
        browserErrors = check_browser_errors(self.driver)

        if browserErrors:
            print "\n*****************************"
            print self.id() + " browser errors:"
            print browserErrors
            print "*****************************"
            self.fail("Browser Errors reported in " + self.id())


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

