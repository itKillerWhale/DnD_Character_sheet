from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from windows.Spells import ShooseSpell
from windows.Characters import List, ShooseCharacter

import sys

from test import Test


def my_excepthook(type, value, tback):
    sys.__excepthook__(type, value, tback)


# app = QApplication(sys.argv)
#     ex = MainWindow()
#
#     if theme:
#         qtmodern.styles.dark(app)
#
#     else:
#         qtmodern.styles.light(app)
#
#     mw = qtmodern.windows.ModernWindow(ex)
#     mw.move(200, 200)
#
#     mw.show()
#     sys.excepthook = except_hook
#     app.exec_()

sys.excepthook = my_excepthook

app = QApplication(sys.argv)

app.setWindowIcon(QIcon('image/logo.jpg'))

window = ShooseCharacter()
window.show()

sys.excepthook = my_excepthook
app.exec()

# treeWidget->header()->setStretchLastSection(false);
# treeWidget->header()->setResizeMode(0, QHeaderView::Stretch);
# treeWidget->header()->setResizeMode(1, QHeaderView::Interactive);
