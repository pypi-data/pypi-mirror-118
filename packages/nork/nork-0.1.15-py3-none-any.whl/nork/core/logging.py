import typer


class Log:

    title: str = "NOR/K"

    @classmethod
    def error(self, msg: str):
        typer.echo(typer.style(
            f"[{self.title}]", fg=typer.colors.WHITE, bg=typer.colors.RED) + f" {msg}")
