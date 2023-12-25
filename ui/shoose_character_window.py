# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/shoose_character_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(748, 455)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(3, 3, 3, 3)
        self.gridLayout.setSpacing(3)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.lineEdit_find = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_find.setObjectName("lineEdit_find")
        self.gridLayout.addWidget(self.lineEdit_find, 0, 0, 1, 1)
        self.pushButton_open = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_open.setObjectName("pushButton_open")
        self.gridLayout.addWidget(self.pushButton_open, 2, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_add_folder = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_add_folder.setObjectName("pushButton_add_folder")
        self.horizontalLayout.addWidget(self.pushButton_add_folder)
        self.pushButton_add_in_folder = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_add_in_folder.setObjectName("pushButton_add_in_folder")
        self.horizontalLayout.addWidget(self.pushButton_add_in_folder)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setMinimumSize(QtCore.QSize(300, 300))
        self.groupBox.setTitle("")
        self.groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_image = QtWidgets.QLabel(self.groupBox)
        self.label_image.setMinimumSize(QtCore.QSize(100, 100))
        self.label_image.setMaximumSize(QtCore.QSize(315, 160))
        self.label_image.setBaseSize(QtCore.QSize(100, 200))
        self.label_image.setText("")
        self.label_image.setScaledContents(False)
        self.label_image.setObjectName("label_image")
        self.verticalLayout.addWidget(self.label_image)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setContentsMargins(3, -1, 3, -1)
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("Bell MT")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_name = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_name.setFont(font)
        self.label_name.setText("")
        self.label_name.setAlignment(QtCore.Qt.AlignCenter)
        self.label_name.setObjectName("label_name")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_name)
        self.label_class = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_class.setFont(font)
        self.label_class.setText("")
        self.label_class.setAlignment(QtCore.Qt.AlignCenter)
        self.label_class.setObjectName("label_class")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.label_class)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("Bell MT")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("Bell MT")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.label_race = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_race.setFont(font)
        self.label_race.setText("")
        self.label_race.setAlignment(QtCore.Qt.AlignCenter)
        self.label_race.setObjectName("label_race")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.label_race)
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("Bell MT")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.label_level = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_level.setFont(font)
        self.label_level.setText("")
        self.label_level.setAlignment(QtCore.Qt.AlignCenter)
        self.label_level.setObjectName("label_level")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.label_level)
        self.verticalLayout.addLayout(self.formLayout)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setContentsMargins(3, -1, 3, 6)
        self.gridLayout_2.setHorizontalSpacing(10)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_22 = QtWidgets.QLabel(self.groupBox)
        self.label_22.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setFamily("Bell MT")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_22.setFont(font)
        self.label_22.setObjectName("label_22")
        self.gridLayout_2.addWidget(self.label_22, 2, 1, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.groupBox)
        self.label_18.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setFamily("Bell MT")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.gridLayout_2.addWidget(self.label_18, 0, 1, 1, 1)
        self.label_21 = QtWidgets.QLabel(self.groupBox)
        self.label_21.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setFamily("Bell MT")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_21.setFont(font)
        self.label_21.setObjectName("label_21")
        self.gridLayout_2.addWidget(self.label_21, 2, 2, 1, 1)
        self.label_19 = QtWidgets.QLabel(self.groupBox)
        self.label_19.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setFamily("Bell MT")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")
        self.gridLayout_2.addWidget(self.label_19, 0, 2, 1, 1)
        self.label_20 = QtWidgets.QLabel(self.groupBox)
        self.label_20.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setFamily("Bell MT")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_20.setFont(font)
        self.label_20.setObjectName("label_20")
        self.gridLayout_2.addWidget(self.label_20, 2, 0, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.groupBox)
        self.label_17.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setFamily("Bell MT")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.gridLayout_2.addWidget(self.label_17, 0, 0, 1, 1)
        self.label_strength = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_strength.setFont(font)
        self.label_strength.setAlignment(QtCore.Qt.AlignCenter)
        self.label_strength.setObjectName("label_strength")
        self.gridLayout_2.addWidget(self.label_strength, 1, 0, 1, 1)
        self.label_dexterity = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_dexterity.setFont(font)
        self.label_dexterity.setAlignment(QtCore.Qt.AlignCenter)
        self.label_dexterity.setObjectName("label_dexterity")
        self.gridLayout_2.addWidget(self.label_dexterity, 1, 1, 1, 1)
        self.label_constitution = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_constitution.setFont(font)
        self.label_constitution.setAlignment(QtCore.Qt.AlignCenter)
        self.label_constitution.setObjectName("label_constitution")
        self.gridLayout_2.addWidget(self.label_constitution, 1, 2, 1, 1)
        self.label_wisdom = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_wisdom.setFont(font)
        self.label_wisdom.setAlignment(QtCore.Qt.AlignCenter)
        self.label_wisdom.setObjectName("label_wisdom")
        self.gridLayout_2.addWidget(self.label_wisdom, 3, 1, 1, 1)
        self.label_charisma = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_charisma.setFont(font)
        self.label_charisma.setAlignment(QtCore.Qt.AlignCenter)
        self.label_charisma.setObjectName("label_charisma")
        self.gridLayout_2.addWidget(self.label_charisma, 3, 2, 1, 1)
        self.label_intelligence = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_intelligence.setFont(font)
        self.label_intelligence.setAlignment(QtCore.Qt.AlignCenter)
        self.label_intelligence.setObjectName("label_intelligence")
        self.gridLayout_2.addWidget(self.label_intelligence, 3, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.gridLayout.addWidget(self.groupBox, 1, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 748, 21))
        self.menubar.setObjectName("menubar")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuCharacter = QtWidgets.QMenu(self.menubar)
        self.menuCharacter.setObjectName("menuCharacter")
        MainWindow.setMenuBar(self.menubar)
        self.actionExpand_all = QtWidgets.QAction(MainWindow)
        self.actionExpand_all.setObjectName("actionExpand_all")
        self.actionCollapse_all = QtWidgets.QAction(MainWindow)
        self.actionCollapse_all.setObjectName("actionCollapse_all")
        self.actionNew = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ui\\../image/icons/newfile.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNew.setIcon(icon)
        self.actionNew.setObjectName("actionNew")
        self.actionAdd_folder = QtWidgets.QAction(MainWindow)
        self.actionAdd_folder.setObjectName("actionAdd_folder")
        self.actionAdd_to_folder = QtWidgets.QAction(MainWindow)
        self.actionAdd_to_folder.setObjectName("actionAdd_to_folder")
        self.actionDelete = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("ui\\../image/icons/delete.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDelete.setIcon(icon1)
        self.actionDelete.setObjectName("actionDelete")
        self.actionNew_folder = QtWidgets.QAction(MainWindow)
        self.actionNew_folder.setObjectName("actionNew_folder")
        self.actionDelete_folder = QtWidgets.QAction(MainWindow)
        self.actionDelete_folder.setIcon(icon1)
        self.actionDelete_folder.setObjectName("actionDelete_folder")
        self.actionDelete_from_folder = QtWidgets.QAction(MainWindow)
        self.actionDelete_from_folder.setObjectName("actionDelete_from_folder")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("ui\\../image/icons/my_files.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon2)
        self.actionOpen.setObjectName("actionOpen")
        self.menuEdit.addAction(self.actionExpand_all)
        self.menuEdit.addAction(self.actionCollapse_all)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionNew_folder)
        self.menuEdit.addAction(self.actionDelete_folder)
        self.menuCharacter.addAction(self.actionNew)
        self.menuCharacter.addAction(self.actionOpen)
        self.menuCharacter.addSeparator()
        self.menuCharacter.addAction(self.actionAdd_to_folder)
        self.menuCharacter.addAction(self.actionDelete_from_folder)
        self.menuCharacter.addSeparator()
        self.menuCharacter.addAction(self.actionDelete)
        self.menubar.addAction(self.menuCharacter.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Персонаж"))
        self.pushButton_open.setText(_translate("MainWindow", "Открыть"))
        self.pushButton_add_folder.setText(_translate("MainWindow", "Добавить папку"))
        self.pushButton_add_in_folder.setText(_translate("MainWindow", "Добавить в папку"))
        self.label_2.setText(_translate("MainWindow", "Name: "))
        self.label_4.setText(_translate("MainWindow", "Class: "))
        self.label_6.setText(_translate("MainWindow", "Race: "))
        self.label_8.setText(_translate("MainWindow", "Level: "))
        self.label_22.setText(_translate("MainWindow", "Wisdom"))
        self.label_18.setText(_translate("MainWindow", "Dexterity"))
        self.label_21.setText(_translate("MainWindow", "Charisma"))
        self.label_19.setText(_translate("MainWindow", "Constitution"))
        self.label_20.setText(_translate("MainWindow", "Intelligence"))
        self.label_17.setText(_translate("MainWindow", "Strength"))
        self.label_strength.setText(_translate("MainWindow", "10"))
        self.label_dexterity.setText(_translate("MainWindow", "10"))
        self.label_constitution.setText(_translate("MainWindow", "10"))
        self.label_wisdom.setText(_translate("MainWindow", "10"))
        self.label_charisma.setText(_translate("MainWindow", "10"))
        self.label_intelligence.setText(_translate("MainWindow", "10"))
        self.menuEdit.setTitle(_translate("MainWindow", "Folder"))
        self.menuCharacter.setTitle(_translate("MainWindow", "Character"))
        self.actionExpand_all.setText(_translate("MainWindow", "Expand all"))
        self.actionExpand_all.setShortcut(_translate("MainWindow", "Ctrl+Shift+Return"))
        self.actionCollapse_all.setText(_translate("MainWindow", "Collapse all"))
        self.actionCollapse_all.setShortcut(_translate("MainWindow", "Ctrl+Shift+Backspace"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionAdd_folder.setText(_translate("MainWindow", "New folder"))
        self.actionAdd_to_folder.setText(_translate("MainWindow", "Add in folder"))
        self.actionDelete.setText(_translate("MainWindow", "Delete"))
        self.actionDelete.setShortcut(_translate("MainWindow", "Ctrl+Del"))
        self.actionNew_folder.setText(_translate("MainWindow", "New folder"))
        self.actionNew_folder.setShortcut(_translate("MainWindow", "Ctrl+F"))
        self.actionDelete_folder.setText(_translate("MainWindow", "Delete folder"))
        self.actionDelete_from_folder.setText(_translate("MainWindow", "Delete from folder"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
