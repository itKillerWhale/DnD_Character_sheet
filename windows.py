from random import randint, choice
import os
import shutil
import sqlite3

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QUndoStack, QKeySequence, QPixmap, QIcon, QFont, QContextMenuEvent, QAction
from PyQt6.QtWidgets import QMessageBox, QMainWindow, QGroupBox, QGridLayout, QLineEdit, QScrollArea, QFileDialog, \
    QTreeWidgetItem, QHeaderView, QInputDialog, QTreeWidget, QMenu, QDialog, QPushButton

from constants import *

from ui.list import Ui_MainWindow as ListUI
from ui.shoose_character_window import Ui_MainWindow as ShooseCharacterUI
from ui.comboboxdialog import Ui_Dialog as ComboBoxDialogUI


# ----- Декораторы -----
# --- Декоратор против зацикливания функций в классе ---
def anti_looping(func):
    def wrapper(self, *args, **kwargs):
        if self.k != 1: return

        self.k -= 1

        func(self)

        self.k += 1

    return wrapper


# --- Декоратор пропускающий только нужные данные в функцию ---
def is_selected(text):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            if bool(text):
                widgets_list = self.treeWidget.selectedItems()
                if not bool(widgets_list):
                    _ = QMessageBox.warning(
                        self,
                        "Ошибка",
                        "Ни один персонаж или папка не выделены",
                        buttons=QMessageBox.StandardButton.Ok,
                        defaultButton=QMessageBox.StandardButton.Ok,
                    )

                if widgets_list[0].get_info()[1] != text:
                    _ = QMessageBox.warning(
                        self,
                        "Ошибка",
                        "Вы не можете произвести это действие с выделенным на данный момент предметом",
                        buttons=QMessageBox.StandardButton.Ok,
                        defaultButton=QMessageBox.StandardButton.Ok,
                    )

            func(self)

        return wrapper

    return decorator


