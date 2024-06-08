import sys
import PyQt5.Qt
import os
import cv2
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
import random

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
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setObjectName("startButton")
        self.verticalLayout.addWidget(self.startButton)
        self.stopButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopButton.setObjectName("stopButton")
        self.verticalLayout.addWidget(self.stopButton)
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
        self.startButton.clicked.connect(self.start_animation)
        self.stopButton.clicked.connect(self.stop_animation)

        # Create a QTimer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.render_numpy_array)
        self.circles = [(random.randint(0, 512), random.randint(0, 512), random.randint(0, 256), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))) for _ in range(5)]
        self.counter = 0

        # Create a 3D numpy array of double datatype
        self.array = np.zeros((512, 512, 3))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.startButton.setText(_translate("MainWindow", "Start"))
        self.stopButton.setText(_translate("MainWindow", "Stop"))

    def start_animation(self):
        # Start the QTimer
        self.timer.start(1)  # update every milisecond

    def stop_animation(self):
        # Stop the QTimer
        self.timer.stop()

    def render_numpy_array(self):
        # Reset the array
        self.array.fill(0)

        # Create expanding circles
        for i, (x, y, r, color) in enumerate(self.circles):
            cv2.circle(self.array, (x, y), (self.counter + r) % 256, color, -1)

        # Normalize the array to the range [0, 255] and convert it to uint8, (MemoryView)
        N= (255 * self.array / np.max(self.array)).astype(np.uint8) 

        # Convert the numpy array to a QImage
        height, width, colors = self.array.shape
        bytesPerLine = colors * width
        qimage = QtGui.QImage(N.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)

        # Convert the QImage to QPixmap and scale it to the size of the QLabel
        pixmap = QtGui.QPixmap.fromImage(qimage).scaled(self.label.size(), QtCore.Qt.KeepAspectRatio)

        # Display the QPixmap in the QLabel
        self.label.setPixmap(pixmap)

        # Increment the counter
        self.counter += 1

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