from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QLabel

from app import paths, styles
from app.models import Card


class CardWidget(QPushButton):
    """A single memory-game card. States: back, front, treasure, matched."""

    def __init__(self, card: Card, parent=None):
        super().__init__(parent)
        self.card = card
        self.state = "back"
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumSize(150, 190)
        self._build_ui()
        self.show_back()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)

        self.name_label = QLabel()
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setWordWrap(True)
        self.name_label.setStyleSheet("font-size: 13px; font-weight: 600; background: transparent;")

        self.price_label = QLabel()
        self.price_label.setAlignment(Qt.AlignCenter)
        self.price_label.setWordWrap(True)
        self.price_label.setStyleSheet("font-size: 13px; font-weight: 800; background: transparent;")

        layout.addWidget(self.image_label, 1)
        layout.addWidget(self.name_label)
        layout.addWidget(self.price_label)

    def show_back(self):
        self.state = "back"
        self.setEnabled(True)
        self.image_label.clear()
        self.image_label.setText("🛒")
        self.image_label.setStyleSheet("font-size: 48px; background: transparent;")
        self.name_label.clear()
        self.price_label.clear()
        self.setStyleSheet(self._back_style())

    def show_front(self):
        self.state = "front"
        self._set_product_image()
        self.name_label.setText(self.card.name)
        self.price_label.clear()
        self.setStyleSheet(self._front_style())

    def show_treasure(self):
        self.state = "treasure"
        self.image_label.clear()
        self.image_label.setText("🎁")
        self.image_label.setStyleSheet("font-size: 56px; background: transparent;")
        self.name_label.clear()
        self.price_label.setText("Promoção encontrada!")
        self.price_label.setStyleSheet(
            f"font-size: 13px; font-weight: 700; color: {styles.COLOR_ACCENT}; background: transparent;"
        )
        self.setStyleSheet(self._treasure_style())

    def show_matched(self):
        self.state = "matched"
        self._set_product_image()
        self.name_label.setText(self.card.name)
        self.price_label.setText(
            f"De R$ {self.card.real_price:.2f}\npor R$ {self.card.promo_price:.2f}"
        )
        self.price_label.setStyleSheet(
            f"font-size: 13px; font-weight: 800; color: {styles.COLOR_ACCENT}; background: transparent;"
        )
        self.setStyleSheet(self._matched_style())
        self.setEnabled(False)

    def _set_product_image(self):
        pixmap = QPixmap(str(paths.card_image_path(self.card.image_filename)))
        self.image_label.clear()
        if pixmap.isNull():
            self.image_label.setText("🖼")
            self.image_label.setStyleSheet("font-size: 40px; background: transparent;")
        else:
            scaled = pixmap.scaled(110, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled)

    def _back_style(self):
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {styles.COLOR_CARD_BACK_START}, stop:1 {styles.COLOR_CARD_BACK_END});
                border: 3px solid #0f2e18;
                border-radius: 14px;
            }}
            QPushButton:hover {{
                border: 3px solid {styles.COLOR_ACCENT};
            }}
        """

    def _front_style(self):
        return """
            QPushButton {
                background-color: white;
                border: 3px solid #cfd8d4;
                border-radius: 14px;
            }
        """

    def _treasure_style(self):
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #6d4c1f, stop:1 #402c0f);
                border: 3px solid {styles.COLOR_ACCENT};
                border-radius: 14px;
            }}
        """

    def _matched_style(self):
        return f"""
            QPushButton {{
                background-color: #fff8e1;
                border: 3px solid {styles.COLOR_ACCENT};
                border-radius: 14px;
            }}
        """
