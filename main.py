from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from windows import ShooseCharacter

import sys


def my_excepthook(type, value, tback):
    sys.__excepthook__(type, value, tback)


sys.excepthook = my_excepthook

app = QApplication(sys.argv)

app.setWindowIcon(QIcon('image/icons/main.ico'))

window = ShooseCharacter()
window.show()

app.exec()

# treeWidget->header()->setStretchLastSection(false);
# treeWidget->header()->setResizeMode(0, QHeaderView::Stretch);
# treeWidget->header()->setResizeMode(1, QHeaderView::Interactive);