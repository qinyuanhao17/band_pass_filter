import sys
import time
import PyQt5
import pyvisa
import serial
import qdarkstyle
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from . import BandPassFilter
import serial.tools.list_ports as lp

#rm = pyvisa.ResourceManager()
#rs = list(rm.list_resources())
step_list = []
a = 0
for i in list(range(1, 16, 1)):
    a = 0.007 * i
    step_list.append(str(a))

class MyWindow(BandPassFilter.Ui_Form,QWidget):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_ui()
        self.my_signal()

        rs = list(lp.comports())
        for item in rs:
            self.comboBox_1.addItem(str(item))
            self.comboBox_2.addItem(str(item))
        for item in step_list:
            self.step_cbx_1.addItem(str(item))
            self.step_cbx_2.addItem(str(item))

    def init_ui(self):
        self.setWindowTitle("Tunable Bandpass Filter")
        self.setWindowIcon(QIcon("window_icon.jpg"))
        self.resize(1200,500)
        self.set_lineEdit_1.setPlaceholderText("Input Wavelength(859.506~920.504,e.g. 900)")
        self.set_lineEdit_2.setPlaceholderText("Input Wavelength(859.506~920.504,e.g. 900)")

        self.set_lineEdit_1.setEnabled(False)
        self.set_lineEdit_2.setEnabled(False)

        self.read_btn_1.setEnabled(False)
        self.read_btn_2.setEnabled(False)

        self.set_lineEdit_1.setEnabled(False)
        self.set_lineEdit_2.setEnabled(False)

        self.inc_1.setEnabled(False)
        self.dec_1.setEnabled(False)
        self.inc_2.setEnabled(False)
        self.dec_2.setEnabled(False)

        self.step_cbx_1.setEnabled(False)
        self.step_cbx_2.setEnabled(False)

        self.plainTextEdit_1.setPlaceholderText('Choose COM ports named: \n "Silicon Labs CP210x USB to UART Bridge" \n'+'Then, press "Open" to activate all components')
        self.plainTextEdit_2.setPlainText('Choose COM ports named: \n "Silicon Labs CP210x USB to UART Bridge" \n'+'Then, press "Open" to activate all components')


    def my_signal(self):

        self.open_button_1.clicked.connect(self.open_ch1)
        self.open_button_2.clicked.connect(self.open_ch2)

        self.read_btn_1.clicked.connect(self.read_ch1)
        self.read_btn_2.clicked.connect(self.read_ch2)

        self.set_lineEdit_1.returnPressed.connect(self.set_ch1)
        self.set_lineEdit_2.returnPressed.connect(self.set_ch2)

        self.dec_1.clicked.connect(self.dec_ch1)
        self.dec_2.clicked.connect(self.dec_ch2)

        self.inc_1.clicked.connect(self.inc_ch1)
        self.inc_2.clicked.connect(self.inc_ch2)

    def open_ch1(self):

        self.set_lineEdit_1.setEnabled(True)
        self.set_lineEdit_2.setEnabled(True)

        self.read_btn_1.setEnabled(True)
        self.read_btn_2.setEnabled(True)

        self.set_lineEdit_1.setEnabled(True)
        self.set_lineEdit_2.setEnabled(True)

        self.inc_1.setEnabled(True)
        self.dec_1.setEnabled(True)

        self.step_cbx_1.setEnabled(True)

        longComeName = self.comboBox_1.currentText()
        n = longComeName.index("-")
        openComName = self.comboBox_1.currentText()[0:n-1]

        ser1 = serial.Serial()
        ser1.port = openComName
        ser1.baudrate = 115200
        ser1.open()

        if ser1.isOpen() == True:
            command = 'DEV?' + '\r\n'
            ser1.write(command.encode())

            devInfo = ser1.readline().decode()
            wlrange = ser1.readline().decode()
            systatus = ser1.readline().decode()

            self.plainTextEdit_1.setPlainText(devInfo + wlrange + systatus)

    def open_ch2(self):

        self.set_lineEdit_2.setEnabled(True)

        self.read_btn_2.setEnabled(True)

        self.wave_lineEdit_2.setEnabled(True)

        self.inc_2.setEnabled(True)
        self.dec_2.setEnabled(True)

        self.step_cbx_2.setEnabled(True)
        longComeName = self.comboBox_2.currentText()
        n = longComeName.index("-")
        openComName = self.comboBox_2.currentText()[0:n]

        ser2 = serial.Serial()
        ser2.port = openComName
        ser2.baudrate = 115200
        ser2.open()

        if ser2.isOpen() == True:
            command = 'DEV?' + '\r\n'
            ser2.write(command.encode())

            devInfo = ser2.readline().decode()
            wlrange = ser2.readline().decode()
            systatus = ser2.readline().decode()

            self.plainTextEdit_2.setPlainText(devInfo + wlrange + systatus)

    def read_ch1(self):
        command = "WL?" + '\r\n'
        portName1 = self.get_portname1()
        ser1 = serial.Serial(port=portName1, baudrate=115200)
        ser1.write(command.encode())

        cur_wl = ser1.readline().decode()
        num = cur_wl.index(":")
        self.wave_lineEdit_1.setText(cur_wl)
        self.plainTextEdit_1.setPlainText(cur_wl)

    def get_portname1(self):
        longPortName = self.comboBox_1.currentText()
        a = longPortName.index('-')
        portName = self.comboBox_1.currentText()[0:a-1]
        return portName

    def get_portname2(self):
        longPortName = self.comboBox_2.currentText()
        a = longPortName.index('-')
        portName = self.comboBox_2.currentText()[0:a-1]
        return portName


    def read_ch2(self):
        command = "WL?" + '\r\n'
        portName = self.get_portname2()
        ser2 = serial.Serial(port=portName, baudrate=115200)
        ser2.write(command.encode())

        cur_wl = ser2.readline().decode()
        self.wave_lineEdit_2.setText(cur_wl)

    def set_ch1(self):
        command = "WL" + self.set_lineEdit_1.text() + '\r\n'
        portName = self.get_portname1()
        ser1 = serial.Serial(port=portName, baudrate=115200)
        ser1.write(command.encode())
        cur_wl = ser1.readline().decode()
        self.plainTextEdit_1.setPlainText(cur_wl)

        # command = "WL?" + '\r\n'
        # ser1.write(command.encode())
        # cur_wl = ser1.readline().decode()
        # num = cur_wl.index(":")
        # self.wave_lineEdit_1.setText(cur_wl[num + 1:])


    def set_ch2(self):
        command = "WL" + self.set_lineEdit_2.text() + '\r\n'
        portName = self.get_portname2()
        ser2 = serial.Serial(port=portName, baudrate=115200)
        ser2.write(command.encode())
        cur_wl = ser2.readline().decode()
        self.plainTextEdit_2.setPlainText(cur_wl)

        # command = "WL?" + '\r\n'
        # ser2.write(command.encode())
        # cur_wl = ser2.readline().decode()
        # num = cur_wl.index(":")
        # self.wave_lineEdit_2.setText(cur_wl[num + 1:])

    def dec_ch1(self):
        stp = self.step_cbx_1.currentText()
        stp_num = step_list.index(stp)+1

        command1 = "SF" + '%d'%(stp_num) + '\r\n'
        portName = self.get_portname1()
        ser1 = serial.Serial(port=portName, baudrate=115200)
        ser1.write(command1.encode())
        #
        command2 = "WL?" + '\r\n'
        ser1.write(command2.encode())
        a=ser1.readline().decode()
        b=ser1.readline().decode()
        cur_wl = ser1.readline().decode()
        num=cur_wl.index(':')
        # self.plainTextEdit_1.setPlainText(a+b+cur_wl)
        self.plainTextEdit_1.setPlainText("Wavelength decreased to: " + cur_wl[num+1:] +'Please press "Read" to check')
    def inc_ch1(self):
        stp = self.step_cbx_1.currentText()
        stp_num = step_list.index(stp) + 1
        command = "SB" + '%d'%(stp_num) + '\r\n'
        portName = self.get_portname1()
        ser1 = serial.Serial(port=portName, baudrate=115200)
        ser1.write(command.encode())

        command2 = "WL?" + '\r\n'
        ser1.write(command2.encode())
        ser1.readline().decode()
        ser1.readline().decode()
        cur_wl = ser1.readline().decode()
        num = cur_wl.index(':')

        self.plainTextEdit_1.setPlainText("Wavelength decreased to: " + cur_wl[num + 1:] + 'Please press "Read" to check')

    def dec_ch2(self):
        stp = self.step_cbx_2.currentText()
        stp_num = step_list.index(stp) + 1

        command1 = "SF" + '%d' % (stp_num) + '\r\n'
        portName = self.get_portname2()
        ser1 = serial.Serial(port=portName, baudrate=115200)
        ser1.write(command1.encode())
        #
        command2 = "WL?" + '\r\n'
        ser1.write(command2.encode())
        ser1.readline().decode()
        ser1.readline().decode()
        cur_wl = ser1.readline().decode()
        num = cur_wl.index(':')

        self.plainTextEdit_2.setPlainText("Wavelength decreased to: " + cur_wl[num + 1:] + 'Please press "Read" to check')

    def inc_ch2(self):
        stp = self.step_cbx_2.currentText()
        stp_num = step_list.index(stp) + 1
        command = "SB" + '%d' % (stp_num) + '\r\n'
        portName = self.get_portname2()
        ser2 = serial.Serial(port=portName, baudrate=115200)
        ser2.write(command.encode())

        command2 = "WL?" + '\r\n'
        ser2.write(command2.encode())
        ser2.readline().decode()
        ser2.readline().decode()
        cur_wl = ser2.readline().decode()
        num = cur_wl.index(':')

        self.plainTextEdit_2.setPlainText("Wavelength decreased to: " + cur_wl[num + 1:] + 'Please press "Read" to check')

    def closeEvent(self, event):
        reply = QMessageBox.question(self, u'Quit', u'Shut down the setup?', QMessageBox.Yes, QMessageBox.No)
        # QtWidgets.QMessageBox.question(self,u'弹窗名',u'弹窗内容',选项1,选项2)
        if reply == QMessageBox.Yes:
            event.accept()  # 关闭窗口
        else:
            event.ignore()  # 忽视点击X事件

if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = MyWindow()
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    w.show()
    app.exec()