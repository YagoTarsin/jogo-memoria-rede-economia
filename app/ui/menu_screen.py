from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

from app.database import get_all_cards, get_setting


class MenuScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(22)

        title = QLabel("Jogo da Memória")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Descubra as promoções da semana!")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignCenter)

        self.info_label = QLabel("")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("font-size: 14px; color: #c8d6cf; background: transparent;")

        play_button = QPushButton("▶  Jogar")
        play_button.setMinimumWidth(280)
        play_button.setMinimumHeight(64)
        play_button.setStyleSheet("font-size: 22px;")
        play_button.clicked.connect(self.main_window.go_to_game)

        config_button = QPushButton("⚙  Configurações")
        config_button.setObjectName("secondaryButton")
        config_button.setMinimumWidth(220)
        config_button.clicked.connect(self.main_window.go_to_config)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(10)
        layout.addWidget(play_button, alignment=Qt.AlignCenter)
        layout.addWidget(config_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.info_label)

    def refresh(self):
        cards = get_all_cards()
        pairs = get_setting("pairs_count", "8")
        self.info_label.setText(
            f"{len(cards)} carta(s) cadastrada(s)  ·  partida configurada para {pairs} pares"
        )
