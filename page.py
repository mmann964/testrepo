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
from locators import ManageStylesDialogLocators
from locators import LeftNavLocators
from locators import NewScreenDialogLocators
from locators import NewPanelDialogLocators
from locators import DeleteScreensDialogLocators
from locators import AppEditorPageLocators
from locators import ScreenEditorPageLocators
from locators import SizeAndPositionPaletteLocators
from locators import ToolTipDialog
import time
#import locators


class TextElement(BasePageElement):
    def __init__(self, *locator):
        self.locator = locator

class BasePage(object):
    """Base class to initialize the base page that will be called from all pages"""

    def __init__(self, driver):
        self.driver = driver

    def highlight(self, *locator):
        """Highlights (blinks) the element"""
        if self.check_object_exists(*locator):
            element = self.driver.find_element(*locator)
            original_style = element.get_attribute('style')
            self.driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element,
                                       "background: yellow; border: 2px solid red;")
            time.sleep(3)
            self.driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element,
                                       original_style)


    def check_object_exists(self, *locator):
        """returns true of the object exists, false if it doesn't"""
        try:
            #lambda driver: self.driver.find_element(*locator)
            self.driver.find_element(*locator)
        except NoSuchElementException:
            return False
        return True

    def dismiss_tooltip(self):
        """Look for the tooltip and close it if necessary"""
        time.sleep(.5)  # give it time to come up if it's going to come up
        self.driver.implicitly_wait(0)
        while self.check_object_exists(*ToolTipDialog.gotIt_btn):
            element = self.driver.find_element(*ToolTipDialog.gotIt_btn)
            element.click()
        self.driver.implicitly_wait(3)
        time.sleep(.5)


    def click_object(self, *locator):
        """clicks on object"""
        self.dismiss_tooltip()
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
        self.dismiss_tooltip()
        WebDriverWait(self.driver, 20).until(
            lambda driver: self.driver.find_element(*locator)
        )
        element = self.driver.find_element(*locator)
        actionChains = ActionChains(self.driver)
        actionChains.double_click(element).perform()

    def click_object_at_location(self, xoffset, yoffset, *locator):
        """clicks object at x, y offset"""
        self.dismiss_tooltip()
        WebDriverWait(self.driver, 20).until(
            lambda driver: self.driver.find_element(*locator)
        )
        element = self.driver.find_element(*locator)
        actionChains = ActionChains(self.driver)
        actionChains.move_to_element_with_offset(element, xoffset, yoffset).click().perform()


class BaseDialog(BasePage):
    """Bass class to initialize basic dialog functionality"""
    expectedTitle = ""
    locatorClass = ManageColorsDialogLocators  # the child class will override, but you need to
                                               # initialize it with something in the parent class


    def does_title_match(self, locatorClass=locatorClass):
        """Verifies the title"""
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

class LoginPage(BasePage):
    """ Login page action methods go here"""
    expectedTitle = "Sign In"

    #fields with user input
    username_field = TextElement(*LoginPageLocators.uname_field)
    password_field = TextElement(*LoginPageLocators.pwd_field)
    signin_button = TextElement(*LoginPageLocators.signin_button)

    def does_title_match(self):
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

    def does_title_match(self):
        """Verifies the page title"""
        return self.expectedTitle in self.driver.title

    def click_add_app_tile(self):
        """Clicks the + button to start adding an app"""
        self.click_object(*WorkspacePageLocators.add_app_tile)

    # define the show dropdown

    def openApp(self, app_name):
        """Double clicks on app with given name"""
        time.sleep(2)
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

class DeleteItemsDialog(BaseDialog):
    expectedTitle = "Delete Items"
    locatorClass = DeleteItemsDialogLocator

    def click_yes_button(self, locatorClass=locatorClass):
        self.click_object(*locatorClass.yes_button)

    def click_no_button(self, locatorClass=locatorClass):
        self.click_object(*locatorClass.no_button)

class ManageColorsDialog(BaseDialog):
    expectedTitle = "Manage colors"
    locatorClass = ManageColorsDialogLocators

    #close button
    #done button
    #colors button
    #gradient button
    #+ button
    #individual color buttons

    def click_done_button(self, locatorClass=locatorClass):
        self.click_object(*locatorClass.done_button)

class ManageFontsDialog(BaseDialog):
    expectedTitle = "Manage Fonts"
    locatorClass = ManageFontsDialogLocators

    #+ button
    #individual font buttons
    def click_done_button(self, locatorClass=locatorClass):
        self.click_object(*locatorClass.done_button)

class ManageImagesDialog(BaseDialog):
    expectedTitle = "Manage Images"
    locatorClass = ManageImagesDialogLocators

