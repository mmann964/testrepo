from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from element import BasePageElement
from locators import LoginPageLocators
from locators import WorkspacePageLocators
from locators import NewApplicationDialogLocators
from locators import TopNavLocators
from locators import DeleteItemsDialogLocator
from locators import ManageColorsDialogLocators
from locators import ManageFontsDialogLocators
from locators import ManageImagesDialogLocators
from locators import LeftNavLocators
from locators import NewScreenDialogLocators
from locators import NewPanelDialogLocators
from locators import DeleteScreensDialogLocators
import time
#import locators


class TextElement(BasePageElement):
    def __init__(self, *locator):
        self.locator = locator

class BasePage(object):
    """Base class to initialize the base page that will be called from all pages"""

    def __init__(self, driver):
        self.driver = driver

    def check_object_exists(self, *locator):
        """returns true of the object exists, false if it doesn't"""
        try:
            #lambda driver: self.driver.find_element(*locator)
            self.driver.find_element(*locator)
        except NoSuchElementException:
            return False
        return True

    def click_object(self, *locator):
        """clicks on object"""
        WebDriverWait(self.driver, 20).until(
            lambda driver: self.driver.find_element(*locator)
        )
        element = self.driver.find_element(*locator)
        for x in range(0, 20):
            try:
                str_error = None
                element.click()
                #self.driver.execute_script("element[0].click()")  #Nope.  Slow.  And doesn't seem to work.
                #element.send_keys(Keys.RETURN)  #Nope.  Doesn't work and causes Safari to think something interfered manually with the browser

            except Exception as str_error:
                pass

            if str_error:
                time.sleep(1)
            else:
                break

    def double_click_object(self, *locator):
        """double clicks object"""
        WebDriverWait(self.driver, 20).until(
            lambda driver: self.driver.find_element(*locator)
        )
        element = self.driver.find_element(*locator)
        actionChains = ActionChains(self.driver)
        actionChains.double_click(element).perform()

class BaseDialog(BasePage):
    """Bass class to initialize basic dialog functionality"""

    def is_title_matches(self, locatorClass, expectedTitle):
        """ Verifies the title """
        WebDriverWait(self.driver, 20).until(
            lambda driver: self.driver.find_element(*locatorClass.title_bar)
        )
        return expectedTitle in self.driver.find_element(*locatorClass.title_bar).text

    def click_close_button(self, locatorClass):
        self.click_object(*locatorClass.close_button)

    def click_cancel_button(self, locatorClass):
        self.click_object(*locatorClass.cancel_button)

    def click_ok_button(self, locatorClass):
        self.click_object(*locatorClass.ok_button)

class LoginPage(BasePage):
    """ Login page action methods go here"""
    expectedTitle = "Sign In"

    #fields with user input
    username_field = TextElement(*LoginPageLocators.uname_field)
    password_field = TextElement(*LoginPageLocators.pwd_field)
    signin_button = TextElement(*LoginPageLocators.signin_button)

    def is_title_matches(self):
        """Verifies that the hardcoded text "Sign In" appears in page title"""
        return self.expectedTitle in self.driver.title

    def click_sign_in_button(self):
        """Clicks Sign In to attempt to login"""
        self.click_object(*LoginPageLocators.signin_button)

    def get_version(self):
        """gets the version string"""
        WebDriverWait(self.driver, 100).until(
            lambda driver: self.driver.find_element(*LoginPageLocators.version_ctrl))
        element = self.driver.find_element(*LoginPageLocators.version_ctrl)
        return element.text

    def login(self, uname, pwd):
        """Logs in with valid name and password"""
        self.username_field = uname
        self.password_field = pwd
        self.click_sign_in_button()


class WorkspacePage(BasePage):
    """ Workspace page action methods go here"""
    expectedTitle = "P2UX Builder"

    def is_title_matches(self):
        """Verifies that the hardcoded text P2UX Builder appears in page title"""
        return self.expectedTitle in self.driver.title

    def click_add_app_tile(self):
        """Clicks the + button to start adding an app"""
        self.click_object(*WorkspacePageLocators.add_app_tile)

    # define the show dropdown

    def openApp(self, app_name):
        """Double clicks on app with given name"""
        locatorStr = ('//*[@title="' + app_name + '"]')
        self.double_click_object(By.XPATH, locatorStr)

    def selectApp(self, app_name):
        """Clicks on app with given name"""
        time.sleep(2)  #this is a hack.  Otherwise it won't find the app consistently.  Need to double-check implicit/explicit waits
        #locatorStr = ('//*[@title="' + app_name + '"]')
        #self.click_object(By.XPATH, locatorStr)
        app_tile = WorkspacePageLocators(app_name)
        self.click_object(*app_tile.app_tile)

    def deleteApp(self, app_name, permDelete = True):
        """Deletes app with given name"""
        delete_items_dialog = DeleteItemsDialog(self.driver)
        self.selectApp(app_name)
        self.click_object(*TopNavLocators.delete_icon)
        # deal with permanently delete dialog if it comes up
        if (self.check_object_exists(*DeleteItemsDialogLocator.title_bar)):
            if (permDelete == True):
                delete_items_dialog.click_yes_button()
            else:
                delete_items_dialog.click_no_button()

    def does_app_exist(self, app_name):
        """Returns true if app tile exists, false if it doesn't"""
        locatorStr = ('//*[@title="' + app_name + '"]')
        if self.check_object_exists(By.XPATH, locatorStr):
            return True
        else:
            return False


    # the top nav sections will go into separate classes, since they're used in other pages

