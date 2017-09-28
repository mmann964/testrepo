import time
import unittest
import base64
import page
import p2uxGeneral

# to run, type one of these commands at the bash prompt:
# python p2uxlogin.py
# nosetests --nocapture p2uxlogin.py
# nosetests --verbosity=3 --nocapture p2uxlogin.py

uname = p2uxGeneral.uname
passwordEnc = p2uxGeneral.passwordEnc
passwordDec = base64.b64decode(passwordEnc)


class P2uxLoginTest(p2uxGeneral.P2uxBaseTest):
    @unittest.skip("skipping for now.")
    def test_00_misc(self):
        """Go to login screen, login, create new app"""
        app_name = "MelSelenium"

        login_page = page.LoginPage(self.driver)
        top_nav = page.TopNav(self.driver)
        workspace_page = page.WorkspacePage(self.driver)
        newapp_dialog = page.NewApplicationDialog(self.driver)

        assert login_page.does_title_match(), "Login Screen title doesn't match."
        verStr = login_page.get_version()
        print "Version = " + verStr

        time.sleep(2)
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

    # @unittest.skip("skipping for now.")
    def test_01_test_title(self):
        """Check title of login screen"""
        login_page = page.LoginPage(self.driver)
        assert login_page.does_title_match(), "Login Screen title doesn't match."

    # @unittest.skip("skipping for now.")
    def test_02_test_valid_login(self):
        """Check that you can login"""
        login_page = page.LoginPage(self.driver)
        workspace_page = page.WorkspacePage(self.driver)
        newapp_dialog = page.NewApplicationDialog(self.driver)

        verStr = login_page.get_version()
        print "Version = " + verStr

        login_page.username_field = uname
        login_page.password_field = passwordDec

        uname2 = login_page.username_field
        print "User name = " + uname2
        # time.sleep(2)
        login_page.click_sign_in_button()
        assert workspace_page.does_title_match(), "Not in Workspace Page after logging in."
        workspace_page.click_add_app_tile()
        newapp_dialog.click_close_button()
        time.sleep(2)

    @unittest.skip("skipping for now.")
    def test_03_start_new_app(self):
        """Check that you can create a new app"""

        # are we back at the login page?
        login_page = page.LoginPage(self.driver)
        workspace_page = page.WorkspacePage(self.driver)
        time.sleep(5)
        login_page.username_field = uname
        login_page.password_field = passwordDec
        login_page.click_sign_in_button()
        time.sleep(5)

        workspace_page.click_add_app_tile()
        time.sleep(5)


if __name__ == "__main__":
    unittest.main()
