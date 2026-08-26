import math
import random

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QMessageBox,
    QDialog,
    QScrollArea,
)

from app.database import get_all_cards, get_setting
from app.ui.card_widget import CardWidget


class GameScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.cards_widgets = []
        self.selected = []
        self.found_cards = []
        self.matched_count = 0
        self.total_pairs = 0
        self.moves = 0
        self.locked = False
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(16)

        header = QHBoxLayout()
        back_button = QPushButton("←  Menu")
        back_button.setObjectName("secondaryButton")
        back_button.clicked.connect(self.main_window.go_to_menu)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 18px; font-weight: 700; background: transparent;")

        restart_button = QPushButton("⟲  Reiniciar")
        restart_button.setObjectName("secondaryButton")
        restart_button.clicked.connect(self.start_new_game)

        header.addWidget(back_button)
        header.addStretch(1)
        header.addWidget(self.status_label)
        header.addStretch(1)
        header.addWidget(restart_button)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)

        self.grid_container = QWidget()
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setSpacing(14)
        scroll.setWidget(self.grid_container)

        root.addLayout(header)
        root.addWidget(scroll, 1)

    def start_new_game(self) -> bool:
        all_cards = get_all_cards()
        try:
            pairs_setting = int(get_setting("pairs_count", "8") or 8)
        except ValueError:
            pairs_setting = 8
        pairs = min(pairs_setting, len(all_cards))

        if pairs < 2:
            QMessageBox.warning(
                self.main_window,
                "Cartas insuficientes",
                "Cadastre pelo menos 2 cartas na tela de Configurações para poder jogar.",
            )
            self.main_window.go_to_config()
            return False

        self._clear_grid()

        chosen = random.sample(all_cards, pairs)
        deck = chosen * 2
        random.shuffle(deck)

        self.total_pairs = pairs
        self.matched_count = 0
        self.moves = 0
        self.selected = []
        self.found_cards = []
        self.locked = False
        self._update_status()

        cols = max(2, min(math.ceil(math.sqrt(len(deck) * 1.6)), 8))

        self.cards_widgets = []
        for index, card in enumerate(deck):
            widget = CardWidget(card)
            widget.clicked.connect(lambda checked=False, w=widget: self._on_card_clicked(w))
            row, col = divmod(index, cols)
            self.grid_layout.addWidget(widget, row, col)
            self.cards_widgets.append(widget)

        return True

    def _clear_grid(self):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def _update_status(self):
        self.status_label.setText(
            f"Pares encontrados: {self.matched_count}/{self.total_pairs}    ·    Jogadas: {self.moves}"
        )

    def _on_card_clicked(self, widget: CardWidget):
        if self.locked or widget.state != "back":
            return

        widget.show_front()
        self.selected.append(widget)

        if len(self.selected) == 2:
            self.locked = True
            self.moves += 1
            self._update_status()
            QTimer.singleShot(650, self._resolve_selection)

    def _resolve_selection(self):
        first, second = self.selected
        if first.card.id == second.card.id:
            first.show_treasure()
            second.show_treasure()
            QTimer.singleShot(550, lambda: self._reveal_match(first, second))
        else:
            first.show_back()
            second.show_back()
            self.selected = []
            self.locked = False

    def _reveal_match(self, first: CardWidget, second: CardWidget):
        first.show_matched()
        second.show_matched()
        self.found_cards.append(first.card)
        self.matched_count += 1
        self.selected = []
        self.locked = False
        self._update_status()

        if self.matched_count == self.total_pairs:
            QTimer.singleShot(400, self._show_victory)

    def _show_victory(self):
        dialog = QDialog(self.main_window)
        dialog.setWindowTitle("Parabéns!")
        dialog.setModal(True)
        dialog.setStyleSheet(self.main_window.styleSheet())
        layout = QVBoxLayout(dialog)
        layout.setSpacing(14)
        layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel("🏆 Parabéns! Você encontrou todas as promoções!")
        title.setWordWrap(True)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: 800; color: #ffb300; background: transparent;")
        layout.addWidget(title)

        moves_label = QLabel(f"Total de jogadas: {self.moves}")
        moves_label.setAlignment(Qt.AlignCenter)
        moves_label.setStyleSheet("background: transparent;")
        layout.addWidget(moves_label)

        total_savings = sum(c.real_price - c.promo_price for c in self.found_cards)
        savings_label = QLabel(f"Economia total nas promoções: R$ {total_savings:.2f}")
        savings_label.setAlignment(Qt.AlignCenter)
        savings_label.setStyleSheet("font-size: 16px; font-weight: 700; color: #ffb300; background: transparent;")
        layout.addWidget(savings_label)

        buttons = QHBoxLayout()
        play_again = QPushButton("Jogar novamente")
        play_again.clicked.connect(lambda: (dialog.accept(), self.start_new_game()))
        menu_button = QPushButton("Voltar ao Menu")
        menu_button.setObjectName("secondaryButton")
        menu_button.clicked.connect(lambda: (dialog.accept(), self.main_window.go_to_menu()))
        buttons.addWidget(play_again)
        buttons.addWidget(menu_button)
        layout.addLayout(buttons)

        dialog.exec()
