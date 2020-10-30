from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from datetime import datetime
import json, glob
from pathlib import Path
import random

Builder.load_file('design.kv')


class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = 'Sign_up_screen'
    def login(self, username, password):
        with open('users.json') as file:
            users= json.load(file)
            if username in users and users[username]['password'] == password:
                self.manager.current = 'Login_screen_success'
            else:
                self.ids.login_failed.text = 'Incorrect Username or Password! Try again...'
                

class SignUpScreen(Screen):
    def add_user(self, username, password):
        with open('users.json') as file:
            users= json.load(file)
        users[username] = {'username': username, 'password': password,
                            'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S") }
        with open('users.json', 'w') as file:
            json.dump(users, file)
        self.manager.current = 'sign_up_screen_success'

class SignUpScreenSuccess(Screen):
    def go_to_login(self):
        # set login screen to transition from the right
        self.manager.transition.direction = 'down'
        self.manager.current = 'Login_screen'

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'Login_screen'
    def get_quote(self, mood):
        mood = mood.lower()
        available_mood = glob.glob("quotes/*txt") # get names of all files in quotes folder
        available_mood = [Path(filename).stem for filename in available_mood]
        print(available_mood)
        if mood in available_mood:
            with open(f"quotes/{mood}.txt", encoding='utf-8') as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = 'Choose either happy, sad or unloved!'

class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == "__main__":
    MainApp().run()