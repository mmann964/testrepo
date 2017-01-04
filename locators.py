from selenium.webdriver.common.by import By

class LoginPageLocators(object):
    """A class for login page locators."""
    uname_field = (By.ID, 'login-username')
    pwd_field = (By.ID, 'login-password')
    signin_button = (By.XPATH, "//input[@value='Sign In']")
    version_ctrl = (By.ID, "login__version")

#<input type="submit" value="Sign In" class="login-form__submit btn--submit">

class WorkspacePageLocators(object):
    """A class for Workspace page locators."""
    add_app_tile = (By.XPATH, "//div[@ng-if='vm.addButton']")  # Tile with + to add an app

    def __init__(self, app_name):
        # App tile -- assign name dynamically
        self.app_tile = (By.XPATH, '//*[@title="' + app_name + '"]')

class NewApplicationDialogLocators(object):
    """A class for New Application dialog locators"""
    title_bar = (By.XPATH, '//*[@class="dialog__title-text ng-binding"]')
    close_button = (By.XPATH, '//*[@class="icon icon-Cancel"]')
    cancel_button = (By.XPATH, '*[@class="btn--dialog ng-binding ng-scope"]')
    done_button = (By.CSS_SELECTOR, 'button.btn--dialog.ng-binding.ng-scope.ok')
    next_button = (By.CSS_SELECTOR, 'button.btn--dialog.ng-binding.ng-scope.ok')
    name_field = (By.ID, 'newapp-name')

class TopNavLocators(object):
    """A class for Top Navigation locators"""
    MyApps_link = (By.CSS_SELECTOR, 'span.ng-binding')
    delete_icon = (By.XPATH, '//*[@class="icon icon-Delete"]')
    colors_icon = (By.XPATH, '//*[@class="icon icon-Colors"]')
    fonts_icon = (By.XPATH, '//*[@class="icon icon-Fonts"]')
    images_icon = (By.XPATH, '//*[@class="icon icon-Images"]')
    menu_dropdown = (By.XPATH, "//span[3]/bldr-user-dropdown")
    logout_menu = (By.XPATH, '//*[@id="item-template"][3]')

    #logout_menu = (By.XPATH, "//li[@id='item-template'])[9]")

class DeleteItemsDialogLocator(object):
    """A class for Delete Items dialog locators"""
    title_bar = (By.XPATH, '//*[@class="dialog__title-text ng-binding"]')
    yes_button = (By.XPATH, '//*[@class="btn--dialog ng-binding ng-scope ok"]')
    no_button = (By.XPATH, '//*[@class="btn--dialog ng-binding ng-scope"]')

class ManageColorsDialogLocators(object):
    """A class for Manage Colors dialog locators"""
    title_bar = (By.XPATH, '//*[@class="dialog__title-text ng-binding"]')
    # Still need Color, Gradient, +, Individual colors buttons
    close_button = (By.XPATH, '//*[@class="icon icon-Cancel"]')
    done_button = (By.CSS_SELECTOR, 'button.btn--dialog.ng-binding.ng-scope.ok')

class ManageFontsDialogLocators(object):
    """A class for Manage Fonts dialog locators"""
    title_bar = (By.XPATH, '//*[@class="dialog__title-text ng-binding"]')
    # Still need +, Individual font delete buttons
    close_button = (By.XPATH, '//*[@class="icon icon-Cancel"]')

class ManageImagesDialogLocators(object):
    """A class for Manage Images dialog locators"""
    title_bar = (By.XPATH, '//*[@class="dialog__title-text ng-binding"]')
    # Still need Search, Filters, +, View, Delete, Individual images buttons
    close_button = (By.XPATH, '//*[@class="icon icon-Cancel"]')
    ok_button = (By.CSS_SELECTOR, 'button.btn--dialog.ng-binding.ng-scope.ok')



