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
    #screen_dropdown = (By.XPATH, '//*[@class="collection__filter ng-binding"')

    # Top Nav Delete and Copy icons
    delete_icon = (By.XPATH, '//*[@title="Delete selected screen"]')
    copy_icon = (By.XPATH, '//*[@title="Copy selected screen"]')

    def __init__(self, screen_name):
        # Screen tile -- assign name dynamically
        self.screen_tile = (By.XPATH, '//*[@title="' + screen_name + '"]/..//*[@class="screen-card__img"]')


class ScreenEditorPageLocators(object):
    """A class for Screen Editor page locators"""
    # I wonder if I should put these in the left nav...
    ImageControl = (By.XPATH, '//*[@class="icon icon-Image"]')
    ButtonControl = (By.XPATH, '//*[@class="icon icon-Button"]')
    RadioControl = (By.XPATH, '//*[@class="icon icon-Radio"]')
    ToggleControl = (By.XPATH, '//*[@class="icon icon-Checkbox"]')
    MapControl = (By.XPATH, '//*[@class="icon icon-Map"]')
    RadialProgressControl = (By.XPATH, '//*[@class="icon icon-RadialProgress"]')
    ProgressControl = (By.XPATH, '//*[@class="icon icon-ProgressBar"]')
    SliderControl = (By.XPATH, '//*[@class="icon icon-Slider"]')
    ScrollContainerControl = (By.XPATH, '//*[@class="icon icon-ScrollContainer"]')
    TextInputControl = (By.XPATH, '//*[@class="icon icon-UserInput"]')
    WebViewControl = (By.XPATH, '//*[@class="icon icon-WebView"]')
    CustomControl = (By.XPATH, '//*[@class="icon icon-CustomControl"]')
    ListCollectionControl = (By.XPATH, '//*[@class="icon icon-List"]')
    GridCollectionControl = (By.XPATH, '//*[@class="icon icon-Grid2"]')
    PageIndicatorControl = (By.XPATH, '//*[@class="icon icon-More"]')

    # Active Components
    copy_component_button = (By.XPATH, '//*[@class="btn btn--selections sm"]/*[@class="icon icon-Duplicate"]')
    delete_component_button = (By.XPATH, '//*[@class="active-component__buttons"]//*[@class="btn btn--selections sm"]//*[@class="icon icon-Delete"]')


    def __init__(self, component_name):
        #self.component_name_tile = (By.XPATH, '//*[@class="active-component__item name"]//*[contains(text(), ' + component_name + ')]')
        self.component_name_tile = (By.XPATH, "//*[contains(text(), '" + component_name + "')]")
        self.component_visible_button = (By.XPATH, "//*[contains(text(), '" + component_name + "')]/../*[@title='Show/hide component']")
        self.component_lock_button = (By.XPATH, "//*[contains(text(), '" + component_name + "')]/../*[@title='Lock component']")



class NewApplicationDialogLocators(DialogLocators):
    """A class for New Application dialog locators"""
    done_button = DialogLocators.ok_button
    next_button = DialogLocators.ok_button
    name_field = (By.ID, 'newapp-name')
    # Device, Appearance "tabs"

class CopyAppDialogLocators(DialogLocators):
    """A class for the Copy App dialog locators"""
    name_field = (By.XPATH, '//*[@title="Name of Copy:"]')

class CopyScreenDialogLocators(DialogLocators):
    """A class for the Copy Screen dialog locators"""
    name_field = (By.XPATH, '//*[@title="Name of Copy:"]')

class CopyPanelDialogLocators(DialogLocators):
    """A class for the Copy Screen dialog locators"""
    name_field = (By.XPATH, '//*[@title="Name of Copy:"]')

class LeftNavLocators(object):
    """A class for Left Navigation locators"""
    New_Screen = (By.XPATH, '//*[@ng-click="vm.addScreen()"]')
    New_Panel = (By.XPATH, '//*[@ng-click="vm.addPanel()"]')


