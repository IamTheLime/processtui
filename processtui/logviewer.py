from random import randint
from uuid import uuid1
from rich.syntax import Syntax
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import Screen
from pygments.lexers.special import OutputLexer
from textual.widget import Widget
from textual.widgets import Static
from textual import log


class LogViewer(Widget):
    id: str = str(uuid1())
    logview: Syntax | None = None

    def update_logview(self, updated_log=""):
        if self.logview == None:
            self.logview = Syntax(
                f"{updated_log}",
                lexer=OutputLexer(),
                line_numbers=False,
                word_wrap=False,
                indent_guides=True,
                theme="github-dark",
            )
        else:
            self.logview.code += f"{updated_log}"

        self.query_one("#code_" + self.id, Static).update(self.logview)
        self.query_one("#code_container_" + self.id, Vertical).scroll_end(
            animate=False, speed=100
        )

    def compose(self) -> ComposeResult:
        yield Container(
            Vertical(
                Static(id="code_" + self.id, expand=True),
                id="code_container_" + self.id,
            )
        )


# class LogViewer(Screen):
#     CSS_PATH = "logviewer.css"

#     async def on_click(self) -> None:
#         logger = self.query_one(Logger)
#         logger.update_logview(f"dsfgdfgsdfgds{randint(1,59)}")
#         log(logger.logview.code)
#         # self.query_one("#test").update("test")

#     def compose(self) -> ComposeResult:
#         yield Logger()
