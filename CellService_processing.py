import sys
from PyQt5.QtWidgets import (QDockWidget, QApplication, QWidget, QRadioButton, QPushButton, QToolTip, QLabel, QVBoxLayout, QDesktopWidget, QStyleFactory)
from PyQt5.QtWidgets import (QCheckBox, QBoxLayout,QFileDialog, QWidget, QMainWindow, QGroupBox, QAction, QMenu, QSystemTrayIcon, QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox)
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
        
        
        self._createToolBars()
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
        self.Original_Label.setScaledContents(True)
        
        # create a filtred label
        self.Filtred_Label = QtWidgets.QLabel(self)
        self.Filtred_Label.setStyleSheet("border: 3px solid red")
        self.principalLayout.addWidget(self.Filtred_Label, 1, 0)
        self.Filtred_Label.resize(128, 128)
        self.Filtred_Label.setScaledContents(True)
        
        self.Original_Label1 = QtWidgets.QLabel(self)
        self.Original_Label1.setStyleSheet("border: 3px solid green")
        self.principalLayout.addWidget(self.Original_Label1, 0, 1)
        self.Original_Label1.resize(128, 128)
        self.Original_Label1.setScaledContents(True)
        
        self.Filtred_Label1 = QtWidgets.QLabel(self)
        self.Filtred_Label1.setStyleSheet("border: 3px solid green")
        self.principalLayout.addWidget(self.Filtred_Label1, 1, 1)
        self.Filtred_Label1.resize(128, 128)
        self.Filtred_Label1.setScaledContents(True)
        
        self.Original_Label2 = QtWidgets.QLabel(self)
        self.Original_Label2.setStyleSheet("border: 3px solid blue")
        self.principalLayout.addWidget(self.Original_Label2, 0, 2)
        self.Original_Label2.resize(128, 128)
        self.Original_Label2.setScaledContents(True)
        
        self.Filtred_Label2 = QtWidgets.QLabel(self)
        self.Filtred_Label2.setStyleSheet("border: 3px solid blue")
        self.principalLayout.addWidget(self.Filtred_Label2, 1, 2)
        self.Filtred_Label2.resize(128, 128)
        self.Filtred_Label2.setScaledContents(True)
        
        self.set_all_images()
        self.maximize_window()
        
    def maximize_window(self):
        screen = QDesktopWidget().screenGeometry()
        self.setFixedSize(int(screen.height()*1.2), int(screen.height()*0.75))

    def set_all_images(self):
        self.parent.set_image(self.parent.red_image, self.Original_Label, "red", mask=False)
        self.parent.set_image(self.parent.green_image, self.Original_Label1, "green", mask=False)
        self.parent.set_image(self.parent.blue_image, self.Original_Label2, "blue", mask=False)
 
    def _createToolBars(self):
        # Adding a widget to the Edit toolbar
        self.setWindowTitle("Binary processing")
        self.editToolBar = QtWidgets.QToolBar("Edit", self)
        self.editToolBar.setFixedSize(2000, 100)
        self.addToolBar(self.editToolBar)
        self.fontSizeSpinBox = QDoubleSpinBox()
        self.fontSizeSpinBox.setFixedSize(80,40)
        self.fontSizeSpinBox.setMaximum(255.000)
        self.fontSizeSpinBox.setSingleStep(0.1)
        self.fontSizeSpinBox.setDecimals(3)
        self.Label_Min = QLabel('Min Threshold ')
        self.Label_Max = QLabel('Max Threshold ')
        self.editToolBar.addWidget(self.Label_Min)
        self.editToolBar.addWidget(self.fontSizeSpinBox)
        self.fontSizeSpinBox2 = QDoubleSpinBox()
        self.fontSizeSpinBox2.setFixedSize(80,40)
        self.fontSizeSpinBox2.setMaximum(255.000)
        self.fontSizeSpinBox2.setSingleStep(0.1)
        self.fontSizeSpinBox2.setDecimals(3)
        self.editToolBar.addSeparator()
        self.editToolBar.addWidget(self.Label_Max)
        self.editToolBar.addWidget(self.fontSizeSpinBox2)
        self.editToolBar.addSeparator()
        self.new_btn_ss5 = """QPushButton{background-color: turquoise;
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
        self.new_btn = """QPushButton{background-color: yellow;
                                    border-style: outset;
                                    border-width: 2px;
                                    border-radius: 15px;
                                    border-color: yellow;
                                    font: bold 14px;
                                    min-width: 5em;
                                    padding: 6px;}
                        QPushButton:pressed {background-color: rgb(255, 255, 255);
                                             border-style: inset;}
                     """
        self.AutomaticButton = QPushButton('AUTOMATIC THRESHOLD')
        self.AutomaticButton.setStyleSheet(self.new_btn_ss5)
        self.AutomaticButton.clicked.connect(self.Automatic_threshold)
        self.editToolBar.addWidget(self.AutomaticButton)
        self.editToolBar.addSeparator()
        
        self.redRadioButton = QRadioButton('RED')
        self.redRadioButton.setStyleSheet(self.new_btn_ss5)
        self.editToolBar.addWidget(self.redRadioButton)
        self.editToolBar.addSeparator()
        self.greenRadioButton = QRadioButton('GREEN')
        self.greenRadioButton.setStyleSheet(self.new_btn_ss5)
        self.editToolBar.addWidget(self.greenRadioButton)
        self.editToolBar.addSeparator()
        self.blueRadioButton= QRadioButton('BLUE')
        self.blueRadioButton.setStyleSheet(self.new_btn_ss5)
        self.editToolBar.addWidget(self.blueRadioButton)
        self.editToolBar.addSeparator()
        
        self.Apply = QPushButton('Binarize')
        self.Apply.setStyleSheet(self.new_btn_ss5)
        self.Apply.clicked.connect(self.runIntensityBinarization)
        self.editToolBar.addWidget(self.Apply)
        
        self.editToolBar.addSeparator()
        self.Next = QPushButton('CLICK FOR SEGMENTATION')
        self.Next.setStyleSheet(self.new_btn)
        self.Next.clicked.connect(self.segmentation)
        self.editToolBar.addWidget(self.Next)
    
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
        
    def segmentation(self):
        self.setWindowTitle("Segmentation processing")
        self.removeToolBar(self.editToolBar)
        self.Filtred_Label.setText(" ")
        self.Filtred_Label1.setText(" ")
        self.Filtred_Label2.setText(" ")
        self.editToolBar2 = QtWidgets.QToolBar("Edit", self)
        self.editToolBar2.setFixedSize(2000, 100)
        self.addToolBar(self.editToolBar2)
        
        self.Label_Raggio= QLabel('Raggio ')
        self.editToolBar2.addWidget(self.Label_Raggio)
        self.Raggio = QDoubleSpinBox()
        self.Raggio.setFixedSize(80,40)
        self.editToolBar2.addWidget(self.Raggio)
        self.editToolBar2.addSeparator()
        
        self.removeCheck = QCheckBox("Remove small object")
        self.editToolBar2.addWidget(self.removeCheck)
        self.erosionCheck = QCheckBox("Erosion")
        self.editToolBar2.addWidget(self.erosionCheck)
        
        self.editToolBar2.addSeparator()
        self.Return = QPushButton('CLICK FOR BINARIZE')
        self.Return.setStyleSheet(self.new_btn)
        self.Return.clicked.connect(self.binaryproject)
        self.editToolBar2.addWidget(self.Return)
        
        
    def binaryproject(self):
        self.removeToolBar(self.editToolBar2)
        self._createToolBars()
        
        
#PER GIUSEPPE: LE MASCHERE SI CHIAMANO self.parent.colore_mask
#              MENTRE LE IMMAGINI IN FORMATO NP SONO self.parent.colore_image