class DeleteItemsDialog(BasePage):
    expectedTitle = "Delete Items"

    def is_title_matches(self):
        """ Verifies the title """
        WebDriverWait(self.driver, 20).until(
            lambda driver: self.driver.find_element(*DeleteItemsDialogLocator.title_bar)
        )
        return self.expectedTitle in self.driver.find_element(*DeleteItemsDialogLocator.title_bar).text

    def click_yes_button(self):
        self.click_object(*DeleteItemsDialogLocator.yes_button)

    def click_no_button(self):
        self.click_object(*DeleteItemsDialogLocator.no_button)

class ManageColorsDialog(BasePage):
    expectedTitle = "Manage colors"
    locatorClass = ManageColorsDialogLocators

    def is_title_matches(self, locatorClass=locatorClass):
        """ Verifies the title """
        WebDriverWait(self.driver, 20).until(
            lambda driver: self.driver.find_element(*locatorClass.title_bar)
        )
        return self.expectedTitle in self.driver.find_element(*locatorClass.title_bar).text

    #close button
    #done button
    #colors button
    #gradient button
    #+ button
    #individual color buttons
    def click_close_button(self, locatorClass=locatorClass):
        self.click_object(*locatorClass.close_button)

    def click_done_button(self, locatorClass=locatorClass):
        self.click_object(*locatorClass.done_button)

class ManageFontsDialog(BasePage):
    expectedTitle = "Manage Fonts"
    locatorClass = ManageFontsDialogLocators

    def is_title_matches(self, locatorClass=locatorClass):
        """ Verifies the title """
        WebDriverWait(self.driver, 20).until(
            lambda driver: self.driver.find_element(*locatorClass.title_bar)
        )
        return self.expectedTitle in self.driver.find_element(*locatorClass.title_bar).text

    #+ button
    #individual font buttons
    def click_close_button(self, locatorClass=locatorClass):
        self.click_object(*locatorClass.close_button)

    def click_done_button(self, locatorClass=locatorClass):
        self.click_object(*locatorClass.done_button)

class ManageImagesDialog(BasePage):
    expectedTitle = "Manage Images"
    locatorClass = ManageImagesDialogLocators

    def is_title_matches(self, locatorClass=locatorClass):
        """ Verifies the title """
        WebDriverWait(self.driver, 20).until(
            lambda driver: self.driver.find_element(*locatorClass.title_bar)
        )
        return self.expectedTitle in self.driver.find_element(*locatorClass.title_bar).text

    #+ button
    #individual font buttons
    def click_close_button(self, locatorClass=locatorClass):
        self.click_object(*locatorClass.close_button)

    def click_ok_button(self, locatorClass=locatorClass):
        self.click_object(*locatorClass.ok_button)

class NewApplicationDialog(BasePage):
    """ New Application dialog action methods go here """
    expectedTitle = "New Application"

    #fields with user input
    appname_field = TextElement(*NewApplicationDialogLocators.name_field)

    def is_title_matches(self):
        """ Verifies the title """
        WebDriverWait(self.driver, 2).until(
            lambda driver: self.driver.find_element(*NewApplicationDialogLocators.close_button)
        )
        return self.expectedTitle in self.driver.find_element(*NewApplicationDialogLocators.title_bar).text

    def click_close_button(self):
        self.click_object(*NewApplicationDialogLocators.close_button)

    def click_cancel_button(self):
        self.click_object(*NewApplicationDialogLocators.cancel_button)

    def click_done_button(self):
        self.click_object(*NewApplicationDialogLocators.done_button)

    def click_next_button(self):
        self.click_object(*NewApplicationDialogLocators.next_button)

    #def click_add_design_button(self):
    #    self.click_object(*NewApplicationDialogLocators.add_design_button)

    def createApp(self, app_name):
        """ Creates an app with the given name"""
        self.appname_field = app_name
        #time.sleep(2)
        self.click_next_button()
        self.click_done_button()

                # Close button - the X at the upper right of the dialog
        #close_button = (By.XPATH, "//div/class='icon icon-Cancel'")
        # Cancel button
        # Done button
        # Name field
        # Description field
        # Status Bar dropdown
        # Device dropdown
        # OS dropdown
        # Orientation dropdown
        # Design Template dropdown
        # Add Design button
        # Also need form factor tree

