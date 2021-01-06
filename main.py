from kivy.app import App #main object
from kivy.lang import Builder # connecting python with kivy (importing kv to py)
from kivy.uix.screenmanager import ScreenManager, Screen
#from kivy.uix.gridlayout import GridLayout (importing kv to py)
import json, glob, random
from datetime import datetime
from pathlib import Path
from hoverable import HoverBehavior

Builder.load_file("design.kv")

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"  #self means LoginScreen object(instance) in this case
        #manager is method of Screen; LoginScreen is parent class, Screen is child calss

    def login(self, uname, pword):
         with open("users.json") as file:
             users = json.load(file)
         if uname in users and users[uname]['password'] == pword:  #print(users.keys())
             self.manager.current = 'login_screen_success'
         else:
             self.ids.login_wrong.text="Wrong username or password!" #text object

class RootWidget(ScreenManager):
    pass

class SignUpScreen(Screen):
    def add_user(self,uname, pword):
        with open("users.json") as file:
            users = json.load(file)
        #print(users) #{'user1':{}, 'user2':{}}

        users[uname]={'username':uname,'password':pword,
            'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S") }
        #print(users)

        with open("users.json", 'w') as file:#overwrite the users 
            # after line 28, a completely new empty file is going to be created
            json.dump(users, file)
        
        self.manager.current = "sign_up_screen_success" 

class SignUpScreenSuccess(Screen):
    def go_to_login(self):
        self.manager.transition.direction='right'
        self.manager.current = "login_screen" 

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction='right'
        self.manager.current = "login_screen" 

    def get_quote(self, feel):
        #print(feel)
        feel = feel.lower()
        available_feelings = glob.glob("quotes/*txt") 
        #print(available_feelings)#['quotes/happy.txt','quotes/sad.txt',..]
        #['quotes\\happy.txt','quotes\\sad.txt',..]
        available_feelings=[Path(filename).stem for filename in 
                                 available_feelings]
        print(available_feelings) #['happy','sad','unloved']
        print(feel)
        if feel in available_feelings:
            with open("quotes/{feel}.txt") as file:
                quotes = file.readlines()
            print(quotes)  #["...", "....."]
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text="Try anotehr feeling"

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == "__main__": # IMPORTANT???
    MainApp().run()
    
# if __name__ == '__main__':
#     MainApp().run()

#$ pip uninstall numpy
#$ pip install numpy==1.19.3
# $ cd "/c/Program Files (x86)/Python37-32"
# Sharon@Sharon_Yang MINGW64 /c/Program Files (x86)/Python37-32
# $ source kivy_venv/Scripts/activate
# (kivy_venv)
# Sharon@Sharon_Yang MINGW64 /c/Program Files (x86)/Python37-32
# $ python /e/Python/main.py
# Sharon@Sharon_Yang MINGW64 /c/Program Files (x86)/Python37-32
# $ python /e/Python/main.py

# shift+Alt+F to format this file