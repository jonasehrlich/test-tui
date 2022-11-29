from textual import app, containers, widgets, binding

OUTPUT_FORMAT_STRING = "%(asctime)s %(message)s"
DATE_FORMAT_STRING = "%Y-%m-%d %H:%M:%S"


class TestTUIApp(app.App):

    CSS_PATH = "test-tui.css"
    BINDINGS = [
        binding.Binding("q", "quit", "Quit"),
        binding.Binding("F5", "reload_tests", "Reload Tests"),
        binding.Binding("o", "toggle_output_pane", "Toggle output pane"),
        binding.Binding("O", "toggle_output_pane", "Toggle output pane"),
    ]

    def compose(self) -> app.ComposeResult:
        yield widgets.Header()

        yield containers.Horizontal(
            widgets.Button("reload", id="reload-tests", variant="primary"),
            id="control-panel",
        )
        yield containers.Horizontal(
            containers.Vertical(
                widgets.Static("test tree"),
                *[widgets.Static(f"Vertical layout, child {number}") for number in range(15)],
                id="left-pane",
            ),
            containers.Container(widgets.Static("log output"), id="test-output-pane"),
            id="app-grid",
        )

        yield containers.Container(
            widgets.Static("This"),
            classes="hidden",
            id="app-output",
        )
        yield widgets.Footer()

    async def on_button_pressed(self, event: widgets.Button.Pressed):
        button_id = event.button.id

        if button_id == "reload-tests":
            await self.action_reload_tests()

    async def action_reload_tests(self) -> None:
        # TODO: send update to status
        self.log("reload tests")

    async def action_toggle_output_pane(self) -> None:
        # self.test_tui_view.output_widget.content.append(f"{datetime.datetime.now()} test")
        # self.test_tui_view.output_logger.info("test")
        output_pane = self.query("#app-output")
        output_pane.toggle_class("hidden")
        self.log("toggle output pane")


test_tui_app = TestTUIApp()
