COLOR_BG = "#1b3a2f"
COLOR_PRIMARY = "#2e7d32"
COLOR_PRIMARY_DARK = "#1b5e20"
COLOR_ACCENT = "#ffb300"
COLOR_DANGER = "#c62828"
COLOR_CARD_BACK_START = "#2e7d32"
COLOR_CARD_BACK_END = "#1b5e20"
COLOR_TEXT_LIGHT = "#ffffff"
COLOR_TEXT_MUTED = "#c8d6cf"

MAIN_STYLESHEET = f"""
QWidget {{
    background-color: {COLOR_BG};
    color: {COLOR_TEXT_LIGHT};
    font-family: 'Segoe UI', Arial, sans-serif;
}}
QPushButton {{
    background-color: {COLOR_PRIMARY};
    border: none;
    border-radius: 10px;
    padding: 14px 24px;
    font-size: 16px;
    font-weight: 600;
    color: white;
}}
QPushButton:hover {{
    background-color: {COLOR_PRIMARY_DARK};
}}
QPushButton:pressed {{
    background-color: #123f1b;
}}
QPushButton:disabled {{
    background-color: #4b5f56;
    color: #9fb3ab;
}}
QPushButton#dangerButton {{
    background-color: {COLOR_DANGER};
}}
QPushButton#dangerButton:hover {{
    background-color: #8e1c1c;
}}
QPushButton#secondaryButton {{
    background-color: transparent;
    border: 2px solid {COLOR_TEXT_LIGHT};
}}
QPushButton#secondaryButton:hover {{
    background-color: rgba(255, 255, 255, 0.12);
}}
QLineEdit, QDoubleSpinBox, QSpinBox {{
    background-color: white;
    color: #1b1b1b;
    border-radius: 6px;
    padding: 8px;
    font-size: 15px;
}}
QTableWidget {{
    background-color: #234c3d;
    border-radius: 8px;
    color: white;
    font-size: 13px;
    gridline-color: #2e6350;
}}
QHeaderView::section {{
    background-color: {COLOR_PRIMARY_DARK};
    color: white;
    padding: 6px;
    border: none;
    font-weight: 600;
}}
QLabel#titleLabel {{
    font-size: 42px;
    font-weight: 800;
    color: {COLOR_ACCENT};
    background: transparent;
}}
QLabel#subtitleLabel {{
    font-size: 18px;
    color: {COLOR_TEXT_MUTED};
    background: transparent;
}}
QScrollBar:vertical {{
    background: #234c3d;
    width: 12px;
}}
QScrollBar::handle:vertical {{
    background: {COLOR_PRIMARY};
    border-radius: 6px;
}}
"""
