from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette


class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)


class ProgressWindow(QDialog):
    def __init__(self, parent, dirpath):
        super().__init__(parent)
        self.init_ui(dirpath)

    def init_ui(self, directory):
        self.setWindowTitle("Opening {}".format(directory))
        self.progress = QProgressBar(self)
        self.progress.setGeometry(0, 0, 600, 30)
        self.show()
        self.setFixedSize(self.width(), self.height())

    def set_maximum(self, value):
        self.maximum = value
        self.progress.setMaximum(self.maximum)

    def set_value(self, value):
        self.progress.setValue(value)
        if value == self.maximum:
            self.destroy()


class MainWindow(QWidget):
    def __init__(self, exit_callback, aggregator_class):
        super().__init__()
        self.aggregator = aggregator_class
        self.exit = exit_callback
        self.maps_list = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Heroes 3 maps cataloguer")
        main_grid = QGridLayout()
        source_button = Button("Maps source directory...", self)
        source_button.clicked.connect(self.select_source_directory)
        destination_button = Button("Maps save directory...", self)
        destination_button.setFixedWidth(source_button.minimumSizeHint().width())
        destination_button.clicked.connect(self.select_destination_directory)
        self.source_path_entry = QLineEdit(self)
        self.destination_path_entry = QLineEdit(self)
        for w in (self.source_path_entry, self.destination_path_entry):
            self.disable_entry(w)
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

    def disable_entry(self, widget):
        back_colour = self.palette().color(QPalette.Background)
        palette = QPalette()
        palette.setColor(widget.backgroundRole(), back_colour)
        widget.setPalette(palette)
        widget.setReadOnly(True)

    def export(self):
        pass

    def _select_directory(self, title):
        res = QFileDialog.getExistingDirectory(self, title)
        if res:
            return res

    def select_source_directory(self):
        self.source_dir = self._select_directory("Source directory")

    def select_destination_directory(self):
        self.destination_dir = self._select_directory("Destination directory")

    def collect_maps(self):
        """"""
        if self.source_dir:
            progress = ProgressWindow(self, self.source_dir)
            files_aggregator = self.aggregator(self.source_dir)
            files_list = files_aggregator.get_files()
            progress.set_maximum(len(files_list))
            count = 0
            for parsed_map in files_aggregator.prepare():
                count += 1
                progress.set_value(count)
                self.maps_list.append(parsed_map)
        #progress.destroy()



def start(aggregator_class):
    app = QApplication([])
    gui = MainWindow(app.exit, aggregator_class)
    gui.show()
    app.exec_()
