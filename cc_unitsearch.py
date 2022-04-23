import sys
import json

from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QTableView, QHeaderView, QVBoxLayout
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem

def pullFromJson():
    with open('CC_UNITS.json') as json_file:
        data = json.load(json_file)
        
        return data

class CCSearch(QWidget):
    def __init__(self):
        super().__init__()

        self.resize(1280, 720)
        mainLayout = QVBoxLayout()
        units = pullFromJson()

        model = QStandardItemModel(len(units), 3)
        model.setHorizontalHeaderLabels(['CC Unit', 'Attila Unit', 'Tier & Type'])
        for row, unit in enumerate(units):
            ccUnit = QStandardItem(unit['CC Name'])
            attilaUnit = QStandardItem(unit['Atilla Name'])
            unitType = QStandardItem(unit['Unit Type'])
            model.setItem(row, 0, ccUnit)
            model.setItem(row, 1, attilaUnit)
            model.setItem(row, 2, unitType)

        filter_proxy_model = QSortFilterProxyModel()
        filter_proxy_model.setSourceModel(model)
        filter_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        filter_proxy_model.setFilterKeyColumn(0)

        search_field = QLineEdit()
        search_field.setStyleSheet('font-size: 35px; height: 60px')
        search_field.textChanged.connect(filter_proxy_model.setFilterRegExp)
        mainLayout.addWidget(search_field)

        table = QTableView()
        table.setStyleSheet('font-size: 35px')
        table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setModel(filter_proxy_model)
        mainLayout.addWidget(table)

        self.setLayout(mainLayout)

def main():
    app = QApplication(sys.argv)
    main = CCSearch()
    main.setWindowTitle('CC Unit Search Prototype')
    main.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
