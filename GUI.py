import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from calculator import calcul
from calculator import change_x_to_num
from calculator import plot_2D
from calculator import plot_3D
from calculator import differentiable_1D
from calculator import differentiable_2D
from calculator import check_domain
from extra_funcs import is_digit
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from extra_funcs import from_list_to_str
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy.interpolate import griddata
from mpl_toolkits.mplot3d import Axes3D

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

        # domain
        self.domain_title_label = QLabel(self)
        self.domain_title_label.move(int(self.width/2) + 100, 230)
        self.domain_title_label.resize(400, 30)

        self.domain_label = QLabel(self)
        self.domain_label.move(int(self.width/2) + 130, 260)
        self.domain_label.resize(400, 100)
        self.domain_label.setAlignment(Qt.AlignTop)

        # Button for equation
        self.button = QPushButton('click', self)
        self.button.move(self.width/2 - 150, 130)
        self.button.clicked.connect(self.on_click_eq)

        # value
        self.value_label = QLabel(self)
        self.value_label.move(int(self.width/2), 10)
        self.value_label.resize(245, 30)
        self.value_label.setText('Values for variables')

        self.va_label = QLabel(self)
        self.va_label.move(int(self.width/2) + 245, 10)
        self.va_label.resize(300, 30)

        self.value = QLineEdit(self)
        self.value.move(int(self.width/2), 50)
        self.value.resize(self.width/2 - 200, 30)

        # Button for value
        self.button2 = QPushButton('click', self)
        self.button2.move(self.width - 150, 50)
        self.button2.clicked.connect(self.on_click_value)

        # Differentiable
        self.differentiable_label = QLabel(self)
        self.differentiable_label.move(int(self.width/2), 90)
        self.differentiable_label.resize(310, 30)
        self.differentiable_label.setText('Differentiable')

        self.differentiable = QLineEdit(self)
        self.differentiable.move(int(self.width/2), 130)
        self.differentiable.resize(self.width/2 - 200, 30)

        self.dt_label = QLabel(self)
        self.dt_label.move(int(self.width/2), 170)
        self.dt_label.resize(600, 30)

        # Button for Differentiable
        self.button2 = QPushButton('click', self)
        self.button2.move(self.width - 150, 130)
        self.button2.clicked.connect(self.on_click_differentiable)

        self.show()
    
    def on_click_eq(self):
        temp = self.variable.text()
        self.eq = self.equation.text()
        self.domain_title_label.setText('')
        self.domain_label.setText('')
        self.dt_label.setText('')

        if not self.eq:
            self.a_label.setText('Enter Equation')
            self.d_label.setText('')
            return 0

        self.var_list = []
        temp = temp.replace(" ", "")
        temp = temp.split(',')

        if temp[0] != '':
            for n in range(len(temp)):
                if temp[n] in ['e', 'pi']:
                    self.a_label.setText(temp[n] + ' is not available')
                    return 0
                self.var_list.append(temp[n])

        ans, self.diff, self.domain, self.in_domain = calcul(self.eq, self.var_list)
        
        if ans == 'Error':
            self.a_label.setText('*Error* ' + self.diff.args[0])
            self.d_label.setText('')
            return 0

        self.a_label.setText('Equation is: ' + str(ans))
        self.d_label.setText('Differential')

        if not self.domain and not self.in_domain:
            str_domain = 'Domain: R'
            if len(self.var_list) == 2:
                str_domain += '^2'
            self.domain_title_label.setText(str_domain)
        else:
            str_domain = ''

            for n in range(len(self.domain)):
                str_domain = str_domain + from_list_to_str('', self.domain[n]) + ' ≠ 0' + '\n'
            for n in range(len(self.in_domain)):
                str_domain = str_domain + from_list_to_str('', self.in_domain[n]) + ' > 0' + '\n'
            self.domain_title_label.setText('Domain')
            self.domain_label.setText(str_domain)

        if self.var_list:
            self.open_new_dialog(self.eq, self.diff, ans, self.domain, self.in_domain, self.var_list)

        if not self.diff:
            self.a_label.setText('Answer is: ' + str(ans))
            self.d_label.setText('')
            return 0
        
        diff_ans = ''
        for n in range(len(self.diff)):
            diff_ans = diff_ans + 'Differentiated by ' + self.var_list[n] + ': ' + self.diff[n] + '\n'

        self.da_label.setText(diff_ans)

        return 0

    def on_click_value(self):
        if not self.variable.text():
            self.va_label.setText('Enter Equation')
            return 0

        if not self.value.text():
            self.va_label.setText('Enter Value')
            return 0
        
        val = self.value.text()
        ans = change_x_to_num(self.eq, self.var_list, val)

        self.va_label.setText(': ' + str(ans))

        return 0

    def on_click_differentiable(self):
        if not self.variable.text():
            self.dt_label.setText('Enter Equation')
            return 0

        if not self.differentiable:
            self.dt_label.setText('Enter Value')
            return 0

        string = self.differentiable.text()

        if self.var_list:
            if len(self.var_list) == 1 and self.eq[0:3] != 'sig':
                if differentiable_1D(self.eq, self.diff, self.domain, self.in_domain, string):
                    self.dt_label.setText('Differentiable at ' + string)
                else:
                    self.dt_label.setText('Non differentiable at ' + string)

            elif len(self.var_list) == 2 and self.eq[0:3] != 'sig':
                [dx, dy] =  differentiable_2D(self.eq, self.diff, self.domain, self.in_domain, string)
                if dx and dy:
                    self.dt_label.setText('Differentiable at direction of ' + self.var_list[0] + ' and ' + self.var_list[1] + ' at ' + string)
                elif dx and not dy:
                    self.dt_label.setText('Differentiable at direction of ' + self.var_list[0] + ' \n Non differentiable at direction of ' + self.var_list[1] + 'at ' + string)
                elif not dx and dy:
                    self.dt_label.setText('Differentiable at direction of ' + self.var_list[1] + ' \n Non differentiable at direction of ' + self.var_list[2] + 'at ' + string)
                else:
                    self.dt_label.setText('Non differentiable at direction of ' + self.var_list[0] + ' and ' + self.var_list[1] + ' at ' + string)
        return 0

    def open_new_dialog(self, eq, eq_diff, ans, domain, in_domain, var_list):
        self.nd = NewWindow(eq, eq_diff, ans, domain, in_domain, var_list)
        self.nd.show()

