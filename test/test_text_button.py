from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Footer, Header, Button, Static
from textual.reactive import reactive
from textual.css.query import NoMatches
import typing as ty


class TextButtonTest(App):

    CSS = """\
Button.text-button {
    height: 1;
    min-width: 2;
    border-top: none;
    border-bottom: none;
    margin: 0 1;
}
"""

    running = reactive(False)

    def compose(self) -> ComposeResult:
        """Compose our UI."""
        yield Header()
        yield Horizontal(
            # Button("test button 1", id="test-button", classes="text-button"),
            Button("test button 1", id="test-button"),
            Button(self.run_stop_button_label, id="run-stop-button", classes="text-button"),
        )
        yield Footer()

    @property
    def run_stop_button_label(self) -> str:
        return "🟥" if self.running else "▶️"

    def watch_running(self, _):
        try:
            run_stop_button = self.query_one("#run-stop-button", Button)
        except NoMatches:
            pass
        else:
            run_stop_button.label = self.run_stop_button_label

        ...

    async def on_button_pressed(self, event: Button.Pressed):
        button_id = event.button.id

        if button_id == "run-stop-button":
            self.running = not self.running


if __name__ == "__main__":
    TextButtonTest().run()
