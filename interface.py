from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPalette, QIntValidator
from PyQt5.QtCore import Qt

import files


class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)


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
        destination_button.setFixedWidth(source_button.minimumSizeHint().width())
        destination_button.clicked.connect(self.select_directory)
        self.source_path_entry = QLineEdit(self)
        self.destination_path_entry = QLineEdit(self)
        filter_frame = QFrame(self)
        self.maps_table = QTableWidget(self)
        export_button = Button("Move selected", self)
        export_button.clicked.connect(self.export)
        quit_button = Button("Quit", self)
        quit_button.clicked.connect(self.exit)

        game_version_selection = QComboBox(filter_frame)
        size_selection = QComboBox(filter_frame)
        self.map_name_search_entry = QLineEdit(filter_frame)
        self.description_search_entry = QLineEdit(filter_frame)
        self.filter_inclusive_button = QRadioButton(filter_frame)
        self.filter_exclusive_button = QRadioButton(filter_frame)
        search_button = Button("Search", filter_frame)
        search_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        filter_area_grid = QGridLayout()
        filter_area_grid.addWidget(QLabel("Filter", filter_frame), 0, 0, 1, 6,
                                   alignment=Qt.AlignCenter)
        filter_area_grid.addWidget(QLabel("Game version:", filter_frame), 1, 0)
        filter_area_grid.addWidget(game_version_selection, 2, 0)
        filter_area_grid.addWidget(QLabel("Map size:"), 3, 0)
        filter_area_grid.addWidget(size_selection, 4, 0)
        filter_area_grid.addWidget(QLabel("Map name contains"), 2, 1,
                                   alignment=Qt.AlignRight)
        filter_area_grid.addWidget(QLabel("Description contains"), 4, 1,
                                   alignment=Qt.AlignRight)
        filter_area_grid.addWidget(self.map_name_search_entry, 2, 2)
        filter_area_grid.addWidget(self.description_search_entry, 4, 2)
        filter_area_grid.addWidget(self.filter_inclusive_button, 2, 3)
        filter_area_grid.addWidget(QLabel("Search mode"), 3, 3,
                                   alignment=Qt.AlignCenter)
        filter_area_grid.addWidget(self.filter_exclusive_button, 4, 3)
        filter_area_grid.addWidget(search_button, 1, 5, 4, 1)

        filter_frame.setLayout(filter_area_grid)

        main_grid.addWidget(source_button, 0, 0)
        main_grid.addWidget(self.source_path_entry, 0, 1)
        main_grid.addWidget(destination_button, 1, 0)
        main_grid.addWidget(self.destination_path_entry, 1, 1)
        main_grid.addWidget(filter_frame, 2, 0, 1, 2)
        main_grid.addWidget(self.maps_table, 3, 0, 1, 2)
        main_grid.addWidget(export_button, 4, 0, alignment=Qt.AlignLeft)
        main_grid.addWidget(quit_button, 4, 1, alignment=Qt.AlignRight)

        self.setLayout(main_grid)

    def export(self):
        pass

    def select_directory(self):
        res = QFileDialog.getExistingDirectory(self, "Source directory")[0]


def start():
    app = QApplication([])
    gui = MainWindow(app.exit)
    gui.show()
    app.exec_()
