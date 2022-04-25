import sys
import json

from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QTableView, QHeaderView, QVBoxLayout
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QRegExp
from PyQt5.QtGui import QStandardItemModel, QStandardItem

def pullFromJson():
    with open('CC_UNITS.json') as json_file:
        data = json.load(json_file)
        
        return data

class CustomFilter(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.role = Qt.DisplayRole

    def filterAcceptsRow(self, sourceRow, sourceParent):
        index0 = self.sourceModel().index(sourceRow, 0, sourceParent)
        index1 = self.sourceModel().index(sourceRow, 1, sourceParent)
        return ((self.filterRegExp().indexIn(self.sourceModel().data(index0, self.role)) >= 0 or self.filterRegExp().indexIn(self.sourceModel().data(index1, self.role)) >= 0))

class CCSearch(QWidget):
    filter_proxy_model = CustomFilter()
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

        self.filter_proxy_model.setSourceModel(model)
        self.filter_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filter_proxy_model.setFilterKeyColumn(0)

        search_field = QLineEdit()
        search_field.setStyleSheet('font-size: 35px; height: 60px')
        search_field.textChanged.connect(self.onTextChanged)
        mainLayout.addWidget(search_field)

        table = QTableView()
        table.setStyleSheet('font-size: 35px')
        table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setModel(self.filter_proxy_model)
        mainLayout.addWidget(table)

        self.setLayout(mainLayout)

    def onTextChanged(self, text):
        self.filter_proxy_model.setFilterRegExp(QRegExp(text, Qt.CaseInsensitive, QRegExp.FixedString))


def main():
    app = QApplication(sys.argv)
    main = CCSearch()
    main.setWindowTitle('CC Unit Search Prototype')
    main.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
