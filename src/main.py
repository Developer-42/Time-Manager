from functools import partial
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
import calendar
import sys
import os
import ntpath
import ast
import pprint


days_de   = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
months_de = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]

days   = days_de
months = months_de


class Data:
    def __init__(self):
        self.today = datetime.today()
        self.weekday = self.today.weekday() # monday = 0, sunday = 6
        self.load_save()

    def load_save(self):
        global tmp_dict
        if "save.txt" in os.listdir():
            with open("save.txt", "r") as file:
                file_str = file.read()
                tmp_dict = dict(ast.literal_eval(file_str))
        else:
            tmp_dict = {}
            with open("save.txt", "w") as file:
                pprint.pprint(tmp_dict, file)
                print("save.txt created")

    def save_days(self, dict_):
        global tmp_dict
        with open("save.txt", "w") as file:
            pprint.pprint(dict_, file)

    def return_day_info(self):
        return [self.today, self.weekday]

    def return_calendar_info(self, year = None, month = None):
        if year is None: year = self.today.year
        if month is None: month = self.today.month
        calendar_days_list = [[], [], []] # previous, current and next month days
        first_day_of_month = date(year, month, 1)
        previous_month = first_day_of_month - relativedelta(months = 1)
        previous_month_days = calendar.monthrange(previous_month.year, previous_month.month)[1]
        next_month = first_day_of_month + relativedelta(months = 1)
        cal_start = previous_month_days - first_day_of_month.weekday()
        chosen_month_days = calendar.monthrange(first_day_of_month.year, first_day_of_month.month)[1]
        for x in range(0, first_day_of_month.weekday()):
            calendar_days_list[0].append(cal_start + x + 1)
        for x in range(1, chosen_month_days + 1):
            calendar_days_list[1].append(x)
        for x in range(1, 7 - next_month.weekday() + 1):
            calendar_days_list[2].append(x)
        return [calendar_days_list, (previous_month.year, previous_month.month), (next_month.year, next_month.month)]


class Cal_Button(QPushButton):
    def __init__(self, text, option, notes_av):
        QPushButton.__init__(self)
        self.setText(text)
        font = QFont()
        font.setPointSize(11)
        self.setFont(font)
        if option == 1:
            if notes_av is True:
                self.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 255, 0)")
            else:
                self.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(128, 128, 128)")
        if option == 2:
            if notes_av == 2:
                self.setStyleSheet("background-color: rgb(0, 255, 0); color: rgb(0, 0, 0)")
            elif notes_av == 1:
                self.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 255, 0)")
            else:
                self.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)")


class MainWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.setWindowTitle("Time Manager")
        self.layout = QVBoxLayout()
        self.hbox = QHBoxLayout()

        self.left_vbox = QVBoxLayout()
        self.left_vbox.setAlignment(Qt.AlignTop)
        self.left_title_year = QLabel()
        self.left_title_year.setAlignment(Qt.AlignCenter)
        self.left_title_year.setFont(QFont("Times", 18, QFont.Bold))
        self.left_title_hbox = QHBoxLayout()
        self.left_title_hbox.setAlignment(Qt.AlignCenter)
        self.left_title_hbox.setSpacing(50)
        self.left_arrow_button1 = QToolButton()
        self.left_arrow_button1.setFixedSize(50, 25)
        self.left_arrow_button1.setIcon(QIcon("arrow1.png"))
        self.left_arrow_button1.setIconSize(QSize(18, 18))
        self.left_title_month = QLabel()
        self.left_title_month.setAlignment(Qt.AlignCenter)
        self.left_title_month.setFont(QFont("Times", 15))
        self.left_title_month.setFixedWidth(100)
        self.left_arrow_button2 = QToolButton()
        self.left_arrow_button2.setFixedSize(50, 25)
        self.left_arrow_button2.setIcon(QIcon("arrow2.png"))
        self.left_arrow_button2.setIconSize(QSize(18, 18))
        self.calendar_vbox = QVBoxLayout()

        self.line = QFrame()
        self.line.setFrameShape(QFrame.VLine)

        self.right_vbox = QVBoxLayout()
        self.right_vbox.setAlignment(Qt.AlignTop)
        self.right_title = QLabel()
        self.right_title.setAlignment(Qt.AlignCenter)
        self.right_title.setFont(QFont("Times", 25, QFont.Bold))
        self.right_textbox = QTextEdit()

        #-----------------------------------------------------------------------

        self.setLayout(self.layout)
        self.layout.addLayout(self.hbox)

        self.hbox.addLayout(self.left_vbox)
        self.left_vbox.addWidget(self.left_title_year)
        self.left_vbox.addLayout(self.left_title_hbox)
        self.left_title_hbox.addWidget(self.left_arrow_button1)
        self.left_title_hbox.addWidget(self.left_title_month)
        self.left_title_hbox.addWidget(self.left_arrow_button2)
        self.left_vbox.addLayout(self.calendar_vbox)

        self.hbox.addWidget(self.line)

        self.hbox.addLayout(self.right_vbox)
        self.right_vbox.addWidget(self.right_title)
        self.right_vbox.addWidget(self.right_textbox)

        #-----------------------------------------------------------------------

        self.day_info = data.return_day_info()
        self.month = self.day_info[0].month - 1
        self.left_title_month.setText(months[self.month])
        self.year = self.day_info[0].year
        self.left_title_year.setText(str(self.year))
        self.change_selected_day(self.day_info[0].day, save = False)

        self.left_arrow_button1.clicked.connect(partial(self.previous_month, 1))
        self.left_arrow_button2.clicked.connect(partial(self.next_month, 1))

    def create_calendar(self, day, year = None, month = None):
        global tmp_dict
        calendar_labels = []
        for x in range(0, len(days)):
            label_obj = QLabel(days[x])
            label_obj.setAlignment(Qt.AlignCenter)
            calendar_labels.append(label_obj)

        ## Create buttons
        calendar_info = data.return_calendar_info(year, month)
        calendar_days, calendar_previous_month, calendar_next_month = calendar_info
        calendar_buttons = [[],[],[]]
        for x in calendar_days[0]:
            if calendar_previous_month + (x, ) in tmp_dict:
                calendar_buttons[0].append(Cal_Button(str(x), 1, True))
            else:
                calendar_buttons[0].append(Cal_Button(str(x), 1, False))
            button_index = calendar_buttons[0].index(calendar_buttons[0][-1])
            calendar_buttons[0][button_index].clicked.connect(partial(self.previous_month, x))

        for x in calendar_days[1]:
            if x == day:
                calendar_buttons[1].append(Cal_Button(str(x), 2, 2))
            elif (year, month, x) in tmp_dict:
                calendar_buttons[1].append(Cal_Button(str(x), 2, 1))
            else:
                calendar_buttons[1].append(Cal_Button(str(x), 2, 0))
            button_index = calendar_buttons[1].index(calendar_buttons[1][-1])
            calendar_buttons[1][button_index].clicked.connect(partial(self.change_selected_day, x))

        for x in calendar_days[2]:
            if calendar_next_month + (x, ) in tmp_dict:
                calendar_buttons[2].append(Cal_Button(str(x), 1, True))
            else:
                calendar_buttons[2].append(Cal_Button(str(x), 1, False))
            button_index = calendar_buttons[2].index(calendar_buttons[2][-1])
            calendar_buttons[2][button_index].clicked.connect(partial(self.next_month, x))

        ## Create grid
        try:
            self.grid_widget.deleteLater()
        except (NameError, AttributeError): pass
        self.grid_widget = QWidget()
        self.calendar_vbox.addWidget(self.grid_widget)
        self.grid = QGridLayout()
        self.grid_widget.setLayout(self.grid)
        self.grid.setAlignment(Qt.AlignCenter)  # !!!!
        for x in range(0, len(calendar_labels)):
            self.grid.addWidget(calendar_labels[x], 1, x)
        grid_add_index = 0
        row_counter = 3
        for list_ in calendar_buttons:
            for y in list_:
                if grid_add_index == 7:
                    row_counter = row_counter + 1
                    grid_add_index = 0
                self.grid.addWidget(y, row_counter, grid_add_index)
                grid_add_index = grid_add_index + 1

    def previous_month(self, select_day = 1):
        old_month = self.month
        old_year  = self.year
        self.month -= 1
        if self.month < 0:
            self.month = 11
            self.year -= 1
        self.left_title_year.setText(str(self.year))
        self.left_title_month.setText(str(months[self.month]))
        self.change_selected_day(select_day, month_year_delta = (old_year, old_month + 1))

    def next_month(self, select_day = 1):
        old_month = self.month
        old_year  = self.year
        self.month += 1
        if self.month > 11:
            self.month = 0
            self.year += 1
        self.left_title_year.setText(str(self.year))
        self.left_title_month.setText(str(months[self.month]))
        self.change_selected_day(select_day, month_year_delta = (old_year, old_month + 1))

    def change_selected_day(self, day, save = True, month_year_delta = None):
        if save is True:
            if month_year_delta is None:
                self.old_date = (self.year, self.month + 1, self.new_date[2])
                self.save_day(self.old_date)
            else:
                self.old_date = month_year_delta + (self.new_date[2], )
                self.save_day(self.old_date)
        self.create_calendar(day, self.year, self.month + 1)
        self.new_date = (self.year, self.month + 1, day)
        self.right_title.setText("{}. {} {}".format(day, months[self.month], self.year))
        try: self.right_textbox.setPlainText(tmp_dict[self.new_date])
        except: self.right_textbox.setPlainText("")

    def save_day(self, date):
        global tmp_dict
        tmp_dict[date] = self.right_textbox.toPlainText()
        if tmp_dict[date].replace(" ", "") == "":
            del tmp_dict[date]

    def closeEvent(self, event):
        quit_msg = "Do you want to save the changes?"
        reply = QMessageBox.question(self, "Save?", quit_msg, QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            self.save_day(self.new_date) # saves last selected day
            data.save_days(tmp_dict)
            event.accept()
        elif reply == QMessageBox.No:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    # Change working directory to the dir of the python script
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    data = Data()
    app = QApplication(sys.argv)
    widget = MainWidget()
    widget.show()
    app.exec_()
