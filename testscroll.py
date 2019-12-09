from kivy.app import App
from kivy.uix.button import Button

class ScrollButton(Button):
    pass

class ScrollApp(App):
    def build(self):
        super(ScrollApp, self).build()
        container = self.root.ids.container
        for i in range(30):
            container.add_widget(ScrollButton(text=str(i)))
        return self.root   # return root does not work

if __name__ == '__main__':
    ScrollApp().run()
