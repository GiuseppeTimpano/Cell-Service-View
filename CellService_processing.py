import sys
from PyQt5.QtWidgets import (QSlider, QDockWidget, QApplication, QWidget, QRadioButton, QPushButton, QToolTip, QLabel, QVBoxLayout, QDesktopWidget, QStyleFactory)
from PyQt5.QtWidgets import (QCheckBox, QBoxLayout,QFileDialog, QWidget, QMainWindow, QGroupBox, QAction, QMenu, QSystemTrayIcon, QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox)
from PyQt5.QtGui import QPixmap, QIcon, QFont, QImage
from PyQt5 import QtWidgets
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSlot
import skimage.io
import skimage.morphology
import numpy as np
from skimage import filters,morphology


class CellServiceBinaryProcessing(QMainWindow):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("CellService")
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.centralwidget.setLayout(self.gridLayout)
        
        init_size = 128
        
        self.radioRed = QtWidgets.QRadioButton(self.centralwidget)
        self.radioRed.setAutoRepeatDelay(100)
        self.radioRed.setText("Red Image")
        self.gridLayout.addWidget(self.radioRed, 0, 0)
        self.radioGreen = QtWidgets.QRadioButton(self.centralwidget)
        self.radioGreen.setAutoRepeatDelay(100)
        self.radioGreen.setText("Green image")
        self.gridLayout.addWidget(self.radioGreen, 0, 1)
        self.radioBlue = QtWidgets.QRadioButton(self.centralwidget)
        self.radioBlue.setText("Blue Image")
        self.gridLayout.addWidget(self.radioBlue, 0, 2)
        
        self.Original_Label = QtWidgets.QLabel(self.centralwidget)
        self.Original_Label.setStyleSheet("border: 3px solid red;")
        self.Original_Label.resize(init_size, init_size)
        self.Original_Label.setScaledContents(True)
        self.gridLayout.addWidget(self.Original_Label, 2, 0)  
        self.Binary_Label = QtWidgets.QLabel(self.centralwidget)
        self.Binary_Label.setScaledContents(True)
        self.Binary_Label.setStyleSheet("border: 3px solid red;")
        self.Binary_Label.resize(init_size, init_size) 
        self.gridLayout.addWidget(self.Binary_Label, 3, 0)
        self.Filtred_Label= QtWidgets.QLabel(self.centralwidget)
        self.Filtred_Label.setScaledContents(True)
        self.Filtred_Label.setStyleSheet("border: 3px solid red;")
        self.Filtred_Label.resize(init_size, init_size)      
        self.gridLayout.addWidget(self.Filtred_Label, 5, 0)
        
        self.Original_Label1 = QtWidgets.QLabel(self.centralwidget)
        self.gridLayout.addWidget(self.Original_Label1, 2, 1)
        self.Original_Label1.setScaledContents(True)
        self.Original_Label1.setStyleSheet("border: 3px solid green;")
        self.Original_Label1.resize(init_size, init_size)
        self.Binary_Label1 = QtWidgets.QLabel(self.centralwidget)
        self.Binary_Label1.setScaledContents(True)
        self.Binary_Label1.setStyleSheet("border: 3px solid green;")
        self.gridLayout.addWidget(self.Binary_Label1, 3, 1)
        self.Filtred_Label1 = QtWidgets.QLabel(self.centralwidget)
        self.Filtred_Label1.setStyleSheet("border: 3px solid green;")
        self.gridLayout.addWidget(self.Filtred_Label1, 5, 1)
        self.Filtred_Label1.resize(init_size, init_size)
        self.Filtred_Label1.setScaledContents(True)
        
        self.Original_Label2 = QtWidgets.QLabel(self.centralwidget)
        self.Original_Label2.setStyleSheet("border: 3px solid blue;")
        self.Original_Label2.setScaledContents(True)
        self.Original_Label2.setMouseTracking(True)
        self.Original_Label2.resize(init_size, init_size)
        self.gridLayout.addWidget(self.Original_Label2, 2, 2)
        self.Binary_Label2 = QtWidgets.QLabel(self.centralwidget)
        self.Binary_Label2.setScaledContents(True)
        self.Binary_Label2.setStyleSheet("border: 3px solid blue;")
        self.Binary_Label2.resize(init_size, init_size)
        self.gridLayout.addWidget(self.Binary_Label2, 3, 2)
        self.Filtred_Label2 = QtWidgets.QLabel(self.centralwidget)        
        self.Filtred_Label2.setStyleSheet("border: 3px solid blue;")
        self.Filtred_Label2.resize(init_size, init_size)
        self.gridLayout.addWidget(self.Filtred_Label2, 5, 2)
        self.Filtred_Label2.setScaledContents(True)
        
        
        self.Selected = QtWidgets.QTabWidget()
        
        self.new_btn_ss5 = """QPushButton{background-color: turquoise;
                                    border-style: outset;
                                    border-width: 2px;
                                    border-radius: 15px;
                                    border-color: turquoise;
                                    font: bold 14px;
                                    min-width: 10em;
                                    padding: 6px;}
                        QPushButton:pressed {background-color: rgb(255, 255, 255);
                                             border-style: inset;}
                     """
        self.new_btn = """QPushButton{background-color: turquoise;
                                    border-style: outset;
                                    border-width: 2px;
                                    border-radius: 15px;
                                    border-color: turquoise;
                                    font: bold 14px;
                                    min-width: 5em;
                                    padding: 6px;}
                        QPushButton:pressed {background-color: rgb(255, 255, 255);
                                             border-style: inset;}
                     """
                     
        self.Binarize = QtWidgets.QWidget()
        self.Selected.addTab(self.Binarize, "Binarize")
        self.fontSizeSpinBox = QtWidgets.QDoubleSpinBox(self.Binarize)
        self.fontSizeSpinBox.setGeometry(QtCore.QRect(10, 10, 81, 31))
        self.fontSizeSpinBox.setDecimals(3)
        self.fontSizeSpinBox.setMaximum(255.0)
        self.fontSizeSpinBox2 = QtWidgets.QDoubleSpinBox(self.Binarize)
        self.fontSizeSpinBox2.setGeometry(QtCore.QRect(10, 50, 81, 31))
        self.fontSizeSpinBox2.setDecimals(3)
        self.fontSizeSpinBox2.setMaximum(255.0)
        self.min = QtWidgets.QLabel(self.Binarize)
        self.min.setGeometry(QtCore.QRect(104, 15, 91, 16))
        self.min.setText("min Threashold")
        self.max = QtWidgets.QLabel(self.Binarize)
        self.max.setText("max Threashold")
        self.max.setGeometry(QtCore.QRect(100, 60, 91, 16))
        self.AutomaticButton = QtWidgets.QPushButton(self.Binarize)
        self.AutomaticButton.setGeometry(QtCore.QRect(80, 90, 141, 41))
        self.AutomaticButton.setText("Automatic_Threashold")
        self.AutomaticButton.setStyleSheet(self.new_btn_ss5)
        self.AutomaticButton.clicked.connect(self.Automatic_threshold)
        self.Apply = QtWidgets.QPushButton(self.Binarize)
        self.Apply.setGeometry(QtCore.QRect(90, 140, 121, 41))
        self.Apply.setText("Apply")
        
        self.Apply.setStyleSheet(self.new_btn_ss5)
        self.Apply.clicked.connect(self.runIntensityBinarization)
        
        self.Segmentation = QtWidgets.QWidget()
        self.Selected.addTab(self.Segmentation, "Segmentation")
        self.Raggio = QtWidgets.QSpinBox(self.Segmentation)
        self.Raggio.setGeometry(QtCore.QRect(21, 11, 71, 31))
        self.RaggioLabel = QtWidgets.QLabel(self.Segmentation)
        self.RaggioLabel.setText("Raggio")
        self.RaggioLabel.setGeometry(QtCore.QRect(104, 15, 81, 21))
        self.removeCheck = QtWidgets.QCheckBox(self.Segmentation)
        self.removeCheck.setGeometry(QtCore.QRect(20, 60, 151, 21))
        self.removeCheck.setText("Remove small object")
        self.erosionCheck = QtWidgets.QCheckBox(self.Segmentation)
        self.erosionCheck.setGeometry(QtCore.QRect(20, 90, 101, 21))
        self.erosionCheck.setText("Erosion")
        self.dilationCheck = QtWidgets.QCheckBox(self.Segmentation)
        self.dilationCheck.setGeometry(QtCore.QRect(140, 90, 81, 20))
        self.dilationCheck.setText("Dilation")
        self.openCheck = QtWidgets.QCheckBox(self.Segmentation)
        self.openCheck.setGeometry(QtCore.QRect(20, 120, 81, 20))
        self.openCheck.setText("Opening")
        self.noiseCheck = QtWidgets.QCheckBox(self.Segmentation)
        self.noiseCheck.setGeometry(QtCore.QRect(140, 120, 81, 20))
        self.noiseCheck.setText("Closing")
        
        self.pushButton = QtWidgets.QPushButton(self.Segmentation)
        self.pushButton.setGeometry(QtCore.QRect(30, 160, 101, 31))
        self.pushButton.setText("Apply")
        self.pushButton.setStyleSheet(self.new_btn)
        self.pushButton.clicked.connect(self.apply_segmentation)
        self.pushButton_2 = QtWidgets.QPushButton(self.Segmentation)
        self.pushButton_2.setGeometry(QtCore.QRect(160, 160, 101, 31))
        self.pushButton_2.setText("Save")
        self.pushButton_2.setStyleSheet(self.new_btn)
        self.pushButton_2.clicked.connect(self.save)
        self.Label_Save=QLabel(self.Segmentation)
        self.Label_Save.setText("Don't forget to save")
        self.Label_Save.setGeometry(QtCore.QRect(90, 180, 200, 70))
        
        self.set_all_images()
        
        self.gridLayout_2.addLayout(self.gridLayout, 0, 1)
        self.gridLayout_2.addWidget(self.Selected, 0, 2)
        self.maximize_window()
        self.show()
        
    def maximize_window(self):
        screen = QDesktopWidget().screenGeometry()
        self.setFixedSize(int(screen.height()*1.2), int(screen.height()*0.9))
    
    def set_all_images(self):
        self.parent.set_image(self.parent.red_image, self.Original_Label, "red", mask=False)
        self.parent.set_image(self.parent.green_image, self.Original_Label1, "green", mask=False)
        self.parent.set_image(self.parent.blue_image, self.Original_Label2, "blue", mask=False)
    
    def runIntensityBinarization(self):
        if self.radioRed.isChecked():
            self.parent.red_mask = self.binarizeImage(self.parent.red_image)
            self.parent.set_image(self.parent.red_mask, self.Binary_Label, "red", mask=True)
        elif self.radioGreen.isChecked():
            self.parent.green_mask = self.binarizeImage(self.parent.green_image)
            self.parent.set_image(self.parent.green_mask, self.Binary_Label1, "green", mask=True)
        elif self.radioBlue.isChecked():
            self.parent.blue_mask = self.binarizeImage(self.parent.blue_image)
            self.parent.set_image(self.parent.blue_mask, self.Binary_Label2, "blue", mask=True)
        else:
            pass
    
    def Automatic_threshold(self):
        self.soglia1=0
        if self.radioRed.isChecked():
            self.soglia1 = filters.threshold_otsu(self.parent.red_image)
        elif self.radioGreen.isChecked():
            self.soglia1 = filters.threshold_otsu(self.parent.green_image)
        elif self.radioBlue.isChecked():
            self.soglia1 = filters.threshold_otsu(self.parent.blue_image)
        else:
            pass
        self.fontSizeSpinBox.setValue(self.soglia1)
    
    def binarizeImage(self,img):
        valore1 = self.fontSizeSpinBox.value()
        valore2 =self.fontSizeSpinBox2.value()
        binarymat = np.zeros_like(img, dtype=np.uint8)
        if (valore1==0):
            valore1=filters.threshold_otsu(img)
        if (valore2!=0):
            mask=np.logical_and(img > valore1, img < valore2)
            binarymat[mask]=1
        if (valore2==0):
            mask=img>valore1
            binarymat[mask]=1
        return binarymat
    
    def apply_segmentation(self):
        self.mask_red=None
        self.mask_green=None
        self.mask_blue=None
        entry=False
        if self.removeCheck.isChecked() or self.erosionCheck.isChecked() or self.noiseCheck.isChecked() or self.openCheck.isChecked or self.dilationCheck.isChecked():
            entry=True
        if entry:
            if self.radioRed.isChecked():
                if self.erosionCheck.isChecked():
                    self.mask_red=morphology.erosion(self.parent.red_mask)
                if self.dilationCheck.isChecked():
                    if(self.mask_red is not None):
                        self.mask_red=morphology.dilation(self.mask_red)
                    else:
                        self.mask_red=morphology.dilation(self.parent.red_mask)
                if self.noiseCheck.isChecked():
                    if(self.mask_red is not None):
                        self.mask_red=morphology.binary_closing(self.mask_red)
                    else:
                        self.mask_red=morphology.binary_closing(self.parent.red_mask)
                if self.openCheck.isChecked():
                    if(self.mask_red is not None):
                        self.mask_red=morphology.binary_opening(self.mask_red)
                    else:
                        self.mask_red=morphology.binary_opening(self.parent.red_mask)
                if self.removeCheck.isChecked():
                    raggio=self.Raggio.value()
                    if(self.mask_red is not None):
                        self.mask_red= morphology.remove_small_objects(self.mask_red.astype(np.bool), raggio)
                    else:
                        self.mask_red= morphology.remove_small_objects(self.parent.red_mask.astype(np.bool), raggio)
                self.parent.set_image(self.mask_red, self.Filtred_Label, "red", mask=True)
            if self.radioGreen.isChecked():
                if self.erosionCheck.isChecked():
                    self.mask_green=morphology.erosion(self.parent.green_mask)
                if self.dilationCheck.isChecked():
                    if(self.mask_green is not None):
                        self.mask_green=morphology.dilation(self.mask_green)
                    else:
                        self.mask_green=morphology.dilation(self.parent.green_mask)
                if self.noiseCheck.isChecked():
                    if(self.mask_green is not None):
                        self.mask_green=morphology.binary_closing(self.mask_green)
                    else:
                        self.mask_green=morphology.binary_closing(self.parent.green_mask)
                if self.openCheck.isChecked():
                    if(self.mask_green is not None):
                        self.mask_green=morphology.binary_opening(self.mask_green)
                    else:
                        self.mask_green=morphology.binary_opening(self.parent.green_mask)
                if self.removeCheck.isChecked():
                    raggio=self.Raggio.value()
                    if(self.mask_green is not None):
                        self.mask_green= morphology.remove_small_objects(self.mask_green.astype(np.bool), raggio)
                    else:
                        self.mask_green= morphology.remove_small_objects(self.parent.green_mask.astype(np.bool), raggio)
                self.parent.set_image(self.mask_green, self.Filtred_Label1, "green", mask=True)
            if self.radioBlue.isChecked():
                if self.noiseCheck.isChecked():
                        self.mask_blue=morphology.binary_closing(self.parent.blue_mask)
                if self.dilationCheck.isChecked():
                    if(self.mask_blue is not None):
                        self.mask_blue=morphology.dilation(self.mask_blue)
                    else:
                        self.mask_blue=morphology.dilation(self.parent.blue_mask)
                if self.openCheck.isChecked():
                    if(self.mask_blue is not None):
                        self.mask_blue=morphology.binary_opening(self.mask_blue)
                    else:
                        self.mask_blue=morphology.binary_opening(self.parent.blue_mask)
                if self.erosionCheck.isChecked():
                    if(self.mask_blue is not None):
                        self.mask_blue=morphology.erosion(self.mask_blue)
                    else:
                        self.mask_blue=morphology.erosion(self.parent.blue_mask)
                if self.removeCheck.isChecked():
                    raggio=self.Raggio.value()
                    if(self.mask_blue is not None):
                        self.mask_blue= morphology.remove_small_objects(self.mask_blue.astype(np.bool), raggio)
                    else:
                        self.mask_blue= morphology.remove_small_objects(self.parent.blue_mask.astype(np.bool), raggio)
                self.parent.set_image(self.mask_blue, self.Filtred_Label2, "blue", mask=True)
        else:
            self.parent.set_image(self.parent.red_mask, self.Filtred_Label, "red", mask=True)
            self.parent.set_image(self.parent.green_mask, self.Filtred_Label1, "green", mask=True)
            self.parent.set_image(self.parent.blue_mask, self.Filtred_Label2, "blue", mask=True)
        entry=False
    
    def save(self):
        self.parent.red_mask = self.mask_red
        self.parent.green_mask = self.mask_green
        self.parent.blue_mask = self.mask_blue
        self.Label_Save.setText("SAVED IMAGES")
        
        
#PER GIUSEPPE: LE MASCHERE SI CHIAMANO self.parent.colore_mask
#              MENTRE LE IMMAGINI IN FORMATO NP SONO self.parent.colore_image


