from PySide2 import QtCore, QtWidgets
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QErrorMessage, QAction
from PySide2.QtGui import QCursor
from PySide2.QtCore import Qt
from Uploader import Uploader
import sys


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(714, 379)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(714, 379))
        MainWindow.setMaximumSize(QtCore.QSize(714, 379))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(50, 40, 611, 279))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 6, 0, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout.addWidget(self.lineEdit_3, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 7, 0, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 8, 0, 1, 1)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout.addWidget(self.lineEdit_4, 4, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pushButton_2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.gridLayout.addLayout(self.horizontalLayout_2, 9, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 5, 0, 1, 1)
        # self.progressBar = QtWidgets.QProgressBar(self.gridLayoutWidget)
        # self.progressBar.setEnabled(True)
        # self.progressBar.setValue(0)
        # self.progressBar.setTextVisible(True)
        # self.progressBar.setObjectName("progressBar")
        # self.gridLayout.addWidget(self.progressBar, 10, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 714, 26))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        self.setupHandlers()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("MainWindow", "Выберите папку:", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("MainWindow", "Пароль:", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("MainWindow", "Выбрать папку", None, -1))
        self.pushButton_2.setText(QtWidgets.QApplication.translate("MainWindow", "Загрузить", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("MainWindow", "Логин:", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("MainWindow", "Введите id группы:", None, -1))
        self.menu.setTitle(QtWidgets.QApplication.translate("MainWindow", "Меню", None, -1))

    def setupHandlers(self):
        self.pushButton.clicked.connect(self.selectDirectory)
        self.pushButton_2.clicked.connect(self.upload)
        aboutAct = QAction('&О программе...', self)
        aboutAct.triggered.connect(self.about)
        self.menu.addAction(aboutAct)

    def about(self):
        msgBox = QMessageBox()
        msgBox.setText('''Программа для загрузки фотографий в группу ВК. Введите данные аккаунта, id группы, выберите папку, из которой загружать изображения и нажмите "Загрузить".''')
        msgBox.exec_()

    def selectDirectory(self):
        self.lineEdit_2.setText(QFileDialog.getExistingDirectory())

    def upload(self):
        try:
            login = self.lineEdit_3.text()
            password = self.lineEdit_4.text()
            group_id = abs(int(self.lineEdit.text()))
            path_to_folder = self.lineEdit_2.text()
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            uploader = Uploader(login, password, group_id, path_to_folder)
            self.progressBar = QtWidgets.QProgressBar(self.gridLayoutWidget)
            self.progressBar.setEnabled(True)
            self.progressBar.setValue(0)
            self.progressBar.setTextVisible(True)
            self.progressBar.setObjectName("progressBar")
            self.gridLayout.addWidget(self.progressBar, 10, 0, 1, 1)
            self.pushButton.setEnabled(False)
            self.pushButton_2.setEnabled(False)
            self.update()
            for i, j in uploader.upload_album():
                self.progressBar.setValue(int(i/j*100))
                QApplication.processEvents()
        except Exception as e:
            errMsgBox = QErrorMessage()
            errMsgBox.showMessage(repr(e))
            errMsgBox.exec_()
        finally:
            self.progressBar.setParent(None)
            self.pushButton.setEnabled(True)
            self.pushButton_2.setEnabled(True)
            QApplication.restoreOverrideCursor()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Ui_MainWindow()
    form.show()
    sys.exit(app.exec_())