class TopNavLocators(object):
    """A class for Top Navigation locators"""
    MyApps_link = (By.CSS_SELECTOR, 'span.ng-binding')
    app_link = (By.XPATH, '//*[@ng-click="vm.routeParent()"]')
    select_icon = (By.XPATH, '//*[@class="icon icon-Pointer"]')
    rectangle_icon = (By.XPATH, '//*[@class="icon icon-Rectangle"]')
    ellipse_icon = (By.XPATH, '//*[@class="icon icon-Ellipse"]')
    line_icon = (By.XPATH, '//*[@class="icon icon-Line"]')
    shape_selection_icon = (By.XPATH, '//*[@class="icon icon-Chevron"]')
    rectangle_dropdown = (By.XPATH, '//*[@class="dropdown-template-margin icon-Rectangle"]')
    ellipse_dropdown = (By.XPATH, '//*[@class="dropdown-template-margin icon-Ellipse"]')
    line_dropdown = (By.XPATH, '//*[@class="dropdown-template-margin icon-Line"]')
    text_icon = (By.XPATH, '//*[@class="icon icon-Text"]')
    #delete_icon = (By.XPATH, '//*[@class="icon icon-Delete"]')
    delete_icon = (By.XPATH, '//*[@title="Delete selected app"]')
    copy_icon = (By.XPATH, '//*[@title="Copy selected app"]')
    colors_icon = (By.XPATH, '//*[@title="Manage colors"]')
    #fonts_icon = (By.XPATH, '//*[@class="icon icon-Fonts"]')
    fonts_icon = (By.XPATH, '//*[@title="Manage Fonts"]')
    images_icon = (By.XPATH, '//*[@title="Manage Images"]')
    styles_icon = (By.XPATH, '//*[@title="Manage Styles"]')
    data_icon = (By.XPATH, '//*[@title="Manage Data"]')
    search_box = (By.XPATH, '//*[@title="Find"]')
    user_menu_dropdown = (By.XPATH, "//span[3]/bldr-user-dropdown")
    logout_menu = (By.XPATH, "//*[contains(text(), 'Logout')]")
    publish_btn = (By.XPATH, '//*[@class="ng-binding ng-scope"]')

    #def __init__(self, app_name):
        # Screen tile -- assign name dynamically
        #self.app_link = (By.XPATH, '//*[@class="ng-scope ng-isolate-scope"]/[contains(text(), ' + app_name + ')]')
        #self.app_link = (By.XPATH, '//*[contains(text(), "' + app_name + '")]')

class RemoveAppsDialogLocators(DialogLocators):
    """A class for Remove Apps dialog locators"""
    permDelete_chkbox = (By.ID, "sm_checkbox_0")
    no_button = DialogLocators.ok_button      # No is the default button in this dialog
    yes_button = (By.XPATH, '//button[2]')  # It's the second button.

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

class ManageDataDialogLocators(DialogLocators):
    """A class for Manage Data dialog locators"""
    # Still need Data Sources, Request Parameters, Variables, add tiles, etc.

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

class ComponentPaletteLocators(object):
    """A class for Component Palette locators"""
    name = (By.XPATH, '//input[@title="Name"]')
    shape = (By.XPATH, '//input[@title="Shape"]')
    style = (By.XPATH, '//input[@title="Style"]')
    opacity = (By.XPATH, '//input[@title="Opacity"]')
    add_style = (By.XPATH, '//*[@class="icon icon-Add"]')

class SizeAndPositionPaletteLocators(object):
    """A class for Size & Position Palette locators"""
    width = (By.XPATH, '//input[@title="W"]')
    height = (By.XPATH, '//input[@title="H"]')

class DefaultPropertiesPaletteLocators(object):
    """A class for Default Properties Palette locators """
    FillColorSwatch = (By.XPATH, '//*[@class="btn--square  "]')

class ToolTipDialog(object):
    """A class for ToolTip Dialog locators"""
    gotIt_btn = (By.XPATH, '//*[@class="tooltip_nav-btn ng-binding ng-scope"]') # Also applies to Next tooltip button
    close_button = (By.XPATH, '//*[@class="icon icon-Cancel"]')
    tooltip_title = (By.XPATH, '//*[@class="tooltip_title ng-binding"]')
    tooltip_text = (By.XPATH, '//*[@class="tooltip_text ng-binding"]')

