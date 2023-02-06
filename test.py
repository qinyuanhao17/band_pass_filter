import sys
import time
import PyQt5
import pyvisa
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget
from . import BandPassFilter

# rm = pyvisa.ResourceManager()
# rs = list(rm.list_resources())
# a = []
# for item in rs:
#     a.append(item)
# print(a)
#
# print(list(rs))
# print(list(rs)[0])
# print(type(list(rs)[0]))
# a=range(1,16,1)
# print(type(a))
# step_list = []
# a = 0
# for i in list(range(1, 16, 1)):
#     a = 0.007 * i
#     step_list.append(a)
# print(step_list)

for i in list(range(1, 16, 1)):
    a = 0.007 * i
    step_list.append(a)


stp_num = int(step_list.index(stp))+1
print(stp_num)

