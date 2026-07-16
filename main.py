import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import NumericProperty, ReferenceListProperty

class Bucket(Widget):
    # Keep track of the bucket's position and size
    pass

class Coin(Widget):
    velocity_y = NumericProperty(-5) # How fast the coin falls

    def move(self):
        self.y += self.velocity_y

class CoinCatcherGame(Widget):
    score = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.coins = []
        # Run the game update loop 60 times a second
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        # Spawn a new coin every 1.5 seconds
        Clock.schedule_interval(self.spawn_coin, 1.5)

    def spawn_coin(self, dt):
        with self.canvas:
            Color(1, 0.84, 0) # Gold Color
            # Spawn coin at a random X coordinate at the top of the screen
            coin = Coin(pos=(random.randint(0, self.width - 50), self.height))
            with coin.canvas:
                coin.ellipse = Ellipse(pos=coin.pos, size=(40, 40))
            self.add_widget(coin)
            self.coins.append(coin)

    def on_touch_move(self, touch):
        # Move the bucket horizontally wherever the user drags their finger
        if touch.y < self.height / 3:
            self.ids.bucket.center_x = touch.x

    def update(self, dt):
        # Update bucket visual position
        bucket = self.ids.bucket
        
        # Loop backwards through coins to safely remove caught/missed ones
        for coin in self.coins[:]:
            coin.move()
            coin.ellipse.pos = coin.pos # Update visual circle position
            
            # Collision Detection: Did the coin hit the bucket?
            if coin.collide_widget(bucket):
                self.score += 1
                self.remove_widget(coin)
                self.coins.remove(coin)
            
            # Missed: Did the coin fall past the screen?
            elif coin.y < 0:
                self.remove_widget(coin)
                self.coins.remove(coin)

# This KV string designs the interface (UI layout)
from kivy.lang import Builder
Builder.load_string('''
<Bucket>:
    size: 120, 30
    canvas:
        Color:
            rgb: 0.8, 0.3, 0.3
        Rectangle:
            pos: self.pos
            size: self.size

<CoinCatcherGame>:
    canvas:
        Color:
            rgb: 0.1, 0.1, 0.15
        Rectangle:
            size: self.size
            pos: self.pos

    Label:
        font_size: 40
        center_x: root.width / 2
        top: root.top - 20
        text: "Coins: " + str(root.score)

    Bucket:
        id: bucket
        pos: root.width / 2 - 60, 50
''')

class CoinCatcherApp(App):
    def build(self):
        return CoinCatcherGame()

if __name__ == '__main__':
    CoinCatcherApp().run()
