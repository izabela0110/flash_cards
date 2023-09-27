# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 20:18:51 2023

@author: izabe
"""

import pandas as pd
import random
import sys
from functools import partial

from PyQt5.QtCore import Qt
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

WINDOW_SIZE_W = 400
WINDOW_SIZE_H = 200
DISPLAY_HEIGHT = 35
BUTTON_SIZE_W = 100
BUTTON_SIZE_H = 30

def read_file(file_location):
    vocabulary = pd.read_excel(file_location)
    return vocabulary
    
def choose_word(vocabulary):
    vs = vocabulary.shape
    chosen_word_line = random.randint(1,vs[0]-1)
    chosen_word = vocabulary.iloc[chosen_word_line,0]
    print(chosen_word)
    return chosen_word

def show_answer(vocabulary, chosen_word):
    polish_words_list = vocabulary.iloc[:,0].to_list()
    chosen_word_index = polish_words_list.index(str(chosen_word))
    answer = vocabulary.iloc[chosen_word_index,1]
    print(answer)
    return answer

class PyFiszkiWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('FiszkiApp')
        self.setFixedSize(WINDOW_SIZE_W,WINDOW_SIZE_H)
        self.generalLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        self._createDisplay()
        self._createButtons()
        
    def _createDisplay(self):
        self.display = QLabel()
        self.display.setFixedHeight(DISPLAY_HEIGHT)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
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
        buttonsLayout.addWidget(self.buttonMap['Answer'],0,0)
        buttonsLayout.addWidget(self.buttonMap['Next Word'],0,1)
        self.generalLayout.addLayout(buttonsLayout)


class PyFiszki:
    
    def __init__(self,model1,model2,view,vocabulary):
        self._evaluate1 = model1
        self._evaluate2 = model2
        self._view = view
        self._connectSignalsAndSlots(vocabulary)

        
    def _connectSignalsAndSlots(self,vocabulary):
        self._view.buttonMap['Next Word'].clicked.connect(partial(choose_word,vocabulary))
        self._view.buttonMap['Answer'].clicked.connect(show_answer)
        
        
        
    
    
    
if __name__ == "__main__":
    vocabulary = read_file(r'C:\Users\izabe\Desktop\fiszki_greckie.xlsx')
    # chosen_word = choose_word(vocabulary)
    # show_answer(vocabulary, chosen_word)
    fiszkiApp = QApplication([])
    fiszkiWindow = PyFiszkiWindow()
    fiszkiWindow.show()
    PyFiszki(choose_word,show_answer,fiszkiWindow,vocabulary)
    sys.exit(fiszkiApp.exec())