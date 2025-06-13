from PySide6.QtWidgets import QApplication

app = QApplication([])

from pages.Main import Main

window = Main()
window.show()

app.exec()
