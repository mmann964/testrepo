import time
import unittest
import base64
import xml.etree.ElementTree as ET
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import logging
import page

# to run, type one of these commands at the bash prompt:
# python p2uxsmoke.py
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
app_name_copy = "SeleniumSmokeTestCopy"
screen_name = "SeleniumTestScreen"
panel_name = "SeleniumTestPanel"

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
            # cls.driver.maximize_window()
        else:
            print "Invalid entry for browser.  Exiting."
            exit()
        cls.driver.implicitly_wait(3)
        cls.driver.get(url)

    def setUp(self):
        # hack -- waiting allows Safari to load the javascript so we can do a click
        if browserType == "3":
            time.sleep(.5)

    @unittest.skip("skipping for now.")
    def test_00_misc(self):
        """Verify you can login with valid credentials"""
        #app_name = "MelSelenium"

        login_page = page.LoginPage(self.driver)
        top_nav = page.TopNav(self.driver)
        workspace_page = page.WorkspacePage(self.driver)
        newapp_dialog = page.NewApplicationDialog(self.driver)

        assert login_page.does_title_match(), "Login Screen title doesn't match."
        verStr = login_page.get_version()
        print "\nVersion = " + verStr

        login_page.login(uname, passwordDec)
        assert workspace_page.does_title_match(), "Not in Workspace Page after logging in."
        time.sleep(2)

        #top_nav.logout()  #I can't get the logout menu to work to save my life :-/
        #time.sleep(5)
        #assert login_page.is_title_matches(), "Login Screen title doesn't match."
        #exit()

        workspace_page.click_add_app_tile()
        assert newapp_dialog.does_title_match(), "Not in New Application dialog."
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
        assert login_page.does_title_match(), "Login Screen title doesn't match."

        login_page.login(uname, passwordDec)
        assert workspace_page.does_title_match, "Not in Workspace Page after logging in."


    #@unittest.skip("skipping for now.")
    def test_02_start_new_app(self):
        """Check that you can create a new app"""
        workspace_page = page.WorkspacePage(self.driver)
        top_nav = page.TopNav(self.driver)
        newapp_dialog = page.NewApplicationDialog(self.driver)

        workspace_page.click_add_app_tile()
        assert newapp_dialog.does_title_match(), "Not in New Application dialog."

        newapp_dialog.createApp(app_name)
        top_nav.click_MyApps_link()   # go back to the workspace
        assert workspace_page.does_app_exist(app_name), "App: " + app_name + " wasn't created."


    #@unittest.skip("skipping for now.")
    def test_03A_manage_fonts(self):
        """Check that you can select each of the manage options from the top nav"""
        top_nav = page.TopNav(self.driver)
        manage_fonts_dialog = page.ManageFontsDialog(self.driver)

        #fonts
        top_nav.click_fonts_icon()
        assert manage_fonts_dialog.does_title_match(), "Not in Manage Fonts dialog"
        manage_fonts_dialog.click_close_button()

    def test_03B_manage_images(self):
        """Check that you can select each of the manage options from the top nav"""
        top_nav = page.TopNav(self.driver)
        manage_images_dialog = page.ManageImagesDialog(self.driver)

        #images
        top_nav.click_images_icon()
        assert manage_images_dialog.does_title_match(), "Not in Manage Images dialog"
        #assert manage_images_dialog.is_title_matches(), "Not in Manage Images dialog"
        manage_images_dialog.click_close_button()

    def test_03C_manage_colors(self):
        """Check that you can select each of the manage options from the top nav"""
        top_nav = page.TopNav(self.driver)
        workspace_page = page.WorkspacePage(self.driver)
        manage_colors_dialog = page.ManageColorsDialog(self.driver)

        #colors -- need to have app selected
        workspace_page.selectApp(app_name)
        top_nav.click_colors_icon()
        assert manage_colors_dialog.does_title_match(), "Not in Manage Colors dialog"
        manage_colors_dialog.click_close_button()

    def test_03D_manage_styles(self):
        """Check that you can select each of the manage options from the top nav"""
        top_nav = page.TopNav(self.driver)
        workspace_page = page.WorkspacePage(self.driver)
        manage_styles_dialog = page.ManageStylesDialog(self.driver)

        #styles -- need to have app selected
        workspace_page.selectApp(app_name)
        top_nav.click_styles_icon()
        assert manage_styles_dialog.does_title_match(), "Not in Manage Styles dialog"
        manage_styles_dialog.click_close_button()

    def test_03E_manage_data(self):
        """Check that you can select each of the manage options from the top nav"""
        top_nav = page.TopNav(self.driver)
        workspace_page = page.WorkspacePage(self.driver)
        manage_data_dialog = page.ManageDataDialog(self.driver)

        #styles -- need to have app selected
        workspace_page.selectApp(app_name)
        top_nav.click_data_icon()
        assert manage_data_dialog.does_title_match(), "Not in Manage Styles dialog"
        manage_data_dialog.click_close_button()

    #@unittest.skip("skipping for now.")
    def test_04_quick_search(self):
        """Check that you can use quick search from the top nav"""
        top_nav = page.TopNav(self.driver)
        workspace_page = page.WorkspacePage(self.driver)

        #positive test -- should find the app
        top_nav.search_field = app_name
        assert workspace_page.does_app_exist(app_name), "App: " + app_name + " isn't shown."
        top_nav.search_field = ""

        #negative test -- shouldn't find the test app
        top_nav.search_field = "hello"
        self.assertFalse(workspace_page.does_app_exist(app_name), app_name + " shouldn't be present")

        #clear out the search filter
        top_nav.search_field = ""
        self.driver.refresh()

    # @unittest.skip("skipping for now.")
    def test_05_create_screen(self):
        """Check that you can open an app and create a new screen"""
        top_nav = page.TopNav(self.driver)
        workspace_page = page.WorkspacePage(self.driver)
        newscreen_dialog = page.NewScreenDialog(self.driver)
        left_nav = page.LeftNav(self.driver)
        app_editor = page.AppEditorPage(self.driver)

        workspace_page.openApp(app_name)
        left_nav.click_new_screen()
        newscreen_dialog.does_title_match(), "New Screen title doesn't match."
        newscreen_dialog.createScreen(screen_name)

        top_nav.click_MyApps_link()
        workspace_page.openApp(app_name)
        assert app_editor.does_screen_exist(screen_name), "Screen: " + screen_name + " wasn't created."

        #top_nav.click_MyApps_link()

    def test_06_add_item_to_screen(self):
        """Check that you can add an item to a screen"""
        top_nav = page.TopNav(self.driver)
        workspace_page = page.WorkspacePage(self.driver)
        app_editor = page.AppEditorPage(self.driver)
        screen_editor = page.ScreenEditorPage(self.driver)

        # from the workspace, open the screen
        top_nav.click_MyApps_link()
        workspace_page.openApp(app_name)
        assert app_editor.does_screen_exist(screen_name), "Screen: " + screen_name + " wasn't created."
        app_editor.openScreen(screen_name)

        # add the items to the screen
        screen_editor.add_button_control()
        screen_editor.add_toggle_control()

        # verify the items have been added to the screen after the screen is reloaded
        top_nav.click_MyApps_link()
        workspace_page.openApp(app_name)
        app_editor.openScreen(screen_name)
        assert screen_editor.does_component_exist("button-1"), "button-1 wasn't created."
        assert screen_editor.does_component_exist("toggle-1"), "toggle-1 wasn't created."

    def test_07_add_color_via_color_picker(self):
        """Add a color via the color picker"""
        top_nav = page.TopNav(self.driver)
        workspace_page = page.WorkspacePage(self.driver)
        app_editor = page.AppEditorPage(self.driver)
        screen_editor = page.ScreenEditorPage(self.driver)
        color_picker = page.ColorPickerDialog(self.driver)
        default_prop_palette = page.DefaultPropertiesPalette(self.driver)


        component_name = "button-1"

        # from the workspace, open the screen
        top_nav.click_MyApps_link()
        workspace_page.openApp(app_name)
        assert app_editor.does_screen_exist(screen_name), "Screen: " + screen_name + " wasn't created."
        app_editor.openScreen(screen_name)

        screen_editor.selectComponent(component_name)
        default_prop_palette.clickFillColorSwatch()
        # Add a new color
        color_picker.add_color("#ff0019ff", "Yellow")
        color_picker.click_close_button()

        # Verify that it was added -- would be nice to check the color name
        screen_editor.selectComponent(component_name)
        default_prop_palette.clickFillColorSwatch()
        x = color_picker.hex_field
        assert (x == "#ff0019ff"), "Color value is " + x + ". It should be #ff0019ff."
        color_picker.click_close_button()

    def test_08_update_color_via_color_picker(self):
        """Update a color via the color picker"""
        top_nav = page.TopNav(self.driver)
        workspace_page = page.WorkspacePage(self.driver)
        app_editor = page.AppEditorPage(self.driver)
        screen_editor = page.ScreenEditorPage(self.driver)
        color_picker = page.ColorPickerDialog(self.driver)
        default_prop_palette = page.DefaultPropertiesPalette(self.driver)

        component_name = "button-1"

        # from the workspace, open the screen
        top_nav.click_MyApps_link()
        workspace_page.openApp(app_name)
        assert app_editor.does_screen_exist(screen_name), "Screen: " + screen_name + " wasn't created."
        app_editor.openScreen(screen_name)

        screen_editor.selectComponent(component_name)
        default_prop_palette.clickFillColorSwatch()
        # Update the color
        color_picker.update_color("#ffff19ff")
        color_picker.click_close_button()

        # Verify that it was updated
        screen_editor.selectComponent(component_name)
        default_prop_palette.clickFillColorSwatch()
        x = color_picker.hex_field
        assert (x == "#ffff19ff"), "Color value is " + x + ". It should be #ffff19ff."
        color_picker.click_close_button()

    def test_09_copy_screen(self):
        """Check that you can copy a screen"""

        top_nav = page.TopNav(self.driver)
        workspace_page = page.WorkspacePage(self.driver)
        app_editor = page.AppEditorPage(self.driver)

        tScreenNameCopy = "SeleniumTestScreenCopy"

        top_nav.click_MyApps_link()
        workspace_page.openApp(app_name)
        app_editor.copyScreen(screen_name, tScreenNameCopy)

        # Verify that the new screen exists
        top_nav.click_MyApps_link()
        workspace_page.openApp(app_name)
        assert app_editor.does_screen_exist(tScreenNameCopy), "Screen: " + tScreenNameCopy + " wasn't created."

        top_nav.click_MyApps_link()

    def test_10_copy_app(self):
        """Check that you can copy an app"""

        top_nav = page.TopNav(self.driver)
        workspace_page = page.WorkspacePage(self.driver)
        app_editor = page.AppEditorPage(self.driver)

        top_nav.click_MyApps_link()
        workspace_page.copyApp(app_name, app_name_copy)

        # Verify that the new app exists
        top_nav.click_MyApps_link()
        assert workspace_page.does_app_exist(app_name_copy), "App: " + app_name_copy + " wasn't created."

        # Verify that you can open the new app
        workspace_page.openApp(app_name_copy)

        # Verify that the screen we created is there
        app_editor.does_screen_exist(screen_name)

        # Delete the app
        top_nav.click_MyApps_link()
        workspace_page.deleteApp(app_name_copy)


    def tearDown(self):
        time.sleep(2)  # without this, it may attribute the browser error to the wrong test case
        browserErrors = check_browser_errors(self.driver)

        if browserErrors:
            print "\n*****************************"
            print self.id() + " browser errors:"
            print browserErrors
            print "*****************************"
            self.fail("Browser Errors reported in " + self.id())


    @classmethod
    def tearDownClass(cls):
        if browserType == "3":
            time.sleep(.5)
        workspace_page = page.WorkspacePage(cls.driver)
        top_nav = page.TopNav(cls.driver)
        #top_nav.search_field = ""
        #cls.driver.refresh()
        #if browserType == "3":
        #    time.sleep(5)
        #    workspace_page = page.WorkspacePage(cls.driver)
        #    top_nav = page.TopNav(cls.driver)


        #delete the app for now -- remove/move this as we start to add tests
        top_nav.click_MyApps_link()

        if (workspace_page.does_app_exist(app_name) == True):
            workspace_page.deleteApp(app_name)

        if (workspace_page.does_app_exist(app_name_copy) == True):
            workspace_page.deleteApp(app_name_copy)


        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
