from selenium.webdriver.common.by import By

class DialogLocators(object):
    """A generic class for dialog locators"""
    title_bar = (By.XPATH, '//*[@class="dialog__title-text ng-binding"]')
    close_button = (By.XPATH, '//*[@class="icon icon-Cancel"]')
    ok_button = (By.CSS_SELECTOR, 'button.btn--dialog.ok')
    cancel_button = (By.CSS_SELECTOR, 'button.btn--dialog')

class LoginPageLocators(object):
    """A class for login page locators."""
    uname_field = (By.ID, 'login-username')
    pwd_field = (By.ID, 'login-password')
    signin_button = (By.XPATH, "//input[@value='Sign In']")
    version_ctrl = (By.ID, "login__version")

class WorkspacePageLocators(object):
    """A class for Workspace page locators."""
    add_app_tile = (By.XPATH, "//*[@ng-if='vm.addButton']")  # Tile with + to add an app

    def __init__(self, app_name):
        # App tile -- assign name dynamically
        self.app_tile = (By.XPATH, '//*[@title="' + app_name + '"]')

class AppEditorPageLocators(object):
    """A class for App Editor page locators."""
    def __init__(self, screen_name):
        # Screen tile -- assign name dynamically
        #self.screen_tile = (By.XPATH, '//*[@title="' + screen_name + '"]')
        self.screen_tile = (By.XPATH, '//*[@title="' + screen_name + '"]/..//*[@class="screen-card__img"]')

class NewApplicationDialogLocators(DialogLocators):
    """A class for New Application dialog locators"""
    done_button = DialogLocators.ok_button
    next_button = DialogLocators.ok_button
    name_field = (By.ID, 'newapp-name')

class LeftNavLocators(object):
    """A class for Left Navigation locators"""
    New_Screen = (By.XPATH, '//*[@ng-click="vm.addScreen()"]')
    New_Panel = (By.XPATH, '//*[@ng-click="vm.addPanel()"]')


class TopNavLocators(object):
    """A class for Top Navigation locators"""
    MyApps_link = (By.CSS_SELECTOR, 'span.ng-binding')
    delete_icon = (By.XPATH, '//*[@class="icon icon-Delete"]')
    colors_icon = (By.XPATH, '//*[@class="icon icon-Colors"]')
    fonts_icon = (By.XPATH, '//*[@class="icon icon-Fonts"]')
    images_icon = (By.XPATH, '//*[@class="icon icon-Images"]')
    styles_icon = (By.XPATH, '//*[@class="icon icon-Styles"]')
    search_box = (By.XPATH, '//*[@title="Find"]')
    menu_dropdown = (By.XPATH, "//span[3]/bldr-user-dropdown")
    logout_menu = (By.XPATH, '//*[@id="item-template"][3]')


class DeleteItemsDialogLocator(DialogLocators):
    """A class for Delete Items dialog locators"""
    yes_button = DialogLocators.ok_button
    no_button = DialogLocators.cancel_button

class ManageColorsDialogLocators(DialogLocators):
    """A class for Manage Colors dialog locators"""
    # Still need Color, Gradient, +, Individual colors buttons
    done_button = DialogLocators.ok_button

class ManageFontsDialogLocators(DialogLocators):
    """A class for Manage Fonts dialog locators"""
    # Still need +, Individual font delete buttons
    done_button = DialogLocators.ok_button

class ManageImagesDialogLocators(DialogLocators):
    """A class for Manage Images dialog locators"""
    # Still need Search, Filters, +, View, Delete, Individual images buttons

class ManageStylesDialogLocators(DialogLocators):
    """A class for Manage Styles dialog locators"""
    # Still need Delete, Individual images buttons

class NewScreenDialogLocators(DialogLocators):
    """A class for the New Screen dialog locators"""
    name_field = (By.XPATH, '//*[@title="Screen Name"]')

class NewPanelDialogLocators(DialogLocators):
    """A class for the New Panel dialog locators"""
    name_field = (By.XPATH, '//*[@title="Panel Name"]')
    width_field = (By.XPATH, '//*[@title="Width"]')
    height_field = (By.XPATH, '//*[@title="Height"]')

class DeleteScreensDialogLocators(DialogLocators):
    """A class for the Delete Screens dialog locators"""




