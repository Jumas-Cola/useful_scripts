# -*- coding: utf-8 -*-

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QErrorMessage
from ExcelSource import ExcelSource
from TemplateInsert import TemplateInsert


class Ui_MainWindow(QMainWindow):
    """
        Шаблонизатор документов Word с получением данных из Excel.
        Первая строка в таблице - имена полей в шаблоне.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.template_setted = False
        self.source_setted = False
        self.out_path_setted = False
        # styles = "styles.stylesheet"
        #
        # with open(styles, "r") as f:
        #     self.setStyleSheet(f.read())

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(490, 274)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 20, 471, 181))
        self.widget.setObjectName("widget")

        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.pushButton_3 = QtWidgets.QPushButton(self.widget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 3, 2, 1, 1)

        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 2)

        self.pushButton_4 = QtWidgets.QPushButton(self.widget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 1, 2, 1, 1)

        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 2)

        self.comboBox = QtWidgets.QComboBox(self.widget)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout.addWidget(self.comboBox, 2, 1, 1, 2)

        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 0, 2, 1, 1)

        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 2)

        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 4, 0, 1, 1)

        self.comboBox_2 = QtWidgets.QComboBox(self.widget)
        self.comboBox_2.setObjectName("comboBox_2")
        self.gridLayout.addWidget(self.comboBox_2, 4, 1, 1, 2)
        self.comboBox_2.addItem('Нет')

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(200, 220, 111, 31))
        self.pushButton.setObjectName("pushButton")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.setupHandlers()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate(
            "MainWindow", "MainWindow", None, -1))
        self.pushButton_3.setText(QtWidgets.QApplication.translate(
            "MainWindow", "Выбрать", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate(
            "MainWindow", "Выберите файл источника", None, -1))
        self.pushButton_4.setText(QtWidgets.QApplication.translate(
            "MainWindow", "Выбрать", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate(
            "MainWindow", "Выберите конечную папку (опц.)", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate(
            "MainWindow", "Выберите лист таблицы", None, -1))
        self.pushButton_2.setText(QtWidgets.QApplication.translate(
            "MainWindow", "Выбрать", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate(
            "MainWindow", "Выберите файл шаблона", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate(
            "MainWindow", "Пуск", None, -1))
        self.label_6.setText(QtWidgets.QApplication.translate(
            "MainWindow", "Имя файла по полю (опц.)", None, -1))

    def setupHandlers(self):
        self.pushButton_2.clicked.connect(self.selectTemplate)
        self.pushButton_4.clicked.connect(self.selectSource)
        self.pushButton_3.clicked.connect(self.selectOutFolder)
        self.pushButton.clicked.connect(self.renderDocs)

    def selectTemplate(self):
        self.template_path = QFileDialog.getOpenFileName(
            filter='*.doc *.docx')[0]
        self.label_3.setText(self.template_path)
        self.template_setted = True

    def selectSource(self):
        self.source_path = QFileDialog.getOpenFileName(
            filter='*.xls *.xlsx')[0]
        self.label_5.setText(self.source_path)
        self.source_obj = ExcelSource(self.source_path)
        sheets = self.source_obj.get_sheets()
        self.comboBox.clear()
        self.comboBox.addItems(sheets)
        self.comboBox_2.clear()
        self.comboBox_2.addItems(['Нет'] + self.source_obj.get_fields(sheets[0]))
        self.source_setted = True

    def selectOutFolder(self):
        self.out_path = str(QFileDialog.getExistingDirectory())
        self.label_4.setText(self.out_path)
        self.out_path_setted = True

    def renderDocs(self):
        try:
            if not (self.source_setted and self.source_path):
                raise Exception('Выберите источник данных!')
            if not (self.template_setted and self.template_path):
                raise Exception('Выберите шаблон!')
            t = TemplateInsert(
                self.template_path,
                self.source_obj.get_data(self.comboBox.currentText()),
                out_path=self.out_path if self.out_path_setted else None,
                name_field=None if self.comboBox_2.currentText() == 'Нет'
                else self.comboBox_2.currentText()
            )
            t.render()
            msgBox = QMessageBox()
            msgBox.setText('Finished!')
            msgBox.exec_()
        except Exception as e:
            errMsgBox = QErrorMessage()
            errMsgBox.showMessage(repr(e))
            errMsgBox.exec_()


if __name__ == '__main__':
    app = QApplication()
    form = Ui_MainWindow()
    form.show()
    exit(app.exec_())
