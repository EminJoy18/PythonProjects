import sys
import PyQt6
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import psycopg2   # to query postgres database

# con = psycopg2.connect(
#     database="student_management",
#     user="postgres",
#     password="postgres",
#     host="localhost",
#     port='5432'
# )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Student Management System")
        self.resize(500, 400)

        # to add menu bar
        file_menu_item = self.menuBar().addMenu('&File')
        edit_menu_item = self.menuBar().addMenu('&Edit')
        help_menu_item = self.menuBar().addMenu('&Help')
        # adding sub-items
        add_students_action = QAction(QIcon('./add.png'), 'Add Student', self)
        add_students_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_students_action)

        search_action = QAction(QIcon('./search.png'), 'Search', self)
        search_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.triggered.connect(self.about)

        # Adding a toolbar and adding elements
        toolbar = QToolBar()
        toolbar.setMovable(True)
        toolbar.addAction(add_students_action)
        toolbar.addAction(search_action)
        self.addToolBar(toolbar)

        # Adding a status bar and elements
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # setting up a table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(('Id', 'Name', 'Course', 'Mobile'))

        # to hide the row number
        self.table.verticalHeader().setVisible(False)

        self.setCentralWidget(self.table)  # this is the main line of code to explicitly make the table visible
        # whenever we use QMainWindow we need to specify a central widget

        # to read the database
        self.read_db()

        # Detecting a cell click
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_action = QPushButton('Edit Record')
        edit_action.clicked.connect(self.edit)

        delete_action = QPushButton('Delete Record')
        delete_action.clicked.connect(self.delete)

        # in order to restrain these buttons from being added to the status bar everytime
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_action)
        self.statusbar.addWidget(delete_action)

    @staticmethod
    def edit(self):
        edit = EditDialog()
        edit.exec()

    @staticmethod
    def delete(self):
        delete = DeleteDialog()
        delete.exec()

    def about(self):
        messagebox = QMessageBox()
        messagebox.setWindowTitle("About")
        messagebox.setText("A Graphical User Interface build for managing student data")
        messagebox.exec()

    def read_db(self):
        # creating a cursor object
        con = psycopg2.connect(
            database="student_management",
            user="postgres",
            password="postgres",
            host="localhost",
            port='5432'
        )
        cursor_obj = con.cursor()
        cursor_obj.execute("SELECT * FROM students")
        result = cursor_obj.fetchall()
        self.table.setRowCount(0)  # so that it begins from zero every time

        for row_num, row_data in enumerate(result):
            self.table.insertRow(row_num)
            for column_num, data in enumerate(row_data):
                self.table.setItem(row_num, column_num, QTableWidgetItem(str(data)))

        con.commit()
        cursor_obj.close()
        con.close()

    @staticmethod
    def insert():
        dialog = InsertDialog()
        dialog.exec()

    @staticmethod
    def search():
        dialog = SearchDialog()
        dialog.exec()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Edit Record")

        index = window.table.currentRow()
        self.iddd = window.table.item(index, 0).text()
        self.ee_student_name = window.table.item(index, 1).text()
        self.c = window.table.item(index, 2).text()
        self.ph = window.table.item(index, 3).text()

        lay = QVBoxLayout()
        self.ename = QLineEdit()
        self.ename.setText(self.ee_student_name)

        self.ecourse = QComboBox()
        course = ['Select a course', 'Maths', 'Physics', 'Chemistry']
        self.ecourse.addItems(course)
        self.ecourse.setCurrentText(self.c)

        self.ephone = QLineEdit()
        self.ephone.setText(self.ph)

        edit = QPushButton('Edit')
        edit.clicked.connect(self.edit_op)

        lay.addWidget(self.ename)
        lay.addWidget(self.ecourse)
        lay.addWidget(self.ephone)
        lay.addWidget(edit)
        self.setLayout(lay)

    def edit_op(self):
        con = psycopg2.connect(
            database="student_management",
            user="postgres",
            password="postgres",
            host="localhost",
            port='5432'
        )
        cursor_obj = con.cursor()
        update_query = """UPDATE students SET name = %s, course = %s, phone = %s WHERE id = %s"""
        record_to_insert = (self.ename.text(), self.ecourse.currentText(), self.ephone.text(), self.iddd)
        cursor_obj.execute(update_query, record_to_insert)
        con.commit()
        cursor_obj.close()
        con.close()

        window.read_db()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Record")
        lay = QGridLayout()

        self.yes = QPushButton("Yes")
        self.yes.clicked.connect(self.delete)
        self.no = QPushButton("No")
        # self.no.clicked.connect(DeleteDialog.close(self))

        lay.addWidget(QLabel("Are you sure you want to delete?"), 0, 0, 1, 2)
        lay.addWidget(self.yes, 2, 0)
        lay.addWidget(self.no, 2, 1)
        self.iddd = window.table.item(window.table.currentRow(), 0).text()
        print(self.iddd)

        self.setLayout(lay)

    def delete(self):
        con = psycopg2.connect(
            database="student_management",
            user="postgres",
            password="postgres",
            host="localhost",
            port='5432'
        )
        cursor_obj = con.cursor()
        delete_query = """DELETE FROM students WHERE id = %s"""
        record_to_insert = (self.iddd, )
        cursor_obj.execute(delete_query, record_to_insert)
        con.commit()
        cursor_obj.close()
        con.close()

        window.read_db()

        self.close()

        messagebox = QMessageBox()
        messagebox.setWindowTitle("Success")
        messagebox.setText("The record was deleted successfully")
        messagebox.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Student Record")
        form = QFormLayout()

        self.name_ip = QLineEdit()
        self.name_ip.setPlaceholderText("Name")

        self.course_ip = QComboBox()
        course = ['Select a course', 'Maths', 'Physics', 'Chemistry']
        self.course_ip.addItems(course)
        self.course_ip.setPlaceholderText("Course")

        self.phone_ip = QLineEdit()
        self.phone_ip.setPlaceholderText("Phone")
        self.add = QPushButton("Add")
        self.add.clicked.connect(self.add_record)

        form.addRow(self.name_ip)
        form.addRow(self.course_ip)
        form.addRow(self.phone_ip)
        form.addRow(self.add)

        self.setLayout(form)

    def add_record(self):
        name = self.name_ip.text()
        course = self.course_ip.itemText(self.course_ip.currentIndex())
        phone = self.phone_ip.text()

        # if name != '' and course != 'Select a course' and phone != '':
        con = psycopg2.connect(
            database="student_management",
            user="postgres",
            password="postgres",
            host="localhost",
            port='5432'
        )
        cursor_obj = con.cursor()
        insert_query = """INSERT INTO students (name,course,phone) VALUES (%s, %s, %s)"""
        record_to_insert = (name, course, phone)
        cursor_obj.execute(insert_query, record_to_insert)
        con.commit()
        cursor_obj.close()
        con.close()

        window.read_db()

        self.name_ip.clear()
        self.course_ip.clear()
        self.phone_ip.clear()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student")
        lay = QVBoxLayout()

        self.name = QLineEdit()
        self.name.setPlaceholderText("Search name")
        search = QPushButton("Search")
        search.clicked.connect(self.s)

        lay.addWidget(self.name)
        lay.addWidget(search)

        self.setLayout(lay)

    def s(self):
        con = psycopg2.connect(
            database="student_management",
            user="postgres",
            password="postgres",
            host="localhost",
            port='5432'
        )
        cursor_obj = con.cursor()
        search_query = """SELECT * FROM students WHERE name = %s"""
        record_to_search = (self.name.text(), )
        cursor_obj.execute(search_query, record_to_search)
        records = cursor_obj.fetchall()

        items = window.table.findItems(self.name.text(), Qt.MatchFlag.MatchFixedString)
        for item in items:
            window.table.item(item.row(), 1).setSelected(True)

        con.commit()
        cursor_obj.close()
        con.close()


app = QApplication([])
window = MainWindow()
window.show()
sys.exit(app.exec())
