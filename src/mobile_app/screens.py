from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen
from kivy.uix.recycleview import RecycleView
from kivy.core.window import Window
from kivy.metrics import dp

from trading_api.trading_api import StocksTrading
from mobile_app.utils import get_logger


logger = get_logger()


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        horizontal_layout_one = BoxLayout()
        horizontal_layout_two = BoxLayout()
        vertical_layout = BoxLayout(orientation="vertical", padding=40)
        self.text_api_key = TextInput(pos_hint={"center_x": 0.5, "center_y": 0.9},
                                      text='', multiline=False, size=(200, 50),
                                      size_hint=(None, None))
        api_key_label = Label(text='API KEY', size_hint=(None, None),
                              size=(100, 50), pos_hint={"center_x": 0.5,
                                                        "center_y": 0.9})
        self.text_api_secret = TextInput(text='', multiline=False,
                                         size_hint=(None, None), size=(200, 50),
                                         pos_hint={"center_x": 0.5,
                                                   "center_y": 0.9})
        api_secret_label = Label(text='API SECRET', size_hint=(None, None),
                                 size=(100, 50), pos_hint={"center_x": 0.5,
                                                           "center_y": 0.9})
        horizontal_layout_one.add_widget(self.text_api_key)
        horizontal_layout_one.add_widget(api_key_label)
        horizontal_layout_two.add_widget(self.text_api_secret)
        horizontal_layout_two.add_widget(api_secret_label)
        vertical_layout.add_widget(horizontal_layout_one)
        vertical_layout.add_widget(horizontal_layout_two)
        self.login_button = Button(text='Login', size_hint=(None, None),
                                   size=(200, 75), pos_hint={"center_x": 0.5,
                                                             "center_y": 1},
                                   on_press=self.submitted)
        vertical_layout.add_widget(self.login_button)
        self.add_widget(vertical_layout)

    def submitted(self, *args):
        api_secret = self.text_api_secret.text
        api_key = self.text_api_key.text
        try:
            stocks_trading = StocksTrading(api_key, api_secret)
            stocks_trading.get_account()
        except Exception:
            logger.error("Unable to authorize")
            self.text_api_secret.text = 'Unable to authorize'
            self.text_api_key.text = 'Unable to authorize'
        else:
            global API_KEY
            global API_SECRET
            API_KEY = api_key
            API_SECRET = api_secret
            orders = OrdersPage(name='orders')
            self.manager.add_widget(orders)
            self.manager.current = 'menu'

    def back_to_orders(self, *args):
        self.manager.current = 'orders'


class Menu(Screen):
    def __init__(self, **kwargs):
        super(Menu, self).__init__(**kwargs)
        input_layout = BoxLayout(spacing=5)
        self.layout_two = BoxLayout(orientation="vertical", padding=40)
        button = Button(text='Find Stock', size_hint=(.5, .1),
                        pos_hint={"center_x": 0.5, "center_y": 0.9},
                        on_press=self.submitted)
        self.text_input = TextInput(text='', multiline=False,
                                    pos_hint={"center_x": 0.2, "center_y": 0.9},
                                    size_hint=(.5, .1))
        show_orders_button = Button(text='current orders',
                                    pos_hint={"center_x": 0.5, "center_y": 0.9},
                                    size_hint=(1, .1))
        show_orders_button.bind(on_press=self.show_orders_button_press)
        self.layout_two.add_widget(show_orders_button)
        input_layout.add_widget(self.text_input)
        input_layout.add_widget(button)
        self.layout_two.add_widget(input_layout)
        self.add_widget(self.layout_two)

    def submitted(self, *args):
        self.manager.current = 'orders'

    def show_orders_button_press(self, *args):
        self.manager.current = 'orders'


class OrdersPage(Screen):
    def __init__(self, **kwargs):
        super(OrdersPage, self).__init__(**kwargs)
        self.grid_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))
        scroll_view = RecycleView(size_hint=(1, None), size=(Window.width,
                                                             Window.height))
        scroll_view.add_widget(self.grid_layout)
        self.add_widget(scroll_view)
        back_button = Button(text='< Back to Menu', on_press=self.back_to_menu,
                             size_hint_y=None, height=dp(40))
        self.grid_layout.add_widget(back_button)
        for order in self.get_orders():
            self.stock_button = Button(text=order, size_hint_y=None, height=dp(
                40), on_press=self.stock)
            self.grid_layout.add_widget(self.stock_button)

    def get_orders(self):
        stocks_trading = StocksTrading(API_KEY, API_SECRET)
        orders_list = [order for order in stocks_trading.list_orders()]
        return orders_list

    def back_to_menu(self, *args):
        self.manager.current = 'menu'

    def stock(self, *args):
        self.manager.current = 'current_stock'


class CurrentStock(Screen):
    def __init__(self, **kwargs):
        super(CurrentStock, self).__init__(**kwargs)
        input_layout = BoxLayout(spacing=5)
        layout_two = BoxLayout(orientation="vertical", padding=40)
        sell_button = Button(text='sell', size_hint=(.5, .2),
                             pos_hint={"center_x": 0.5, "center_y": 0.9},
                             on_press=self.sell_order)
        buy_button = Button(text='buy', pos_hint={"center_x": 0.2,
                                                  "center_y": 0.9},
                                 size_hint=(.5, .2), on_press=self.buy_order)
        back_orders_button = Button(text='< Back to Orders',
                                    pos_hint={"center_x": 0.5, "center_y": 0.9},
                                    size_hint=(1, .2),
                                    on_press=self.back_to_orders)
        quantity_layout = BoxLayout(spacing=5)
        quantity_label = Label(text='quantity', size_hint=(.5, .2),
                               pos_hint={"center_x": 0.5, "center_y": 0.9})
        self.quantity_text_input = TextInput(text='', multiline=False,
                                    pos_hint={"center_x": 0.2, "center_y": 0.9},
                                    size_hint=(.5, .2))
        layout_two.add_widget(back_orders_button)
        quantity_layout.add_widget(self.quantity_text_input)
        quantity_layout.add_widget(quantity_label)
        input_layout.add_widget(sell_button)
        input_layout.add_widget(buy_button)
        layout_two.add_widget(quantity_layout)
        layout_two.add_widget(input_layout)
        self.add_widget(layout_two)

    def buy_order(self, *args):
        orders_screen = self.manager.get_screen('orders')
        menu_screen = self.manager.get_screen('menu')
        stock_name = menu_screen.text_input.text or orders_screen.stock_button.text
        stock_trading = StocksTrading(API_KEY, API_SECRET)
        stock_trading.buy_order(stock_name, self.quantity_text_input_input.text)

    def sell_order(self, *args):
        orders_screen = self.manager.get_screen('orders')
        menu_screen = self.manager.get_screen('menu')
        stock_name = menu_screen.text_input.text or orders_screen.stock_button.text
        stock_trading = StocksTrading(API_KEY, API_SECRET)
        stock_trading.sell_order(stock_name,
                                 self.quantity_text_input_input.text)

    def back_to_orders(self, *args):
        self.manager.current = 'orders'