class ManageStylesDialog(BaseDialog):
    expectedTitle = "Manage Styles"
    locatorClass = ManageStylesDialogLocators

class NewApplicationDialog(BaseDialog):
    """ New Application dialog action methods go here """
    expectedTitle = "New Application"
    locatorClass = NewApplicationDialogLocators

    #fields with user input
    appname_field = TextElement(*locatorClass.name_field)
    #appname_field = TextElement(*NewApplicationDialogLocators.name_field)

    def click_done_button(self, locatorClass=locatorClass):
        self.click_object(*locatorClass.done_button)

    def click_next_button(self, locatorClass=locatorClass):
        self.click_object(*locatorClass.next_button)

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
    locatorClass = TopNavLocators
    search_field = TextElement(*locatorClass.search_box)

    def click_MyApps_link(self, locatorClass=locatorClass):
        self.click_object(*locatorClass.MyApps_link)

    def click_fonts_icon(self, locatorClass=locatorClass):
        self.click_object(*locatorClass.fonts_icon)

    def click_images_icon(self, locatorClass=locatorClass):
        self.click_object(*locatorClass.images_icon)

    def click_colors_icon(self, locatorClass=locatorClass):
        self.click_object(*locatorClass.colors_icon)

    def click_styles_icon(self, locatorClass=locatorClass):
        self.click_object(*locatorClass.styles_icon)

    def click_app_link(self, locatorClass=locatorClass):
        self.click_object(*locatorClass.app_link)

    def logout(self, locatorClass=locatorClass):
        """Logs out"""
        WebDriverWait(self.driver, 2).until(
            lambda driver: self.driver.find_element(*locatorClass.user_menu_dropdown)
        )
        self.click_object(*locatorClass.user_menu_dropdown)
        self.click_object(*locatorClass.logout_menu)

class LeftNav(BasePage):
    """Left Navigation methods go here"""
    locatorClass = LeftNavLocators

    def click_new_screen(self, locatorClass=locatorClass):
        #Workaround for BUILDER-1381:  wait for Home screen tile to load before clicking New Screen
        wait = WebDriverWait(self.driver, 10)
        #screen_tile = AppEditorPageLocators("Home")
        #element = wait.until(expected_conditions.element_to_be_clickable((*screen_tile.screen_tile)))  #syntax error
        element = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//*[@title="Home"]/..//*[@class="screen-card__img"]')))

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
        self.click_ok_button()

class NewPanelDialog(BaseDialog):
    """ New Panel dialog action methods go here """
    expectedTitle = "New Panel"
    locatorClass = NewPanelDialogLocators

    #fields with user input
    panelname_field = TextElement(*locatorClass.name_field)
    width_field = TextElement(*locatorClass.width_field)
    height_field = TextElement(*locatorClass.height_field)

    def createPanel(self, panel_name, width = 100, height = 100):
        """ Creates an app with the given name"""
        self.panelname_field = panel_name
        if width != 100:
            self.width_field = ""
            self.width_field = width
        if height != 100:
            self.height_field = ""
            self.height_field = height
        self.click_ok_button()

class DeleteScreensDialog(BaseDialog):
    """ Delete Screens dialog action methods go here """
    expectedTitle = "Delete Screens"
    locatorClass = DeleteScreensDialogLocators

class AppEditorPage(BasePage):
    """ App Editor page action methods go here"""
    expectedTitle = "P2UX Builder"

    def does_title_match(self):
        """Verifies the page title"""
        return self.expectedTitle in self.driver.title

    def openScreen(self, screen_name):
        """Double clicks on app with given name"""
        time.sleep(1)
        screen_tile = AppEditorPageLocators(screen_name)
        self.double_click_object(*screen_tile.screen_tile)

    def selectScreen(self, screen_name):
        """Clicks on screen with given name"""
        time.sleep(1)  #this is a hack.  Otherwise it won't find the app consistently.  Need to double-check implicit/explicit waits
        screen_tile = AppEditorPageLocators(screen_name)
        self.click_object_at_location(1, 1, *screen_tile.screen_tile)  #clicking without specifying location opens the screen

    def deleteScreen(self, screen_name):
        """Deletes screen with given name"""
        delete_screens_dialog = DeleteScreensDialog(self.driver)
        self.selectScreen(screen_name)
        self.click_object(*TopNavLocators.delete_icon)
        time.sleep(1)
        delete_screens_dialog.click_ok_button(delete_screens_dialog.locatorClass)
        time.sleep(1)

    def does_screen_exist(self, screen_name):
        """Returns true if screen tile exists, false if it doesn't"""
        locatorStr = ('//*[@title="' + screen_name + '"]')
        if self.check_object_exists(By.XPATH, locatorStr):
            return True
        else:
            return False


