import time
import unittest
import base64
import xml.etree.ElementTree as ET
from selenium import webdriver
import page

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

print "browserType: " + browserType
print "url: " + url
print "uname: " + uname
print "passwordEnc: " + passwordEnc
passwordDec = base64.b64decode(passwordEnc)
app_name = "SeleniumSmokeTest"

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
        LOGGER.debug("Could not get browser logs for driver %s due to exception: %s",
                     driver, e)
        return []

    errors = []
    for entry in browserlogs:
        if entry['level'] == 'SEVERE':
            errors.append(entry)
    return errors


class P2uxSmokeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if browserType == "1":
            print "Browser = Chrome"
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

    @unittest.skip("skipping for now.")
    def test_00_misc(self):
        """Verify you can login with valid credentials"""
        #app_name = "MelSelenium"

        login_page = page.LoginPage(self.driver)
        top_nav = page.TopNav(self.driver)
        workspace_page = page.WorkspacePage(self.driver)
        newapp_dialog = page.NewApplicationDialog(self.driver)

        assert login_page.is_title_matches(), "Login Screen title doesn't match."
        verStr = login_page.get_version()
        print "\nVersion = " + verStr

        login_page.login(uname, passwordDec)
        assert workspace_page.is_title_matches, "Not in Workspace Page after logging in."
        time.sleep(2)

        #top_nav.logout()  #I can't get the logout menu to work to save my life :-/
        #time.sleep(5)
        #assert login_page.is_title_matches(), "Login Screen title doesn't match."
        #exit()

        workspace_page.click_add_app_tile()
        assert newapp_dialog.is_title_matches(), "Not in New Application dialog."
        newapp_dialog.createApp(app_name)

        time.sleep(2)
        workspace_page.openApp(app_name)
        time.sleep(2)
        top_nav.click_MyApps_link()
        workspace_page.deleteApp(app_name)
        time.sleep(2)
        #workspace_page.deleteApp("defaults", False)
        # newapp_dialog.click_close_button()  #this is an example of deleting an app without the permanently delete confirmation

        #top_nav.logout()
        #time.sleep(2)


    def test_01_login(self):
        """Check that you can login with valid credentials"""
        login_page = page.LoginPage(self.driver)
        workspace_page = page.WorkspacePage(self.driver)

        verStr = login_page.get_version()
        print "\nVersion = " + verStr
        assert login_page.is_title_matches(), "Login Screen title doesn't match."

        login_page.login(uname, passwordDec)
        assert workspace_page.is_title_matches, "Not in Workspace Page after logging in."


    #@unittest.skip("skipping for now.")
    def test_02_start_new_app(self):
        """Check that you can create a new app"""
        workspace_page = page.WorkspacePage(self.driver)
        newapp_dialog = page.NewApplicationDialog(self.driver)

        workspace_page.click_add_app_tile()
        assert newapp_dialog.is_title_matches(), "Not in New Application dialog."

        newapp_dialog.createApp(app_name)
        assert workspace_page.does_app_exist(app_name), True


    #@unittest.skip("skipping for now.")
    def test_03_manage_options(self):
        """Check that you can select each of the manage options from the top nav"""
        top_nav = page.TopNav(self.driver)
        workspace_page = page.WorkspacePage(self.driver)
        manage_fonts_dialog = page.ManageFontsDialog(self.driver)
        manage_images_dialog = page.ManageImagesDialog(self.driver)
        manage_colors_dialog = page.ManageColorsDialog(self.driver)

        #fonts
        top_nav.click_fonts_icon()
        assert manage_fonts_dialog.is_title_matches(), "Not in Manage Fonts dialog"
        manage_fonts_dialog.click_close_button()

        #images
        top_nav.click_images_icon()
        assert manage_images_dialog.is_title_matches(), "Not in Manage Images dialog"
        manage_images_dialog.click_close_button()

        #colors -- need to have app selected
        workspace_page.selectApp(app_name)
        top_nav.click_colors_icon()
        assert manage_colors_dialog.is_title_matches(), "Not in Manage Colors dialog"
        manage_colors_dialog.click_close_button()


    @unittest.skip("skipping for now.")
    def test_04_quick_search(self):
        """Check that you can use quick search from the top nav"""

    def tearDown(self):
        browserErrors = check_browser_errors(self.driver)

        if browserErrors:
            print "\n*****************************"
            print self.id() + " browser errors:"
            print browserErrors
            print "*****************************"


    @classmethod
    def tearDownClass(cls):
        workspace_page = page.WorkspacePage(cls.driver)
        #delete the app for now -- remove/move this as we start to add tests
        workspace_page.deleteApp(app_name)

        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
