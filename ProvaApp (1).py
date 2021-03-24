import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QToolTip, QLabel, QVBoxLayout, QDesktopWidget, QStyleFactory)
from PyQt5.QtWidgets import (QFileDialog, QWidget, QMainWindow, QGroupBox, QAction, QMenu, QSystemTrayIcon, QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox)
from PyQt5.QtGui import QPixmap, QIcon, QFont, QImage
from PyQt5 import QtWidgets
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSlot
import skimage.io
import numpy as np
from copy import deepcopy
from skimage import filters
from PIL import Image


class CellProgram(QMainWindow):
    
    create_image = np.zeros((100,100, 3), dtype=np.uint8)
    imageSave = QImage(create_image.data,  create_image.shape[1], create_image.shape[0], create_image.strides[0], QImage.Format_RGB888)
    imageRed =  QImage(create_image.data,  create_image.shape[1], create_image.shape[0], create_image.strides[0], QImage.Format_RGB888)
    imageBlue =  QImage(create_image.data,  create_image.shape[1], create_image.shape[0], create_image.strides[0], QImage.Format_RGB888)
    imageGreen =  QImage(create_image.data,  create_image.shape[1], create_image.shape[0], create_image.strides[0], QImage.Format_RGB888)
    
    def __init__(self):
        super().__init__()

        self.initUI()
        
        self.show()        

    def initUI(self):
        # create a widget and layout
        self.principalWidget = QtWidgets.QGroupBox(self)
        self.setCentralWidget(self.principalWidget)
        self.principalLayout = QtWidgets.QGridLayout()
        self.principalWidget.setLayout(self.principalLayout)
        
        # add menubar
        self.initMenuBar()
        
        # create a RGB label
        self.labelRGB = QtWidgets.QLabel(self)
        self.labelRGB.setStyleSheet("border: 3px solid black")
        self.principalLayout.addWidget(self.labelRGB, 0, 0)
        self.labelRGB.resize(128, 128)
        
        # create a red label
        self.labelRed = QtWidgets.QLabel(self)
        self.labelRed.setStyleSheet("border: 3px solid red")
        self.principalLayout.addWidget(self.labelRed, 0, 1)
        self.labelRed.resize(128, 128)
        
         # create a green label
        self.labelGreen = QtWidgets.QLabel(self)
        self.labelGreen.setStyleSheet("border: 3px solid green")
        self.principalLayout.addWidget(self.labelGreen, 1, 0)
        self.labelGreen.resize(128, 128)
        
         # create a blue label
        self.labelBlue = QtWidgets.QLabel(self)
        self.labelBlue.setStyleSheet("border: 3px solid blue")
        self.principalLayout.addWidget(self.labelBlue, 1, 1)
        self.labelBlue.resize(128, 128)
        
        # set the window
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setGeometry(600, 300, 700, 600)
        self.setWindowTitle('Cell visualizer')
        self.setWindowIcon(QIcon('icon.png'))
        self.move(20, 20)
        self.trayIcon = QtWidgets.QSystemTrayIcon(QIcon('icon.png'))
        self.trayIcon.setToolTip('Cell visualizer')
        self.trayIcon.show()
        
        self.maximize_window()
        
    def maximize_window(self):
        screen = QDesktopWidget().screenGeometry()
        self.setFixedSize(int(screen.height()*1.2), int(screen.height()*0.9))
    
    def initMenuBar(self):
        # create a menuBar
        self.menubar = QMainWindow.menuBar(self)
        
        # create first menu
        self.title = self.menubar.addMenu('Open File')
        # add first choice
        self.firstChoiceFirstMenu = QtWidgets.QAction('Open a RGB image')
        self.firstChoiceFirstMenu.triggered.connect(self.openRGBImage)
        self.title.addAction(self.firstChoiceFirstMenu)
        self.firstChoiceFirstMenu.setStatusTip('Open a new RGB image')
        # add second choice
        self.secondChoiceFirstMenu = QtWidgets.QAction('Open a single channel image')
        self.secondChoiceFirstMenu.triggered.connect(self.openSingleChannel)
        self.title.addAction(self.secondChoiceFirstMenu)
        # add third choice
        self.thirdChoiceFirstMenu = QtWidgets.QMenu('Save')
        self.title.addMenu(self.thirdChoiceFirstMenu)
        
        # create second menu
        self.second_title = self.menubar.addMenu('Edit')
        # add fisrt choice 
        self.firstChoiceSecondMenu = QtWidgets.QAction('Clear all')
        self.firstChoiceSecondMenu.triggered.connect(self.clearAll)
        self.second_title.addAction(self.firstChoiceSecondMenu)
        
        self.impMenuRGB = QtWidgets.QAction('Save RGB image')
        self.thirdChoiceFirstMenu.addAction(self.impMenuRGB)
        self.impMenuRGB.triggered.connect(self.file_save_RGB)
        
        self.impMenuRed = QtWidgets.QAction('Save red image')
        self.thirdChoiceFirstMenu.addAction(self.impMenuRed)
        self.impMenuRed.triggered.connect(self.file_save_red)
        
        self.impMenuGreen = QtWidgets.QAction('Save green image')
        self.thirdChoiceFirstMenu.addAction(self.impMenuGreen)
        self.impMenuGreen.triggered.connect(self.file_save_green)
        
        self.impMenuBlue = QtWidgets.QAction('Save blue image')
        self.thirdChoiceFirstMenu.addAction(self.impMenuBlue)
        self.impMenuBlue.triggered.connect(self.file_save_blue)
        
        # create third menu
        self.third_title = self.menubar.addMenu("Image Processing")
        # add first choice 
        self.firstChoiceThirdMenu = QtWidgets.QAction("Image binarization")
        self.firstChoiceThirdMenu.triggered.connect(self.window2)
        self.third_title.addAction(self.firstChoiceThirdMenu)
        # add second choice 
        self.secondChoiceThirdMenu = QtWidgets.QAction("Segmentation")
        self.third_title.addAction(self.secondChoiceThirdMenu)
        
        # create 4th menu
        self.fourth_title = self.menubar.addMenu("Image analisys")
        # add first choice
        self.firstChoiceFourthMenu = QtWidgets.QAction("Similarity")
        self.firstChoiceFourthMenu.triggered.connect(self.window3)
        self.fourth_title.addAction(self.firstChoiceFourthMenu)
        
    def window2(self):
        self.w = ProcessingWindow()
        self.w.show()
    
    def window3(self):
        self.window3 = AnalysisWindow()
        self.window3.show()
    
    def file_save_RGB(self):
        self.qt_image.save("RGB.tif")
    
    def file_save_red(self):
        self.qt_image_red.save("Red.tif")
    
    def file_save_green(self):
        self.qt_image_green.save("Green.tif")
    
    def file_save_blue(self):
        self.qt_image_blue.save("Blue.tif")
        
    def set_RGBimage(self, image):
        self.qt_image = QImage(image.data, image.shape[1], image.shape[0], image.strides[0], QImage.Format_RGB888)      
        pixMap = QPixmap.fromImage(self.qt_image)
        self.labelRGB.setPixmap(pixMap)
        self.labelRGB.setScaledContents(True)
        CellProgram.imageSave = self.qt_image
        self.maximize_window()

    def set_redImage(self, Redimage):
        red_image = np.zeros((Redimage.shape[0], Redimage.shape[1], 3), dtype=np.uint8)
        red_image[:,:,0] = Redimage
        self.qt_image_red = QImage(red_image.data, red_image.shape[1], red_image.shape[0], red_image.strides[0], QImage.Format_RGB888)
        pixRedMap = QPixmap.fromImage(self.qt_image_red)
        self.labelRed.setPixmap(pixRedMap)
        CellProgram.imageRed = self.qt_image_red
        self.labelRed.setScaledContents(True)
        
        self.maximize_window()
    
    def set_greenImage(self, Greenimage):
        green_image = np.zeros((Greenimage.shape[0], Greenimage.shape[1], 3), dtype=np.uint8)
        green_image[:,:,1] = Greenimage
        self.qt_image_green = QImage(green_image.data, green_image.shape[1], green_image.shape[0], green_image.strides[0], QImage.Format_RGB888)
        pixGreenMap = QPixmap.fromImage(self.qt_image_green)
        self.labelGreen.setPixmap(pixGreenMap)
        self.labelGreen.setScaledContents(True)
        CellProgram.imageGreen = self.qt_image_green
        self.maximize_window()
    
    def set_blueImage(self, Blueimage):
        blue_image = np.zeros((Blueimage.shape[0], Blueimage.shape[1], 3), dtype=np.uint8)
        blue_image[:,:,2] = Blueimage
        self.qt_image_blue = QImage(blue_image.data, blue_image.shape[1], blue_image.shape[0], blue_image.strides[0], QImage.Format_RGB888)
        pixBlueMap = QPixmap.fromImage(self.qt_image_blue)
        self.labelBlue.setPixmap(pixBlueMap)
        self.labelBlue.setScaledContents(True)
        CellProgram.imageBlue = self.qt_image_blue
        self.maximize_window()

    def openRGBImage(self):
        fileName = QFileDialog().getOpenFileName(self, "Open RGB image file", "", "Image files (*.jpg, *.jpeg, *.tif, *.png)")
        if fileName:
            RGBImage = skimage.io.imread(fileName[0]).astype(np.uint8)
            redImage = deepcopy(RGBImage[:,:,0])
            greenImage = deepcopy(RGBImage[:,:,1])
            blueImage = deepcopy(RGBImage[:,:,2])
            
            self.set_RGBimage(RGBImage)
            self.set_redImage(redImage)
            self.set_greenImage(greenImage)
            self.set_blueImage(blueImage)
    
    def openSingleChannel(self):
        fileNameRed = QFileDialog().getOpenFileName(self, "Open red image", "", "Image Files (*.jpg, *.jpeg, *.tif, *.png)")
        if fileNameRed:
            redImage = skimage.io.imread(fileNameRed[0]).astype(np.uint8)[:,:,0]
        else:
            return
        
        fileNameGreen = QFileDialog().getOpenFileName(self, "Open green image", "", "Image Files (*.jpg, *.jpeg, *.tif, *.png)")
        if fileNameGreen:
            greenImage = skimage.io.imread(fileNameGreen[0]).astype(np.uint8)[:,:,1]
        else:
            return 
        
        fileNameBlue = QFileDialog().getOpenFileName(self, "Open blue image", "", "Image Files (*.jpg, *.jpeg, *.tif, *.png)")
        if fileNameBlue:
            blueImage = skimage.io.imread(fileNameBlue[0]).astype(np.uint8)[:,:,2]
        else:
            return
        
        RGB_Image = np.dstack((redImage, greenImage, blueImage)).astype(np.uint8)
        self.set_RGBimage(RGB_Image)
        self.set_redImage(redImage)
        self.set_greenImage(greenImage)
        self.set_blueImage(blueImage)
        
    def clearAll(self):
        self.labelRGB.clear()
        self.labelRed.clear()
        self.labelGreen.clear()
        self.labelBlue.clear()        

