import sys
import PyQt5.Qt
import os
import cv2
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.label)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Connect the push button's clicked signal to the slot
        self.pushButton.clicked.connect(self.start_animation)

        # Create a QTimer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.render_numpy_array)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))

    def start_animation(self):
        # Start the QTimer
        self.timer.start(1)  # update every milisecond

    def render_numpy_array(self):
        # Create a numpy array
        array = np.random.randint(0, 256, (512, 512), dtype=np.uint8)

        # Convert the numpy array to a QImage
        qimage = QtGui.QImage(array.data, array.shape[1], array.shape[0], QtGui.QImage.Format_Grayscale8)

        # Convert the QImage to QPixmap and scale it to the size of the QLabel
        pixmap = QtGui.QPixmap.fromImage(qimage).scaled(self.label.size(), QtCore.Qt.KeepAspectRatio)

        # Display the QPixmap in the QLabel
        self.label.setPixmap(pixmap)

    def resizeEvent(self, event):
        # Update the QPixmap when the window is resized
        self.render_numpy_array()

if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    window = PyQt5.QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())