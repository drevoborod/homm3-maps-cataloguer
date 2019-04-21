from collections import namedtuple

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPalette, QBrush, QColor, QIcon

import constants


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


class Filter(QFrame):
    def __init__(self, parent, callable):
        super().__init__(parent)
        self.callable = callable
        self.init_ui()

    def init_ui(self):
        self.setFrameShape(QFrame.Panel)
        self.game_version_selection = QComboBox(self)
        self.game_version_selection.addItems(["Any"] +
                                             list(constants.MAP_TYPE.values()))
        self.size_selection = QComboBox(self)
        self.size_selection.addItems(["Any"] + list(constants.MAP_SIZE.values()))
        self.map_name_entry = QLineEdit(self)
        self.description_entry = QLineEdit(self)

        search_button = QToolButton(self)
        search_button.setText("Search")
        search_button.clicked.connect(self.callable)
        search_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        search_button.setIcon(QIcon('magnifier.png'))
        search_button.setIconSize(QSize(50, 50))
        search_button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        filter_area_grid = QGridLayout()

        filter_header_frame = QFrame(self)
        filter_header_frame_layout = QHBoxLayout()
        filter_header = QLabel("Filter", filter_header_frame)
        font = filter_header.font()
        font.setPointSize(font.pointSize() + 2)
        font.setBold(True)
        filter_header.setFont(font)
        filter_header_frame_layout.addWidget(filter_header,
                                             alignment=Qt.AlignCenter)
        filter_header_frame.setLayout(filter_header_frame_layout)

        filter_area_grid.addWidget(filter_header_frame, 0, 0, 1, 6)
        filter_area_grid.addWidget(QLabel("Game version:", self), 1, 0)
        filter_area_grid.addWidget(self.game_version_selection, 2, 0)
        filter_area_grid.addWidget(QLabel("Map size:"), 3, 0)
        filter_area_grid.addWidget(self.size_selection, 4, 0)
        filter_area_grid.addWidget(QLabel("Map name contains:"), 2, 1,
                                   alignment=Qt.AlignRight)
        filter_area_grid.addWidget(QLabel("Description contains:"), 4, 1,
                                   alignment=Qt.AlignRight)
        filter_area_grid.addWidget(self.map_name_entry, 2, 2)
        filter_area_grid.addWidget(self.description_entry, 4, 2)
        filter_area_grid.addWidget(search_button, 1, 4, 4, 1)

        self.setLayout(filter_area_grid)

    def _get_filter_values(self):
        res = namedtuple("FilterValues", "type,size,name,descr")
        game_ver = [self.game_version_selection.currentText()]
        if game_ver[0] == "Any":
            game_ver = constants.MAP_TYPE.values()
        map_size = [self.size_selection.currentText()]
        if map_size[0] == "Any":
            map_size = constants.MAP_SIZE.values()
        return res(game_ver, map_size,
                   self.map_name_entry.text(), self.description_entry.text())

    def apply(self, maps_list):
        filter_values = self._get_filter_values()
        res = []
        for map_item in maps_list:
            if (map_item.type in filter_values.type
                    and constants.MAP_SIZE[map_item.size] in filter_values.size
                    and filter_values.name.lower() in map_item.name.lower()
                    and filter_values.descr.lower() in map_item.description.lower()):
                res.append(map_item)
        return res


