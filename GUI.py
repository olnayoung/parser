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
from extra_funcs import diff
from extra_funcs import is_digit
from extra_funcs import from_list_to_str
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from extra_funcs import from_list_to_str
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Calculator'
        self.left = 1200
        self.top = 500
        self.width = 2000
        self.height = 1000
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # # get variable
        self.v_label = QLabel('Variable', self)
        self.v_label.move(20, 10)
    
        self.variable = QLineEdit(self)
        self.variable.move(20, 50)
        self.variable.resize(self.width/2 - 200, 30)

        # get equation
        self.e_label = QLabel('Equation', self)
        self.e_label.move(20, 90)
        self.e_label.resize(110, 30)

        self.equation = QLineEdit(self)
        self.equation.move(20, 130)
        self.equation.resize(self.width/2 - 200, 30)
        self.equation.returnPressed.connect(self.on_click_eq)

        # show equation
        self.a_label = QLabel(self)
        self.a_label.move(20, 170)
        self.a_label.resize(self.width, 120)
        self.a_label.setAlignment(Qt.AlignTop)
        self.a_label.setWordWrap(True)

        # differential
        self.d_label = QLabel(self)
        self.d_label.move(20, 610)
        self.d_label.resize(self.width, 30)

        self.da_label = QLabel(self)
        self.da_label.move(50, 640)
        self.da_label.resize(self.width, 230)
        self.da_label.setAlignment(Qt.AlignTop)
        self.da_label.setWordWrap(True)

        # domain
        self.domain_title_label = QLabel(self)
        self.domain_title_label.move(20, 330)
        self.domain_title_label.resize(400, 30)

        self.domain_label = QLabel(self)
        self.domain_label.move(50, 360)
        self.domain_label.resize(self.width/2, 200)
        self.domain_label.setAlignment(Qt.AlignTop)
        self.domain_label.setWordWrap(True)
        self.domain_label.setScaledContents(True)

        # Button for equation
        self.button = QPushButton('click', self)
        self.button.move(self.width/2 - 150, 130)
        self.button.clicked.connect(self.on_click_eq)

        # value
        self.value_label = QLabel('Values for variables', self)
        self.value_label.move(int(self.width/2), 10)
        self.value_label.resize(245, 30)

        self.va_label = QLabel(self)
        self.va_label.move(int(self.width/2) + 245, 10)
        self.va_label.resize(int(self.width/2), 30)

        self.value = QLineEdit(self)
        self.value.move(int(self.width/2), 50)
        self.value.resize(self.width/2 - 200, 30)
        self.value.returnPressed.connect(self.on_click_value)

        # Button for value
        self.button1 = QPushButton('click', self)
        self.button1.move(self.width - 150, 50)
        self.button1.clicked.connect(self.on_click_value)

        # Differentiable
        self.differentiable_label = QLabel('Differentiable', self)
        self.differentiable_label.move(int(self.width/2), 90)
        self.differentiable_label.resize(310, 30)

        self.differentiable = QLineEdit(self)
        self.differentiable.move(int(self.width/2), 130)
        self.differentiable.resize(self.width/2 - 200, 30)
        self.differentiable.returnPressed.connect(self.on_click_differentiable)

        self.dt_label = QLabel(self)
        self.dt_label.move(int(self.width/2), 170)
        self.dt_label.resize(int(self.width/2), 60)
        self.dt_label.setAlignment(Qt.AlignTop)

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
            self.da_label.setText('')
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

        self.var_list.sort()

        ans, self.domain, self.in_domain = calcul(self.eq, self.var_list)
        
        if ans == 'Error':
            self.a_label.setText('*Error* ' + self.domain.args[0])
            self.d_label.setText('')
            return 0
        
        if self.eq[0:3] == 'sig':
            self.eq = ans[0]
        
            self.diff = []
            for n in range(len(self.var_list)):
                differential = ans[1]
                if differential[0] == 'Error':
                    self.diff = 'Error' + differential[1].args[0]
                    break
                else:
                    self.diff.append(differential[0])
        else:
            self.eq = from_list_to_str('', ans)

            self.diff = []
            for n in range(len(self.var_list)):
                differential = diff(ans, self.var_list[n], self.var_list)
                if differential[0] == 'Error':
                    self.diff = 'Error' + differential[1].args[0]
                    break
                else:
                    self.diff.append(from_list_to_str('', differential[0]))

        self.a_label.setText('Equation is: ' + str(self.eq))
        self.d_label.setText('Differential')

        if not self.domain and not self.in_domain:
            str_domain = 'Domain: R'
            if len(self.var_list) > 1:
                str_domain = str_domain + '^' + str(len(self.var_list))
            self.domain_title_label.setText(str_domain)
        else:
            str_domain = ''

            for n in range(len(self.domain)):
                str_domain = str_domain + from_list_to_str('', self.domain[n]) + ' ≠ 0' + '\n'
            for n in range(len(self.in_domain)):
                str_domain = str_domain + from_list_to_str('', self.in_domain[n]) + ' ≥ 0' + '\n'
            self.domain_title_label.setText('Domain')
            self.domain_label.setText(str_domain)

        if not is_digit(self.eq):
            if len(self.var_list) < 3 and self.eq[0:3] != 'sig':
                self.open_new_dialog(self.eq, self.diff, self.domain, self.in_domain, self.var_list)

        if not self.diff:
            self.a_label.setText('Answer is: ' + str(self.eq))
            self.d_label.setText('')
            self.da_label.setText('')
            return 0
        
        diff_ans = ''
        if isinstance(self.diff, str):
            diff_ans = self.diff
        else:
            for n in range(len(self.diff)):
                diff_ans = diff_ans + 'Differentiated by ' + self.var_list[n] + ': ' + self.diff[n] + '\n'

        self.da_label.setText(diff_ans)

        return 0

    def on_click_value(self):
        if not self.variable.text() or not self.eq:
            self.va_label.setText(': Enter Equation')
            return 0

        if not self.value.text():
            self.va_label.setText(': Enter Value')
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
            if self.eq[0:3] == 'sig':
                self.dt_label.setText('It is sigma')

            elif len(self.var_list) == 1:
                differentiable = differentiable_1D(self.eq, self.diff, self.domain, self.in_domain, string, self.var_list)
                if differentiable == 1:
                    self.dt_label.setText('Differentiable at ' + string)
                elif differentiable == 0:
                    self.dt_label.setText('Non differentiable at ' + string)
                else:
                    self.dt_label.setText(differentiable)

            elif len(self.var_list) == 2:
                [dx, dy] = differentiable_2D(self.eq, self.diff, self.domain, self.in_domain, string, self.var_list)
                if dx == 1 and dy == 1:
                    self.dt_label.setText('Differentiable at ' + string)
                elif dx == 0 and dy == 0:
                    self.dt_label.setText('Non differentiable at ' + string)
                else:
                    self.dt_label.setText(dx + dy)

        return 0

    def open_new_dialog(self, eq, eq_diff, domain, in_domain, var_list):
        self.nd = NewWindow(eq, eq_diff, domain, in_domain, var_list)
        self.nd.show()

