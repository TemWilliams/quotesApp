import glob
from datetime import datetime
from pathlib import Path
import random

from kivy.app import App
from kivy.lang import Builder
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen
import json
from kivy.core.window import Window

# Draw color on background first
Window.clearcolor = (1, 1, 1, 1)
# Use Build object to load widgets.
Builder.load_file("design.kv", encoding="utf8")


# Create first class inheriting the Screen object.
class LoginScreen(Screen):
    """Opening screen of the application"""

    # This function brings user to the sign up screen.
    def sign_up(self):
        self.manager.transition.direction = "left"
        self.manager.current = "sign_up_screen"

    # This function takes user to forgot password screen.
    def forgot_password(self):
        self.manager.transition.direction = "left"
        self.manager.current = "forgot_password_screen"

    # open json file and check if user enters correct login
    def login(self, usrname, passwrd):
        with open("users.json") as file:
            user = json.load(file)
        # If login matches send to login screen success
        if usrname and passwrd in user:
            self.manager.transition.direction = "left"
            self.manager.current = "login_screen_success"
            self.ids.wrong_cred.text = ""
            self.ids.username.text = ""
            self.ids.password.text = ""
        # otherwise tell them wrong login
        else:
            self.ids.wrong_cred.text = "Wrong login or password"


# Create second class inheriting the ScreenManager object.
class RootWidget(ScreenManager):
    """Holds screen widgets to the"""
    pass


# Class for my sign up screen inheriting the Screen object.
class SignUpScreen(Screen):
    """Allows user to register for app and takes data from inputs"""

    # Function that adds a new user to application.
    def add_user(self, user, passw, email):
        # Open json original json file.
        with open("users.json") as file:
            new_users = json.load(file)
        # Set up dictionary output for json file.
        new_users[user] = {"Username": user, "Password": passw, "Email": email,
                           "Date": datetime.now().strftime("%a-%b-%d %I-%M-%p-%y")}
        # Update json file with a new user.
        with open("users.json", "w") as updateFile:
            json.dump(new_users, updateFile)
        # Bring user to success screen
        self.manager.current = "success_screen"
        self.ids.username.text = ""
        self.ids.password.text = ""


class SuccessScreen(Screen):
    """Redirect back to login page layout"""

    def main_page(self):
        # Direct users to main menu.
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"


class LoginScreenSuccess(Screen):
    """Redirects user to login page"""

    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

    def get_quote(self, feel):
        feel = feel.lower()
        available_feeling = glob.glob("quotes/*.txt")

        available_feeling = [Path(filename).stem for filename
                             in available_feeling]

        if feel in available_feeling:
            with open(f"quotes/{feel}.txt", encoding="utf-8") as file:
                quotes = file.read().splitlines()
                rand_quotes = random.choice(quotes)

                self.ids.quotes.text = rand_quotes
        else:
            self.ids.quotes.text = "Feeling not supported".center(175)


class ForgotPasswordScreen(Screen):
    """Check to see if email is on file then send email
    to users associated account with login info"""

    def email_check(self, email, usrname):
        with open("users.json") as file:
            user = json.load(file)
        if email and usrname in user:
            self.ids.email_sent.text = "password: {}".format(user[usrname]["Password"])
        else:
            self.ids.email_sent.text = "Wrong login"


# Create instance of our app inherit the App object
class MainApp(App):
    """Initialize application and return widgets to screen"""

    def build(self):
        return RootWidget()


# Class allows logout button to change colors and use image
# inherits objects in specific order
class ImageButton(ButtonBehavior, Image, HoverBehavior):
    pass


if __name__ == "__main__":
    # Call instance and start run loop
    MainApp().run()
