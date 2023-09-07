# Form implementation generated from reading ui file 'dictation.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1048, 652)
        self.tabWidget = QtWidgets.QTabWidget(parent=Form)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1051, 651))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.treeViewAllDictationWord = QtWidgets.QTreeView(parent=self.tab_2)
        self.treeViewAllDictationWord.setGeometry(QtCore.QRect(0, 0, 201, 591))
        self.treeViewAllDictationWord.setObjectName("treeViewAllDictationWord")
        self.stackedWidget = QtWidgets.QStackedWidget(parent=self.tab_2)
        self.stackedWidget.setGeometry(QtCore.QRect(210, 10, 631, 571))
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.btnStartLearnWord = QtWidgets.QPushButton(parent=self.page)
        self.btnStartLearnWord.setGeometry(QtCore.QRect(250, 530, 89, 25))
        self.btnStartLearnWord.setObjectName("btnStartLearnWord")
        self.layoutWidget = QtWidgets.QWidget(parent=self.page)
        self.layoutWidget.setGeometry(QtCore.QRect(40, 70, 520, 451))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.listViewAllWord = QtWidgets.QListView(parent=self.layoutWidget)
        self.listViewAllWord.setItemAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.listViewAllWord.setObjectName("listViewAllWord")
        self.horizontalLayout_5.addWidget(self.listViewAllWord)
        self.listViewRecentErrorWord = QtWidgets.QListView(parent=self.layoutWidget)
        self.listViewRecentErrorWord.setObjectName("listViewRecentErrorWord")
        self.horizontalLayout_5.addWidget(self.listViewRecentErrorWord)
        self.layoutWidget1 = QtWidgets.QWidget(parent=self.page)
        self.layoutWidget1.setGeometry(QtCore.QRect(100, 40, 401, 25))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.labelAllWord = QtWidgets.QLabel(parent=self.layoutWidget1)
        self.labelAllWord.setObjectName("labelAllWord")
        self.horizontalLayout_6.addWidget(self.labelAllWord)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.labelRecentErrorWord = QtWidgets.QLabel(parent=self.layoutWidget1)
        self.labelRecentErrorWord.setObjectName("labelRecentErrorWord")
        self.horizontalLayout_6.addWidget(self.labelRecentErrorWord)
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.layoutWidget2 = QtWidgets.QWidget(parent=self.page_2)
        self.layoutWidget2.setGeometry(QtCore.QRect(30, 10, 551, 541))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.progressBarWordPlay = QtWidgets.QProgressBar(parent=self.layoutWidget2)
        self.progressBarWordPlay.setProperty("value", 24)
        self.progressBarWordPlay.setObjectName("progressBarWordPlay")
        self.verticalLayout_3.addWidget(self.progressBarWordPlay)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.textEditWordDisplay = QtWidgets.QTextEdit(parent=self.layoutWidget2)
        self.textEditWordDisplay.setObjectName("textEditWordDisplay")
        self.verticalLayout_3.addWidget(self.textEditWordDisplay)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_3.addItem(spacerItem3)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.btnWordPlaySetting = QtWidgets.QPushButton(parent=self.layoutWidget2)
        self.btnWordPlaySetting.setObjectName("btnWordPlaySetting")
        self.horizontalLayout_8.addWidget(self.btnWordPlaySetting)
        spacerItem4 = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem4)
        self.btnWordPlayPrev = QtWidgets.QPushButton(parent=self.layoutWidget2)
        self.btnWordPlayPrev.setObjectName("btnWordPlayPrev")
        self.horizontalLayout_8.addWidget(self.btnWordPlayPrev)
        self.btnWordPlayStop = QtWidgets.QPushButton(parent=self.layoutWidget2)
        self.btnWordPlayStop.setObjectName("btnWordPlayStop")
        self.horizontalLayout_8.addWidget(self.btnWordPlayStop)
        self.btnWordPlayNext = QtWidgets.QPushButton(parent=self.layoutWidget2)
        self.btnWordPlayNext.setObjectName("btnWordPlayNext")
        self.horizontalLayout_8.addWidget(self.btnWordPlayNext)
        self.verticalLayout_3.addLayout(self.horizontalLayout_8)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_3.addItem(spacerItem5)
        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.layoutWidget3 = QtWidgets.QWidget(parent=self.page_3)
        self.layoutWidget3.setGeometry(QtCore.QRect(30, 10, 551, 541))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget3)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_4.addItem(spacerItem6)
        self.progressBar_3 = QtWidgets.QProgressBar(parent=self.layoutWidget3)
        self.progressBar_3.setProperty("value", 24)
        self.progressBar_3.setObjectName("progressBar_3")
        self.verticalLayout_4.addWidget(self.progressBar_3)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_4.addItem(spacerItem7)
        self.lineEdit_4 = QtWidgets.QLineEdit(parent=self.layoutWidget3)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.verticalLayout_4.addWidget(self.lineEdit_4)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_4.addItem(spacerItem8)
        self.textEditWordDisplay_2 = QtWidgets.QTextEdit(parent=self.layoutWidget3)
        self.textEditWordDisplay_2.setObjectName("textEditWordDisplay_2")
        self.verticalLayout_4.addWidget(self.textEditWordDisplay_2)
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_4.addItem(spacerItem9)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.pushButton_12 = QtWidgets.QPushButton(parent=self.layoutWidget3)
        self.pushButton_12.setObjectName("pushButton_12")
        self.horizontalLayout_9.addWidget(self.pushButton_12)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem10)
        self.pushButton_13 = QtWidgets.QPushButton(parent=self.layoutWidget3)
        self.pushButton_13.setObjectName("pushButton_13")
        self.horizontalLayout_9.addWidget(self.pushButton_13)
        self.pushButton_14 = QtWidgets.QPushButton(parent=self.layoutWidget3)
        self.pushButton_14.setObjectName("pushButton_14")
        self.horizontalLayout_9.addWidget(self.pushButton_14)
        self.pushButton_15 = QtWidgets.QPushButton(parent=self.layoutWidget3)
        self.pushButton_15.setObjectName("pushButton_15")
        self.horizontalLayout_9.addWidget(self.pushButton_15)
        self.verticalLayout_4.addLayout(self.horizontalLayout_9)
        spacerItem11 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_4.addItem(spacerItem11)
        self.stackedWidget.addWidget(self.page_3)
        self.tabWidget.addTab(self.tab_2, "")
        self.widget = QtWidgets.QWidget()
        self.widget.setObjectName("widget")
        self.LoadAudioBtn = QtWidgets.QPushButton(parent=self.widget)
        self.LoadAudioBtn.setGeometry(QtCore.QRect(40, 70, 89, 25))
        self.LoadAudioBtn.setObjectName("LoadAudioBtn")
        self.WordTimelistView = QtWidgets.QListView(parent=self.widget)
        self.WordTimelistView.setGeometry(QtCore.QRect(20, 120, 331, 411))
        self.WordTimelistView.setObjectName("WordTimelistView")
        self.SaveAudioWordsDBBtn = QtWidgets.QPushButton(parent=self.widget)
        self.SaveAudioWordsDBBtn.setGeometry(QtCore.QRect(190, 550, 89, 25))
        self.SaveAudioWordsDBBtn.setObjectName("SaveAudioWordsDBBtn")
        self.pushButton_4 = QtWidgets.QPushButton(parent=self.widget)
        self.pushButton_4.setGeometry(QtCore.QRect(50, 550, 89, 25))
        self.pushButton_4.setObjectName("pushButton_4")
        self.layoutWidget4 = QtWidgets.QWidget(parent=self.widget)
        self.layoutWidget4.setGeometry(QtCore.QRect(470, 170, 491, 191))
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget4)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.AudioWordInput = QtWidgets.QLineEdit(parent=self.layoutWidget4)
        self.AudioWordInput.setObjectName("AudioWordInput")
        self.verticalLayout.addWidget(self.AudioWordInput)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.WordTimeStartInput = QtWidgets.QLineEdit(parent=self.layoutWidget4)
        self.WordTimeStartInput.setObjectName("WordTimeStartInput")
        self.horizontalLayout_2.addWidget(self.WordTimeStartInput)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem12)
        self.WordTimeEndInput = QtWidgets.QLineEdit(parent=self.layoutWidget4)
        self.WordTimeEndInput.setObjectName("WordTimeEndInput")
        self.horizontalLayout_2.addWidget(self.WordTimeEndInput)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.WordAudioStartBtn = QtWidgets.QPushButton(parent=self.layoutWidget4)
        self.WordAudioStartBtn.setObjectName("WordAudioStartBtn")
        self.horizontalLayout_4.addWidget(self.WordAudioStartBtn)
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem13)
        self.WordSaveBtn = QtWidgets.QPushButton(parent=self.layoutWidget4)
        self.WordSaveBtn.setObjectName("WordSaveBtn")
        self.horizontalLayout_4.addWidget(self.WordSaveBtn)
        spacerItem14 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem14)
        self.WordAudioEndBtn = QtWidgets.QPushButton(parent=self.layoutWidget4)
        self.WordAudioEndBtn.setObjectName("WordAudioEndBtn")
        self.horizontalLayout_4.addWidget(self.WordAudioEndBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.layoutWidget5 = QtWidgets.QWidget(parent=self.widget)
        self.layoutWidget5.setGeometry(QtCore.QRect(360, 430, 671, 96))
        self.layoutWidget5.setObjectName("layoutWidget5")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget5)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.StartAudioBtn = QtWidgets.QPushButton(parent=self.layoutWidget5)
        self.StartAudioBtn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("play.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.StartAudioBtn.setIcon(icon)
        self.StartAudioBtn.setObjectName("StartAudioBtn")
        self.horizontalLayout.addWidget(self.StartAudioBtn)
        self.ResetAudioBtn = QtWidgets.QPushButton(parent=self.layoutWidget5)
        self.ResetAudioBtn.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("stop.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.ResetAudioBtn.setIcon(icon1)
        self.ResetAudioBtn.setObjectName("ResetAudioBtn")
        self.horizontalLayout.addWidget(self.ResetAudioBtn)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.AudiohorizontalSlider = QtWidgets.QSlider(parent=self.layoutWidget5)
        self.AudiohorizontalSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.AudiohorizontalSlider.setObjectName("AudiohorizontalSlider")
        self.verticalLayout_5.addWidget(self.AudiohorizontalSlider)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.AudioStartTimeLabel = QtWidgets.QLabel(parent=self.layoutWidget5)
        self.AudioStartTimeLabel.setObjectName("AudioStartTimeLabel")
        self.horizontalLayout_3.addWidget(self.AudioStartTimeLabel)
        spacerItem15 = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem15)
        self.AudioEndTimeLabel = QtWidgets.QLabel(parent=self.layoutWidget5)
        self.AudioEndTimeLabel.setObjectName("AudioEndTimeLabel")
        self.horizontalLayout_3.addWidget(self.AudioEndTimeLabel)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.horizontalLayout.addLayout(self.verticalLayout_5)
        self.AudioVolumBtn = QtWidgets.QPushButton(parent=self.layoutWidget5)
        self.AudioVolumBtn.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("volume.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.AudioVolumBtn.setIcon(icon2)
        self.AudioVolumBtn.setObjectName("AudioVolumBtn")
        self.horizontalLayout.addWidget(self.AudioVolumBtn)
        self.AudioVolumSlider = QtWidgets.QSlider(parent=self.layoutWidget5)
        self.AudioVolumSlider.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.AudioVolumSlider.setObjectName("AudioVolumSlider")
        self.horizontalLayout.addWidget(self.AudioVolumSlider)
        self.tabWidget.addTab(self.widget, "")

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(1)
        self.stackedWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "Tab 1"))
        self.btnStartLearnWord.setText(_translate("Form", "开始学习"))
        self.labelAllWord.setText(_translate("Form", "全部单词"))
        self.labelRecentErrorWord.setText(_translate("Form", "近期错词"))
        self.textEditWordDisplay.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:48pt; font-weight:600;\">A</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:48pt; color:#888a85; vertical-align:super;\">               adj   yige   </span><span style=\" font-size:48pt; vertical-align:super;\">  </span><span style=\" font-size:48pt; font-weight:600; vertical-align:sub;\">    </span>                                   </p></body></html>"))
        self.btnWordPlaySetting.setText(_translate("Form", "Setting"))
        self.btnWordPlayPrev.setText(_translate("Form", "<"))
        self.btnWordPlayStop.setText(_translate("Form", "||"))
        self.btnWordPlayNext.setText(_translate("Form", ">"))
        self.textEditWordDisplay_2.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:48pt; font-weight:600;\">A</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:48pt; color:#888a85; vertical-align:super;\">               adj   yige   </span><span style=\" font-size:48pt; vertical-align:super;\">  </span><span style=\" font-size:48pt; font-weight:600; vertical-align:sub;\">    </span>                                   </p></body></html>"))
        self.pushButton_12.setText(_translate("Form", "PushButton"))
        self.pushButton_13.setText(_translate("Form", "PushButton"))
        self.pushButton_14.setText(_translate("Form", "PushButton"))
        self.pushButton_15.setText(_translate("Form", "PushButton"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "Tab 2"))
        self.LoadAudioBtn.setText(_translate("Form", "LoadAudio"))
        self.SaveAudioWordsDBBtn.setText(_translate("Form", "Save"))
        self.pushButton_4.setText(_translate("Form", "LoadStorage"))
        self.WordAudioStartBtn.setText(_translate("Form", "WordStart"))
        self.WordSaveBtn.setText(_translate("Form", "WordSave"))
        self.WordAudioEndBtn.setText(_translate("Form", "WordEnd"))
        self.AudioStartTimeLabel.setText(_translate("Form", "TextLabel"))
        self.AudioEndTimeLabel.setText(_translate("Form", "TextLabel"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.widget), _translate("Form", "Page"))
