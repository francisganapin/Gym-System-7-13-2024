import os
import pandas as pd
from PyQt6.QtCore import Qt, QAbstractTableModel
from PyQt6.QtWidgets import QTableView, QApplication

class DataFrameModel(QAbstractTableModel):
    def __init__(self, df=pd.DataFrame(), parent=None):
        super().__init__(parent)
        self._df = df

    def rowCount(self, parent=None):
        return len(self._df.index)

    def columnCount(self, parent=None):
        return len(self._df.columns)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid():
            if role == Qt.ItemDataRole.DisplayRole:
                return str(self._df.iloc[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._df.columns[section]
            if orientation == Qt.Orientation.Vertical:
                return self._df.index[section]
        return None

    def setData(self, df):
        self.beginResetModel()
        self._df = df
        self.endResetModel()

class MainWindow:
    def __init__(self):
        self.model = DataFrameModel()
        self.tableView_3 = QTableView()
        self.tableView_3.setModel(self.model)

    def load_data(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, 'login_records.csv')    
        df = pd.read_csv(file_path)

        model = DataFrameModel(df)
        self.tableView_3.setModel(model)

# Example usage:
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.display_login_records()
    window.tableView_3.show()
    sys.exit(app.exec())
