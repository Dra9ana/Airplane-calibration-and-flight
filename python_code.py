from PyQt5.QtWidgets import QApplication, QPushButton, QLineEdit, QLabel, QWidget, QSizePolicy
import sys
import time
import serial
import numpy as np

from threading import Thread

import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure




com_port = "COM5"
baud_rate = 9600
ser = serial.Serial(com_port, baud_rate)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Zadatak 13.1.4'
        self.left = 200
        self.top = 200
        self.width = 500
        self.height = 400
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.name = QLineEdit('Operator''s name', self)
        self.name.resize(200, 50)
        self.name.move(10,10)

        self.surname = QLineEdit('Operator''s surname', self)
        self.surname.resize(200, 50)
        self.surname.move(250,10)

        self.calibration = QPushButton('Start of calibration', self)
        self.calibration.resize(200,50)
        self.calibration.move(10,70)
        self.calibration.clicked.connect(self.calibration_fcn)

        self.flight = QPushButton('Start of flight', self)
        self.flight.resize(200,50)
        self.flight.move(250,70)
        self.flight.clicked.connect(self.flight_fcn)


        self.stop = QPushButton('Stop', self)
        self.stop.resize(200,50)
        self.stop.move(250,140)
        self.stop.clicked.connect(self.stop_fcn)


        self.text_output = QLabel(' ', self)
        self.text_output.resize(100, 50)
        self.text_output.move(10,130)

        self.popups = []

        self.show()
    def calibration_fcn(self):

            window1=Calibration(self.name.text(), self.surname.text())
            window1.show();
            self.popups.append(window1)

    def flight_fcn(self):

            global state
            inChar='L'
            inChar1='\n'
            ser.write(inChar.encode())
            ser.write(inChar1.encode())
            state='F'
            t3=Thread(target=self.show_flight())
            t3.start();
    def show_flight(self):

            window2=MainWindow()
            window2.show();
            self.popups.append(window2)

    def stop_fcn(self):

            inChar='.';
            inChar1='\n'
            global end_program

            ser.write(inChar.encode())
            ser.write(inChar1.encode())
            ser.close()

            for i in self.popups:
                i.close()
            self.close()
            end_program=1;



class Calibration(QWidget):
    def __init__(self, name, surname):
        super().__init__()
        self.title = 'Calibration'
        self.left = 200
        self.top = 200
        self.width = 300
        self.height = 200
        self.initUI()
        self.name=name
        self.surname=surname


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)


        self.x = QPushButton('x', self)
        self.x.resize(70,50)
        self.x.move(10,20)
        self.x.clicked.connect(self.button_fcn_x)

        self.y = QPushButton('y', self)
        self.y.resize(70,50)
        self.y.move(10,80)
        self.y.clicked.connect(self.button_fcn_y)

        self.z = QPushButton('z', self)
        self.z.resize(70,50)
        self.z.move(10,140)
        self.z.clicked.connect(self.button_fcn_z)

        self.stop = QPushButton('Stop', self)
        self.stop.resize(200,50)
        self.stop.move(100,80)
        self.stop.clicked.connect(self.stop_fcn)

        self.text_output = QLabel(' ', self)
        self.text_output.resize(70, 50)
        self.text_output.move(10,130)




    def button_fcn_x(self):

            global state
            state='X'
            inChar='x'
            inChar1='\n'

            ser.write(inChar.encode())
            ser.write(inChar1.encode())




    def button_fcn_y(self):

            global state
            state='Y'
            poruka='y'
            inChar1='\n'

            ser.write(poruka.encode())
            ser.write(inChar1.encode())




    def button_fcn_z(self):
            mejl='z'
            global state
            state='Z'
            inChar1='\n'
            ser.write(mejl.encode())
            ser.write(inChar1.encode())


    def stop_fcn(self):

            global state
            state='W'
            global k
            global n;
            f = open("ispis.txt", "a")
            f.write('Name:\n')
            f.write(self.name +'\n')
            f.write('Surname:\n')
            f.write(self.surname +'\n')
            axis=['x','y','z']
            for i in range(0,3):
                         f.write(axis[i]+'paremeters are:\n')
                         f.write(str(k[i])+' '+str(n[i])+'\n');
            f.close()
            self.close()


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)



    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.stop = QPushButton('Stop', self)
        self.stop.resize(200,50)
        self.stop.move(800,80)
        self.stop.clicked.connect(self.stop_fcn)

    def stop_fcn(self):
            inChar='.'
            ser.write(inChar.encode())
            self.close()
class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.setCentralWidget(self.canvas)
        self.title = 'Flight'
        self.left = 150
        self.top = 150
        self.width = 1000
        self.height = 1000
        self.initUI()


        fs=1
        self.xdata = list(np.linspace(-10,10,100))
        self.ydata = list(np.linspace(-10,10,100))
        self.zdata = list(np.linspace(-10,10,100))
        self.tdata = np.arange(0, len(self.ydata)/fs, 1/fs)





        self.update_plot()

        self.show()

         #Setup a timer to trigger the redraw by calling update_plot.
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.stop = QPushButton('Stop', self)
        self.stop.resize(200,50)
        self.stop.move(800,80)
        self.stop.clicked.connect(self.stop_fcn)

    def stop_fcn(self):
            inChar='.'
            inChar1='\n'
            ser.write(inChar.encode())
            ser.write(inChar1.encode())
            self.timer.stop()
            self.close()



    def update_plot(self):
        # Drop off the first y element, append a new one.
            global x,y,z
            self.xdata = x
            self.ydata = y
            self.zdata = z
            self.canvas.axes.cla()  # Clear the canvas.
            self.canvas.axes.plot(self.tdata, self.xdata, 'r')
            self.canvas.axes.plot(self.tdata, self.ydata, 'g')
            self.canvas.axes.plot(self.tdata, self.zdata, 'b')
            # Trigger the canvas to update and redraw.
            self.canvas.draw()

def fun1():
     global end_program
     global count
     global state
     global k,n
     global x,y,z
     global exit_windows
     global id
     id=0
     end_program = 0;
     count=0;
     state=''
     k=[0,0,0]
     n=[0,0,0]
     x=list(np.linspace(-10,10,100))
     y=list(np.linspace(-10,10,100))
     z=list(np.linspace(-10,10,100))
     exit_windows=False
     data=0
     data_prev=0
     data_prev_prev=0

     while(True):
               if(end_program):
                   ser.close()
                   exit_windows=True;
                   break
               try:

                   data=ser.readline().decode()
                   data=float(data)
               except:
                   ser.close()
                   exit_windows=True
                   break

               if(state=='Y'):

                   if(count==0):
                      k[1]=data
                      count=1;
                   else:
                       count=0;
                       n[1]=data
               if(state=='X'):

                   if(count==0):
                      k[0]=data
                      count=1;
                   else:
                       count=0;
                       n[0]=data
               if(state=='Z'):

                   if(count==0):
                      k[2]=data
                      count=1;
                   else:
                       count=0;
                       n[2]=data


               if(state=='F'):

                      x = x[1:] + [float(data)]


                      y = y[1:] + [float(ser.readline().decode())]


                      z = z[1:] + [float(ser.readline().decode())]



def fun2():


    try:
          app = QApplication(sys.argv)
          ex = App()
          ex.show()
          app.exec_()
    except:
        for w in ex.popups:
            w.close();
        ex.close();

try:
    t1=Thread(target=fun1)
    t2=Thread(target=fun2)

    t1.start()
    t2.start()
except:
    t1.end()
    t2.end()
