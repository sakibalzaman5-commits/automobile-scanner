import json
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle

class GarageApp(App):
    def build(self):
        self.db = self.load_database()

        main_layout = BoxLayout(orientation='vertical', padding=25, spacing=15)
        
        with main_layout.canvas.before:
            Color(0.1, 0.12, 0.18, 1)
            self.rect = Rectangle(size=(800, 1200), pos=main_layout.pos)
        main_layout.bind(size=self._update_rect, pos=self._update_rect)

        title = Label(
            text='GARAGE SCANNER', 
            font_size=28, 
            bold=True, 
            color=(0.2, 0.8, 1, 1),
            size_hint=(1, 0.1)
        )
        main_layout.add_widget(title)

        self.input = TextInput(
            hint_text='OBD Code (e.g. P0303)', 
            font_size=20, 
            size_hint=(1, 0.12),
            multiline=False,
            padding_y=(15, 15)
        )
        main_layout.add_widget(self.input)

        btn_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.12))
        
        search_btn = Button(
            text='Search', 
            font_size=18, 
            bold=True,
            background_color=(0, 0.6, 1, 1)
        )
        search_btn.bind(on_press=self.search_code)
        
        clear_btn = Button(
            text='Clear', 
            font_size=18, 
            background_color=(0.8, 0.2, 0.2, 1)
        )
        clear_btn.bind(on_press=self.clear_input)

        btn_layout.add_widget(search_btn)
        btn_layout.add_widget(clear_btn)
        main_layout.add_widget(btn_layout)

        self.result_label = Label(
            text=f'Total Codes Loaded: {len(self.db)}\nEnter a code to scan', 
            font_size=18, 
            color=(0.9, 0.9, 0.9, 1),
            size_hint=(1, 0.5)
        )
        main_layout.add_widget(self.result_label)

        return main_layout

    def load_database(self):
        if os.path.exists("codes.json"):
            try:
                with open("codes.json", "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print("Error loading database:", e)
                return {}
        return {}

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def search_code(self, instance):
        code = self.input.text.strip().upper()
        if code in self.db:
            self.result_label.text = f"CODE: {code}\n\nMeaning:\n{self.db[code]}"
            self.result_label.color = (0.2, 1, 0.4, 1)
        else:
            self.result_label.text = "Code Not Found!"
            self.result_label.color = (1, 0.3, 0.3, 1)

    def clear_input(self, instance):
        self.input.text = ""
        self.result_label.text = f"Total Codes Loaded: {len(self.db)}\nEnter a code to scan"
        self.result_label.color = (0.9, 0.9, 0.9, 1)

if __name__ == '__main__':
    GarageApp().run()
