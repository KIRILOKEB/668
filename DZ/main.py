import json

from PySide6.QtCore import *
from PySide6.QtWidgets import *

from ui import Ui_MainWindow

class EditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        with open("notes.json", "r", encoding="UTF-8") as file:
            self.data = json.load(file)
        
        self.ui.listWidget.addItems(self.data)
            
        self.connects()
            
    def connects(self):
        self.ui.pushButton.clicked.connect(self.create_note)
        self.ui.pushButton_2.clicked.connect(self.delete_note)
        self.ui.pushButton_3.clicked.connect(self.save_note)
        self.ui.listWidget.itemClicked.connect(self.choose_note)

    def choose_note(self, item):
        note_name = item.text()
        self.ui.textEdit.setText(self.data[note_name]['text'])
        self.ui.listWidget_2.addItems(self.data[note_name]['tags'])

        
    def create_note(self):
        
        note_name, ok = QInputDialog.getText(
            window,
            "Створення замітки",
            "Введіть назву замітки: "
        )
        
        if not ok:
            return
        
        if note_name in self.data:
            return
        
        self.data[note_name] = {
            "text": "",
            "tags": []
        }
            
        self.ui.listWidget.addItem(note_name)
    
    def delete_note(self):
        
        note_selected = self.ui.listWidget.selectedItems()
        
        if note_selected:
            note_name = note_selected[0].text()
            
            del self.data[note_name]
            
            self.ui.listWidget.clear()
            self.ui.listWidget.addItems(self.data)
            with open ('notes_json', 'a', encoding='UTF=8') as file:
                self.data = json.load(self)
    def save_note(self):
        note_selected = self.ui.listWidget.selectedItems()
        if note_selected:
            note_name = note_selected[0].text()
            self.data[note_name]['text'] = self.ui.textEdit.toPlainText()
            with open ('notes_json', 'a', encoding='UTF=8') as file:
                self.data = json.load(self)
    def create_tag(self):
        note_selected = self.ui.listWidget.selectedItems()
        if note_selected:
            note_name = note_selected[0].text()
            tag_name = self.ui.lineEdit.text()
            self.data[note_name]['tags'].append(tag_name)
            self.ui.listWidget_2.addItem(tag_name)
    
    def delete_tag(self):
        note_selected = self.ui.listWidget.selectedItems()
        if note_selected:
            note_name = note_selected[0].text()
            tag_selected = self.ui.listWidget_2.selectedItems()
            if tag_selected:
                tag_name = tag_selected[0].text()
                self.data[note_name]['tags'].remove(tag_name)
                self.ui.listWidget_2.clear()
                self.ui.listWidget_2.addItems(self.data[note_name]['tags'])

    def find_by_tag(self):
        pass
        
app = QApplication([])
window = EditorWindow()

window.show()
app.exec()