from PySide6.QtWidgets import QWidget


def reset_layout(widget: QWidget):
    old_layout = widget.layout()
    if old_layout is not None:
        while old_layout.count():
            child = old_layout.takeAt(0)
            if child.widget():
                child.widget().setParent(None)
        QWidget().setLayout(old_layout)  # Detach safely