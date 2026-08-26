from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QStackedWidget

from app import styles
from app.database import init_db
from app.ui.menu_screen import MenuScreen
from app.ui.config_screen import ConfigScreen
from app.ui.game_screen import GameScreen


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        init_db()

        self.setWindowTitle("Jogo da Memória - Promoções do Supermercado")
        self.setStyleSheet(styles.MAIN_STYLESHEET)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.menu_screen = MenuScreen(self)
        self.config_screen = ConfigScreen(self)
        self.game_screen = GameScreen(self)

        self.stack.addWidget(self.menu_screen)
        self.stack.addWidget(self.config_screen)
        self.stack.addWidget(self.game_screen)

        self.go_to_menu()
        self.showFullScreen()

    def go_to_menu(self):
        self.menu_screen.refresh()
        self.stack.setCurrentWidget(self.menu_screen)

    def go_to_config(self):
        self.config_screen.refresh()
        self.stack.setCurrentWidget(self.config_screen)

    def go_to_game(self):
        if self.game_screen.start_new_game():
            self.stack.setCurrentWidget(self.game_screen)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
        else:
            super().keyPressEvent(event)