# ----- Вспомогательные классы -----
class Sqlite3Client:
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection
        self.cursor = connection.cursor()

        self.tables = list(
            map(lambda t: t, self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")))

    def select(self, db_name: str, args: str, filters=None, text_filter=None, sort=None, reversed=False) -> list:
        # --- Отлов неправильных значений ---
        if not (bool(db_name) and bool(args)):
            raise Exception("Имя или аргументы пустые")

        # --- Работа с данными ---
        data = list(self.cursor.execute(
            f"""SELECT {args} FROM {db_name}""" + (f""" WHERE {filters}""" if bool(filters) else "")))

        if len(args.split(", ")) == 1 and args != "*":
            data = list(map(lambda x: x[0], data))

        if bool(text_filter):
            data = list(
                filter(lambda character: any([text_filter in collum.lower() for collum in map(str, character[1:])]),
                       data))

        if bool(sort):
            data = list(sorted(data, key=lambda x: x[args.split(", ").index(sort)]))

        if reversed:
            data = data[::-1]

        return data

    def delete(self, db_name: str, filters: str):
        # --- Отлов неправильных значений ---
        if not (bool(db_name) and bool(filters)):
            raise Exception("Имя или филтры пустые")

        # --- Работа с данными ---
        self.cursor.execute(f"""DELETE FROM {db_name} WHERE {filters}""")

        self.connection.commit()

    def insert(self, db_name: str, collums_name: [str], collums_values: list):
        # --- Отлов неправильных значений ---
        if not (bool(db_name) and bool(collums_name) and bool(collums_values)):
            raise Exception("Имя или значения пустые")

        if len(collums_name) != len(collums_values):
            raise ValueError("Кол-во значений не равно")

        # --- Работа с данными ---
        self.cursor.execute(f"""INSERT INTO {db_name} {tuple(collums_name)} 
        VALUES ({', '.join(['?'] * len(collums_values))})""", collums_values)

        self.connection.commit()


# ----- Измененные виджеты -----


class TreeWidgetItem(QTreeWidgetItem):
    fontCharacters = QFont("MS Shell Dlg 2", 10)

    def __init__(self, id, type, *args, **kvargs, ):
        super().__init__(*args, **kvargs)

        self.id = id
        self.type = type

        self.characters = []

    def get_info(self) -> (int, str):
        return (self.id, self.type)

    def new_character(self, character_id, character_name, character_race, character_class, character_level):
        if not self.type == "folder":
            raise Exception("Это не являеться папкой")

        character = TreeWidgetItem(character_id, "character", (character_name, character_race, character_class,
                                                               str(character_level) + " lvl"))
        character.setFont(0, TreeWidgetItem.fontCharacters)

        self.characters.append(character)

        self.addChild(character)


class TreeWidget(QTreeWidget):
    fontFolder = QFont("MS Shell Dlg 2", 12)

    def __init__(self, window: QMainWindow, *args, **kvargs, ):
        super().__init__(*args, **kvargs)

        self.window = window

        self.menu_character = QMenu(parent=self)
        self.menu_character.addAction(self.window.actionOpen)
        self.menu_character.addSeparator()
        self.menu_character.addAction(self.window.actionAdd_to_folder)
        self.menu_character.addAction(self.window.actionDelete_from_folder)
        self.menu_character.addSeparator()
        self.menu_character.addAction(self.window.actionDelete)

        self.menu_folder = QMenu(parent=self)
        self.menu_folder.addAction(window.actionNew_folder)
        self.menu_folder.addAction(window.actionDelete_folder)

        self.menu_treeWidget = QMenu(parent=self)
        self.menu_treeWidget.addAction(window.actionNew_folder)

        self.folders = []

    def contextMenuEvent(self, event: QContextMenuEvent):
        widget = self.selectedItems()

        if not bool(widget):
            self.menu_treeWidget.move(event.globalX(), event.globalY())
            self.menu_treeWidget.show()

        widget = widget[0]

        id, type = widget.get_info()

        if type == "character":
            self.menu_character.move(event.globalX(), event.globalY())
            self.menu_character.show()

        elif type == "folder":
            self.menu_folder.move(event.globalX(), event.globalY())
            self.menu_folder.show()

        elif type == "All" or type == "Likes":
            self.menu_treeWidget.move(event.globalX(), event.globalY())
            self.menu_treeWidget.show()

    def new_folder(self, folder_name: str, folder_id: int or None, icon=None) -> TreeWidgetItem:
        folder = TreeWidgetItem(folder_id, "folder", self)
        self.addTopLevelItem(folder)
        if bool(icon): folder.setIcon(0, icon)
        folder.setText(0, folder_name)
        folder.setFont(0, TreeWidget.fontFolder)

        self.folders.append(folder)

        return folder

    def get_expanded_folders(self) -> dict:
        folders_name = list(map(lambda folder: folder.text(0), self.folders))
        expanded_list = list(map(lambda folder: folder.isExpanded(), self.folders))
        expanded_folders_dict = dict(zip(folders_name, expanded_list))

        return expanded_folders_dict

    def expend_folders(self, expanded_folders_dict: [TreeWidgetItem]):
        if not bool(expanded_folders_dict):
            return

        folders_name = list(map(lambda folder: folder.text(0), self.folders))
        for folder_name, f in list(expanded_folders_dict.items()):
            if folder_name in folders_name:
                self.folders[folders_name.index(folder_name)].setExpanded(f)

    def clear(self):
        super().clear()
        self.folders = []


# ----- Классы окон -----
class ComboBoxDialog(QDialog, ComboBoxDialogUI):
    def __init__(self, folders: list, parent=None):
        QDialog.__init__(self, parent=parent)
        uic.loadUi('ui/comboboxdialog.ui', self)

        for id, name, index in folders:
            self.comboBox.addItem(name)


class ShooseCharacter(QMainWindow, ShooseCharacterUI):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        uic.loadUi('ui/shoose_character_window.ui', self)
        self.setWindowTitle("Интерактивный лист персонажа")

        self.Characters = Sqlite3Client(sqlite3.connect("db/Сharacters.db"))

        self.parent = parent

        self.label_stats_list = [self.label_strength, self.label_dexterity, self.label_constitution,
                                 self.label_intelligence, self.label_wisdom, self.label_charisma]

        self.character_id = None

        # self.button = QPushButton("^")
        # self.button.move(30,30)
        # self.button.show()

        # --- Настройка и обновление TreeView ---
        self.treeWidget = TreeWidget(self)

        self.centralwidget.layout().addWidget(self.treeWidget, 1, 0)

        self.treeWidget.setColumnCount(4)
        header = self.treeWidget.header()
        self.treeWidget.setHeaderLabels(["Имя", "Раса", "Класс", "Уровень"])

        header.resizeSection(1, 10)
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)

        self.update_treeview()

        self.treeWidget.itemClicked.connect(self.open_information)
        self.treeWidget.itemDoubleClicked.connect(self.open_character)

        # --- Настройка кнопок ---

        self.lineEdit_find.textChanged.connect(self.update_treeview)

        self.actionExpand_all.triggered.connect(self.treeWidget.expandAll)
        self.actionCollapse_all.triggered.connect(self.treeWidget.collapseAll)
        self.actionNew_folder.triggered.connect(self.add_folder)
        self.actionNew.triggered.connect(self.new_character)
        self.actionOpen.triggered.connect(self.open_character)
        self.actionDelete_folder.triggered.connect(self.delete_folder)
        self.actionAdd_to_folder.triggered.connect(self.add_character_in_folder)
        self.actionDelete_from_folder.triggered.connect(self.delete_character_from_folder)
        self.actionDelete.triggered.connect(self.delete_character)

        self.comboBox.activated.connect(self.update_treeview)
        self.pushButton_is_reversed.clicked.connect(
            lambda: self.pushButton_is_reversed.setText("↑" if self.pushButton_is_reversed.text() == "↓" else "↓"))
        self.pushButton_is_reversed.clicked.connect(self.update_treeview)

    def update_treeview(self):
        Expanded_data = []
        if bool(self.treeWidget.folders):
            Expanded_data = self.treeWidget.get_expanded_folders()

        self.treeWidget.clear()

        text_filter = self.lineEdit_find.text().lower()
        sort = "name, race, class, level".split(", ")[self.comboBox.currentIndex()]
        is_reversed = self.pushButton_is_reversed.text() == "↓"

        # --- Вкладка All ---
        folder = self.treeWidget.new_folder("All", None, icon=QIcon("image/icons/my_files.ico"))

        characters = self.Characters.select("character_list", "id, name, race, class, level",
                                            text_filter=text_filter, sort=sort, reversed=is_reversed)

        for character in characters:
            folder.new_character(*character)

        # --- Вкладка Likes ---
        folder = self.treeWidget.new_folder("Likes", None, icon=QIcon("image/icons/likes.ico"))
        character_id = self.Characters.select("likes", "id")
        characters = self.Characters.select("character_list", "id, name, race, class, level",
                                            text_filter=text_filter,
                                            filters=f"id = {character_id[0]}" if len(
                                                character_id) == 1 else f"id in {tuple(character_id)}",
                                            sort=sort, reversed=is_reversed)

        for character in characters:
            folder.new_character(*character)

        # --- Остальные вкладки ---
        folders = self.Characters.select("folders", "*")
        folders = sorted(folders, key=lambda x: x[-1])

        for folder_id, name, index in folders:
            folder = self.treeWidget.new_folder(name, folder_id)

            characters_id = self.Characters.select("characters_in_folder", "character_id",
                                                   filters=f"folder_id = {folder_id}")

            if len(characters_id) == 0:
                characters = []

            elif len(characters_id) > 1:
                characters = self.Characters.select("character_list", "id, name, race, class, level",
                                                    filters=f"id in {tuple(characters_id)}", sort=sort,
                                                    reversed=is_reversed)

            else:
                characters = self.Characters.select("character_list", "id, name, race, class, level",
                                                    filters=f"id = {characters_id[0]}")

            for character in characters:
                folder.new_character(*character)

        self.treeWidget.expend_folders(Expanded_data)

    def open_information(self, widget: TreeWidgetItem):
        widgets_list = self.treeWidget.selectedItems()
        if not bool(widgets_list):
            return
        if widgets_list[0].get_info()[1] != "character":
            return

        character_id = widgets_list[0].get_info()[0]

        with sqlite3.connect('db/Сharacters.db') as con:
            cursor = con.cursor()

            character_collums = ["name", "strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma",
                                 "class", "level", "race"]
            character = list(cursor.execute(
                f"""SELECT {', '.join(character_collums)} FROM character_list WHERE id = {character_id}"""))[0]

        character_dict = dict(zip(character_collums, list(character)))

        stats = list(character_dict.values())[1:7]
        for i in range(6):
            self.label_stats_list[i].setText(str(stats[i]))

        self.label_name.setText(character_dict["name"])
        self.label_class.setText(character_dict["class"])
        self.label_race.setText(character_dict["race"])
        self.label_level.setText(str(character_dict["level"]) + " lvl")

        pixmap = QPixmap(f"image/characters/{character_id}.png")
        if pixmap.isNull():
            pixmap = QPixmap("image/characters/stub.png")
        self.label_image.setPixmap(
            pixmap.scaled(self.label_image.width(), self.label_image.height(), Qt.AspectRatioMode.KeepAspectRatio))

    def open_character(self, widget):
        # Если вызывает кнопка widget = False
        if widget is False:
            # Достаем выбраный виджет из treeWidget
            widget = self.treeWidget.selectedItems()
            # Проверяем есть ли в списке элементы
            if not bool(widget):
                return

            # т.к. возвращяеться список берем 0 элемент
            widget = widget[0]

        # Если у widget нет parent, значит он wihet верхнего типа и пользователь не выбрал перса
        if widget.parent() is None:
            return

        # Достаем id из widget
        character_id = widget.get_info()[0]

        f = True
        if self.parent:
            f = self.parent.close()

        if f:
            self.character_window = List(character_id, parent=self)
            if self.parent:
                self.character_window.move(self.parent.x(), self.parent.y())
            self.character_window.show()

    def new_character(self):
        self.window = List(None, parent=self)
        self.window.show()

    @is_selected(text="character")
    def add_character_in_folder(self):
        widgets_list = self.treeWidget.selectedItems()
        character_id = widgets_list[0].get_info()[0]

        with sqlite3.connect('db/Сharacters.db') as con:
            cursor = con.cursor()
            folders = list(cursor.execute(f"""SELECT * FROM folders"""))
            folders = sorted(folders, key=lambda x: x[-1])

        self.dialog = ComboBoxDialog(folders, parent=self)
        ok = self.dialog.exec()

        if ok:
            folder_id = folders[self.dialog.comboBox.currentIndex()][-1]
            print(folders)
            print(folder_id)

            with sqlite3.connect('db/Сharacters.db') as con:
                cursor = con.cursor()
                cursor.execute(f'INSERT INTO characters_in_folder (character_id, folder_id)'
                               f'VALUES ({character_id}, {folder_id})')

                con.commit()

            self.update_treeview()

    @is_selected(text="character")
    def delete_character_from_folder(self):
        widgets_list = self.treeWidget.selectedItems()
        character_id = widgets_list[0].get_info()[0]

        folder_id = widgets_list[0].parent().get_info()[0]

        with sqlite3.connect('db/Сharacters.db') as con:
            cursor = con.cursor()

            cursor.execute(
                f"""DELETE FROM characters_in_folder WHERE character_id = {character_id} AND folder_id = {folder_id}""")

            con.commit()

        self.update_treeview()

    @is_selected(text="character")
    def delete_character(self):
        widgets_list = self.treeWidget.selectedItems()
        character_id = widgets_list[0].get_info()[0]

        with sqlite3.connect('db/Сharacters.db') as con:
            cursor = con.cursor()

            character_name = list(cursor.execute(f"""SELECT name FROM character_list WHERE id = {character_id} """))[0][
                0]

        button = QMessageBox.warning(
            self,
            "Удаление персонажа",
            f"Вы хотите удалить персонажа {character_name}.\nУдалить?",
            buttons=QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel,
            defaultButton=QMessageBox.StandardButton.Cancel,
        )

        if button == QMessageBox.StandardButton.Ok:
            with sqlite3.connect('db/Сharacters.db') as con:
                cursor = con.cursor()

                cursor.execute(f"""DELETE FROM character_list WHERE id = {character_id}""")
                cursor.execute(f"""DELETE FROM characters_in_folder WHERE character_id = {character_id}""")
                cursor.execute(f"""DELETE FROM likes WHERE character_id = {character_id}""")

                con.commit()

        self.update_treeview()

    # --- Действия с папками ---

    def add_folder(self):
        text, f = QInputDialog.getText(
            self,
            'Новая папка',
            'Введите название новой папки', )

        if f:
            with sqlite3.connect('db/Сharacters.db') as con:
                cursor = con.cursor()

                folders = list(map(lambda x: x[0].lower(), cursor.execute(f"""SELECT name FROM folders""")))

                if text.lower() in folders:
                    _ = QMessageBox.warning(
                        self,
                        "Папка",
                        "Папка с таким названием уже есть",
                        buttons=QMessageBox.StandardButton.Ok,
                        defaultButton=QMessageBox.StandardButton.Ok,
                    )

                    return

                idexes = list(map(lambda n: n[0], cursor.execute(f"""SELECT folder_index FROM folders""")))
                print(idexes)

                if bool(idexes):
                    index = max(idexes) + 1
                else:
                    index = 1

                print(index)
                cursor.execute(f"""INSERT INTO folders (name, folder_index) VALUES (?, ?)""", (text, index))

        self.update_treeview()

    @is_selected(text="folder")
    def delete_folder(self):
        widgets_list = self.treeWidget.selectedItems()
        folder_id = widgets_list[0].get_info()[0]

        button = QMessageBox.warning(
            self,
            "Удаление папки",
            f"Вы хотите удалить папку {widgets_list[0].text(0)}.\nУдалить?",
            buttons=QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel,
            defaultButton=QMessageBox.StandardButton.Cancel,
        )

        if button == QMessageBox.StandardButton.Ok:
            with sqlite3.connect('db/Сharacters.db') as con:
                cursor = con.cursor()

                cursor.execute(f'DELETE FROM folders WHERE id = {folder_id}')
                cursor.execute(f'DELETE FROM characters_in_folder WHERE folder_id = {folder_id}')

                con.commit()

        self.update_treeview()

    def closeEvent(self, a0):
        self.Characters.connection.close()


# -------------------------------------------------------
# #######################################################
# -------------------------------------------------------
class List(QMainWindow, ListUI):
    def __init__(self, id, parent=None):
        QMainWindow.__init__(self)
        uic.loadUi('ui/list.ui', self)
        self.setWindowTitle("Интерактивный лист персонажа")

        self.Characters = Sqlite3Client(sqlite3.connect("db/Сharacters.db"))

        if parent:
            parent.close()
        # ----- Важные переменные -----
        self.is_new = id is None
        self.id = id
        self.k = 1
        self.UndoStack = QUndoStack()

        # ----- Работа с Menu -----
        # --- Создание шорткатов ---
        undo = QKeySequence("Ctrl+Z")
        self.action_undo.setShortcut(undo)

        redo = QKeySequence("Ctrl+Y")
        self.action_redo.setShortcut(redo)

        new = QKeySequence("Ctrl+N")
        self.action_new.setShortcut(new)

        save = QKeySequence("Ctrl+S")
        self.action_save.setShortcut(save)

        open = QKeySequence("Ctrl+O")
        self.action_open.setShortcut(open)

        generate_name = QKeySequence("Alt+N")
        self.action_name.setShortcut(generate_name)

        # --- Подключение кнопок к функциям ---
        self.action_save.triggered.connect(self.save)
        self.action_undo.triggered.connect(self.undo)
        self.action_redo.triggered.connect(self.redo)
        self.menu_edit.triggered.connect(self.update_undo_redo)
        self.action_open.triggered.connect(self.open)
        self.action_new.triggered.connect(self.new)

        self.action_name.triggered.connect(self.generate_name)

        # ----- Списки всех виджетов -----
        # --- checkBoxes ----
        self.checkBox_saving_throw_list = [self.checkBox_strength, self.checkBox_dexterity, self.checkBox_constitution,
                                           self.checkBox_intelligence, self.checkBox_wisdom, self.checkBox_charisma]
        self.tab_checkBox_saving_throw_list = [self.tab_checkBox_strength, self.tab_checkBox_dexterity,
                                               self.tab_checkBox_constitution, self.tab_checkBox_intelligence,
                                               self.tab_checkBox_wisdom, self.tab_checkBox_charisma]
        self.checkBox_skills_list = [self.checkBox_acrobatics, self.checkBox_althletics, self.checkBox_magic,
                                     self.checkBox_deception, self.checkBox_history, self.checkBox_insight,
                                     self.checkBox_intimidation, self.checkBox_investigation, self.checkBox_medicine,
                                     self.checkBox_nature, self.checkBox_perception, self.checkBox_performance,
                                     self.checkBox_persuasion, self.checkBox_religion, self.checkBox_sleight_of_hand,
                                     self.checkBox_stealth, self.checkBox_survival, self.checkBox_animal_handlings]

        self.label_ststs_list_for_skills = [self.label_dexterity, self.label_strength, self.label_intelligence,
                                            self.label_charisma, self.label_intelligence, self.label_wisdom,
                                            self.label_charisma, self.label_intelligence, self.label_wisdom,
                                            self.label_wisdom, self.label_wisdom, self.label_charisma,
                                            self.label_charisma, self.label_intelligence, self.label_dexterity,
                                            self.label_dexterity, self.label_wisdom, self.label_wisdom]
        # --- spinBoxes ---
        self.spinBox_stats_list = [self.spinBox_strength, self.spinBox_dexterity, self.spinBox_constitution,
                                   self.spinBox_intelligence, self.spinBox_wisdom, self.spinBox_charisma]
        self.tab_spinBox_stats_list = [self.tab_spinBox_strength, self.tab_spinBox_dexterity,
                                       self.tab_spinBox_constitution,
                                       self.tab_spinBox_intelligence, self.tab_spinBox_wisdom,
                                       self.tab_spinBox_charisma]

        self.spinBox_money_list = [self.spinBox_copper, self.spinBox_silver, self.spinBox_gold, self.spinBox_electrum,
                                   self.spinBox_platinum]
        self.tab_spinBox_money_list = [self.tab_spinBox_copper, self.tab_spinBox_silver, self.tab_spinBox_gold,
                                       self.tab_spinBox_electrum, self.tab_spinBox_platinum]

        # --- labels ---
        self.label_stats_list = [self.label_strength, self.label_dexterity, self.label_constitution,
                                 self.label_intelligence, self.label_wisdom, self.label_charisma]

        # --- lineEdits ---
        self.lineEdit_list = [self.lineEdit_name, self.lineEdit_race, self.lineEdit_class, self.lineEdit_background,
                              self.lineEdit_worldview, self.lineEdit_player_name]
        self.tab_lineEdit_list = [self.tab_lineEdit_name, self.tab_lineEdit_race, self.tab_lineEdit_class,
                                  self.tab_lineEdit_background, self.tab_lineEdit_worldview,
                                  self.tab_lineEdit_player_name]

        # --- textEdit ---
        self.textEdit_list = [self.textEdit_personal_traits, self.textEdit_ideals, self.textEdit_attachments,
                              self.textEdit_vices, self.textEdit_abilities, self.textEdit_inventory,
                              self.textEdit_languages]

        self.tab_textEdit_list = [self.tab_textEdit_personal_traits, self.tab_textEdit_ideals,
                                  self.tab_textEdit_attachments, self.tab_textEdit_vices, self.tab_textEdit_abilities,
                                  self.tab_textEdit_inventory, self.tab_textEdit_languages]

        # --- dicts ---

        # self.spinBox_stats_to_label_dict = dict(zip(self.spinBox_stats_list, self.label_stats_list))
        # self.spinBox_stats_to_tab_spinBox_stats_dict = dict(zip(self.spinBox_stats_list, self.tab_spinBox_stats_list))
        # self.tab_spinBox_stats_to_spinBox_stats_dict = dict(zip(self.tab_spinBox_stats_list, self.spinBox_stats_list))

        # self.lineEdit_to_tab_lineEdit_dict = dict(zip(self.lineEdit_list, self.tab_lineEdit_list))
        # self.tab_lineEdit_to_lineEdit_dict = dict(zip(self.tab_lineEdit_list, self.lineEdit_list))

        # self.label_ststs_list_to_spinBox_stats = dict(
        #     zip(self.checkBox_skills_list, self.label_ststs_list_for_skills))

        # self.checkBox_saving_throw_to_label_stats_list = dict(
        #     zip(self.checkBox_saving_throw_list, self.label_stats_list))

        # self.checkBox_saving_throw_to_tab_checkBox_saving_throw = dict(
        #     zip(self.checkBox_saving_throw_list, self.tab_checkBox_saving_throw_list))
        # self.tab_checkBox_saving_throw_to_checkBox_saving_throw = dict(
        #     zip(self.tab_checkBox_saving_throw_list, self.checkBox_saving_throw_list))

        # self.skill_en_to_skill_checkBox = dict(zip(SKILLS_EN, self.checkBox_skills_list))
        # self.skill_ru_to_skill_checkBox = dict(zip(SKILLS_RU, self.checkBox_skills_list))

        # self.spinBox_money_to_tab_spinBox_money_dict = dict(zip(self.spinBox_money_list, self.tab_spinBox_money_list))
        # self.tab_spinBox_money_to_spinBox_money_dict = dict(zip(self.tab_spinBox_money_list, self.spinBox_money_list))

        # self.textEdit_to_tab_textEdit_dict = dict(zip(self.textEdit_list, self.tab_textEdit_list))
        # self.tab_textEdit_to_textEdit_dict = dict(zip(self.tab_textEdit_list, self.textEdit_list))

        # self.stats_ru_to_spinBox_stats = dict(zip(STATS_RU, self.spinBox_stats_list))
        # self.stats_en_to_spinBox_stats = dict(zip(STATS_EN, self.spinBox_stats_list))

        # ----- Соеденение всех обновлений с функциями -----
        for lineEdit in self.lineEdit_list + self.tab_lineEdit_list:
            lineEdit.textChanged.connect(self.update_lineEdit)

        for spinBox in self.spinBox_stats_list + self.tab_spinBox_stats_list:
            spinBox.valueChanged.connect(self.update_stat)

        for checkBox in self.checkBox_skills_list + self.checkBox_saving_throw_list:
            checkBox.stateChanged.connect(self.update_skills)

        for checkBox in self.checkBox_saving_throw_list + self.tab_checkBox_saving_throw_list:
            checkBox.stateChanged.connect(self.update_saving_throws)

        for spinBox in self.spinBox_money_list + self.tab_spinBox_money_list:
            spinBox.valueChanged.connect(self.update_money)

        for textEdit in self.textEdit_list + self.tab_textEdit_list:
            textEdit.textChanged.connect(self.update_textEdit)

        self.spinBox_class_level.valueChanged.connect(self.update_xp)
        self.spinBox_class_level.valueChanged.connect(self.update_skills)
        self.tab_spinBox_class_level.valueChanged.connect(self.update_xp)

        self.comboBox_hp_cube.activated.connect(self.update_hp_cube)
        self.tab_comboBox_hp_cube.activated.connect(self.update_hp_cube)
        self.spinBox_class_level.valueChanged.connect(self.update_hp_cube)

        self.spinBox_hp.valueChanged.connect(self.update_hp)
        self.tab_spinBox_hp.valueChanged.connect(self.update_hp)

        self.spinBox_speed.valueChanged.connect(self.update_speed)
        self.tab_spinBox_speed.valueChanged.connect(self.update_speed)

        self.spinBox_armor_class.valueChanged.connect(self.update_armor_class)
        self.tab_spinBox_armor_class.valueChanged.connect(self.update_armor_class)

        self.spinBox_xp.valueChanged.connect(self.update_level)
        self.tab_spinBox_xp.valueChanged.connect(self.update_level)

        self.pushButton_random_stats.clicked.connect(self.set_randon_stats)
        self.pushButton_full_random_stats.clicked.connect(self.set_full_random_stats)
        self.tab_pushButton_hp_average.clicked.connect(self.set_average_hp)
        self.tab_pushButton_level_random.clicked.connect(self.set_level_random_hp)
        self.tab_pushButton_full_random.clicked.connect(self.set_full_random_hp)

        self.tab_textEdit_skills.textChanged.connect(self.update_skills_tab)

        self.spellcasting_list_comboBox_main_stat.activated.connect(self.update_spellcasting_list)

        self.pushButton_shoose_file.clicked.connect(self.shoose_image)
        self.pushButton_delete_image.clicked.connect(self.delete_image)

        self.checkBox_inspiration.stateChanged.connect(self.update_inspiration)
        self.comboBox_inspiration.activated.connect(self.update_inspiration)

        # --- Создание полей для weapons ---
        # layout = QGridLayout(self)
        # self.weapon_name_1 = QLineEdit()
        # self.weapon_attack_bonus_1 = QLineEdit()
        # self.weapon_damage_1 = QLineEdit()
        #
        # layout.addWidget(self.weapon_name_1, 0, 0)
        # layout.addWidget(self.weapon_attack_bonus_1, 0, 1)
        # layout.addWidget(self.weapon_damage_1, 0, 2)
        #
        # w = QWidget()
        # w.setLayout(layout)
        #
        # self.weapon_scrollArea.setWidget(w)

        # ----- Окрываем персонажа -----
        if not self.is_new:
            self.open_character(id=self.id)

    # ----- Вспомогательные функции -----
    def get_stat_bonus(self, stat: str) -> int:
        stats_ru_to_spinBox_stats = dict(zip(STATS_RU, self.spinBox_stats_list))
        stats_en_to_spinBox_stats = dict(zip(STATS_EN, self.spinBox_stats_list))

        stat = stat.capitalize()

        if stat in STATS_RU:
            value = stats_ru_to_spinBox_stats[stat].value()

        else:
            value = stats_en_to_spinBox_stats[stat].value()

        stat_bonus = (value - 10) // 2

        return stat_bonus

    def get_character(self):
        character = (self.id, self.lineEdit_name.text(), self.spinBox_strength.value(),
                     self.spinBox_dexterity.value(), self.spinBox_constitution.value(),
                     self.spinBox_intelligence.value(), self.spinBox_wisdom.value(), self.spinBox_charisma.value(),
                     ", ".join(
                         [STATS_EN[i] if checkBox_saving_throws.isChecked() else "" for i, checkBox_saving_throws in
                          enumerate(self.checkBox_saving_throw_list)]),
                     self.tab_textEdit_skills.toPlainText(), self.lineEdit_class.text(),
                     self.spinBox_class_level.value(), self.spinBox_xp.value(), self.lineEdit_race.text(),
                     self.lineEdit_background.text(), self.lineEdit_worldview.text(),
                     self.lineEdit_player_name.text(), self.spinBox_hp.value(), self.spinBox_armor_class.value(),
                     self.spinBox_speed.value(), self.label_inspiration.text(), self.textEdit_abilities.toPlainText(),
                     "1", self.textEdit_inventory.toPlainText(),
                     ", ".join(list(map(str, [self.spinBox_copper.value(), self.spinBox_silver.value(),
                                              self.spinBox_gold.value(),
                                              self.spinBox_electrum.value(), self.spinBox_platinum.value()]))),
                     self.textEdit_languages.toPlainText(), self.textEdit_personal_traits.toPlainText(),
                     self.textEdit_ideals.toPlainText(), self.textEdit_attachments.toPlainText(),
                     self.textEdit_vices.toPlainText())

        return character

    # ----- Функции обновления значений в полях -----
    def open_character(self, id=None):
        if not bool(id):
            pass

        with sqlite3.connect('db/Сharacters.db') as con:
            cursor = con.cursor()

            character = list(cursor.execute(f"""SELECT * FROM character_list WHERE id = {self.id}"""))[0]

        character_collums = ["id", "name", "strength", "dexterity", "constitution", "intelligence", "wisdom",
                             "charisma", "saving_throws", "skills", "class", "level", "xp", "race", "background",
                             "worldview", "player_name", "hp", "armor_class", "speed", "inspiration", "abilities",
                             "weapons", "inventory", "money", "languages", "personal_traits", "ideals", "attachments",
                             "vices"]
        character_dict = dict(zip(character_collums, list(character)))

        self.lineEdit_name.setText(character_dict["name"])
        self.spinBox_xp.setValue(character_dict["xp"])

        saving_throws = character_dict["saving_throws"]
        stats = list(character_dict.values())[2:8]
        for i in range(6):
            self.spinBox_stats_list[i].setValue(stats[i])
            if STATS_EN[i] in saving_throws:
                self.checkBox_saving_throw_list[i].setChecked(True)

        self.tab_textEdit_skills.setPlainText(character_dict["skills"])
        self.update_skills(self)
        self.lineEdit_class.setText(character_dict["class"])

        self.lineEdit_race.setText(character_dict["race"])
        self.lineEdit_worldview.setText(character_dict["worldview"])
        self.lineEdit_background.setText(character_dict["background"])
        self.lineEdit_player_name.setText(character_dict["player_name"])
        self.spinBox_hp.setValue(character_dict["hp"])
        self.spinBox_armor_class.setValue(character_dict["armor_class"])
        self.spinBox_speed.setValue(character_dict["speed"])
        if bool(character_dict["inspiration"]):
            self.checkBox_inspiration.setChecked(True)
            self.comboBox_inspiration.setCurrentText(character_dict["inspiration"])
            self.label_inspiration.setText(character_dict["inspiration"])

        self.textEdit_abilities.setPlainText(character_dict["abilities"])
        self.textEdit_inventory.setPlainText(character_dict["inventory"])

        money = list(map(int, character_dict["money"].split(", ")))
        self.spin_Box_money_list = [self.spinBox_copper, self.spinBox_silver, self.spinBox_gold, self.spinBox_electrum,
                                    self.spinBox_platinum]
        for i in range(5):
            self.spin_Box_money_list[i].setValue(money[i])

        self.textEdit_languages.setPlainText(character_dict["languages"])
        self.textEdit_personal_traits.setPlainText(character_dict["personal_traits"])
        self.textEdit_ideals.setPlainText(character_dict["ideals"])
        self.textEdit_attachments.setPlainText(character_dict["attachments"])
        self.textEdit_vices.setPlainText(character_dict["vices"])

        pixmap = QPixmap(f"image/characters/{self.id}.png")
        if pixmap.isNull():
            pixmap = QPixmap("image/characters/stub.png")
        self.label_image.setPixmap(
            pixmap.scaled(self.label_image.width(), self.label_image.height(), Qt.AspectRatioMode.KeepAspectRatio))

    def update_stat(self):
        # --- dicts ---
        spinBox_stats_to_label_dict = dict(zip(self.spinBox_stats_list, self.label_stats_list))
        spinBox_stats_to_tab_spinBox_stats_dict = dict(zip(self.spinBox_stats_list, self.tab_spinBox_stats_list))
        tab_spinBox_stats_to_spinBox_stats_dict = {v: k for k, v in spinBox_stats_to_tab_spinBox_stats_dict.items()}

        sender = self.sender()
        if sender in self.spinBox_stats_list:
            spinBox_stats_to_tab_spinBox_stats_dict[sender].setValue(sender.value())
        else:
            tab_spinBox_stats_to_spinBox_stats_dict[sender].setValue(sender.value())
            sender = tab_spinBox_stats_to_spinBox_stats_dict[sender]

        spinBox_stats_to_label_dict[sender].setText(str((sender.value() - 10) // 2))

        self.label_initiative.setText(self.label_dexterity.text())

        self.update_skills(self)

    @anti_looping
    def update_skills(self):
        # --- dict ---
        label_ststs_list_to_spinBox_stats = dict(zip(self.checkBox_skills_list, self.label_ststs_list_for_skills))
        checkBox_saving_throw_to_label_stats_list = dict(zip(self.checkBox_saving_throw_list, self.label_stats_list))

        # Вытаскиваем значения бонуса мастерства и ставим его
        skill_bonus = SKILLS_BONUS_DICT[self.spinBox_class_level.value()]
        self.label_skill_bonus.setText("+ " + str(skill_bonus))

        # Обновляем спасброски
        for checkBox_saving_throw in self.checkBox_saving_throw_list:
            # Ищем значение для спасбросков (в словаре) и переводим в число
            n = int(checkBox_saving_throw_to_label_stats_list[checkBox_saving_throw].text())

            # Если мы владеем спасброском прибавляем бонус мастерста
            if checkBox_saving_throw.isChecked():
                n += skill_bonus

            # Обновляем текст спасброска с новым значением
            checkBox_saving_throw.setText(str(n))

        # Обновляем скилы
        for checkBox_skill in self.checkBox_skills_list:
            # Ищем значение для скилов (в словаре) и переводим в число
            n = int(label_ststs_list_to_spinBox_stats[checkBox_skill].text())

            # Если мы владеем скилом прибавляем бонус мастерста
            if checkBox_skill.isChecked():
                n += skill_bonus

            # Обновляем текст скила с новым значением
            checkBox_skill.setText(str(n))

        # Обновляем список скилов (tab_textEdit_skills) в tab
        # Создаем список для весх названий скилов
        text_list = []
        # Перебираем номер checkBox и его ?отмеченночти?, и добавляем в список если он checked
        for i, checkBox in (filter(lambda checkBox: checkBox[1].isChecked(), enumerate(self.checkBox_skills_list))):
            text_list.append(SKILLS_RU[i])
        self.tab_textEdit_skills.setPlainText(", ".join(text_list))

        # обновляем пассивное восприятие
        passive_perception = self.checkBox_perception.text()
        if "+" in passive_perception:
            passive_perception = passive_perception.replace("+", "")
        passive_perception = int(passive_perception) + 10

        self.label_passive_perception.setText(str(passive_perception))

        # # Подключаем сигнал от tab_textEdit_skills обратно

        self.k += 1
        self.update_spellcasting_list(self)
        self.k -= 1

    @anti_looping
    def update_skills_tab(self):
        skill_en_to_skill_checkBox = dict(zip(SKILLS_EN, self.checkBox_skills_list))
        skill_ru_to_skill_checkBox = dict(zip(SKILLS_RU, self.checkBox_skills_list))

        skills = self.tab_textEdit_skills.toPlainText()

        for skill in SKILLS_EN:
            if skill in skills:
                skill_en_to_skill_checkBox[skill].setChecked(True)

        for skill in SKILLS_RU:
            if skill in skills:
                skill_ru_to_skill_checkBox[skill].setChecked(True)

    @anti_looping
    def update_saving_throws(self):
        checkBox_saving_throw_to_tab_checkBox_saving_throw = dict(
            zip(self.checkBox_saving_throw_list, self.tab_checkBox_saving_throw_list))
        tab_checkBox_saving_throw_to_checkBox_saving_throw = {v: k for k, v in
                                                              checkBox_saving_throw_to_tab_checkBox_saving_throw.items()}

        sender = self.sender()
        if sender in self.checkBox_saving_throw_list:
            checkBox_saving_throw_to_tab_checkBox_saving_throw[sender].setChecked(sender.isChecked())
        elif sender in self.tab_checkBox_saving_throw_list:
            tab_checkBox_saving_throw_to_checkBox_saving_throw[sender].setChecked(sender.isChecked())

    @anti_looping
    def update_spellcasting_list(self):
        main_stat = self.spellcasting_list_comboBox_main_stat.currentText()
        stat_bonus = self.get_stat_bonus(main_stat)
        level_bonus = int(self.label_skill_bonus.text().replace("+", ""))

        self.label_saving_throw_difficulty.setText(str(8 + stat_bonus + level_bonus))
        self.label_attack_roll_bonus.setText("+ " + str(stat_bonus + level_bonus))

    @anti_looping
    def update_hp_cube(self):
        sender = self.sender()

        if sender == self.comboBox_hp_cube:
            self.tab_comboBox_hp_cube.setCurrentText(self.comboBox_hp_cube.currentText())

        elif sender == self.tab_comboBox_hp_cube:
            self.comboBox_hp_cube.setCurrentText(self.tab_comboBox_hp_cube.currentText())

        k = self.spinBox_class_level.value()
        hp_cube = self.comboBox_hp_cube.currentText()
        text = str(k) + " " + hp_cube

        self.label_hp_cube.setText(text)
        self.tab_label_hp_cube.setText(text)

    @anti_looping
    def update_xp(self):
        sender = self.sender()
        if sender == self.spinBox_class_level:
            self.tab_spinBox_class_level.setValue(self.spinBox_class_level.value())
        elif sender == self.tab_spinBox_class_level:
            self.spinBox_class_level.setValue(self.tab_spinBox_class_level.value())

        xp = LEVEL_TO_XP_DICT[self.spinBox_class_level.value()]

        if self.spinBox_xp.value() != xp: self.spinBox_xp.setValue(xp)
        if self.tab_spinBox_xp.value() != xp: self.tab_spinBox_xp.setValue(xp)

    @anti_looping
    def update_level(self):
        sender = self.sender()

        if sender == self.spinBox_xp and sender.value() != self.tab_spinBox_xp.value:
            self.tab_spinBox_xp.setValue(self.spinBox_xp.value())

            for level in range(1, 21):
                if sender.value() >= LEVEL_TO_XP_DICT[level]:
                    self.spinBox_class_level.setValue(level)
                    self.tab_spinBox_class_level.setValue(level)

        elif sender == self.tab_spinBox_xp and sender.value() != self.spinBox_xp.value:
            self.tab_spinBox_xp.setValue(self.tab_spinBox_xp.value())

            for level in range(1, 21):
                if sender.value() >= LEVEL_TO_XP_DICT[level]:
                    self.spinBox_class_level.setValue(level)
                    self.tab_spinBox_class_level.setValue(level)

        if sender == self.spinBox_xp:
            self.tab_spinBox_xp.setValue(self.spinBox_xp.value())
        elif sender == self.tab_spinBox_xp:
            self.spinBox_xp.setValue(self.tab_spinBox_xp.value())

        self.k += 1
        self.update_skills(self)
        self.k -= 1

    @anti_looping
    def update_lineEdit(self):
        lineEdit_to_tab_lineEdit_dict = dict(zip(self.lineEdit_list, self.tab_lineEdit_list))
        tab_lineEdit_to_lineEdit_dict = {v: k for k, v in lineEdit_to_tab_lineEdit_dict.items()}

        sender = self.sender()
        if sender in self.lineEdit_list:
            lineEdit_to_tab_lineEdit_dict[sender].setText(sender.text())
        else:
            tab_lineEdit_to_lineEdit_dict[sender].setText(sender.text())

    @anti_looping
    def update_hp(self):
        sender = self.sender()

        if sender == self.spinBox_hp:
            self.tab_spinBox_hp.setValue(self.spinBox_hp.value())
        else:
            self.spinBox_hp.setValue(self.tab_spinBox_hp.value())

        self.label_max_hp.setText(str(self.spinBox_hp.value()))

    @anti_looping
    def update_speed(self):
        sender = self.sender()

        if sender == self.spinBox_speed:
            self.tab_spinBox_speed.setValue(self.spinBox_speed.value())

        else:
            self.spinBox_speed.setValue(self.tab_spinBox_speed.value())

    @anti_looping
    def update_armor_class(self):
        sender = self.sender()

        if sender == self.spinBox_armor_class:
            self.tab_spinBox_armor_class.setValue(self.spinBox_armor_class.value())

        else:
            self.spinBox_armor_class.setValue(self.tab_spinBox_armor_class.value())

    @anti_looping
    def update_money(self):
        spinBox_money_to_tab_spinBox_money_dict = dict(zip(self.spinBox_money_list, self.tab_spinBox_money_list))
        tab_spinBox_money_to_spinBox_money_dict = {v: k for k, v in spinBox_money_to_tab_spinBox_money_dict.items()}

        sender = self.sender()

        if sender in self.spinBox_money_list:
            spinBox_money_to_tab_spinBox_money_dict[sender].setValue(sender.value())

        elif sender in self.tab_spinBox_money_list:
            tab_spinBox_money_to_spinBox_money_dict[sender].setValue(sender.value())

    @anti_looping
    def update_textEdit(self):
        textEdit_to_tab_textEdit_dict = dict(zip(self.textEdit_list, self.tab_textEdit_list))
        tab_textEdit_to_textEdit_dict = {v: k for k, v in textEdit_to_tab_textEdit_dict.items()}

        sender = self.sender()

        if sender in self.textEdit_list:
            textEdit_to_tab_textEdit_dict[sender].setPlainText(sender.toPlainText())

        elif sender in self.tab_textEdit_list:
            tab_textEdit_to_textEdit_dict[sender].setPlainText(sender.toPlainText())

    @anti_looping
    def update_inspiration(self):
        self.comboBox_inspiration.setEnabled(self.checkBox_inspiration.isChecked())

        text = ""
        if self.checkBox_inspiration.isChecked():
            text = self.comboBox_inspiration.currentText()
        else:
            self.comboBox_inspiration.setCurrentText("d6")

        self.label_inspiration.setText(text)

    # ----- Функции кнопок -----
    def add_weapon(self):
        groupBox = QGroupBox()
        groupBox.setMaximumSize(173, 65)

        grindlayout = QGridLayout()
        groupBox.setLayout(grindlayout)

        lineEdit_name = QLineEdit()
        lineEdit_attack_bonus = QLineEdit()
        lineEdit_damage_and_type = QLineEdit()

        grindlayout.addWidget(lineEdit_name, 0, 0)
        grindlayout.addWidget(lineEdit_attack_bonus, 0, 1)
        grindlayout.addWidget(lineEdit_damage_and_type, 0, 2)

        a = QScrollArea

        self.verticalLayout_4.addWidget(groupBox)

    # --- Кнопки статов ---

    # set_randon_stats выставляет случайные статы опираясь на распределение 1 лвл
    def set_randon_stats(self):
        # способ распределения статов засчет очков которые тратяться на статы
        points = 27
        stats_list = [8] * 6
        while points > 0:
            i = randint(0, 5)
            if stats_list[i] < 13:
                stats_list[i] += 1
                points -= 1
            elif stats_list[i] < 15:
                stats_list[i] += 1
                points -= 2
            else:
                continue

        for i in range(6):
            self.spinBox_stats_list[i].setValue(stats_list[i])

    # set_full_random_stats выставляет случайные статы (от 1 до 20)
    def set_full_random_stats(self):
        for i in range(6):
            self.spinBox_stats_list[i].setValue(randint(1, 20))

    def set_average_hp(self):
        k = self.spinBox_class_level.value()
        hp_cube = int(self.comboBox_hp_cube.currentText().replace("d", ""))
        constitution_bonus = self.label_constitution.text()
        constitution_bonus = int(
            constitution_bonus.replace("+", "") if "+" in constitution_bonus else constitution_bonus)

        hp = hp_cube + constitution_bonus * k + (hp_cube // 2 + 1) * (k - 1)

        self.spinBox_hp.setValue(hp)

    def set_level_random_hp(self):
        k = self.spinBox_class_level.value()
        hp_cube = int(self.comboBox_hp_cube.currentText().replace("d", ""))
        constitution_bonus = self.label_constitution.text()
        constitution_bonus = int(
            constitution_bonus.replace("+", "") if "+" in constitution_bonus else constitution_bonus)

        hp = hp_cube + constitution_bonus * k + sum([randint(1, hp_cube)] * (k - 1))

        self.spinBox_hp.setValue(hp)

    def set_full_random_hp(self):
        k = self.spinBox_class_level.value()
        hp_cube = int(self.comboBox_hp_cube.currentText().replace("d", ""))
        constitution_bonus = self.label_constitution.text()
        constitution_bonus = int(
            constitution_bonus.replace("+", "") if "+" in constitution_bonus else constitution_bonus)

        hp = randint(hp_cube + constitution_bonus, hp_cube * k + constitution_bonus * (k - 1))

        self.spinBox_hp.setValue(hp)

    def shoose_image(self):
        filter_file = "Images (*.png *.jpeg .jpg)"
        get_photo = QFileDialog().getOpenFileName(
            self,
            'Select photo',
            '',
            filter_file
        )[0]

        path_save = 'image/characters/'

        if get_photo:
            os.makedirs(path_save, exist_ok=True)

            product_photo = path_save + str(self.id) + ".png"
            shutil.copyfile(get_photo, product_photo)

            pixmap = QPixmap(get_photo)
            if pixmap.isNull():
                pixmap = QPixmap("image/characters/stub.png")
            self.label_image.setPixmap(
                pixmap.scaled(self.label_image.width(), self.label_image.height(), Qt.AspectRatioMode.KeepAspectRatio))

    def delete_image(self):
        try:
            os.remove(f"image/characters/{self.id}.png")
        except FileNotFoundError:
            pass

        pixmap = QPixmap("image/characters/stub.png")
        self.label_image.setPixmap(
            pixmap.scaled(self.label_image.width(), self.label_image.height(), Qt.AspectRatioMode.KeepAspectRatio))

    # ----- Events -----
    def closeEvent(self, event):
        if not self.is_new:
            with sqlite3.connect('db/Сharacters.db') as con:
                cursor = con.cursor()

                character_old = list(cursor.execute(f"""SELECT * FROM character_list WHERE id = {self.id}"""))[0]

            character_new = self.get_character()

            if character_new == character_old:
                self.window = ShooseCharacter(parent=self)
                self.window.show()
                return

        button = QMessageBox.question(
            self,
            "Сохранить изменения?",
            "Есть несохраненныйе изменения.",
            buttons=QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Cancel,
            defaultButton=QMessageBox.StandardButton.Save,
        )

        if button == QMessageBox.StandardButton.Cancel:
            event.ignore()
            return
        elif button == QMessageBox.StandardButton.Discard:
            event.accept()
        elif QMessageBox.StandardButton.Save:
            self.save()

        self.Characters.connection.close()
        self.window = ShooseCharacter(parent=self)
        self.window.show()

    def resizeEvent(self, a0):
        pixmap = QPixmap(f"image/characters/{self.id}.png")
        if pixmap.isNull():
            pixmap = QPixmap("image/characters/stub.png")
        self.label_image.setPixmap(
            pixmap.scaled(self.label_image.width(), self.label_image.height(), Qt.AspectRatioMode.KeepAspectRatio))

    # ----- Функции меню -----
    def update_undo_redo(self):
        self.action_undo.setEnabled(self.UndoStack.canUndo())
        self.action_redo.setEnabled(self.UndoStack.canRedo())

    def save(self, character_new=None):
        if not bool(character_new):
            character_new = self.get_character()

        if self.is_new:
            with sqlite3.connect('db/Сharacters.db') as con:
                cursor = con.cursor()

                cursor.execute(
                    f'INSERT INTO character_list(name, strength, dexterity, constitution, intelligence, wisdom, '
                    f'charisma, saving_throws, skills, class, level, xp, race, background, worldview, player_name, hp, '
                    f'armor_class, speed, inspiration, abilities, weapons, inventory, money, languages, '
                    f'personal_traits, ideals, attachments, vices) VALUES  (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, '
                    f'?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', character_new[1:])

                con.commit()

        else:
            with sqlite3.connect('db/Сharacters.db') as con:
                cursor = con.cursor()

                cursor.execute(
                    f'UPDATE character_list SET name = ?, strength = ?, dexterity = ?, constitution = ?,'
                    f'intelligence = ?, wisdom = ?, charisma = ?, saving_throws = ?, skills = ?, class = ?, level = ?, '
                    f'xp = ?, race = ?,'
                    f' background = ?, worldview = ?, player_name = ?, hp = ?, armor_class = ?, speed = ?, inspiration = ?,'
                    f' abilities = ?, weapons = ?, inventory = ?, money = ?, languages = ?, personal_traits = ?,'
                    f' ideals = ?, attachments = ?, vices = ? WHERE id = {self.id}', character_new[1:])

                con.commit()

    def redo(self):
        self.UndoStack.redo()

    def undo(self):
        self.UndoStack.undo()

    def open(self):
        self.window = ShooseCharacter(parent=self)
        self.window.show()

    def new(self):
        self.window = List(None, parent=self)
        self.window.show()

    def generate_name(self):
        name = choice(NAMES_RU)
        while name == self.lineEdit_name.text():
            name = choice(NAMES_RU)
        self.lineEdit_name.setText(name)
