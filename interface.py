from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPalette, QIntValidator
from PyQt5.QtCore import Qt

import files


class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))


class MainWindow(QWidget):
    def __init__(self, exit_callback):
        super().__init__()
        self.exit = exit_callback
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Heroes 3 maps cataloguer")
        main_grid = QGridLayout()

        source_button = Button("Maps source directory...", self)
        source_button.clicked.connect(self.select_directory)

        destination_button = Button("Maps save directory...", self)
        destination_button.clicked.connect(self.select_directory)

        self.source_path_input = QLineEdit(self)
        self.destination_path_input = QLineEdit(self)

        filter_frame = QFrame(self)

        self.maps_table = QTableWidget(self)

        export_button = Button("Move selected", self)
        export_button.clicked.connect(self.export)

        quit_button = Button("Quit", self)
        quit_button.clicked.connect(self.exit)

        game_version = QLabel("Game version:", filter_frame)
        game_version_selection = QComboBox(filter_frame)

        filter_area_grid = QGridLayout()

        filter_area_grid.addWidget(game_version)
        filter_area_grid.addWidget(game_version_selection)

        filter_frame.setLayout(filter_area_grid)

        main_grid.addWidget(source_button, 0, 0)
        main_grid.addWidget(self.source_path_input, 0, 1)
        main_grid.addWidget(destination_button, 1, 0)
        main_grid.addWidget(self.destination_path_input, 1, 1)
        main_grid.addWidget(filter_frame, 2, 0, 1, 2)
        main_grid.addWidget(self.maps_table, 3, 0, 1, 2)
        main_grid.addWidget(export_button, 4, 0, alignment=Qt.AlignLeft)
        main_grid.addWidget(quit_button, 4, 1, alignment=Qt.AlignRight)
        self.setLayout(main_grid)
        self.show()


    def export(self):
        pass

    def select_directory(self):
        res = QFileDialog.getExistingDirectory(self, "Source directory")[0]



app = QApplication([])
main = MainWindow(app.exit)
app.exec_()