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

class CellServiceBinaryProcessing(QMainWindow):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Binary processing")
        
        self._createToolBars()
        self.StatBar = self.statusBar()
        self.init_ui()

    def init_ui(self):
        self.StatBar = self.statusBar()
        
        self.setStyle(QStyleFactory.create('Cleanlooks'))
        self.principalWidget = QtWidgets.QGroupBox(self)
        self.setCentralWidget(self.principalWidget)
        self.principalLayout = QtWidgets.QGridLayout()
        self.principalWidget.setLayout(self.principalLayout)

        # create a original label
        self.Original_Label = QtWidgets.QLabel(self)
        self.Original_Label.setStyleSheet("border: 3px solid red")
        self.principalLayout.addWidget(self.Original_Label, 0, 0)
        self.Original_Label.resize(128, 128)
        
        # create a filtred label
        self.Filtred_Label = QtWidgets.QLabel(self)
        self.Filtred_Label.setStyleSheet("border: 3px solid red")
        self.principalLayout.addWidget(self.Filtred_Label, 1, 0)
        self.Filtred_Label.resize(128, 128)
        
        self.Original_Label1 = QtWidgets.QLabel(self)
        self.Original_Label1.setStyleSheet("border: 3px solid green")
        self.principalLayout.addWidget(self.Original_Label1, 0, 1)
        self.Original_Label1.resize(128, 128)
        
        self.Filtred_Label1 = QtWidgets.QLabel(self)
        self.Filtred_Label1.setStyleSheet("border: 3px solid green")
        self.principalLayout.addWidget(self.Filtred_Label1, 1, 1)
        self.Filtred_Label1.resize(128, 128)
        
        self.Original_Label2 = QtWidgets.QLabel(self)
        self.Original_Label2.setStyleSheet("border: 3px solid blue")
        self.principalLayout.addWidget(self.Original_Label2, 0, 2)
        self.Original_Label2.resize(128, 128)
        
        self.Filtred_Label2 = QtWidgets.QLabel(self)
        self.Filtred_Label2.setStyleSheet("border: 3px solid blue")
        self.principalLayout.addWidget(self.Filtred_Label2, 1, 2)
        self.Filtred_Label2.resize(128, 128)
        
        self.set_all_images()
        self.maximize_window()
        
    def maximize_window(self):
        screen = QDesktopWidget().screenGeometry()
        self.setFixedSize(int(screen.height()*1.5), int(screen.height()*0.75))

    def set_all_images(self):
        self.parent.set_image(self.parent.red_image, self.Original_Label, "red", mask=False)
        self.parent.set_image(self.parent.green_image, self.Original_Label1, "green", mask=False)
        self.parent.set_image(self.parent.blue_image, self.Original_Label2, "blue", mask=False)
 
    def _createToolBars(self):
        # Adding a widget to the Edit toolbar
        editToolBar = QtWidgets.QToolBar("Edit", self)
        editToolBar.setFixedSize(2000, 100)
        self.addToolBar(editToolBar)
        self.fontSizeSpinBox = QDoubleSpinBox()
        self.fontSizeSpinBox.setFixedSize(80,40)
        self.fontSizeSpinBox.setMaximum(255.000)
        self.fontSizeSpinBox.setSingleStep(0.1)
        self.fontSizeSpinBox.setDecimals(3)
        self.Label_Min = QLabel('Min Threshold ')
        self.Label_Max = QLabel('Max Threshold ')
        editToolBar.addWidget(self.Label_Min)
        editToolBar.addWidget(self.fontSizeSpinBox)
        self.fontSizeSpinBox2 = QDoubleSpinBox()
        self.fontSizeSpinBox2.setFixedSize(80,40)
        self.fontSizeSpinBox2.setMaximum(255.000)
        self.fontSizeSpinBox2.setSingleStep(0.1)
        self.fontSizeSpinBox2.setDecimals(3)
        editToolBar.addSeparator()
        editToolBar.addWidget(self.Label_Max)
        editToolBar.addWidget(self.fontSizeSpinBox2)
        editToolBar.addSeparator()
        new_btn_ss5 = """QPushButton{background-color: turquoise;
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
        self.AutomaticButton = QPushButton('AUTOMATIC THRESHOLD')
        self.AutomaticButton.setStyleSheet(new_btn_ss5)
        self.AutomaticButton.clicked.connect(self.Automatic_threshold)
        editToolBar.addWidget(self.AutomaticButton)
        editToolBar.addSeparator()
        
        self.redRadioButton = QRadioButton('RED')
        self.redRadioButton.setStyleSheet(new_btn_ss5)
        editToolBar.addWidget(self.redRadioButton)
        editToolBar.addSeparator()
        self.greenRadioButton = QRadioButton('GREEN')
        self.greenRadioButton.setStyleSheet(new_btn_ss5)
        editToolBar.addWidget(self.greenRadioButton)
        editToolBar.addSeparator()
        self.blueRadioButton= QRadioButton('BLUE')
        self.blueRadioButton.setStyleSheet(new_btn_ss5)
        editToolBar.addWidget(self.blueRadioButton)
        editToolBar.addSeparator()
        
        self.Apply = QPushButton('Binarize')
        self.Apply.setStyleSheet(new_btn_ss5)
        self.Apply.clicked.connect(self.runIntensityBinarization)
        editToolBar.addWidget(self.Apply)
    
    def Automatic_threshold(self):
        self.soglia1=0
        if self.redRadioButton.isChecked():
            self.soglia1 = filters.threshold_otsu(self.parent.red_image)
        elif self.greenRadioButton.isChecked():
            self.soglia1 = filters.threshold_otsu(self.parent.green_image)
        elif self.blueRadioButton.isChecked():
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
        print(binarymat)
        return binarymat
    
    def runIntensityBinarization(self):
        if self.redRadioButton.isChecked():
            self.parent.red_mask = self.binarizeImage(self.parent.red_image)
            self.parent.set_image(self.parent.red_mask, self.Filtred_Label, "red", mask=True)
        elif self.greenRadioButton.isChecked():
            self.parent.green_mask = self.binarizeImage(self.parent.green_image)
            self.parent.set_image(self.parent.green_mask, self.Filtred_Label1, "green", mask=True)
        elif self.blueRadioButton.isChecked():
            self.parent.blue_mask = self.binarizeImage(self.parent.blue_image)
            self.parent.set_image(self.parent.blue_mask, self.Filtred_Label2, "blue", mask=True)
        else:
            pass

#PER GIUSEPPE: LE MASCHERE SI CHIAMANO self.parent.colore_mask
#              MENTRE LE IMMAGINI IN FORMATO NP SONO self.parent.colore_image


