import gzip
import json
from pathlib import Path

_DATA_PATH = Path(__file__).parent / "data" / "palettes.json.gz"

_palettes = None


def _load():
    global _palettes
    if _palettes is None:
        with gzip.open(_DATA_PATH, "rt", encoding="utf-8") as f:
            _palettes = json.load(f)
    return _palettes


def get_palette(name):
    return _load()[name]


def all_names():
    return list(_load().keys())


def palette_count():
    return len(_load())
