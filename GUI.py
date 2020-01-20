import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from calculator import calcul
from calculator import change_x_to_num
from calculator import plot_2D
from calculator import plot_3D
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas 
from matplotlib.figure import Figure

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'title'
        self.left = 1500
        self.top = 700
        self.width = 1500
        self.height = 1000
        self.im_width = 550
        self.im_height = 550
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
        self.variable.resize(self.width/2 - 200, 30)

        # get equation
        self.e_label = QLabel(self)
        self.e_label.move(20, 90)
        self.e_label.resize(110, 30)
        self.e_label.setText('Equation')

        self.equation = QLineEdit(self)
        self.equation.move(20, 130)
        self.equation.resize(self.width/2 - 200, 30)

        # show equation
        self.a_label = QLabel(self)
        self.a_label.move(20, 170)
        self.a_label.resize(self.width, 30)

        # differential
        self.d_label = QLabel(self)
        self.d_label.move(20, 230)
        self.d_label.resize(self.width, 30)

        self.da_label = QLabel(self)
        self.da_label.move(50, 260)
        self.da_label.resize(self.width, 100)
        self.da_label.setAlignment(Qt.AlignTop)

        # Graph
        self.im_label = QLabel(self)
        self.im_label.move((self.width - self.im_width)/2, self.height/2 - 100)
        self.im_label.resize(self.im_width, self.im_height)
        
        # Button for equation
        self.button = QPushButton('click', self)
        self.button.move(self.width/2 - 150, 130)
        
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
        self.value.resize(self.width/2 - 200, 30)

        self.va_label = QLabel(self)
        self.va_label.move(int(self.width/2), 90)
        self.va_label.resize(310, 30)

        # Button for value
        self.button2 = QPushButton('click', self)
        self.button2.move(self.width - 150, 50)

        # connect button to function on_click
        self.button2.clicked.connect(self.on_click_value)
        self.show()
    
    def on_click_eq(self):
        temp = self.variable.text()
        self.eq = self.equation.text()

        self.var_list = []
        temp = temp.replace(" ", "")
        temp = temp.split(',')

        if temp[0] != '':
            for n in range(len(temp)):
                if temp[n] in ['e', 'pi']:
                    self.a_label.setText(temp[n] + ' is not available')
                    return 0
                self.var_list.append(temp[n])

        ans, diff, domain, in_domain = calcul(self.eq, self.var_list)
        # print(ans)

        self.a_label.setText('Equation is: ' + ans)
        self.d_label.setText('Differential')

        diff_ans = ''
        for n in range(len(diff)):
            diff_ans = diff_ans + 'Differentiated by ' + self.var_list[n] + ': ' + diff[n] + '\n'
            # print(diff[n])

        self.da_label.setText(diff_ans)

        if len(self.var_list) == 1 and self.eq[0:3] != 'sig':
            name = plot_2D(ans, domain, in_domain, self.var_list, [-50, 50], 0.1)
            pixmap = QPixmap(name).scaled(self.im_width, self.im_height)
            self.im_label.setPixmap(pixmap)

        elif len(self.var_list) == 2 and self.eq[0:3] != 'sig':
            name = plot_3D(ans, domain, in_domain, self.var_list, [-50, 50], [-50, 50], 1)
            pixmap = QPixmap(name).scaled(self.im_width, self.im_height)
            self.im_label.setPixmap(pixmap)

        return 0

    def on_click_value(self):
        if not self.variable.text():
            self.va_label.setText('Enter Equation')

            return 0
        
        val = self.value.text()
        ans = change_x_to_num(self.eq, self.var_list, val)

        self.va_label.setText(str(ans))

        return 0

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())