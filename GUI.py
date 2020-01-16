import sys
from PyQt5.QtWidgets import *
# from PyQt5.QtGui import QIcon
# from PyQt5.QtCore import pyqtSlot
from calculator import calcul
from calculator import change_x_to_num

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'title'
        self.left = 1500
        self.top = 700
        self.width = 1000
        self.height = 1000
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # get variable
        self.v_label = QLabel(self)
        self.v_label.move(20, 10)
        self.v_label.setText('Variable')
    
        self.variable = QLineEdit(self)
        self.variable.move(20, 50)
        self.variable.resize(300, 30)

        # get equation
        self.e_label = QLabel(self)
        self.e_label.move(20, 90)
        self.e_label.resize(110, 30)
        self.e_label.setText('Equation')

        self.equation = QLineEdit(self)
        self.equation.move(20, 130)
        self.equation.resize(300, 30)

        # show equation
        self.a_label = QLabel(self)
        self.a_label.move(20, 170)
        self.a_label.resize(self.width, 30)

        # differential
        self.d_label = QLabel(self)
        self.d_label.move(20, 230)
        self.d_label.resize(self.width, 30)

        self.da_label = QLabel(self)
        self.da_label.move(50, 240)
        self.da_label.resize(self.width, 100)
        
        # Button for equation
        self.button = QPushButton('click', self)
        self.button.move(330, 130)
        
        # connect button to function on_click
        self.button.clicked.connect(self.on_click_eq)
        # self.show()

        # value
        self.value_label = QLabel(self)
        self.value_label.move(int(self.width/2), 10)
        self.value_label.resize(310, 30)
        self.value_label.setText('Values for variables')

        self.value = QLineEdit(self)
        self.value.move(int(self.width/2), 50)
        self.value.resize(300, 30)

        self.va_label = QLabel(self)
        self.va_label.move(int(self.width/2), 90)
        self.va_label.resize(310, 30)

        # Button for value
        self.button2 = QPushButton('click', self)
        self.button2.move(810, 50)

        # connect button to function on_click
        self.button2.clicked.connect(self.on_click_value)
        self.show()
    
    def on_click_eq(self):
        temp = self.variable.text()
        self.eq = self.equation.text()

        self.var_list = []
        temp = temp.split(',')

        if temp[0] != '':
            for n in range(len(temp)):
                var = temp[n].split(' ')
                if var[-1] in ['e', 'pi']:
                    self.a_label.setText(var[-1] + ' is not available')
                    return 0
                self.var_list.append(var[-1])

        ans, diff, domain, in_domain = calcul(self.eq, self.var_list)

        self.a_label.setText('Equation is: ' + ans)
        self.d_label.setText('Differential')

        diff_ans = ''
        for n in range(len(diff)):
            diff_ans = diff_ans + 'Differentiated by ' + self.var_list[n] + ': ' + diff[n] + '\n'

        self.da_label.setText(diff_ans)

        return 0

    def on_click_value(self):
        val = self.value.text()
        ans = change_x_to_num(self.eq, self.var_list, val)

        self.va_label.setText(ans)

        return 0

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())