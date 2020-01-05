from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from mobile_app.screens import LoginScreen, Menu, CurrentStock


class MainApp(App):
    def build(self):
        screen_manager = ScreenManager()
        login = LoginScreen(name='login')
        menu = Menu(name='menu')
        current_stock = CurrentStock(name='current_stock')
        screen_manager.add_widget(login)
        screen_manager.add_widget(menu)
        screen_manager.add_widget(current_stock)
        return screen_manager


if __name__ == '__main__':
    app = MainApp()
    app.run()