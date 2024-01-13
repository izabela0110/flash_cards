# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 20:18:51 2023

@author: izabe
"""

import pandas as pd
import random
import sys
from functools import partial

from PyQt5.QtCore import Qt,QSize
from PyQt5.QtWidgets import ( 
    QApplication,
    QGridLayout,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
    )
from PyQt5.QtGui import QImage, QPalette, QBrush, QFont

WINDOW_SIZE_W = 350
WINDOW_SIZE_H = 200
DISPLAY_HEIGHT = 48
BUTTON_SIZE_W = 100
BUTTON_SIZE_H = 30

class Vocabulary:
    
    def __init__(self, file_location):
        self.file_location = file_location
        self.read_file()
        self.chosen_word = None
        
    def read_file(self):
        self.vocabulary = pd.read_excel(self.file_location)
        
    
    def choose_word(self):
        vs = self.vocabulary.shape
        chosen_word_line = random.randint(1,vs[0]-1)
        self.chosen_word = self.vocabulary.iloc[chosen_word_line,0]
        

    def show_answer(self):
        polish_words_list = self.vocabulary.iloc[:,0].to_list()
        chosen_word_index = polish_words_list.index(self.chosen_word)
        self.answer = self.vocabulary.iloc[chosen_word_index,1]


class PyFiszkiWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Greek Flash Cards')
        self.setFixedSize(WINDOW_SIZE_W,WINDOW_SIZE_H)
        oImage = QImage("C:\Iza\Rodos 2023\IMG_20230902_191550.jpg")
        sImage = oImage.scaled(QSize(WINDOW_SIZE_W,WINDOW_SIZE_H)) 
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))                        
        self.setPalette(palette) 
        # self.setStyleSheet("background-color: #40E0D0;")
        self.generalLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        self._createDisplay()
        self._createButtons()
        
    def _createDisplay(self):
        self.display = QLabel('Welcome to Greek Flash Cards App:) Click \'Next Word\' to start')
        self.display.setFixedHeight(DISPLAY_HEIGHT)
        self.display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.display.setFont(QFont('Arial', 12))
        self.display.setWordWrap(True)
        # self.display.setReadOnly(True)
        self.generalLayout.addWidget(self.display)
        
    def setDisplayText(self,text):
        self.display.setText(text)
        self.display.setFocus()
        
    def displayText(self):
        return self.display.text()
    
    def clearDisplay(self):
        self.setDisplayText('')
        
    def _createButtons(self):
        buttonsLayout = QGridLayout()
        self.buttonMap = {'Answer':QPushButton('Answer'),
                          'Next Word':QPushButton('Next Word')}
        for key,value in self.buttonMap.items():
            self.buttonMap[key].setFixedSize(BUTTON_SIZE_W,BUTTON_SIZE_H)
            self.buttonMap[key].setStyleSheet("background-color: #00CED1;")
        buttonsLayout.addWidget(self.buttonMap['Answer'],0,0)
        buttonsLayout.addWidget(self.buttonMap['Next Word'],0,1)
        self.generalLayout.addLayout(buttonsLayout)


class PyFiszki:
    
    def __init__(self,model,view):
        self._evaluate = model
        self._view = view
        self._connectSignalsAndSlots()
        
    def _updateLabelsChosenWord(self):
        self._view.setDisplayText(self._evaluate.chosen_word)
        
    def _updateLabelsAnswer(self):
        self._view.setDisplayText(self._evaluate.answer)
                
    def _connectSignalsAndSlots(self):
        self._view.buttonMap['Next Word'].clicked.connect(self._evaluate.choose_word)
        self._view.buttonMap['Next Word'].clicked.connect(self._updateLabelsChosenWord)
        self._view.buttonMap['Answer'].clicked.connect(self._evaluate.show_answer)
        self._view.buttonMap['Answer'].clicked.connect(self._updateLabelsAnswer)
        
    
if __name__ == "__main__":
    vocab = Vocabulary(r'C:\Users\izabe\Desktop\fiszki_greckie.xlsx')
    fiszkiApp = QApplication([])
    fiszkiWindow = PyFiszkiWindow()
    fiszkiWindow.show()
    pyfiszki = PyFiszki(vocab,fiszkiWindow)
    sys.exit(fiszkiApp.exec())
    