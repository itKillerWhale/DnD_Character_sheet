STATS_RU = ["Сила", "Ловкость", "Телосложение", "Интеллект", "Мудрость", "Харизма"]
STATS_EN = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]

STATS_RU_TO_EN = {'Сила': 'Strength', 'Ловкость': 'Constitution', 'Телосложение': 'Dexterity',
                  'Интеллект': 'Intelligence', 'Мудрость': 'Wisdom', 'Харизма': 'Charisma'}
STATS_EN_TO_RU = {'Strength': 'Сила', 'Constitution': 'Ловкость', 'Dexterity': 'Телосложение',
                  'Intelligence': 'Интеллект', 'Wisdom': 'Мудрость', 'Charisma': 'Харизма'}

SKILLS_RU = ["Акробатика", "Атлетика", "Магия", "Обман", "История", "Проницательность", "Запугивание", "Расследование",
             "Медицина", "Природа", "Восприятие", "Выступление", "Убеждение", "Религия", "Ловкость рук", "Скрытость",
             "Выживание", "Обращение с животными"]

SKILLS_EN = ["Acrobatics", "Athletics", "Insight", "Survival", "Animal Handing", "Intimidation", "Performance",
             "History", "Sleight of Hand", "Arcane", "Medicine", "Deception", "Nature", "Insight", "Investigation",
             "Religion", "Stealth", "Persuasion"]

SKILLS_TO_STATS_RU = {"Акробатика": "Ловкость", "Атлетика": "Сила", "Внимание": "Мудрость", "Выживание": "Мудрость",
                      "Дрессировка": "Мудрость", "Запугивание": "Харизма", "Исполнение": "Харизма",
                      "История": "Интеллект", "Ловкость рук": "Ловкость", "Магия": "Интеллект", "Медицина": "Мудрость",
                      "Обман": "Харизма", "Природа": "Интеллект", "Проницательность": "Мудрость",
                      "Расследование": "Интеллект", "Религия": "Интеллект", "Скрытость": "Ловкость",
                      "Убеждение": "Харизма"}

SKILLS_TO_STATS_EN = {'Acrobatics': 'Constitution', 'Athletics': 'Strength', 'Insight': 'Wisdom', 'Survival': 'Wisdom',
                      'Animal Handing': 'Wisdom', 'Intimidation': 'Charisma', 'Performance': 'Charisma',
                      'History': 'Intelligence', 'Sleight of Hand': 'Constitution', 'Arcane': 'Intelligence',
                      'Medicine': 'Wisdom', 'Deception': 'Charisma', 'Nature': 'Intelligence',
                      'Investigation': 'Intelligence', 'Religion': 'Intelligence', 'Stealth': 'Constitution',
                      'Persuasion': 'Charisma'}

SKILLS_BONUS_DICT = {1: 2, 2: 2, 3: 2, 4: 2, 5: 3, 6: 3, 7: 3, 8: 3, 9: 4, 10: 4, 11: 4, 12: 4, 13: 5, 14: 5, 15: 5,
                     16: 5, 17: 6, 18: 6, 19: 6, 20: 6}

LEVEL_TO_XP_DICT = {1: 0, 2: 300, 3: 900, 4: 2700, 5: 6500, 6: 14000, 7: 23000, 8: 34000, 9: 48000, 10: 64000, 11: 85000,
                    12: 100000, 13: 120000, 14: 140000, 15: 165000, 16: 195000, 17: 225000, 18: 265000, 19: 305000,
                    20: 355000}
XP_TO_LEVEL_DICT = {xp: level for level, xp in LEVEL_TO_XP_DICT.items()}

NAMES_RU = ["Артос", "Партос", "Взнос"]