class ScreenEditorPage(BasePage):
    """ Screen Editor page action methods go here"""
    expectedTitle = "P2UX Builder"
    locatorClass = ScreenEditorPageLocators

    def does_title_match(self):
        """Verifies the page title"""
        return self.expectedTitle in self.driver.title

    def add_image_control(self, locatorClass=locatorClass):
        #self.double_click_object(*locatorClass.ImageControl)
        self.click_object(*locatorClass.ImageControl)

    def add_button_control(self, locatorClass=locatorClass):
        #self.double_click_object(*locatorClass.ButtonControl)
        self.click_object(*locatorClass.ButtonControl)

    def add_radio_control(self, locatorClass=locatorClass):
        #self.double_click_object(*locatorClass.RadioControl)
        self.click_object(*locatorClass.RadioControl)

    def add_toggle_control(self, locatorClass=locatorClass):
        self.click_object(*locatorClass.ToggleControl)

    def add_map_control(self, locatorClass=locatorClass):
        self.click_object(*locatorClass.MapControl)

    def add_radial_progress_control(self, locatorClass=locatorClass):
        self.click_object(*locatorClass.RadialProgressControl)

    def add_progress_control(self, locatorClass=locatorClass):
        self.click_object(*locatorClass.ProgressControl)

    def add_slider_control(self, locatorClass=locatorClass):
        self.click_object(*locatorClass.SliderControl)

    def add_scrollcontainer_control(self, locatorClass=locatorClass):
        self.click_object(*locatorClass.ScrollContainerControl)

    def add_text_input_control(self, locatorClass=locatorClass):
        self.click_object(*locatorClass.TextInputControl)

    def add_web_view_control(self, locatorClass=locatorClass):
        self.click_object(*locatorClass.WebViewControl)

    def add_custom_control(self, locatorClass=locatorClass):
        self.click_object(*locatorClass.CustomControl)

    def add_list_collection_control(self, locatorClass=locatorClass):
        self.click_object(*locatorClass.ListCollectionControl)

    def add_grid_collection_control(self, locatorClass=locatorClass):
        self.click_object(*locatorClass.GridCollectionControl)

    def add_page_indicator_control(self, locatorClass=locatorClass):
        self.click_object(*locatorClass.PageIndicatorControl)

    def selectComponent(self, component_name):
        """Selects the component with given name"""
        time.sleep(1)  #this is a hack.  Otherwise it won't find the app consistently.  Need to double-check implicit/explicit waits
        component_tiles = ScreenEditorPageLocators(component_name)
        self.click_object_at_location(1, 1, *component_tiles.component_name_tile)  #clicking without specifying location opens the screen

    def hideOrShowComponent(self, component_name):
        """Clicks hide/show button for component with given name"""
        # Should add separate functions for hide and show, based on the current state
        time.sleep(1)  #this is a hack.  Otherwise it won't find the app consistently.  Need to double-check implicit/explicit waits
        component_tiles = ScreenEditorPageLocators(component_name)
        self.click_object(*component_tiles.component_visible_button)

    def lockComponent(self, component_name):
        """Clicks lock/unlock button for component with given name"""
        # Should add separate functions for lock and unlock, based on current state
        time.sleep(1)  #this is a hack.  Otherwise it won't find the app consistently.  Need to double-check implicit/explicit waits
        component_tiles = ScreenEditorPageLocators(component_name)
        self.click_object(*component_tiles.component_lock_button)

    def copyComponent(self, component_name, locatorClass=locatorClass):
        """Selects the given component and copies it"""
        time.sleep(1)
        self.selectComponent(component_name)
        # self.highlight(*locatorClass.copy_component_button)
        self.click_object(*locatorClass.copy_component_button)

    def deleteComponent(self, component_name, locatorClass=locatorClass):
        """Selects the given component and copies it"""
        time.sleep(1)
        self.selectComponent(component_name)
        #self.highlight(*locatorClass.delete_component_button)
        self.click_object(*locatorClass.delete_component_button)

class SizeAndPositionPalette(BasePage):
    """Size and Position Palette page action methods go here"""
    locatorClass = SizeAndPositionPaletteLocators

    #fields with user input
    width = TextElement(*locatorClass.width)

    def highlightWidth(self, locatorClass=locatorClass):
        self.highlight(*locatorClass.width)

    def getWidth(self):
        return self.width

    def setWidth(self, val):
        self.width = ""
        self.width = val