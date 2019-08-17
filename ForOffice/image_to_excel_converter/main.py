
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QErrorMessage
from PySide2.QtGui import QCursor
from PySide2.QtCore import Qt
from ImageToExcel import ImageToExcel
import sys
import os


class Ui_MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        styles = "styles.stylesheet"

        with open(styles, "r") as f:
            self.setStyleSheet(f.read())

    def setupUi(self, MainWindow):
        MainWindow.setObjectName('MainWindow')
        MainWindow.setFixedWidth(470)
        MainWindow.setFixedHeight(283)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName('centralwidget')
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 10, 441, 231))
        self.widget.setObjectName('widget')
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName('gridLayout')
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setObjectName('lineEdit')
        self.gridLayout.addWidget(self.lineEdit, 4, 0, 1, 4)
        self.label_2 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName('label_2')
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 2)
        self.label_3 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName('label_3')
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 4)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setObjectName('pushButton_2')
        self.gridLayout.addWidget(self.pushButton_2, 5, 2, 1, 2)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName('pushButton')
        self.gridLayout.addWidget(self.pushButton, 5, 0, 1, 2)
        self.label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName('label')
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.spinBox_2 = QtWidgets.QSpinBox(self.widget)
        self.spinBox_2.setObjectName('spinBox_2')
        self.gridLayout.addWidget(self.spinBox_2, 2, 2, 1, 2)
        self.spinBox = QtWidgets.QSpinBox(self.widget)
        self.spinBox.setObjectName('spinBox')
        self.gridLayout.addWidget(self.spinBox, 2, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 470, 26))
        self.menubar.setObjectName('menubar')
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        self.setupHandlers()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate(
            'MainWindow', 'MainWindow', None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate(
            'MainWindow', 'Indent Left', None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate(
            'MainWindow', 'File Name', None, -1))
        self.pushButton_2.setText(QtWidgets.QApplication.translate(
            'MainWindow', 'Make Excel form Image', None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate(
            'MainWindow', 'Select File', None, -1))
        self.label.setText(QtWidgets.QApplication.translate(
            'MainWindow', 'Indent Top', None, -1))

    def setupHandlers(self):
        self.pushButton.clicked.connect(self.selectFile)
        self.pushButton_2.clicked.connect(self.img_to_excel)

    def selectFile(self):
        self.lineEdit.setText(
            QFileDialog.getOpenFileName(filter='*.png *.jpg')[0])

    def img_to_excel(self):
        filename, file_ext = os.path.splitext(str(self.lineEdit.text()))
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        try:
            t = ImageToExcel(self.lineEdit.text(), filename + '.xlsx',
                             self.spinBox.value(), self.spinBox_2.value())
            t.img_to_excel()
            msgBox = QMessageBox()
            msgBox.setText('Finished!')
            msgBox.exec_()
        except Exception as e:
            errMsgBox = QErrorMessage()
            errMsgBox.showMessage(repr(e))
            errMsgBox.exec_()
        finally:
            QApplication.restoreOverrideCursor()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Ui_MainWindow()
    form.show()
    sys.exit(app.exec_())
