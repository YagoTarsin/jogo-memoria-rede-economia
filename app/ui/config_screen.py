import shutil
import uuid
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QDoubleSpinBox,
    QSpinBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QFileDialog,
    QMessageBox,
    QHeaderView,
    QAbstractItemView,
)

from app import paths
from app.database import (
    get_all_cards,
    add_card,
    update_card,
    delete_card,
    get_setting,
    set_setting,
)


class ConfigScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.cards = []
        self.editing_card_id = None
        self.selected_image_path = None
        self._existing_image_filename = None
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(16)

        header = QHBoxLayout()
        back_button = QPushButton("←  Menu")
        back_button.setObjectName("secondaryButton")
        back_button.clicked.connect(self.main_window.go_to_menu)
        title = QLabel("⚙  Configurações")
        title.setStyleSheet("font-size: 26px; font-weight: 800; background: transparent;")
        header.addWidget(back_button)
        header.addStretch(1)
        header.addWidget(title)
        header.addStretch(1)
        root.addLayout(header)

        body = QHBoxLayout()
        body.setSpacing(20)
        root.addLayout(body, 1)

        # ---------- left: registered cards ----------
        left = QVBoxLayout()
        list_label = QLabel("Cartas cadastradas")
        list_label.setStyleSheet("font-size: 16px; font-weight: 700; background: transparent;")
        left.addWidget(list_label)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Imagem", "Nome", "Preço", "Promoção", "Ações"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)
        left.addWidget(self.table, 1)

        pairs_box = QHBoxLayout()
        pairs_label = QLabel("Pares por partida:")
        pairs_label.setStyleSheet("background: transparent;")
        self.pairs_spin = QSpinBox()
        self.pairs_spin.setMinimum(2)
        self.pairs_spin.setMaximum(2)
        save_pairs_button = QPushButton("Salvar quantidade")
        save_pairs_button.clicked.connect(self._save_pairs)
        pairs_box.addWidget(pairs_label)
        pairs_box.addWidget(self.pairs_spin)
        pairs_box.addWidget(save_pairs_button)
        pairs_box.addStretch(1)
        left.addLayout(pairs_box)

        body.addLayout(left, 3)

        # ---------- right: add / edit form ----------
        right = QVBoxLayout()
        form_label = QLabel("Cadastrar / editar carta")
        form_label.setStyleSheet("font-size: 16px; font-weight: 700; background: transparent;")
        right.addWidget(form_label)

        form = QFormLayout()
        form.setSpacing(10)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ex.: Café Torrado 500g")

        self.real_price_input = QDoubleSpinBox()
        self.real_price_input.setPrefix("R$ ")
        self.real_price_input.setMaximum(99999)
        self.real_price_input.setDecimals(2)

        self.promo_price_input = QDoubleSpinBox()
        self.promo_price_input.setPrefix("R$ ")
        self.promo_price_input.setMaximum(99999)
        self.promo_price_input.setDecimals(2)

        image_row = QHBoxLayout()
        self.image_preview = QLabel("Sem imagem")
        self.image_preview.setFixedSize(120, 100)
        self.image_preview.setAlignment(Qt.AlignCenter)
        self.image_preview.setStyleSheet("background-color: white; color: #333; border-radius: 6px;")
        choose_image_button = QPushButton("Escolher imagem")
        choose_image_button.clicked.connect(self._choose_image)
        image_row.addWidget(self.image_preview)
        image_row.addWidget(choose_image_button)

        form.addRow("Nome:", self.name_input)
        form.addRow("Preço normal:", self.real_price_input)
        form.addRow("Preço promoção:", self.promo_price_input)
        form.addRow("Imagem:", image_row)

        right.addLayout(form)

        form_buttons = QHBoxLayout()
        self.save_button = QPushButton("Salvar carta")
        self.save_button.clicked.connect(self._save_card)
        self.cancel_button = QPushButton("Cancelar edição")
        self.cancel_button.setObjectName("secondaryButton")
        self.cancel_button.clicked.connect(self._reset_form)
        self.cancel_button.setVisible(False)
        form_buttons.addWidget(self.save_button)
        form_buttons.addWidget(self.cancel_button)
        right.addLayout(form_buttons)
        right.addStretch(1)

        body.addLayout(right, 2)

    def refresh(self):
        self.cards = get_all_cards()
        self._populate_table()

        self.pairs_spin.setMaximum(max(2, len(self.cards)))
        try:
            current = int(get_setting("pairs_count", "8") or 8)
        except ValueError:
            current = 8
        self.pairs_spin.setValue(min(max(current, 2), self.pairs_spin.maximum()))

    def _populate_table(self):
        self.table.setRowCount(0)
        for card in self.cards:
            row = self.table.rowCount()
            self.table.insertRow(row)

            thumb_label = QLabel()
            thumb_label.setAlignment(Qt.AlignCenter)
            pixmap = QPixmap(str(paths.card_image_path(card.image_filename)))
            if not pixmap.isNull():
                thumb_label.setPixmap(pixmap.scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.table.setCellWidget(row, 0, thumb_label)

            self.table.setItem(row, 1, QTableWidgetItem(card.name))
            self.table.setItem(row, 2, QTableWidgetItem(f"R$ {card.real_price:.2f}"))
            self.table.setItem(row, 3, QTableWidgetItem(f"R$ {card.promo_price:.2f}"))

            actions = QWidget()
            actions_layout = QHBoxLayout(actions)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            edit_button = QPushButton("Editar")
            edit_button.clicked.connect(lambda checked=False, c=card: self._start_edit(c))
            delete_button = QPushButton("Excluir")
            delete_button.setObjectName("dangerButton")
            delete_button.clicked.connect(lambda checked=False, c=card: self._delete(c))
            actions_layout.addWidget(edit_button)
            actions_layout.addWidget(delete_button)
            self.table.setCellWidget(row, 4, actions)

            self.table.setRowHeight(row, 56)

    def _choose_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Escolher imagem", "", "Imagens (*.png *.jpg *.jpeg *.webp *.bmp)"
        )
        if file_path:
            self.selected_image_path = file_path
            pixmap = QPixmap(file_path).scaled(110, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_preview.setPixmap(pixmap)

    def _start_edit(self, card):
        self.editing_card_id = card.id
        self.name_input.setText(card.name)
        self.real_price_input.setValue(card.real_price)
        self.promo_price_input.setValue(card.promo_price)
        self.selected_image_path = None
        self._existing_image_filename = card.image_filename

        pixmap = QPixmap(str(paths.card_image_path(card.image_filename)))
        if not pixmap.isNull():
            self.image_preview.setPixmap(pixmap.scaled(110, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.image_preview.setText("Sem imagem")

        self.save_button.setText("Salvar alterações")
        self.cancel_button.setVisible(True)

    def _delete(self, card):
        confirm = QMessageBox.question(
            self, "Excluir carta", f'Tem certeza que deseja excluir "{card.name}"?'
        )
        if confirm == QMessageBox.Yes:
            delete_card(card.id)
            image_path = paths.card_image_path(card.image_filename)
            if image_path.exists():
                try:
                    image_path.unlink()
                except OSError:
                    pass
            if self.editing_card_id == card.id:
                self._reset_form()
            self.refresh()

    def _save_card(self):
        name = self.name_input.text().strip()
        real_price = self.real_price_input.value()
        promo_price = self.promo_price_input.value()

        if not name:
            QMessageBox.warning(self, "Dados incompletos", "Informe o nome do produto.")
            return
        if promo_price >= real_price:
            QMessageBox.warning(
                self, "Preços inválidos", "O preço da promoção deve ser menor que o preço normal."
            )
            return

        if self.selected_image_path:
            extension = Path(self.selected_image_path).suffix or ".png"
            filename = f"{uuid.uuid4().hex}{extension}"
            shutil.copy(self.selected_image_path, paths.card_image_path(filename))
        elif self.editing_card_id and self._existing_image_filename:
            filename = self._existing_image_filename
        else:
            QMessageBox.warning(self, "Imagem obrigatória", "Escolha uma imagem para o produto.")
            return

        if self.editing_card_id:
            update_card(self.editing_card_id, name, filename, real_price, promo_price)
        else:
            add_card(name, filename, real_price, promo_price)

        self._reset_form()
        self.refresh()

    def _reset_form(self):
        self.editing_card_id = None
        self.selected_image_path = None
        self._existing_image_filename = None
        self.name_input.clear()
        self.real_price_input.setValue(0)
        self.promo_price_input.setValue(0)
        self.image_preview.clear()
        self.image_preview.setText("Sem imagem")
        self.save_button.setText("Salvar carta")
        self.cancel_button.setVisible(False)

    def _save_pairs(self):
        set_setting("pairs_count", str(self.pairs_spin.value()))
        QMessageBox.information(self, "Configuração salva", "Quantidade de pares atualizada.")