class ProcessingWindow(CellProgram):
    create_image = np.zeros((100,100, 3), dtype=np.uint8)
    imageRGB = QImage(create_image.data,  create_image.shape[1], create_image.shape[0], create_image.strides[0], QImage.Format_RGB888)
    imageRED = QImage(create_image.data,  create_image.shape[1], create_image.shape[0], create_image.strides[0], QImage.Format_RGB888)
    imageGREEN = QImage(create_image.data,  create_image.shape[1], create_image.shape[0], create_image.strides[0], QImage.Format_RGB888)
    imageBLU = QImage(create_image.data,  create_image.shape[1], create_image.shape[0], create_image.strides[0], QImage.Format_RGB888)
    binarymatRGB = np.zeros((100,100, 3), dtype=np.uint8)
    binarymatRED = np.zeros((100,100, 3), dtype=np.uint8)
    binarymatGREEN = np.zeros((100,100, 3), dtype=np.uint8)
    binarymatBLUE = np.zeros((100,100, 3), dtype=np.uint8)
    
    def __init__(self):
        QMainWindow.__init__(self)
        self.image = CellProgram.imageSave
        self.imageBlue = CellProgram.imageBlue
        self.imageGreen = CellProgram.imageGreen
        self.imageRed = CellProgram.imageRed
        self.temp = CellProgram.imageSave
        self.x = None
        self._createToolBars()

        self.setWindowTitle('Processing')

        self.StatBar = self.statusBar()

        self.setStyle(QStyleFactory.create('Cleanlooks'))
        
        
        
        # create a widget and layout
        self.principalWidget = QtWidgets.QGroupBox(self)
        self.setCentralWidget(self.principalWidget)
        self.principalLayout = QtWidgets.QGridLayout()
        self.principalWidget.setLayout(self.principalLayout)

        # create a original label
        self.Original_Label = QtWidgets.QLabel(self)
        self.Original_Label.setStyleSheet("border: 3px solid black")
        self.principalLayout.addWidget(self.Original_Label, 0, 0)
        self.Original_Label.resize(128, 128)
        
        # create a filtred label
        self.Filtred_Label = QtWidgets.QLabel(self)
        self.Filtred_Label.setStyleSheet("border: 3px solid black")
        self.principalLayout.addWidget(self.Filtred_Label, 1, 0)
        self.Filtred_Label.resize(128, 128)
        
        self.Original_Label1 = QtWidgets.QLabel(self)
        self.Original_Label1.setStyleSheet("border: 3px solid black")
        self.principalLayout.addWidget(self.Original_Label1, 0, 1)
        self.Original_Label1.resize(128, 128)
        
        self.Filtred_Label1 = QtWidgets.QLabel(self)
        self.Filtred_Label1.setStyleSheet("border: 3px solid black")
        self.principalLayout.addWidget(self.Filtred_Label1, 1, 1)
        self.Filtred_Label1.resize(128, 128)
        
        self.Original_Label2 = QtWidgets.QLabel(self)
        self.Original_Label2.setStyleSheet("border: 3px solid black")
        self.principalLayout.addWidget(self.Original_Label2, 0, 2)
        self.Original_Label2.resize(128, 128)
        
        self.Filtred_Label2 = QtWidgets.QLabel(self)
        self.Filtred_Label2.setStyleSheet("border: 3px solid black")
        self.principalLayout.addWidget(self.Filtred_Label2, 1, 2)
        self.Filtred_Label2.resize(128, 128)
        
        self.Original_Label3 = QtWidgets.QLabel(self)
        self.Original_Label3.setStyleSheet("border: 3px solid black")
        self.principalLayout.addWidget(self.Original_Label3, 0, 3)
        self.Original_Label3.resize(128, 128)
        
        self.Filtred_Label3 = QtWidgets.QLabel(self)
        self.Filtred_Label3.setStyleSheet("border: 3px solid black")
        self.principalLayout.addWidget(self.Filtred_Label3, 1, 3)
        self.Filtred_Label3.resize(128, 128)
        
        pixRGBMap = QPixmap.fromImage(self.image)
        self.Original_Label.setPixmap(pixRGBMap)
        self.Original_Label.setScaledContents(True)
        ProcessingWindow.imageRGB = self.image
        pixREDMap = QPixmap.fromImage(self.imageRed)
        self.Original_Label1.setPixmap(pixREDMap)
        self.Original_Label1.setScaledContents(True)
        ProcessingWindow.imageRED = self.imageRed
        pixGREENMap = QPixmap.fromImage(self.imageGreen)
        self.Original_Label2.setPixmap(pixGREENMap)
        self.Original_Label2.setScaledContents(True)
        ProcessingWindow.imageGREEN = self.imageGreen
        self.Original_Label3.clear()
        pixBLUEMap = QPixmap.fromImage(self.imageBlue)
        self.Original_Label3.setPixmap(pixBLUEMap)
        self.Original_Label3.setScaledContents(True)
        ProcessingWindow.imageBLUE = self.imageBlue
        self.maximize_window()
        
    def maximize_window(self):
        screen = QDesktopWidget().screenGeometry()
        self.setFixedSize(int(screen.height()*1.5), int(screen.height()*0.75))
        
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
        self.Label_Status = QLabel("NESSUNA")
        self.Label_Status.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        editToolBar.addWidget(self.Label_Status)
        editToolBar.addSeparator()
        self.Apply = QPushButton("Apply")
        self.Apply.setStyleSheet(new_btn_ss5)
        self.Apply.clicked.connect(self.leggivalore)
        editToolBar.addWidget(self.Apply)
        editToolBar.addSeparator()
        self.AutomaticButton = QPushButton('AUTOMATIC THRESHOLD')
        self.AutomaticButton.setStyleSheet(new_btn_ss5)
        self.AutomaticButton.clicked.connect(self.Automatic_threshold)
        editToolBar.addWidget(self.AutomaticButton)
        editToolBar.addSeparator()
        self.AutomaticButton_RGB = QPushButton('RGB')
        self.AutomaticButton_RGB.setStyleSheet(new_btn_ss5)
        self.AutomaticButton_RGB.clicked.connect(self.cliccatoRGB)
        self.AutomaticButton_RGB.setCheckable(True)
        editToolBar.addWidget(self.AutomaticButton_RGB)
        editToolBar.addSeparator()
        self.AutomaticButton_RED = QPushButton('RED')
        self.AutomaticButton_RED.setStyleSheet(new_btn_ss5)
        self.AutomaticButton_RED.clicked.connect(self.cliccatoRED)
        editToolBar.addWidget(self.AutomaticButton_RED)
        editToolBar.addSeparator()
        self.AutomaticButton_GREEN = QPushButton('GREEN')
        self.AutomaticButton_GREEN.setStyleSheet(new_btn_ss5)
        self.AutomaticButton_GREEN.clicked.connect(self.cliccatoGREEN)
        editToolBar.addWidget(self.AutomaticButton_GREEN)
        editToolBar.addSeparator()
        self.AutomaticButton_BLUE = QPushButton('BLUE')
        self.AutomaticButton_BLUE.setStyleSheet(new_btn_ss5)
        self.AutomaticButton_BLUE.clicked.connect(self.cliccatoBLUE)
        editToolBar.addWidget(self.AutomaticButton_BLUE)
        
    
    def cliccatoRGB(self):
        self.temp=self.image
        self.x="RGB"
        self.Label_Status.setText("RGB")
    
    def cliccatoRED(self):
        self.temp=self.imageRed
        self.x="RED"
        self.Label_Status.setText("RED")
    
    def cliccatoGREEN(self):
        self.temp=self.imageGreen
        self.x="GREEN"
        self.Label_Status.setText("GREEN")
    
    def cliccatoBLUE(self):
        self.temp=self.imageBlue
        self.x="BLUE"
        self.Label_Status.setText("BLUE")
    
    def Automatic_threshold(self):
        #https://stackoverflow.com/questions/19902183/qimage-to-numpy-array-using-pyside
        arr=self.converti_in_array(self.temp)
        self.soglia1 = filters.threshold_otsu(arr)
        self.fontSizeSpinBox.setValue(self.soglia1)
    
    def converti_in_array (self,image):
        pixmap = QPixmap.fromImage(image)
        self.image1 = pixmap.toImage()
        self.size = self.image1.size()
        s = self.image1.bits().asstring(self.size.width() * self.size.height() * self.image1.depth() // 8)  # format 0xffRRGGBB
        arr = np.fromstring(s, dtype=np.uint8).reshape((self.size.height(), self.size.width(), self.image1.depth() // 8))
        return arr
        
    def leggivalore(self):
        valore1 = self.fontSizeSpinBox.value()
        valore2 =self.fontSizeSpinBox2.value()
        arr=self.converti_in_array(self.temp)
        binarymat=np.zeros_like(arr)
        if (valore1==0):
            valore1=filters.threshold_otsu(arr)
        if (valore2!=0):
            mask=np.logical_and(arr > valore1, arr < valore2)
            binarymat[mask]=1
        if (valore2==0):
            mask=arr>valore1
            binarymat[mask]=1
        self.qt_binarymat = QImage(binarymat.data, binarymat.shape[1], binarymat.shape[0], binarymat.strides[0], QImage.Format_RGB30)
        pixCURRENTMap = QPixmap.fromImage(self.qt_binarymat)
        if(self.x == "RGB"):
            ProcessingWindow.binarymatRGB=binarymat
            self.Filtred_Label.setPixmap(pixCURRENTMap)
            self.Filtred_Label.setScaledContents(True)
        if(self.x == "RED"):
            ProcessingWindow.binarymatRED=binarymat
            self.Filtred_Label1.setPixmap(pixCURRENTMap)
            self.Filtred_Label1.setScaledContents(True)
        if(self.x == "GREEN"):
            ProcessingWindow.binarymatGREEN=binarymat
            self.Filtred_Label2.setPixmap(pixCURRENTMap)
            self.Filtred_Label2.setScaledContents(True)
        if(self.x == "BLUE"):
            ProcessingWindow.binarymatBLUE=binarymat
            self.Filtred_Label3.setPixmap(pixCURRENTMap)
            self.Filtred_Label3.setScaledContents(True)

class AnalysisWindow(ProcessingWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.image = CellProgram.imageSave
        self.imageBlue = CellProgram.imageBlue
        self.imageGreen = CellProgram.imageGreen
        self.imageRed = CellProgram.imageRed
        self._createToolBarsAnalysis()
        self.imageRMask = ProcessingWindow.binarymatRED
        self.imageBMask = ProcessingWindow.binarymatBLUE
        self.imageGMask = ProcessingWindow.binarymatGREEN
        self.current = 0
        
        self.StatBar = self.statusBar()
        self.setWindowTitle('Analysis')
        
        self.setStyle(QStyleFactory.create('Cleanlooks'))
        
        # create a widget and layout
        self.principalWidget = QtWidgets.QGroupBox(self)
        self.setCentralWidget(self.principalWidget)
        self.principalLayout = QtWidgets.QGridLayout()
        self.principalWidget.setLayout(self.principalLayout)

        # create a original label
        self.Label_Red = QtWidgets.QLabel(self)
        self.Label_Red.setStyleSheet("border: 3px solid black")
        self.principalLayout.addWidget(self.Label_Red, 0, 0)
        self.Label_Red.resize(128, 128)
        
        # create a filtred label
        self.Label_Green = QtWidgets.QLabel(self)
        self.Label_Green.setStyleSheet("border: 3px solid black")
        self.principalLayout.addWidget(self.Label_Green, 0, 1)
        self.Label_Green.resize(128, 128)
        
        self.Label_Blue = QtWidgets.QLabel(self)
        self.Label_Blue.setStyleSheet("border: 3px solid black")
        self.principalLayout.addWidget(self.Label_Blue, 1, 0)
        self.Label_Blue.resize(128, 128)
        
        self.Label_Common = QtWidgets.QLabel(self)
        self.Label_Common.setStyleSheet("border: 3px solid black")
        self.principalLayout.addWidget(self.Label_Common, 1, 1)
        self.Label_Common.resize(128, 128)
        
        self.Label_Red.clear()
        pixREDMap = QPixmap.fromImage(self.imageRed)
        self.Label_Red.setPixmap(pixREDMap)
        self.Label_Red.setScaledContents(True)
        ProcessingWindow.imagecurrent = self.imageRed
        self.Label_Blue.clear()
        pixBLUEMap = QPixmap.fromImage(self.imageBlue)
        self.Label_Blue.setPixmap(pixBLUEMap)
        self.Label_Blue.setScaledContents(True)
        ProcessingWindow.imagecurrent = self.imageBlue
        self.Label_Green.clear()
        pixGREENMap = QPixmap.fromImage(self.imageGreen)
        self.Label_Green.setPixmap(pixGREENMap)
        self.Label_Green.setScaledContents(True)
        ProcessingWindow.imagecurrent = self.imageGreen
        
        self.maximize_window()
        
    def maximize_window(self):
        screen = QDesktopWidget().screenGeometry()
        self.setFixedSize(int(screen.height()*1.35), int(screen.height()*0.9))
    
    def _createToolBarsAnalysis(self):
        # Adding a widget to the Edit toolbar
        editToolBar = QtWidgets.QToolBar("Edit", self)
        
        editToolBar.setFixedSize(1000, 100)
        self.addToolBar(editToolBar)
        
        self.Blue_Red_button = QPushButton('Blue-red similarity')
        new_btn_ss = """QPushButton{background-color: purple;
                                    border-style: outset;
                                    border-width: 2px;
                                    border-radius: 15px;
                                    border-color: purple;
                                    font: bold 14px;
                                    min-width: 10em;
                                    padding: 6px;}
                        QPushButton:pressed {background-color: rgb(255, 255, 255);
                                             border-style: inset;}
                     """
        self.Blue_Red_button.setStyleSheet(new_btn_ss)
        self.Blue_Red_button.clicked.connect(self.scelta1)
        self.Blue_Red_button.clicked.connect(self.similarityMeasureAndOverlap)
        editToolBar.addWidget(self.Blue_Red_button)
        editToolBar.addSeparator()
        new_btn_ss2 = """QPushButton{background-color: cyan;
                                    border-style: outset;
                                    border-width: 2px;
                                    border-radius: 15px;
                                    border-color: cyan;
                                    font: bold 14px;
                                    min-width: 10em;
                                    padding: 6px;}
                        QPushButton:pressed {background-color: rgb(255, 255, 255);
                                             border-style: inset;}
                     """
        self.Blue_Green_button = QPushButton('Blue-green similarity')
        self.Blue_Green_button.setStyleSheet(new_btn_ss2)
        self.Blue_Green_button.clicked.connect(self.scelta2)
        self.Blue_Green_button.clicked.connect(self.similarityMeasureAndOverlap)
        editToolBar.addWidget(self.Blue_Green_button)
        editToolBar.addSeparator()
        new_btn_ss3 = """QPushButton{background-color: gray;
                                    border-style: outset;
                                    border-width: 2px;
                                    border-radius: 15px;
                                    border-color: gray;
                                    font: bold 14px;
                                    min-width: 10em;
                                    padding: 6px;}
                        QPushButton:pressed {background-color: rgb(255, 255, 255);
                                             border-style: inset;}
                     """
        self.Red_Green_button = QPushButton('Red-green similarity')
        self.Red_Green_button.setStyleSheet(new_btn_ss3)
        self.Red_Green_button.clicked.connect(self.scelta3)
        self.Red_Green_button.clicked.connect(self.similarityMeasureAndOverlap)
        editToolBar.addWidget(self.Red_Green_button)
        editToolBar.addSeparator()
        new_btn_ss4 = """QPushButton{background-color: yellow;
                                    border-style: outset;
                                    border-width: 2px;
                                    border-radius: 15px;
                                    border-color: yellow;
                                    font: bold 14px;
                                    min-width: 10em;
                                    padding: 6px;}
                        QPushButton:pressed {background-color: rgb(255, 255, 255);
                                             border-style: inset;}
                     """
        self.AllImageSimilarity = QPushButton("Total similarity")
        self.AllImageSimilarity.setStyleSheet(new_btn_ss4)
        self.AllImageSimilarity.clicked.connect(self.imagesOverlap)
        editToolBar.addWidget(self.AllImageSimilarity)
        editToolBar.addSeparator()
        self.Label_Similarity = QLabel('Scegli immagini')
        self.Label_Similarity.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        editToolBar.addWidget(self.Label_Similarity)
        
    def scelta1(self):
        self.current=1
    
    def scelta2(self):
        self.current=2
    
    def scelta3(self):
        self.current=3
    
    def imagesOverlap(self):
        similarity=0
        overlapping = np.zeros_like(self.imageRMask)
        for i in range(self.imageRMask.shape[0]):
          for j in range(self.imageRMask.shape[1]):
              for z in range(self.imageRMask.shape[2]):
                  if (self.imageRMask[i][j][z]==1 and self.imageGMask[i][j][z]==1
                      and self.imageBMask[i][j][z]==1):
                          overlapping[i][j][z]=1
                          similarity+=1
        self.qt_binarymat = QImage(overlapping.data, overlapping.shape[1], overlapping.shape[0], overlapping.strides[0], QImage.Format_RGB30)
        pixCURRENTMap = QPixmap.fromImage(self.qt_binarymat)
        self.Label_Common.setPixmap(pixCURRENTMap)
        self.Label_Common.setScaledContents(True)
        self.Label_Similarity.setText(str(round((similarity*100)/(self.imageRMask.shape[0] * self.imageRMask.shape[1] * self.imageRMask.shape[2]), 2))+ "%")
    
    def similarityMeasureAndOverlap(self):
        similarity = 0
        if (self.current == 1):
            image1Mask = self.imageRMask
            image2Mask = self.imageBMask
        if (self.current == 2):
            image1Mask = self.imageGMask
            image2Mask = self.imageBMask
        if (self.current == 3):
            image1Mask = self.imageRMask
            image2Mask = self.imageGMask
        overlapping = np.zeros_like(image1Mask)
        for i in range(image1Mask.shape[0]):
          for j in range(image2Mask.shape[1]):
              for z in range(image2Mask.shape[2]):
                  if (image1Mask[i][j][z]==image2Mask[i][j][z]):
                      similarity += 1
                  if (image1Mask[i][j][z]==1 and image2Mask[i][j][z]==1):
                      overlapping[i][j][z]=1
        print(overlapping)
        self.qt_binarymat = QImage(overlapping.data, overlapping.shape[1], overlapping.shape[0], overlapping.strides[0], QImage.Format_RGB30)
        pixCURRENTMap = QPixmap.fromImage(self.qt_binarymat)
        self.Label_Common.setPixmap(pixCURRENTMap)
        self.Label_Common.setScaledContents(True)
        self.Label_Similarity.setText(str(round((similarity*100)/(image1Mask.shape[0] * image1Mask.shape[1] * image1Mask.shape[2]), 2))+ "%")
                
def main():
    app = QApplication(sys.argv)
    # sys.argv è una lista di argomenti a riga di comando
    # in modo da eseguire lo scripts anche da shell
    ex = CellProgram()
    
    sys.exit(app.exec_())
    
    
if __name__ == '__main__':
    main()