class MainWindow(QWidget):
    def __init__(self, exit_callback, aggregator_class):
        super().__init__()
        self.aggregator = aggregator_class
        self.exit = exit_callback
        self.maps_list = []
        self.filtered_maps_list = []
        self.selected_map_files = set()
        self.source_dir = None
        self.destination_dir = None
        self.init_ui()
        self.center()

    def init_ui(self):
        self.setWindowTitle("Heroes 3 maps cataloguer")
        main_grid = QGridLayout()

        source_frame = QFrame(self)
        source_button = Button("Import maps from...", source_frame)
        source_button.clicked.connect(self.select_source_directory)
        self.source_path_entry = QLineEdit(source_frame)
        self.disable_entry(self.source_path_entry)

        source_area_grid = QHBoxLayout()
        source_area_grid.addWidget(source_button)
        source_area_grid.addWidget(self.source_path_entry)

        source_frame.setLayout(source_area_grid)

        self.filter = Filter(self, self.fill_table)

        self.maps_table = QTableWidget(self)
        self.move_checkbox = QCheckBox(self)
        self.move_checkbox.setText(
            "Remove selected maps from source directory on export")
        self.overwrite_checkbox = QCheckBox(self)
        self.overwrite_checkbox.setText(
            "Overwrite existing files in target directory")
        self.export_button = Button("Export maps", self)
        self.export_button.clicked.connect(self.export)
        self.export_button.setEnabled(False)
        quit_button = Button("Quit", self)
        quit_button.clicked.connect(self.exit)

        main_grid.addWidget(source_frame, 0, 0, 1, 2)
        main_grid.addWidget(self.filter, 1, 0, 1, 2)
        main_grid.addWidget(self.maps_table, 2, 0, 1, 2)
        main_grid.addWidget(self.move_checkbox, 3, 0)
        main_grid.addWidget(self.overwrite_checkbox, 4, 0)
        main_grid.addWidget(self.export_button, 5, 0, alignment=Qt.AlignLeft)
        main_grid.addWidget(quit_button, 5, 1, alignment=Qt.AlignRight)
        self.setLayout(main_grid)

    def center(self):
        width = QDesktopWidget().availableGeometry().size().width() // 100 * 75
        height = QDesktopWidget().availableGeometry().size().height() // 100 * 75
        self.setGeometry(0, 0, width, height)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def disable_entry(self, widget):
        back_colour = self.palette().color(QPalette.Background)
        palette = QPalette()
        palette.setColor(widget.backgroundRole(), back_colour)
        widget.setPalette(palette)
        widget.setReadOnly(True)

    def export(self):
        directory = self._select_directory("Destination directory")
        if directory:
            self.destination_dir = directory
            if self.move_checkbox.isChecked():
                func = self.aggregator.move
            else:
                func = self.aggregator.copy
            for file in self.selected_map_files:
                func(file, self.destination_dir, self.overwrite_checkbox.isChecked())

    def _select_directory(self, title):
        res = QFileDialog.getExistingDirectory(self, title)
        if res:
            return res

    def select_source_directory(self):
        #source_dir = self._select_directory("Source directory")
        source_dir = "/home/user1/games/Heroes of Might and Magic III/Maps/"
        if source_dir:
            self.source_dir = source_dir
            self.source_path_entry.setText(self.source_dir)
            self.collect_maps()
            self.fill_table()

    def collect_maps(self):
        """Parse maps data."""
        progress = ProgressWindow(self, self.source_dir)
        files_aggregator = self.aggregator(self.source_dir)
        files_list = files_aggregator.get_files()
        progress.set_maximum(len(files_list))
        count = 0
        for parsed_map in files_aggregator.prepare():
            count += 1
            progress.set_value(count)
            self.maps_list.append(parsed_map)
        progress.destroy()

    def fill_table(self):
        self.filtered_maps_list = self.filter.apply(self.maps_list)
        self.maps_table.setRowCount(len(self.filtered_maps_list))
        self.maps_table.setColumnCount(8)
        self.maps_table.setHorizontalHeaderLabels(
            ["", "Name", "Description", "Size", "Type", "Has underground?",
             "Total players", "Human players"]
        )
        font = self.maps_table.horizontalHeader().font()
        font.setBold(True)
        self.maps_table.horizontalHeader().setFont(font)
        self.maps_table.setSelectionMode(QAbstractItemView.NoSelection)
        for row_number, row in enumerate(self.filtered_maps_list):
            row_checker = self._table_widget(row_number)
            map_size = constants.MAP_SIZE[row.size]
            underground = "Yes" if row.dungeon else "No"
            self.maps_table.setCellWidget(row_number, 0, row_checker)
            self.maps_table.setItem(row_number, 1, TableCell(row.name))
            self.maps_table.setItem(row_number, 2, TableCell(row.description))
            self.maps_table.setItem(row_number, 3, TableCell(map_size))
            self.maps_table.setItem(row_number, 4, TableCell(row.type))
            self.maps_table.setItem(row_number, 5, TableCell(underground))
            self.maps_table.setItem(row_number, 6, TableCell(str(row.players.total)))
            self.maps_table.setItem(row_number, 7, TableCell(str(row.players.humans)))
        self.maps_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.maps_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.maps_table.resizeRowsToContents()
        self.maps_table.resizeColumnsToContents()

    def _table_widget(self, row_number):
        frame = QFrame(self.maps_table)
        row_checker = QCheckBox(frame)
        row_checker.stateChanged.connect(
            lambda x, y=row_checker, z=row_number:
            self.select_map(checkbutton=y, number=z))
        layout = QHBoxLayout()
        layout.addWidget(row_checker, alignment=Qt.AlignCenter)
        frame.setLayout(layout)
        return frame

    def select_map(self, checkbutton, number):
        if checkbutton.isChecked():
            self.selected_map_files.add(self.filtered_maps_list[number].path)
        else:
            self.selected_map_files.discard(self.filtered_maps_list[number].path)
        self.export_button.setEnabled(True if len(self.selected_map_files) > 0
                                      else False)


class TableCell(QTableWidgetItem):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.setFlags(Qt.ItemIsSelectable)
        self.setForeground(QBrush(QColor(0, 0, 0)))


app = None


def start(aggregator_class):
    global app
    app = QApplication([])
    gui = MainWindow(app.exit, aggregator_class)
    gui.show()
    app.exec_()
