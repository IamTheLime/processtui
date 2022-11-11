from rich.console import RenderableType
from rich.syntax import Syntax
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.screen import Screen
from pygments.lexers.special import OutputLexer
from textual.widgets import Static


class Logger(Static):
    logview: reactive[Syntax] = reactive(
        Syntax(
            "",
            lexer=OutputLexer(),
            line_numbers=True,
            word_wrap=False,
            indent_guides=True,
            theme="github-dark",
        )
    )

    def update_logview(self, updated_log=""):
        previous_log = self.logview.code if self.logview else ""

        self.logview = Syntax(
            previous_log + f"{updated_log}\n",
            lexer=OutputLexer(),
            line_numbers=True,
            word_wrap=False,
            indent_guides=True,
            theme="github-dark",
        )

    def render(self) -> RenderableType:
        return self.logview


class LogViewer(Screen):
    async def on_click(self) -> None:
        logger = self.query_one(Logger)
        logger.update_logview("dsfgdfgsdfgds")

    def compose(self) -> ComposeResult:
        yield Logger(id="log", expand=True)