class TopNav(BasePage):
    """Top Navigation methods go here"""
    search_field = TextElement(*TopNavLocators.search_box)

    def click_MyApps_link(self):
        self.click_object(*TopNavLocators.MyApps_link)

    def click_fonts_icon(self):
        self.click_object(*TopNavLocators.fonts_icon)

    def click_images_icon(self):
        self.click_object(*TopNavLocators.images_icon)

    def click_colors_icon(self):
        self.click_object(*TopNavLocators.colors_icon)

    def logout(self):
        """Logs out"""
        WebDriverWait(self.driver, 2).until(
            lambda driver: self.driver.find_element(*TopNavLocators.menu_dropdown)
        )
        self.click_object(*TopNavLocators.menu_dropdown)
        time.sleep(2)
        #WebDriverWait(self.driver, 5).until(
        #    lambda driver: self.driver.find_element(*TopNavLocators.logout_menu)
        #)
        self.click_object(*TopNavLocators.logout_menu)

class LeftNav(BasePage):
    """Left Navigation methods go here"""
    locatorClass = LeftNavLocators

    def click_new_screen(self, locatorClass=locatorClass):
        self.click_object(*locatorClass.New_Screen)

    def click_new_panel(self, locatorClass=locatorClass):
        self.click_object(*locatorClass.New_Panel)


class NewScreenDialog(BaseDialog):
    """New Screen dialog action methods go here"""
    expectedTitle = "New Screen"
    locatorClass = NewScreenDialogLocators

    #fields with user input
    screenname_field = TextElement(*locatorClass.name_field)

    def createScreen(self, screen_name):
        """ Creates an app with the given name"""
        self.screenname_field = screen_name
        #time.sleep(2)
        self.click_ok_button(self.locatorClass)

class NewScreenDialogOld(BasePage):
    """ New Screen dialog action methods go here """
    expectedTitle = "New Screen"
    locatorClass = NewScreenDialogLocators

    #fields with user input
    screenname_field = TextElement(*locatorClass.name_field)

    def is_title_matches(self, locatorClass=locatorClass):
        """ Verifies the title """
        WebDriverWait(self.driver, 20).until(
            lambda driver: self.driver.find_element(*locatorClass.title_bar)
        )
        return self.expectedTitle in self.driver.find_element(*locatorClass.title_bar).text


    def click_close_button(self, locatorClass=locatorClass):
        self.click_object(*locatorClass.close_button)

    def click_cancel_button(self, locatorClass=locatorClass):
        self.click_object(*locatorClass.cancel_button)

    def click_ok_button(self, locatorClass=locatorClass):
        self.click_object(*locatorClass.ok_button)

    def createScreen(self, screen_name):
        """ Creates an app with the given name"""
        self.screenname_field = screen_name
        #time.sleep(2)
        self.click_ok_button()

class NewPanelDialog(BasePage):
    """ New Panel dialog action methods go here """
    expectedTitle = "New Panel"
    locatorClass = NewPanelDialogLocators

    #fields with user input
    panelname_field = TextElement(*locatorClass.name_field)
    width_field = TextElement(*locatorClass.width_field)
    height_field = TextElement(*locatorClass.height_field)

    def is_title_matches(self, locatorClass=locatorClass):
        """ Verifies the title """
        WebDriverWait(self.driver, 20).until(
            lambda driver: self.driver.find_element(*locatorClass.title_bar)
        )
        return self.expectedTitle in self.driver.find_element(*locatorClass.title_bar).text


    def click_close_button(self, locatorClass=locatorClass):
        self.click_object(*locatorClass.close_button)

    def click_cancel_button(self, locatorClass=locatorClass):
        self.click_object(*locatorClass.cancel_button)

    def click_ok_button(self, locatorClass=locatorClass):
        self.click_object(*locatorClass.ok_button)

    def createPanel(self, panel_name, width = 100, height = 100):
        """ Creates an app with the given name"""
        self.panelname_field = panel_name
        if width != 100:
            self.width_field = ""
            self.width_field = width
        if height != 100:
            self.height_field = ""
            self.height_field = height
        #time.sleep(2)
        self.click_ok_button()

class DeleteScreensDialog(BasePage):
    """ Delete Screens dialog action methods go here """
    expectedTitle = "Delete Screens"
    locatorClass = DeleteScreensDialogLocators

    def is_title_matches(self, locatorClass=locatorClass):
        """ Verifies the title """
        WebDriverWait(self.driver, 20).until(
            lambda driver: self.driver.find_element(*locatorClass.title_bar)
        )
        return self.expectedTitle in self.driver.find_element(*locatorClass.title_bar).text


    def click_close_button(self, locatorClass=locatorClass):
        self.click_object(*locatorClass.close_button)

    def click_cancel_button(self, locatorClass=locatorClass):
        self.click_object(*locatorClass.cancel_button)

    def click_ok_button(self, locatorClass=locatorClass):
        self.click_object(*locatorClass.ok_button)