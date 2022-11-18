import argparse
from email.policy import default
import json
from typing import Type
from pydantic import BaseModel
from textual.containers import Container
from textual.app import App, ComposeResult, CSSPathType
from textual.widgets import Static
from textual.widget import Widget
from textual.driver import Driver

from processtui.logviewer import LogViewer


CommandIdentifier = str


class CommandDefinition(BaseModel):
    name: CommandIdentifier
    command: str


CommandDefinitions = dict[CommandIdentifier, CommandDefinition]


class Service(Static):
    # defer the rendering to this
    pass


class ServicesBar(Container):
    command_definitions = []

    def __init__(
        self,
        *children: Widget,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        command_definitions: CommandDefinitions,
    ) -> None:
        super().__init__(*children, name=name, id=id, classes=classes)
        self.command_definitions = command_definitions

    def update_services(self, services=list[str]):
        self.services = services
        self.mount_services()

    def mount_services(self):
        for service in self.query(Service):
            service.remove()
        for service in self.services:
            self.mount(Service(service))

    def compose(self) -> ComposeResult:
        for command, _command_definition in self.command_definitions.items():
            yield Service(command)

    def on_click(self):
        self.update_services(["test"])


class MainTUI(App):
    CSS_PATH = "layout.css"
    BINDINGS = [("l", "toggle_logs", "Show Logs")]

    logs: bool = False

    command_definitions: CommandDefinitions

    def __init__(
        self,
        driver_class: Type[Driver] | None = None,
        css_path: CSSPathType = None,
        watch_css: bool = False,
        command_definitions={},
    ):
        super().__init__(driver_class, css_path, watch_css)
        self.command_definitions = command_definitions

    def compose(self) -> ComposeResult:
        yield ServicesBar(id="sidebar", command_definitions=self.command_definitions)
        yield Container(id="body")

    def action_toggle_logs(self) -> None:
        if self.logs:
            self.pop_screen()
        else:
            self.push_screen(LogViewer())
        self.logs = not self.logs


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="ProgramName",
        description="What the program does",
        epilog="Text at the bottom of help",
    )

    parser.add_argument("filename")
    args = parser.parse_args()

    with open(args.filename, "r") as f:
        command_definitions_json = json.loads(f.read())
        command_definitions = {}

        for command_definition_identifier in command_definitions_json:
            command_definitions[command_definition_identifier] = CommandDefinition(
                **command_definitions_json[command_definition_identifier]
            )

        app = MainTUI(command_definitions=command_definitions)
        app.run()
