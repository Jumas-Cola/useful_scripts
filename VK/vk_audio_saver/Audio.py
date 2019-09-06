from PySide2 import QtCore, QtWidgets
from PySide2.QtWidgets import QErrorMessage
from PySide2.QtWidgets import QWidget
import os
from vk_api.audio import VkAudio
from urllib.request import urlretrieve
import re
import datetime
from multiprocessing import Pool
from functools import partial


def get_download_folder():
    home = os.path.expanduser("~")
    return os.path.join(home, "Downloads")


class AudioList_Form(QWidget):
    def __init__(self, vk, parent=None):
        super().__init__(parent)
        self.vk = vk
        self.vk_audio = VkAudio(vk)
        self.folder = None
        self.pool = Pool(1)
        self.setupUi()

    def setupUi(self):
        self.setObjectName("Form")
        self.resize(771, 553)
        self.layoutWidget = QtWidgets.QWidget(self)
        self.layoutWidget.setGeometry(QtCore.QRect(15, 20, 741, 521))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 1, 1, 1)
        self.listWidget = QtWidgets.QListWidget(self.layoutWidget)
        self.listWidget.setObjectName("listWidget")
        self.gridLayout.addWidget(self.listWidget, 2, 0, 1, 3)
        self.lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 2, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 3, 1, 1, 1)
        self.pushButton_2.setVisible(False)

        self.retranslateUi()
        self.setupHandlers()
        QtCore.QMetaObject.connectSlotsByName(self)

    def setupHandlers(self):
        self.pushButton.clicked.connect(self.loadAudioList)
        self.listWidget.itemClicked.connect(self.itemClick)
        self.pushButton_2.clicked.connect(self.downloadAll)

    @staticmethod
    def chunkify(lst, n):
        return [lst[i::n] for i in range(n)]

    @staticmethod
    def download(audios, folder='vk_music'):
        for audio in audios:
            url = audio['url']
            file_name = '{}-{}.mp3'.format(audio['artist'], audio['title'])
            file_name = re.sub(r'[ \|/:*?"<>+%!@]', '_', file_name)
            try:
                urlretrieve(url, os.path.join(folder, file_name))
            except Exception as e:
                errMsgBox = QErrorMessage()
                errMsgBox.showMessage(repr(e))
                errMsgBox.exec_()

    def downloadAll(self):
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)
        func = partial(self.download, folder=self.folder)
        self.pool.map_async(func, self.chunkify(self.audios, 10))

    def loadAudioList(self):
        try:
            user = self.vk.method(
                'users.get', {'user_ids': self.lineEdit.text()})[0]
            self.user_id = user['id']
            self.folder = os.path.join(
                get_download_folder(), '{}_audio'.format(self.user_id))
            self.audios = self.vk_audio.get(owner_id=self.user_id)
            self.label_2.setText('Имя: {}'.format(
                user['first_name'].encode('utf-8', 'ignore').decode()))
            self.label_3.setText('Фамилия: {}'.format(
                user['last_name'].encode('utf-8', 'ignore').decode()))
            self.label_4.setText(
                'Всего аудиозаписей: {}'.format(len(self.audios)))
            self.listWidget.clear()
            for audio in self.audios:
                item = QtWidgets.QListWidgetItem('{} - {}    ({})'.format(
                    audio['artist'],
                    audio['title'],
                    str(datetime.timedelta(seconds=int(audio['duration']))))
                )
                item.url = audio['url']
                item.artist = audio['artist']
                item.title = audio['title']
                self.listWidget.addItem(item)
            self.pushButton_2.setVisible(True)
        except Exception as e:
            errMsgBox = QErrorMessage()
            errMsgBox.showMessage(repr(e))
            errMsgBox.exec_()

    def itemClick(self, item):
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)
        file_name = '{}-{}.mp3'.format(item.artist, item.title)
        file_name = re.sub(r'[ \|/:*?"<>+%!@]', '_', file_name)
        try:
            self.pool.apply_async(urlretrieve, args=(
                item.url, os.path.join(self.folder, file_name)))
        except Exception as e:
            errMsgBox = QErrorMessage()
            errMsgBox.showMessage(repr(e))
            errMsgBox.exec_()

    def retranslateUi(self):
        self.label.setText("Введите id пользователя или короткое имя:")
        self.pushButton.setText("Получить список аудио")
        self.pushButton_2.setText("Скачать всё")