class NewWindow(QDialog):
    def __init__(self, eq, eq_diff, domain, in_domain, var_list, parent=None):
        super(NewWindow, self).__init__(parent)

        self.eq = eq
        self.eq_diff = eq_diff
        self.domain = domain
        self.in_domain = in_domain
        self.var_list = var_list

        self.ran_x = [-10, 10]
        self.ran_y = [-10, 10]
        self.n_interval = 100
        self.interval_x = (self.ran_x[1] - self.ran_x[0]) / self.n_interval
        self.interval_y = (self.ran_y[1] - self.ran_y[0]) / self.n_interval

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.plot()

        # set the layout
        self.layout = QGridLayout(self)
        self.setGeometry(1200, 500, 2000, 1000)
        self.layout.addWidget(self.toolbar, 0, 0)

        if len(self.var_list) == 1 or len(self.var_list) == 2:
            self.range_label = QLabel('Range   ', self)
            self.range_label.setFixedSize(110, 30)

            self.range_x_label = QLabel(self.var_list[0] + ':', self)
            self.range_x_label.setFixedSize(30, 30)

            self.x_value1 = QLineEdit(str(self.ran_x[0]), self)
            self.x_value1.setFixedSize(80, 30)

            self._label = QLabel(' ~ ', self)
            self._label.setFixedSize(40, 30)

            self.x_value2 = QLineEdit(str(self.ran_x[1]), self)
            self.x_value2.setFixedSize(80, 30)

            self.range = QHBoxLayout(self)
            self.range.addWidget(self.range_label, Qt.AlignLeft)
            self.range.setSpacing(0)
            self.range.addWidget(self.range_x_label, Qt.AlignLeft)
            self.range.setSpacing(0)
            self.range.addWidget(self.x_value1, Qt.AlignLeft)
            self.range.setSpacing(0)
            self.range.addWidget(self._label, Qt.AlignLeft)
            self.range.setSpacing(0)
            self.range.addWidget(self.x_value2, Qt.AlignLeft)

            if len(self.var_list) == 2:
                self.range_y_label = QLabel(', ' + self.var_list[1] + ' : ', self)
                self.range_y_label.setFixedSize(50, 30)

                self.y_value1 = QLineEdit(str(self.ran_y[0]), self)
                self.y_value1.setFixedSize(80, 30)

                self.y_label = QLabel(' ~ ', self)
                self.y_label.setFixedSize(40, 30)

                self.y_value2 = QLineEdit(str(self.ran_y[1]), self)
                self.y_value2.setFixedSize(80, 30)

                self.range.setSpacing(0)
                self.range.addWidget(self.range_y_label, Qt.AlignLeft)
                self.range.setSpacing(0)
                self.range.addWidget(self.y_value1, Qt.AlignLeft)
                self.range.setSpacing(0)
                self.range.addWidget(self.y_label, Qt.AlignLeft)
                self.range.setSpacing(0)
                self.range.addWidget(self.y_value2, Qt.AlignLeft)

            self.t_label = QLabel(self)
            self.t_label.setFixedSize(30, 30)
            self.range.addWidget(self.t_label, Qt.AlignLeft)

            self.range.setSpacing(100)
            self.button_range = QPushButton('click', self)
            self.button_range.setFixedSize(110, 30)
            self.button_range.clicked.connect(self.get_range)
            self.range.setSpacing(0)
            self.range.addWidget(self.button_range, Qt.AlignLeft)

            self.tt_label = QLabel(self)
            self.tt_label.setFixedSize(700, 30)
            self.range.addWidget(self.tt_label, Qt.AlignLeft)

            self.range.addStretch()
            self.layout.addLayout(self.range, 1, 0)

        self.layout.addWidget(self.canvas, 2, 0)
        self.setLayout(self.layout)

    def plot(self):
        self.figure.clear()
        
        if self.var_list:

            if len(self.var_list) == 1 and self.eq[0:3] != 'sig':
                self.ax = self.figure.add_subplot(121)
                self.ax.set_ylabel('f('+self.var_list[0]+')')
                self.plot_2D_graph(self.eq)

                self.ax = self.figure.add_subplot(122)
                self.ax.set_ylabel('df/d'+self.var_list[0])
                self.plot_2D_graph(self.eq_diff[0])

                plt.tight_layout()

            elif len(self.var_list) == 2 and self.eq[0:3] != 'sig':
                self.ax = self.figure.add_subplot(1,3,1, projection='3d')
                self.ax.set_zlabel('f('+self.var_list[0]+', '+self.var_list[1]+')')
                self.plot_3D_graph(self.eq)

                for m in range(2):
                    self.ax = self.figure.add_subplot(1,3,m+2, projection='3d')
                    self.ax.set_zlabel('df/d'+self.var_list[m])
                    self.plot_3D_graph(self.eq_diff[m])

                plt.tight_layout()

        self.canvas.draw()

    def get_range(self):
        if is_digit(self.x_value1.text()) and is_digit(self.x_value2.text()):
            self.ran_x[0] = float(self.x_value1.text())
            self.ran_x[1] = float(self.x_value2.text())
            self.interval_x = (self.ran_x[1] - self.ran_x[0]) / self.n_interval
        else:
            self.tt_label.setText('  Write ONLY digits')
            return 0
 
        if len(self.var_list) == 2:
            if is_digit(self.y_value1.text()) and is_digit(self.y_value2.text()):
                self.ran_y[0] = float(self.y_value1.text())
                self.ran_y[1] = float(self.y_value2.text())
                self.interval_y = (self.ran_y[1] - self.ran_y[0]) / self.n_interval
            else:
                self.tt_label.setText('  Write ONLY digits')
                return 0

        if self.ran_x[0] >= self.ran_x[1] or self.ran_y[0] >= self.ran_y[1]:
            self.tt_label.setText('  The Right value must be bigger than the Left value')
            return 0
        
        self.plot()

    def plot_2D_graph(self, equation):
        plt.grid()
        self.ax.set_xlabel(self.var_list[0])
        [ipt, opt] = plot_2D(equation, self.domain, self.in_domain, self.var_list, self.ran_x, self.interval_x)

        for n in range(len(ipt)):
            self.ax.plot(ipt[n], opt[n], 'b')

    def plot_3D_graph(self, equation):
        self.ax.set_xlabel(self.var_list[0])
        self.ax.set_ylabel(self.var_list[1])
        [ipt1, ipt2, opt] = plot_3D(equation, self.domain, self.in_domain, self.var_list, self.ran_x, self.ran_y, self.interval_x, self.interval_y)

        xi = np.linspace(min(ipt1), max(ipt1))
        yi = np.linspace(min(ipt2), max(ipt2))
        X, Y = np.meshgrid(xi, yi)
        Z = griddata((ipt1, ipt2), opt, (X,Y))
        self.ax.plot_surface(X, Y, Z, cmap = 'cool', vmin = np.nanmin(Z), vmax = np.nanmax(Z))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())