import runpy

import typer
from pathlib import Path


APP_NAME = "Cloudflare CLI"
app_dir = Path(typer.get_app_dir(APP_NAME))
app_dir.mkdir(exist_ok=True)
cache = Path(app_dir / ".cache.json")
cache.touch(exist_ok=True)
app = typer.Typer(no_args_is_help=True)

commands_path = Path(__file__).parent.resolve() / "command_groups"

for file in commands_path.glob("*.py"):
    module = runpy.run_path(file)[file.stem]
    app.add_typer(module, name=file.stem)


__all__ = (
    "app"
)