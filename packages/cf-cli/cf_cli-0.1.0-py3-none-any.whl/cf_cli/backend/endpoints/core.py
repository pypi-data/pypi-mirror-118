from pathlib import Path

import typer
import orjson

BASE_URL = "https://api.cloudflare.com/client/v4"

_cache_path = Path(Path(typer.get_app_dir("Cloudflare CLI")) / ".cache.json")

with open(_cache_path, "r") as cache_file:
    CACHE = orjson.loads(cache_file.read())

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {CACHE['token']}"
}