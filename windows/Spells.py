import sqlite3

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QHeaderView

from ui.shoose_spell_window import Ui_MainWindow as ShooseSpellUI

from others import Sqlite3Client, TreeWidget


class ShooseSpell(QMainWindow, ShooseSpellUI):
    def __init__(self, parent=None, level=None):
        QMainWindow.__init__(self, parent=parent)
        uic.loadUi('ui/shoose_spell_window.ui', self)
        self.setWindowTitle("Заклинания")

        self.Spells = Sqlite3Client(sqlite3.connect("db/D&D.db"))

        self.verticalLayout_2.maximumSize().setWidth(480)

        # self.db = Sqlite3Client(sqlite3.connect("../db/Spells.db"))

        if level:
            pass

        # --- treeWidget ---
        self.treeWidget = TreeWidget(self)
        self.centralwidget.layout().addWidget(self.treeWidget, 1, 0)

        self.treeWidget.setColumnCount(3)
        header = self.treeWidget.header()
        self.treeWidget.setHeaderLabels(["Название", "Школа", "Уровень"])

        header.resizeSection(1, 10)
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

        # --- Настройка фильтров ---
        schools = set()
        for spell_stat in self.Spells.select("spells", "school"):
            schools.add(spell_stat)

        schools = sorted(list(schools))
        self.comboBox_school.addItems(schools)
        self.index_to_school_dict = dict(zip(range(1, len(schools) + 1), schools))

        classes = set()
        for spell_classes in self.Spells.select("spells", "classes"):
            for spell_class in spell_classes.split(", "):
                if not bool(spell_class):
                    continue
                spell_class = spell_class.replace("TCE", "").capitalize()
                classes.add(spell_class)

        classes = sorted(list(classes))
        self.comboBox_class.addItems(classes)
        self.index_to_classes_dict = dict(zip(range(1, len(classes) + 1), classes))

        # --- Настройка сигналов ---
        self.treeWidget.itemSelectionChanged.connect(self.update_spell_card)

        self.lineEdit_find.textChanged.connect(self.update_treeview)

        self.update_treeview()

        # print(self.horizontalLayout_filters_level.children())
        for i, checkBox in enumerate([self.checkBox, self.checkBox_2, self.checkBox_3, self.checkBox_4, self.checkBox_5,
                         self.checkBox_5, self.checkBox_6, self.checkBox_7, self.checkBox_8, self.checkBox_9,
                         self.checkBox_10, self.checkBox_11, self.checkBox_12, self.checkBox_13, self.checkBox_14]):
            if bool(level):
                if level != i:
                    checkBox.setEnabled(False)
                    checkBox.setChecked(False)

            checkBox.stateChanged.connect(self.update_treeview)
        self.comboBox_class.currentIndexChanged.connect(self.update_treeview)
        self.comboBox_school.currentIndexChanged.connect(self.update_treeview)

        self.comboBox.activated.connect(self.update_treeview)

    def update_treeview(self):
        Expanded_data = []
        if bool(self.treeWidget.folders):
            Expanded_data = self.treeWidget.get_expanded_folders()

        self.treeWidget.clear()

        # --- Фильтры ---
        # - Фильтр по имени (поле ввода сферху) -
        text_filter = self.lineEdit_find.text().lower()

        # - Фильтр по уровню заклинания (поле настроек) -
        level_filter = list(map(lambda checkBox: checkBox.isChecked(),
                                [self.horizontalLayout_filters_level.itemAt(i).widget() for i in range(10)]))

        # - Фильтр по компонентам (В, С, М) заклинания (поле настроек) -
        components_filter = []
        components_list = [["В"], ["С"], ["М"]]
        for i, f in enumerate(list(map(lambda checkBox: not checkBox.isChecked(),
                                       [self.horizontalLayout_components_CheckBoxes.itemAt(i).widget() for i in
                                        range(3)]))):
            if f:
                components_filter += components_list[i]

        # - Фильтр по времени накладывания заклинания (поле настроек) -
        application_time_filter = []
        application_time_list = [["1 действие"], ["1 бонусное действие"], ["1 реакция"], ["час", "мин"]]
        for i, f in enumerate(list(map(lambda checkBox: checkBox.isChecked(),
                                       [self.horizontalLayout_application_time_CheckBoxes.itemAt(i).widget() for i in
                                        range(4)]))):
            if f:
                application_time_filter += application_time_list[i]

        # - Фильтр по кассам и подклассам которым доступно заклинание (поле настроек) -
        spell_class = self.comboBox_class.currentText()
        class_filter = spell_class.lower() if spell_class != "Любой" else ""

        # - Фильтр по школе заклинания (поле настроек) -
        school = self.comboBox_school.currentText()
        school_filter = school if school != "Любая" else ""

        # --- Остальные вкладки ---
        index_to_stat_dict = {1: "level", 2: "school"}
        currentIndex = self.comboBox.currentIndex()
        if currentIndex == 0:
            folder = self.treeWidget.new_folder("Все заклинания", None)

            for spell_data in self.Spells.select("spells",
                                                 "id, name_ru, level, school, application_time, components, classes, archetypes",
                                                 text_filter=text_filter):

                # if not level_filter[spell_data[2]]:
                #     continue
                # if not any([string in spell_data[4] for string in application_time_filter]):
                #     continue
                # if not all([string not in spell_data[5] for string in components_filter]):
                #     continue
                # if school_filter not in spell_data[3]:
                #     continue
                # if class_filter not in spell_data[6] and class_filter not in spell_data[7]:
                #     continue
                # print(school_filter, class_filter)
                if any([not level_filter[spell_data[2]],
                        not any([string in spell_data[4] for string in application_time_filter]),
                        not all([string not in spell_data[5] for string in components_filter]),
                        school_filter not in spell_data[3],
                        class_filter not in spell_data[6] and class_filter not in spell_data[7]]):
                    continue

                folder.new_spell(*spell_data[:4])

            if not bool(folder.spells) and bool(folder.text(0)):
                del folder

            self.treeWidget.expandAll()

        elif currentIndex == 3:
            self.treeWidget.new_folder("Классы", None)
            # --- Classes ---
            folders = set()
            for spell_classes in self.Spells.select("spells", "classes"):
                for spell_class in spell_classes.split(", "):
                    # print(spell_class)
                    folders.add(spell_class)

            folders = sorted(list(folders))

            for folder_name in folders:
                if not bool(folder_name):
                    continue
                folder = self.treeWidget.new_folder(folder_name, None)

                for spell_data in self.Spells.select("spells",
                                                     "id, name_ru, level, school, application_time, components, classes, archetypes",
                                                     filters=f"classes LIKE '%{folder_name}%'",
                                                     text_filter=text_filter):
                    if any([not level_filter[spell_data[2]],
                            not any([string in spell_data[4] for string in application_time_filter]),
                            not all([string not in spell_data[5] for string in components_filter]),
                            school_filter not in spell_data[3],
                            class_filter not in spell_data[6] and class_filter not in spell_data[7]]):
                        continue

                    folder.new_spell(*spell_data[:4])

                if not bool(folder.spells) and bool(folder.text(0)):
                    del folder

            folders = self.treeWidget.folders
            for folder in folders:
                folder.setText(0, folder.text(0).capitalize().replace("tce", " TCE"))

            self.treeWidget.new_folder("", None)
            self.treeWidget.new_folder("Подклассы", None)
            # --- archetypes ---
            folders = set()
            for spell_classes in self.Spells.select("spells", "archetypes"):
                for spell_class in spell_classes.split(", "):
                    # print(spell_class)
                    folders.add(spell_class)

            folders = sorted(list(folders))

            for folder_name in folders:
                if not bool(folder_name):
                    continue
                folder = self.treeWidget.new_folder(folder_name, None)

                for spell_data in self.Spells.select("spells",
                                                     "id, name_ru, level, school, application_time, components, classes, archetypes",
                                                     filters=f"archetypes LIKE '%{folder_name}%'",
                                                     text_filter=text_filter):
                    if any([not level_filter[spell_data[2]],
                            not any([string in spell_data[4] for string in application_time_filter]),
                            not all([string not in spell_data[5] for string in components_filter]),
                            school_filter not in spell_data[3],
                            class_filter not in spell_data[6] and class_filter not in spell_data[7]]):
                        continue

                    folder.new_spell(*spell_data[:4])

            folders = self.treeWidget.folders
            for folder in folders:
                folder.setText(0, folder.text(0).capitalize().replace("tce", " TCE"))

        else:
            folders = set()
            for spell_stat in self.Spells.select("spells", index_to_stat_dict[currentIndex]):
                folders.add(spell_stat)

            folders = sorted(list(folders))
            # print(folders)

            for folder_name in folders:
                folder = self.treeWidget.new_folder(str(folder_name), None)

                # # print(folder_name)
                # print(f"{index_to_stat_dict[currentIndex]} = '{folder_name}'")
                for spell_data in self.Spells.select("spells",
                                                     "id, name_ru, level, school, application_time, components, classes, archetypes",
                                                     filters=f"{index_to_stat_dict[currentIndex]} = '{folder_name}'",
                                                     text_filter=text_filter):
                    if any([not level_filter[spell_data[2]],
                            not any([string in spell_data[4] for string in application_time_filter]),
                            not all([string not in spell_data[5] for string in components_filter]),
                            school_filter not in spell_data[3],
                            class_filter not in spell_data[6] and class_filter not in spell_data[7]]):
                        continue

                    folder.new_spell(*spell_data[:4])

                if not bool(folder.spells) and bool(folder.text(0)):
                    del folder

            folders = self.treeWidget.folders
            for folder in folders:
                text = folder.text(0).capitalize()
                if currentIndex == 1:
                    text += " уровень"
                if text == "0 уровень":
                    text = "Заговор"

                folder.setText(0, text)

        # folders = self.Characters.select("folders", "*")
        # folders = sorted(folders, key=lambda x: x[-1])
        #
        # for folder_id, name, index in folders:
        #     folder = self.treeWidget.new_folder(name, folder_id)
        #
        #     characters_id = self.Characters.select("characters_in_folder", "character_id",
        #                                            filters=f"folder_id = {folder_id}")
        #
        #     if len(characters_id) == 0:
        #         characters = []
        #
        #     elif len(characters_id) > 1:
        #         characters = self.Characters.select("character_list", "id, name, race, class, level",
        #                                             filters=f"id in {tuple(characters_id)}", sort=sort,
        #                                             reversed=is_reversed)
        #
        #     else:
        #         characters = self.Characters.select("character_list", "id, name, race, class, level",
        #                                             filters=f"id = {characters_id[0]}")
        #
        #     for character in characters:
        #         folder.new_character(*character)

        self.treeWidget.expend_folders(Expanded_data)

    def update_spell_card(self):
        spell_id, spell_type = self.treeWidget.selectedItems()[0].get_info()

        if spell_type != "spell":
            return

        data = self.Spells.select("spells", "name_ru, level, school, classes, description", filters=f"id = {spell_id}")[0]

        self.label_spell_name.setText(data[0])
        self.label_level_2.setText(str(data[1]) + " уровень" if data[1] > 0 else "Заговор")
        self.label_school_2.setText(data[2])
        self.label_classes_2.setText(' '.join(word.capitalize().replace("tce", " TCE") for word in data[3].split()))
        self.textEdit_description.setPlainText(data[4])

    def selecting_spell(self):
        pass


    def open_spell(self):
        self.treeWidget.currentItem()
        print(self.treeWidget.currentItem().id)


