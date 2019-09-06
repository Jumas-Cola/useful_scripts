# -*- coding: utf-8 -*-

from PySide2 import QtCore, QtWidgets
from PySide2.QtWidgets import QApplication, QMainWindow, QErrorMessage
from Login import Login_Form
from Audio import AudioList_Form


class Ui_MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(548, 358)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.login = Login_Form()
        self.statusbar.setObjectName("login")
        self.gridLayout.addWidget(self.login)

        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")

        self.action = QtWidgets.QAction(self)
        self.action.setObjectName("action")

        self.retranslateUi()
        self.setupHandlers()
        QtCore.QMetaObject.connectSlotsByName(self)

    def setupHandlers(self):
        self.login.pushButton.clicked.connect(self.getVkSession)
        self.action.triggered.connect(self.initLogin)

    def getVkSession(self):
        try:
            self.vk = self.login.getVkSession()
            self.initAudioList()
        except Exception as e:
            errMsgBox = QErrorMessage()
            errMsgBox.showMessage(repr(e))
            errMsgBox.exec_()

    def initLogin(self):
        self.audio_list.deleteLater()
        for i in reversed(range(self.gridLayout.count())):
            self.gridLayout.itemAt(i).widget().setParent(None)
        self.resize(548, 358)
        self.login = Login_Form()
        self.statusbar.setObjectName("login")
        self.gridLayout.addWidget(self.login)
        self.menu.removeAction(self.action)
        self.menubar.removeAction(self.menu.menuAction())
        self.setupHandlers()

    def initAudioList(self):
        self.login.deleteLater()
        for i in reversed(range(self.gridLayout.count())):
            self.gridLayout.itemAt(i).widget().setParent(None)
        self.resize(771, 600)
        self.audio_list = AudioList_Form(self.vk)
        self.statusbar.setObjectName("audio_list")
        self.gridLayout.addWidget(self.audio_list)

        self.menu.addAction(self.action)
        self.menubar.addAction(self.menu.menuAction())
        self.menu.setTitle('Свойства')
        self.action.setText('Сменить пользователя')

    def retranslateUi(self):
        self.setWindowTitle("vk_audio_saver")


if __name__ == '__main__':
    app = QApplication()
    form = Ui_MainWindow()
    form.show()
    exit(app.exec_())
