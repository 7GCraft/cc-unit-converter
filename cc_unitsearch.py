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
    def __init__(self):
        super().__init__()

        self.resize(1280, 720)
        self.filter_proxy_model = CustomFilter()
        
        mainLayout = QVBoxLayout()
        units = pullFromJson()

        unitItems = self.createUnitItems(units=units)

        self.createFilteredModel(unitItems=unitItems)

        table = self.createTable()
        search_field = self.createSearchField()

        mainLayout.addWidget(search_field)
        mainLayout.addWidget(table)

        self.setLayout(mainLayout)

    def createUnitItems(self, units):
        unitItems = QStandardItemModel(len(units), 3)
        unitItems.setHorizontalHeaderLabels(['CC Unit', 'Attila Unit', 'Tier & Type'])
        for row, unit in enumerate(units):
            ccUnit = QStandardItem(unit['CC Units'])
            attilaUnit = QStandardItem(unit['Atilla Units'])
            unitType = QStandardItem(unit['Tier'])
            unitItems.setItem(row, 0, ccUnit)
            unitItems.setItem(row, 1, attilaUnit)
            unitItems.setItem(row, 2, unitType)
        return unitItems

    def createFilteredModel(self, unitItems):
        self.filter_proxy_model.setSourceModel(unitItems)
        self.filter_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filter_proxy_model.setFilterKeyColumn(0)

    def createTable(self):
        table = QTableView()
        table.setStyleSheet('font-size: 35px')
        table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setModel(self.filter_proxy_model)
        return table

    def createSearchField(self):
        search_field = QLineEdit()
        search_field.setStyleSheet('font-size: 35px; height: 60px')
        search_field.textChanged.connect(self.onTextChanged)
        return search_field
        
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
