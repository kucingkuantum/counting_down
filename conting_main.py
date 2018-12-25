#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 13:48:45 2018

@author: siregar
"""

import sys
#from PyQt5.QtCore import *
#from PyQt5.QtGui import QFileDialog
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
from PyQt5.Qt import QMainWindow,qApp,  QTimer
from contingdown import Ui_MainWindow
from os.path import basename, dirname
#import function_spectra as fs
import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
import time
import os
import glob
import pyaudio  
import wave 
import ctypes

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self,parent=None):
        super(MyMainWindow, self).__init__(parent)
        qApp.installEventFilter(self)
        
        self.setupUi(self)
#        self.setFixedSize(self.size()) 
        self.label_3.hide()
        self.pushButton.clicked.connect(self.readone)
        self.show()
        
    
    def readone(self):
        self.label_3.hide()
        self.label.show()
        if (self.lineEditPresentation.text() =='' or self.lineEditQuestion.text() ==''):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Presentation or Question is empty")
            msg.setInformativeText("Please fill in only the number")
            msg.setWindowTitle("Warning")
            msg.setStandardButtons(QMessageBox.Ok )
            retval = msg.exec_()
        else:
            m = float(self.lineEditPresentation.text())
            t = int(m*60)
        
            self.counter = t
            mins, secs = divmod(t, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            self.lcdNumber.display(timeformat)
            self.timer = QTimer()
            
            self.timer.setInterval(1000)
            self.timer.timeout.connect(self.recurring_timer)
            self.timer.start()
            
                
              
    def recurring_timer(self):
        self.counter -=1
        mins, secs = divmod(self.counter, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        self.lcdNumber.display(timeformat)
        if (self.counter == -1):
            self.bell()
            self.lcdNumber.display('{:02d}:{:02d}'.format(0, 0))
#            self.timer.stop()
            
            self.bell()
            self.question()
        #time.sleep(1)
    def bell(self):
        chunk = 1024
        #open a wav format music  
        f = wave.open("service-bell_daniel_simion.wav","rb")  
        #instantiate PyAudio  
        p = pyaudio.PyAudio()  
        #open stream  
        stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                        channels = f.getnchannels(),  
                        rate = f.getframerate(),  
                        output = True)  
        #read data  
        data = f.readframes(chunk)  
        
        #play stream  
        while data:  
            stream.write(data)  
            data = f.readframes(chunk)  
        
        #stop stream  
        stream.stop_stream()  
        stream.close()  
        
        #close PyAudio  
        p.terminate()  

    def question(self):

        q = float(self.lineEditQuestion.text())
        t = int(q*60)
#        self.label.setText('Question')
#        self.label.setStyleSheet("*{color:black; font-size:90px}")
        self.label.hide()
        self.label_3.show()
        self.counter = t
        
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        self.lcdNumber.display(timeformat)
        self.timer = QTimer()
        
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer2)
        self.timer.start()
    
    def recurring_timer2(self):
        self.counter -=1
        mins, secs = divmod(self.counter, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        self.lcdNumber.display(timeformat)
        if (self.counter == -1):
            self.bell()
            self.lcdNumber.display('{:02d}:{:02d}'.format(0, 0))
#            self.timer.stop()
            self.bell()
            self.bell()
            self.timer.stop()


        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())

    