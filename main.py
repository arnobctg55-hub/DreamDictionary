from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.clock import Clock

import json
import os
import urllib.parse
import urllib.request
import threading

Window.clearcolor = get_color_from_hex("#EAF3FF")

# Offline Dictionary
dictionary = {
    "apple": {
        "meaning": "আপেল",
        "example": "I eat an apple."
    },
    "beautiful": {
        "meaning": "সুন্দর",
        "example": "This flower is beautiful."
    },
    "book": {
        "meaning": "বই",
        "example": "I read a book."
    },
    "dream": {
        "meaning": "স্বপ্ন",
        "example": "Follow your dream."
    },
    "education": {
        "meaning": "শিক্ষা",
        "example": "Education is important."
    },
    "friend": {
        "meaning": "বন্ধু",
        "example": "He is my friend."
    },
    "love": {
        "meaning": "ভালোবাসা",
        "example": "Love is powerful."
    },
    "water": {
        "meaning": "পানি",
        "example": "I drink water."
    }
}


class DictionaryApp(App):

    def build(self):

        self.title = "Dream Dictionary"

        main = BoxLayout(
            orientation="vertical",
            padding=18,
            spacing=12
        )

        title = Label(
            text="[b]Dream Dictionary[/b]",
            markup=True,
            font_size=28,
            color=get_color_from_hex("#1769D2"),
            size_hint_y=None,
            height=65
        )

        self.search = TextInput(
            hint_text="Search English or Bangla...",
            multiline=False,
            size_hint_y=None,
            height=55,
            font_size=18
        )

        search_btn = Button(
            text="SEARCH",
            size_hint_y=None,
            height=50,
            background_color=get_color_from_hex("#1976D2"),
            background_normal=""
        )

        search_btn.bind(on_press=self.search_word)

        self.result = Label(
            text="Welcome to Dream Dictionary!",
            color=get_color_from_hex("#12345A"),
            font_size=18,
            halign="left",
            valign="top",
            size_hint_y=None
        )

        self.result.bind(
            texture_size=self.update_height
        )

        scroll = ScrollView()
        scroll.add_widget(self.result)

        main.add_widget(title)
        main.add_widget(self.search)
        main.add_widget(search_btn)
        main.add_widget(scroll)

        return main

    def update_height(self, instance, size):
        instance.height = size[1] + 30

    def search_word(self, instance):

        word = self.search.text.strip().lower()

        if not word:
            self.result.text = "Please enter a word."
            return

        if word in dictionary:

            data = dictionary[word]

            self.result.text = (
                f"[b]Word:[/b] {word}\n\n"
                f"[b]Meaning:[/b] {data['meaning']}\n\n"
                f"[b]Example:[/b] {data['example']}"
            )

            self.result.markup = True

        else:

            self.result.text = "Searching online..."

            threading.Thread(
                target=self.online_search,
                args=(word,),
                daemon=True
            ).start()

    def online_search(self, word):

        try:

            url = (
                "https://api.mymemory.translated.net/get?"
                + urllib.parse.urlencode({
                    "q": word,
                    "langpair": "en|bn"
                })
            )

            request = urllib.request.Request(
                url,
                headers={"User-Agent": "DreamDictionary/1.0"}
            )

            with urllib.request.urlopen(
                request, timeout=10
            ) as response:

                data = json.loads(
                    response.read().decode("utf-8")
                )

            meaning = data["responseData"]["translatedText"]

            Clock.schedule_once(
                lambda dt: self.show_result(word, meaning)
            )

        except Exception:

            Clock.schedule_once(
                lambda dt: self.show_result(
                    word, "Word not found. Check internet."
                )
            )

    def show_result(self, word, meaning):

        self.result.text = (
            f"[b]Word:[/b] {word}\n\n"
            f"[b]Meaning:[/b] {meaning}\n\n"
            f"[b]Example:[/b] Online example coming soon."
        )

        self.result.markup = True


if __name__ == "__main__":
    DictionaryApp().run()