class NewWindow(QDialog):
    def __init__(self, eq, eq_diff, ans, domain, in_domain, var_list, parent=None):
        super(NewWindow, self).__init__(parent)

        self.eq = eq
        self.eq_diff = eq_diff
        self.ans = ans
        self.domain = domain
        self.in_domain = in_domain
        self.var_list = var_list

        self.figure = plt.figure()

        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.plot()

        # set the layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

        self.setGeometry(1500, 700, 2000, 1000)

    def plot(self):
        self.figure.clear()
        
        if self.var_list:
            ran = [-5, 5]
            interval = 0.1

            if len(self.var_list) == 1 and self.eq[0:3] != 'sig':
                ax = self.figure.add_subplot(121)
                plt.grid()
                [ipts, opts] = plot_2D(self.eq, self.domain, self.in_domain, self.var_list, ran, interval)

                for n in range(len(ipts)):
                    ax.plot(ipts[n], opts[n], 'b')
                plt.axis('equal')
                
                ax = self.figure.add_subplot(122)
                plt.grid()
                [ipts, opts] = plot_2D(self.eq_diff[0], self.domain, self.in_domain, self.var_list, ran, interval)

                for n in range(len(ipts)):
                    ax.plot(ipts[n], opts[n], 'b')
                plt.axis('equal')

                plt.tight_layout()

            elif len(self.var_list) == 2 and self.eq[0:3] != 'sig':
                # self.figure, axs = plt.subplots(2, 2)
                # ax = Axes3D(self.figure)
                ax = self.figure.add_subplot(1,3,1, projection='3d')
                [ipt1, ipt2, opt] = plot_3D(self.eq, self.domain, self.in_domain, self.var_list, ran, ran, interval)

                xi = np.linspace(min(ipt1), max(ipt1))
                yi = np.linspace(min(ipt2), max(ipt2))
                X, Y = np.meshgrid(xi, yi)
                Z = griddata((ipt1, ipt2), opt, (X,Y), method='linear')
                ax.contour3D(xi, yi, Z, 50)

                for m in range(2):
                    ax = self.figure.add_subplot(1,3,m+2, projection='3d')
                    [ipt1, ipt2, opt] = plot_3D(self.eq_diff[m], self.domain, self.in_domain, self.var_list, ran, ran, interval)

                    xi = np.linspace(min(ipt1), max(ipt1))
                    yi = np.linspace(min(ipt2), max(ipt2))
                    X, Y = np.meshgrid(xi, yi)
                    Z = griddata((ipt1, ipt2), opt, (X,Y), method='linear')
                    ax.contour3D(xi, yi, Z, 50)
                plt.tight_layout()

        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())