from PySide6.QtWidgets import QApplication, QLabel

app = QApplication([])
label = QLabel("Test Window")
label.show()
app.exec()