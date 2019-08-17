# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\StarlightX\Desktop\randomas\main.ui',
# licensing of 'C:\Users\StarlightX\Desktop\randomas\main.ui' applies.
#
# Created: Mon May 27 23:21:03 2019
#      by: pyside2-uic  running on PySide2 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QApplication, QDialog
import sys
import generator


class Ui_Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(593, 538)
        Dialog.setWindowTitle("Dialog")

        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)

        # Choice Generate Type
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setFont(font)
        self.comboBox.setGeometry(QtCore.QRect(180, 40, 221, 32))
        # self.comboBox.setCurrentText("")
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItems(['Password', 'Login'])

        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(30, 91, 531, 411))
        self.widget.setObjectName("widget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(13)
        font.setWeight(75)
        font.setBold(True)

        # Numbers Slider
        self.horizontalSlider = QtWidgets.QSlider(self.widget)
        self.horizontalSlider.setMaximum(10)
        self.horizontalSlider.setProperty("value", 3)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setFont(font)
        self.label_5.setText("Nums:")
        self.label_5.setObjectName("label_5")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setFont(font)
        self.label.setText(str(self.horizontalSlider.value()))
        self.label.setObjectName("label")

        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        # Lower Slider
        self.horizontalSlider_2 = QtWidgets.QSlider(self.widget)
        self.horizontalSlider_2.setMaximum(10)
        self.horizontalSlider_2.setProperty("value", 5)
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")
        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setFont(font)
        self.label_6.setText("Lower:")
        self.label_6.setObjectName("label_6")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setFont(font)
        self.label_2.setText(str(self.horizontalSlider_2.value()))
        self.label_2.setObjectName("label_2")

        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")

        # Upper Slider
        self.horizontalSlider_3 = QtWidgets.QSlider(self.widget)
        self.horizontalSlider_3.setMaximum(10)
        self.horizontalSlider_3.setProperty("value", 2)
        self.horizontalSlider_3.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_3.setObjectName("horizontalSlider_3")
        self.label_7 = QtWidgets.QLabel(self.widget)
        self.label_7.setFont(font)
        self.label_7.setText("Upper:")
        self.label_7.setObjectName("label_7")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setFont(font)
        self.label_3.setText(str(self.horizontalSlider_3.value()))
        self.label_3.setObjectName("label_3")

        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")

        # Signs Slider
        self.horizontalSlider_4 = QtWidgets.QSlider(self.widget)
        self.horizontalSlider_4.setMaximum(10)
        self.horizontalSlider_4.setProperty("value", 2)
        self.horizontalSlider_4.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_4.setObjectName("horizontalSlider_4")
        self.label_8 = QtWidgets.QLabel(self.widget)
        self.label_8.setFont(font)
        self.label_8.setText("Signs:")
        self.label_8.setObjectName("label_8")
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setFont(font)
        self.label_4.setText(str(self.horizontalSlider_4.value()))
        self.label_4.setObjectName("label_4")

        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)

        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setFont(font)
        self.pushButton.setText("Generate")
        self.pushButton.setObjectName("pushButton")

        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setText("Copy")
        self.pushButton_2.setObjectName("pushButton_2")

        self.spinBox = QtWidgets.QSpinBox(self.widget)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(1000)
        self.spinBox.setObjectName("spinBox")

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.widget)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.plainTextEdit.setFont(font)

        # Adding Widgets
        self.horizontalLayout_3.addWidget(self.label_5)
        self.horizontalLayout_3.addWidget(self.label)
        self.horizontalLayout_3.addWidget(self.horizontalSlider)
        self.horizontalLayout_4.addWidget(self.label_6)
        self.horizontalLayout_4.addWidget(self.label_2)
        self.horizontalLayout_4.addWidget(self.horizontalSlider_2)
        self.horizontalLayout_5.addWidget(self.label_7)
        self.horizontalLayout_5.addWidget(self.label_3)
        self.horizontalLayout_5.addWidget(self.horizontalSlider_3)
        self.horizontalLayout_6.addWidget(self.label_8)
        self.horizontalLayout_6.addWidget(self.label_4)
        self.horizontalLayout_6.addWidget(self.horizontalSlider_4)
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.horizontalLayout_2.addWidget(self.spinBox)
        self.verticalLayout.addWidget(self.plainTextEdit)

        self.setupHandlers()

        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def setupHandlers(self):
        self.horizontalSlider.valueChanged.connect(self.onSliderChange)
        self.horizontalSlider_2.valueChanged.connect(self.onSliderChange)
        self.horizontalSlider_3.valueChanged.connect(self.onSliderChange)
        self.horizontalSlider_4.valueChanged.connect(self.onSliderChange)
        self.comboBox.currentIndexChanged.connect(self.onComboBoxChange)
        self.pushButton.clicked.connect(self.onPushButtonClick)
        self.pushButton_2.clicked.connect(self.onPushButton_2Click)

    def onSliderChange(self):
        self.label.setText(str(self.horizontalSlider.value()))
        self.label_2.setText(str(self.horizontalSlider_2.value()))
        self.label_3.setText(str(self.horizontalSlider_3.value()))
        self.label_4.setText(str(self.horizontalSlider_4.value()))

    def onComboBoxChange(self):
        if self.comboBox.currentIndex() == 0:
            self.horizontalSlider.setEnabled(True)
            self.horizontalSlider_2.setEnabled(True)
            self.horizontalSlider_3.setEnabled(True)
            self.horizontalSlider_4.setEnabled(True)
        elif self.comboBox.currentIndex() == 1:
            self.horizontalSlider.setDisabled(True)
            self.horizontalSlider_2.setDisabled(True)
            self.horizontalSlider_3.setDisabled(True)
            self.horizontalSlider_4.setDisabled(True)

    def onPushButtonClick(self):
        index = self.comboBox.currentIndex()
        spin_box = self.spinBox.value()
        nums = self.horizontalSlider.value()
        low = self.horizontalSlider_2.value()
        up = self.horizontalSlider_3.value()
        signs = self.horizontalSlider_4.value()
        if index == 0:
            self.plainTextEdit.clear()
            for password in generator.PassGenerator(spin_box, nums, low, up, signs):
                self.plainTextEdit.insertPlainText(password + '\n')
        elif index == 1:
            self.plainTextEdit.clear()
            for login in generator.LoginGenerator(spin_box, 10):
                self.plainTextEdit.insertPlainText(login + '\n')

    def onPushButton_2Click(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.plainTextEdit.toPlainText())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Ui_Dialog()
    form.show()
    sys.exit(app.exec_())
