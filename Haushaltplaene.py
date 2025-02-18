import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QHBoxLayout, \
    QListWidget, QListWidgetItem, QMessageBox, QDialog
from PyQt5.QtGui import QIcon


class RenamePlanDialog(QDialog):
    def __init__(self, old_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Plan umbenennen")
        self.setGeometry(300, 200, 300, 150)

        self.old_name = old_name

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Namen des Plans ändern"))

        hbox_old = QHBoxLayout()
        hbox_old.addWidget(QLabel("Alter Name:"))
        hbox_old.addWidget(QLabel(self.old_name))
        layout.addLayout(hbox_old)

        hbox_new = QHBoxLayout()
        hbox_new.addWidget(QLabel("Neuer Name:"))
        self.new_name_input = QLineEdit()
        hbox_new.addWidget(self.new_name_input)
        layout.addLayout(hbox_new)

        button_layout = QHBoxLayout()
        self.rename_button = QPushButton("Ändern")
        self.rename_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Abbrechen")
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.rename_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def get_new_name(self):
        return self.new_name_input.text()


class DeleteConfirmationDialog(QDialog):
    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Bestätigung")
        self.setGeometry(300, 200, 250, 100)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(message))

        button_layout = QHBoxLayout()
        self.yes_button = QPushButton("JA")
        self.yes_button.clicked.connect(self.accept)
        self.no_button = QPushButton("NEIN")
        self.no_button.clicked.connect(self.reject)

        button_layout.addWidget(self.yes_button)
        button_layout.addWidget(self.no_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)


class HaushaltsplanGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Haushaltspläne")
        self.setGeometry(200, 200, 500, 300)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.listWidget = QListWidget()
        layout.addWidget(self.listWidget)

        self.populate_list()

        self.new_plan_button = QPushButton("Neuen Plan erstellen")
        self.new_plan_button.clicked.connect(self.create_new_plan)
        layout.addWidget(self.new_plan_button)

        self.setLayout(layout)

    def populate_list(self):
        plans = ["HaushaltsPlan 1", "Toller neuer Name für Plan 2", "Plan noch nicht verwendet"]

        for plan in plans:
            item = QListWidgetItem()

            widget = QWidget()
            hbox = QHBoxLayout()

            name_input = QLineEdit(plan)
            if "nicht verwendet" in plan:
                name_input.setDisabled(True)
                name_input.setStyleSheet("color: gray;")

            edit_button = QPushButton()
            edit_button.setIcon(QIcon("edit_icon.png"))
            edit_button.clicked.connect(lambda _, inp=name_input: self.edit_plan(inp))

            delete_button = QPushButton()
            delete_button.setIcon(QIcon("delete_icon.png"))
            delete_button.clicked.connect(lambda _, inp=item: self.delete_plan(inp))

            hbox.addWidget(name_input)
            hbox.addWidget(edit_button)
            hbox.addWidget(delete_button)
            widget.setLayout(hbox)

            item.setSizeHint(widget.sizeHint())
            self.listWidget.addItem(item)
            self.listWidget.setItemWidget(item, widget)

    def edit_plan(self, name_input):
        dialog = RenamePlanDialog(name_input.text(), self)
        if dialog.exec_():
            new_name = dialog.get_new_name()
            if new_name:
                name_input.setText(new_name)

    def delete_plan(self, item):
        dialog = DeleteConfirmationDialog("Willst du den Plan wirklich löschen?", self)
        if dialog.exec_():
            row = self.listWidget.row(item)
            self.listWidget.takeItem(row)

    def create_new_plan(self):
        new_item = QListWidgetItem()

        widget = QWidget()
        hbox = QHBoxLayout()

        name_input = QLineEdit("Neuer Plan")

        edit_button = QPushButton()
        edit_button.setIcon(QIcon("edit_icon.png"))
        edit_button.clicked.connect(lambda _, inp=name_input: self.edit_plan(inp))

        delete_button = QPushButton()
        delete_button.setIcon(QIcon("delete_icon.png"))
        delete_button.clicked.connect(lambda _, inp=new_item: self.delete_plan(inp))

        hbox.addWidget(name_input)
        hbox.addWidget(edit_button)
        hbox.addWidget(delete_button)
        widget.setLayout(hbox)

        new_item.setSizeHint(widget.sizeHint())
        self.listWidget.addItem(new_item)
        self.listWidget.setItemWidget(new_item, widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HaushaltsplanGUI()
    window.show()
    sys.exit(app.exec_())
