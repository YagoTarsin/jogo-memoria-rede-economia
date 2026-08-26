import sqlite3
from typing import List, Optional

from app import paths
from app.models import Card

DB_PATH = paths.DATA_DIR / "database.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_connection()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS cards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                image_filename TEXT NOT NULL,
                real_price REAL NOT NULL,
                promo_price REAL NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def add_card(name: str, image_filename: str, real_price: float, promo_price: float) -> int:
    conn = get_connection()
    try:
        cur = conn.execute(
            "INSERT INTO cards (name, image_filename, real_price, promo_price) VALUES (?, ?, ?, ?)",
            (name, image_filename, real_price, promo_price),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def update_card(card_id: int, name: str, image_filename: str, real_price: float, promo_price: float) -> None:
    conn = get_connection()
    try:
        conn.execute(
            "UPDATE cards SET name = ?, image_filename = ?, real_price = ?, promo_price = ? WHERE id = ?",
            (name, image_filename, real_price, promo_price, card_id),
        )
        conn.commit()
    finally:
        conn.close()


def delete_card(card_id: int) -> None:
    conn = get_connection()
    try:
        conn.execute("DELETE FROM cards WHERE id = ?", (card_id,))
        conn.commit()
    finally:
        conn.close()


def get_all_cards() -> List[Card]:
    conn = get_connection()
    try:
        rows = conn.execute("SELECT * FROM cards ORDER BY id").fetchall()
        return [
            Card(row["id"], row["name"], row["image_filename"], row["real_price"], row["promo_price"])
            for row in rows
        ]
    finally:
        conn.close()


def get_card(card_id: int) -> Optional[Card]:
    conn = get_connection()
    try:
        row = conn.execute("SELECT * FROM cards WHERE id = ?", (card_id,)).fetchone()
        if row is None:
            return None
        return Card(row["id"], row["name"], row["image_filename"], row["real_price"], row["promo_price"])
    finally:
        conn.close()


def get_setting(key: str, default: str = "") -> str:
    conn = get_connection()
    try:
        row = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
        return row["value"] if row else default
    finally:
        conn.close()


def set_setting(key: str, value: str) -> None:
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO settings (key, value) VALUES (?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (key, value),
        )
        conn.commit()
    finally:
        conn.close()
