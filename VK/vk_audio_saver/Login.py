from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QErrorMessage
from PySide2.QtWidgets import QWidget
import vk_api


class Login_Form(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.resize(548, 358)
        self.widget = QtWidgets.QWidget(self)
        self.widget.setGeometry(QtCore.QRect(130, 120, 281, 111))

        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        self.label = QtWidgets.QLabel(self.widget)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.widget)

        self.gridLayout.addWidget(self.lineEdit, 0, 1, 2, 1)
        self.label_2 = QtWidgets.QLabel(self.widget)

        self.gridLayout.addWidget(self.label_2, 1, 0, 2, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)

        self.gridLayout.addWidget(self.lineEdit_2, 2, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.widget)

        self.gridLayout.addWidget(self.pushButton, 3, 0, 1, 2)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def getVkSession(self):
        login = self.lineEdit.text()
        password = self.lineEdit_2.text()
        return self.signIn(login, password)

    def signIn(self, login, password):
        vk = vk_api.VkApi(login=login, password=password)
        vk.auth()
        return vk

    def retranslateUi(self):
        self.label.setText("Логин:")
        self.label_2.setText("Пароль:")
        self.pushButton.setText("Войти")
