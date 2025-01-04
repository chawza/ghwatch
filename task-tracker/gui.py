from textual.app import App
from textual.containers import Vertical
from textual.widgets import Static, TextArea, Button
from textual.screen import Screen
from textual import events

class WelcomeScreen(Screen):
    def compose(self):
        yield Static("Enter Github Userrname")
        yield TextArea(id="username_input")
        yield Button('Submit', id="submit_button")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit_button":
            self.check_login()

    def on_key(self, event: events.Key) -> None:
        if event.key == "enter":
            self.check_login()

    def check_login(self):
        username = self.query_one("#username_input").text
        self.mount(Static(f'Entered: {username}'))

class TaskTrackerApp(App):
    def compose(self):
        yield WelcomeScreen()
