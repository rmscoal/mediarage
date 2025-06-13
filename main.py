from PySide6.QtWidgets import QApplication
from pages.Main import Main

app = QApplication([])

window = Main()
window.show()

app.exec()
