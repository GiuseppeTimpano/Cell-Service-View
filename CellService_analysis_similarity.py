import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QRadioButton, QPushButton, QToolTip, QLabel, QVBoxLayout, QDesktopWidget, QStyleFactory)
from PyQt5.QtWidgets import (QFileDialog, QWidget, QMainWindow, QGroupBox, QAction, QMenu, QSystemTrayIcon, QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox)
from PyQt5.QtGui import QPixmap, QIcon, QFont, QImage
from PyQt5 import QtWidgets
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSlot
import skimage.io
import numpy as np
from skimage import filters

class CellServiceAnalysisSimilarity(QMainWindow):
    
    def __init__(self, parent):
        
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Analisys")
        self.StatBar = self.statusBar()
        self._createToolBarsAnalysis()
        self.setStyle(QStyleFactory.create('Cleanlooks'))
        self.initUI()
        
    def initUI(self):
        
        # create a widget and layout
        self.principalWidget = QtWidgets.QGroupBox(self)
        self.setCentralWidget(self.principalWidget)
        self.principalLayout = QtWidgets.QGridLayout()
        self.principalWidget.setLayout(self.principalLayout)

        # create a original label
        self.Label_Red = QtWidgets.QLabel(self)
        self.Label_Red.setStyleSheet("border: 3px solid red")
        self.principalLayout.addWidget(self.Label_Red, 0, 0)
        self.Label_Red.resize(128, 128)
        
        # create a filtred label
        self.Label_Green = QtWidgets.QLabel(self)
        self.Label_Green.setStyleSheet("border: 3px solid green")
        self.principalLayout.addWidget(self.Label_Green, 0, 1)
        self.Label_Green.resize(128, 128)
        
        self.Label_Blue = QtWidgets.QLabel(self)
        self.Label_Blue.setStyleSheet("border: 3px solid blue")
        self.principalLayout.addWidget(self.Label_Blue, 1, 0)
        self.Label_Blue.resize(128, 128)
        
        self.Label_Common = QtWidgets.QLabel(self)
        self.Label_Common.setStyleSheet("border: 3px solid black")
        self.principalLayout.addWidget(self.Label_Common, 1, 1)
        self.Label_Common.resize(128, 128)
        
        self.Label_Red.clear()
        self.Label_Red.setScaledContents(True)
        
        self.Label_Blue.clear()
        self.Label_Blue.setScaledContents(True)
        
        self.Label_Green.clear()
        self.Label_Green.setScaledContents(True)
        
        self.set_all_images()
        self.maximize_window()
    
    def maximize_window(self):
        
        screen = QDesktopWidget().screenGeometry()
        self.setFixedSize(int(screen.height()*1.), int(screen.height()*0.8))
    
    def _createToolBarsAnalysis(self):
        # Adding a widget to the Edit toolbar
        editToolBar = QtWidgets.QToolBar("Edit", self)
        
        editToolBar.setFixedSize(1000, 50)
        self.addToolBar(editToolBar)
        
        new_btn_ss = """QPushButton{background-color: cyan;
                                    border-style: outset;
                                    border-width: 2px;
                                    border-radius: 15px;
                                    border-color: cyan;
                                    font: bold 14px;
                                    min-width: 5em;
                                    padding: 6px;}
                        QPushButton:pressed {background-color: rgb(255, 255, 255);
                                             border-style: inset;}
                     """
                     
        self.red_blue_RadioButton = QRadioButton('RED-BLUE similarity')
        self.red_blue_RadioButton.setStyleSheet(new_btn_ss)
        editToolBar.addWidget(self.red_blue_RadioButton)
        editToolBar.addSeparator()
        
        self.blue_green_RadioButton = QRadioButton('BLUE-GREEN similarity')
        self.blue_green_RadioButton.setStyleSheet(new_btn_ss)
        editToolBar.addWidget(self.blue_green_RadioButton)
        editToolBar.addSeparator()
        
        self.red_green_RadioButton = QRadioButton('RED-GREEN similarity')
        self.red_green_RadioButton.setStyleSheet(new_btn_ss)
        editToolBar.addWidget(self.red_green_RadioButton)
        editToolBar.addSeparator()
        
        self.all_image_RadioButton = QRadioButton('TOTAL similarity')
        self.all_image_RadioButton.setStyleSheet(new_btn_ss)
        editToolBar.addWidget(self.all_image_RadioButton)
        editToolBar.addSeparator()
        
        self.Apply_Similarity = QPushButton('Apply similarity')
        self.Apply_Similarity.setStyleSheet(new_btn_ss)
        self.Apply_Similarity.clicked.connect(self.runSimilarity)
        editToolBar.addWidget(self.Apply_Similarity)
        editToolBar.addSeparator()
        
        self.Label_Similarity = QLabel('Scegli immagini')
        self.Label_Similarity.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
        editToolBar.addWidget(self.Label_Similarity)
    
    def set_all_images(self):
        self.parent.set_image(self.parent.red_image, self.Label_Red, "red", mask=False)
        self.parent.set_image(self.parent.green_image, self.Label_Green, "green", mask=False)
        self.parent.set_image(self.parent.blue_image, self.Label_Blue, "blue", mask=False)
        
    def two_similarity_overlap(self, image1, image2):
        similarity = 0
        overlapping = np.zeros_like(image1)
        
        for i in range(image1.shape[0]):
            for j in range(image1.shape[1]):
                if (image1[i][j]==image2[i][j]):
                    similarity += 1
                    overlapping[i][j]=1
        self.Label_Similarity.setText(str(round((similarity*100)/(self.parent.red_mask.shape[0]* self.parent.red_mask.shape[1]), 2))+ "%")
        return overlapping
    
    def runSimilarity(self):
        if self.red_blue_RadioButton.isChecked():
            self.parent.set_image(self.two_similarity_overlap(self.parent.red_mask, self.parent.blue_mask), self.Label_Common, "red", mask=True)
        elif self.red_green_RadioButton.isChecked():
            self.parent.set_image(self.two_similarity_overlap(self.parent.red_mask, self.parent.green_mask), self.Label_Common, "green", mask=True)
        elif self.blue_green_RadioButton.isChecked():
            self.parent.set_image(self.two_similarity_overlap(self.parent.blue_mask, self.parent.green_mask), self.Label_Common, "blue", mask=True)
        elif self.all_image_RadioButton.isChecked():
            self.parent.set_image(self.AllimagesOverlap(), self.Label_Common, "blue", mask=True)
        else:
            pass
        self.Label_Common.setScaledContents(True)
    
    def AllimagesOverlap(self):
        similarity=0
        overlapping = np.zeros_like(self.parent.red_mask)
        for i in range(self.parent.red_mask.shape[0]):
          for j in range(self.parent.red_mask.shape[1]):
              if (self.parent.red_mask[i][j]==1 and self.parent.green_mask[i][j]==1 
                  and self.parent.blue_mask[i][j]==1):
                          overlapping[i][j]=1
                          similarity+=1
                          
        self.parent.set_image(overlapping, self.Label_Common, "red", mask=True)
        self.Label_Common.setScaledContents(True)
        self.Label_Similarity.setText(str(round((similarity*100)/(self.parent.red_mask.shape[0]* self.parent.red_mask.shape[1]), 2))+ "%")
        
