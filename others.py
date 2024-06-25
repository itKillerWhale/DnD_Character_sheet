import sqlite3

from PyQt6 import uic

from PyQt6.QtGui import QFont, QContextMenuEvent
from PyQt6.QtWidgets import QMessageBox, QMainWindow, QTreeWidgetItem, QTreeWidget, QMenu, QDialog

from ui.comboboxdialog import Ui_Dialog as ComboBoxDialogUI



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
        # print(filters)
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

        # print()
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
        self.spells = []

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

    def new_spell(self, spell_id, spell_name, spell_level, spell_school):
        if not self.type == "folder":
            raise Exception("Это не являеться папкой")

        spell = TreeWidgetItem(spell_id, "spell", (
            spell_name, spell_school.capitalize(), str(spell_level) + " уровень" if spell_level != 0 else "Заговор"))
        spell.setFont(0, TreeWidgetItem.fontCharacters)

        self.spells.append(spell)

        self.addChild(spell)


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
