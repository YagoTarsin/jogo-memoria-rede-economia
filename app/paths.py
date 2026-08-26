from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
CARDS_DIR = ASSETS_DIR / "cards"
DATA_DIR = BASE_DIR / "data"

CARDS_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)


def card_image_path(filename: str) -> Path:
    return CARDS_DIR / filename
