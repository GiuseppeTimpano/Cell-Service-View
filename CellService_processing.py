import sys
from PyQt5.QtWidgets import (QDockWidget, QApplication, QWidget, QRadioButton, QPushButton, QToolTip, QLabel, QVBoxLayout, QDesktopWidget, QStyleFactory)
from PyQt5.QtWidgets import (QCheckBox, QBoxLayout,QFileDialog, QWidget, QMainWindow, QGroupBox, QAction, QMenu, QSystemTrayIcon, QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox)
from PyQt5.QtGui import QPixmap, QIcon, QFont, QImage
from PyQt5 import QtWidgets
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSlot
import skimage.io
import skimage.morphology
import numpy as np
from skimage import filters

class CellServiceBinaryProcessing(QMainWindow):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        
        self.init_ui()
        self._createToolBars()
        

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
        self.greenRadioButton = QRadioButton('GREEN')
        self.greenRadioButton.setStyleSheet(self.new_btn_ss5)
        self.editToolBar.addWidget(self.greenRadioButton)
        self.blueRadioButton= QRadioButton('BLUE')
        self.blueRadioButton.setStyleSheet(self.new_btn_ss5)
        self.editToolBar.addWidget(self.blueRadioButton)
        self.editToolBar.addSeparator()
        
        self.Apply = QPushButton('Binarize')
        self.Apply.setStyleSheet(self.new_btn_ss5)
        self.Apply.clicked.connect(self.runIntensityBinarization)
        self.editToolBar.addWidget(self.Apply)
        
        self.editToolBar.addSeparator()
        self.Next = QPushButton('NEXT STEP')
        self.Next.setStyleSheet(self.new_btn)
        self.Next.clicked.connect(self.segmentation)
        self.editToolBar.addWidget(self.Next)
        self.set_all_images()
    
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
        self.parent.set_image(self.parent.red_mask, self.Original_Label, "red", mask=True)
        self.Filtred_Label1.setText(" ")
        self.parent.set_image(self.parent.green_mask, self.Original_Label1, "green", mask=True)
        self.Filtred_Label2.setText(" ")
        self.parent.set_image(self.parent.blue_mask, self.Original_Label2, "blue", mask=True)
        self.editToolBar2 = QtWidgets.QToolBar("Edit", self)
        self.editToolBar2.setFixedSize(2000, 100)
        self.addToolBar(self.editToolBar2)
        
        self.Label_Raggio= QLabel('Raggio ')
        self.editToolBar2.addWidget(self.Label_Raggio)
        self.Raggio = QDoubleSpinBox()
        self.Raggio.setFixedSize(80,40)
        self.Raggio.setMaximum(255.000)
        self.editToolBar2.addWidget(self.Raggio)
        self.editToolBar2.addSeparator()
        
        self.removeCheck = QCheckBox("Remove small object")
        self.editToolBar2.addWidget(self.removeCheck)
        self.erosionCheck = QCheckBox("Erosion")
        self.editToolBar2.addWidget(self.erosionCheck)
        self.noiseCheck = QCheckBox("Remove Noise")
        self.editToolBar2.addWidget(self.noiseCheck)
        self.editToolBar2.addSeparator()
        
        self.redRadioButton2 = QRadioButton('RED')
        self.redRadioButton2.setStyleSheet(self.new_btn_ss5)
        self.editToolBar2.addWidget(self.redRadioButton2)
        self.greenRadioButton2 = QRadioButton('GREEN')
        self.greenRadioButton2.setStyleSheet(self.new_btn_ss5)
        self.editToolBar2.addWidget(self.greenRadioButton2)
        self.blueRadioButton2= QRadioButton('BLUE')
        self.blueRadioButton2.setStyleSheet(self.new_btn_ss5)
        self.editToolBar2.addWidget(self.blueRadioButton2)
        
        self.editToolBar2.addSeparator()
        self.Apply2 = QPushButton('APPLY')
        self.Apply2.setStyleSheet(self.new_btn_ss5)
        self.Apply2.clicked.connect(self.apply_segmentation)
        self.editToolBar2.addWidget(self.Apply2)
        
        self.editToolBar2.addSeparator()
        self.Save = QPushButton('SAVE AND VIEW')
        self.Save.setStyleSheet(self.new_btn_ss5)
        self.Save.clicked.connect(self.binaryproject)
        self.editToolBar2.addWidget(self.Save)
        
        self.editToolBar2.addSeparator()
        self.Return = QPushButton('COME BACK')
        self.Return.setStyleSheet(self.new_btn)
        self.Return.clicked.connect(self.binaryproject)
        self.editToolBar2.addWidget(self.Return)
    
    def apply_segmentation(self):
        self.mask_red=None
        self.mask_green=None
        self.mask_blue=None
        entry=False
        if self.removeCheck.isChecked() or self.erosionCheck.isChecked() or self.noiseCheck.isChecked():
            entry=True
        if entry:
            if self.redRadioButton2.isChecked():
                if self.erosionCheck.isChecked():
                    self.mask_red=skimage.morphology.erosion(self.parent.red_mask)
                if self.removeCheck.isChecked():
                    raggio=self.Raggio.value()
                    if(self.mask_red is not None):
                        self.mask_red= skimage.morphology.remove_small_objects(self.mask_red.astype(np.bool), raggio)
                    else:
                        self.mask_red= skimage.morphology.remove_small_objects(self.parent.red_mask.astype(np.bool), raggio)
                if self.noiseCheck.isChecked():
                    if(self.mask_red is not None):
                        self.mask_red=skimage.morphology.closing(self.mask_red)
                    else:
                        self.mask_red=skimage.morphology.closing(self.parent.red_mask)
                self.parent.set_image(self.mask_red, self.Filtred_Label, "red", mask=True)
            if self.greenRadioButton2.isChecked():
                if self.erosionCheck.isChecked():
                    self.mask_green=skimage.morphology.erosion(self.parent.green_mask)
                if self.removeCheck.isChecked():
                    raggio=self.Raggio.value()
                    if(self.mask_green is not None):
                        self.mask_green= skimage.morphology.remove_small_objects(self.mask_green.astype(np.bool), raggio)
                    else:
                        self.mask_green= skimage.morphology.remove_small_objects(self.parent.green_mask.astype(np.bool), raggio)
                if self.noiseCheck.isChecked():
                    if(self.mask_green is not None):
                        self.mask_green=skimage.morphology.closing(self.mask_green)
                    else:
                        self.mask_green=skimage.morphology.closing(self.parent.green_mask)
                self.parent.set_image(self.mask_green, self.Filtred_Label1, "green", mask=True)
            if self.blueRadioButton2.isChecked():
                if self.erosionCheck.isChecked():
                    self.mask_blue=skimage.morphology.erosion(self.parent.blue_mask)
                if self.removeCheck.isChecked():
                    raggio=self.Raggio.value()
                    if(self.mask_blue is not None):
                        self.mask_blue= skimage.morphology.remove_small_objects(self.mask_blue.astype(np.bool), raggio)
                    else:
                        self.mask_blue= skimage.morphology.remove_small_objects(self.parent.blue_mask.astype(np.bool), raggio)
                if self.noiseCheck.isChecked():
                    if(self.mask_blue is not None):
                        self.mask_blue=skimage.morphology.closing(self.mask_blue)
                    else:
                        self.mask_blue=skimage.morphology.closing(self.parent.blue_mask)
                self.parent.set_image(self.mask_blue, self.Filtred_Label2, "blue", mask=True)
        else:
            self.parent.set_image(self.parent.red_mask, self.Filtred_Label, "red", mask=True)
            self.parent.set_image(self.parent.green_mask, self.Filtred_Label1, "green", mask=True)
            self.parent.set_image(self.parent.blue_mask, self.Filtred_Label2, "blue", mask=True)
        entry=False
    
    def save(self):
        self.parent.red_mask=self.mask_red
        self.parent.green_mask=self.mask_green
        self.parent.blue_mask=self.mask_blue
        self.parent.set_image(self.parent.red_mask, self.Filtred_Label, "red", mask=True)
        self.parent.set_image(self.parent.green_mask, self.Filtred_Label1, "green", mask=True)
        self.parent.set_image(self.parent.blue_mask, self.Filtred_Label2, "blue", mask=True)
        self.binaryproject()
        
    def binaryproject(self):
        self.removeToolBar(self.editToolBar2)
        self._createToolBars()
        
        
#PER GIUSEPPE: LE MASCHERE SI CHIAMANO self.parent.colore_mask
#              MENTRE LE IMMAGINI IN FORMATO NP SONO self.parent.colore_image