class PublishContentDialogLocators(DialogLocators):
    """A class for Publish Content dialog locators"""
    iOS_Phone_box = (By.XPATH, '//') #iOS_table, android_phone, Android_tablet have same id
    # <input type="checkbox" class="sq ng-pristine ng-untouched ng-valid ng-not-empty" ng-model="config.build" ng-click="checkSelections()" ng-disabled="publishDone">
    publish_private_box = (By.ID, 'publish-private')
    publish_button = DialogLocators.ok_button

class StyleDialogLocators(DialogLocators):
    """Generic Style dialog locators"""
    # Should put the button to open/close general settings here.
    name_field = (By.XPATH, '//*[@title="Name of Style (required)"]')
    size_chkbox = (By.ID, 'attr_0_Size (W,H)')
    position_chkbox = (By.ID, 'attr_1_Position (X,Y)')
    opacity_chkbox = (By.ID, 'attr_2_Opacity')
    rotation_chkbox = (By.ID, 'attr_0_Rotation')
    interactions_chkbox = (By.ID, 'attr_1_Interactions')

class ButtonStyleDialogLocators(StyleDialogLocators):
    """Locators for Button Style Dialogs"""
    # also works for toggle buttons
    padding_chkbox = (By.ID, 'attr_0_Padding')
    shape_chkbox = (By.ID, 'attr_1_Shape')

    fill_chkbox = (By.ID, 'attr_0_Fill')
    border_chkbox = (By.ID, 'attr_1_Border')
    shadow_chkbox = (By.ID, 'attr_2_Shadow')
    corner_radius_chkbox = (By.ID, 'attr_0_Corner Radius')
    icon_chkbox = (By.ID, 'attr_1_Icon')
    text_value_chkbox = (By.ID, 'attr_2_Text Value')
    font_type_chkbox = (By.ID, 'attr_0_Font Type')
    font_color_chkbox = (By.ID, 'attr_1_Font Color')
    font_size_chkbox = (By.ID, 'attr_2_Font Size')
    alignment_chkbox = (By.ID, 'attr_0_Alignment')
    vertical_alignment_chkbox = (By.ID, 'attr_1_Vertical Alignment')
    all_caps_chkbox = (By.ID, 'attr_2_All Caps')
    truncation_chkbox = (By.ID, 'attr_0_Truncation')
    font_shadow_chkbox = (By.ID, 'attr_1_Font Shadow')

class RadioButtonStyleDialogLocators(ButtonStyleDialogLocators):
    """Additional locators for Radio Buttons"""
    radio_group_chkbox = (By.ID, 'attr_1_Radio Group')
    shape_chkbox = (By.ID, 'attr_2_Shape')

class ImageStyleDialogLocators(StyleDialogLocators):
    """Locators for Image Styles"""
    border_chkbox = (By.ID, 'attr_0_Border')
    shadow_chkbox = (By.ID, 'attr_1_Shadow')
    corner_radius_chkbox = (By.ID, 'attr_2_Corner Radius')
    shape_chkbox = (By.ID, 'attr_0_Shape')
    tap_through_chkbox = (By.ID, 'attr_1_Tap Through')
    scale_chkbox = (By.ID, 'attr_0_Scale')
    image_chkbox = (By.ID, 'attr_1_Image')

class ColorPickerLocators(DialogLocators):
    """Locators for Color Picker"""
    close_button = (By.XPATH, '//*[@class="icon-Cancel wnd-top__cancel"]')
    # Color/Gradients


    # Hex, R, G, B, A
    hexVal = (By.XPATH, '//input[@title="HEX"]')
    RVal = (By.XPATH, '//input[@title="R"]')
    GVal = (By.XPATH, '//input[@title="G"]')
    BVal = (By.XPATH, '//input[@title="B"]')
    #AVal = (By.XPATH, '//input[@title="A"]')

    # Big Color Swatch
    bigSwatch = (By.XPATH, '//*[@class="btn--square btn--square lg "]')

    # Color Name?


    # Palette settings

    # Palette Tiles

    # Update
    Update = (By.ID, 'color_picker_update')

    # Add new color/ new color name
    AddNewColor = (By.XPATH, '//*[@class="icon icon-Add"]')
    NewColorName = (By.XPATH, '//input[@type="text"]')

    # Gradient style dropdown/choices

    # Gradient direction dropdown/choices
