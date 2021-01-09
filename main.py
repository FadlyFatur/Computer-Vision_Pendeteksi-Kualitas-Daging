import sys
import cv2
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QFileDialog
from PyQt5.uic import loadUi
import numpy as np



class ShowImage (QMainWindow):
    def __init__(self):
        super(ShowImage,self).__init__()
        loadUi('project.ui',self)
        self.image = None
        self.loadButton.clicked.connect(self.loadClicked)
        self.saveButton.clicked.connect(self.save_Button)
        self.startButton.clicked.connect(self.Cek_Kualitas)
        self.MarblingButton.clicked.connect(self.marbling)

    def marbling(self):
        # # MARBLING

        # ROI Cropping
        print('---------------------Gambar Asli---------------------')
        r = cv2.selectROI(self.image)

        # Crop image
        img_crop = self.image[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]


        print('-------------------------Grayscale-------------------')

        img = cv2.cvtColor(img_crop, cv2.COLOR_BGR2GRAY)  # grayscale


        print('-------------Ekualisasi Histogram--------------------')
        hist, bins = np.histogram(img.flatten(), 256, [0, 256])

        cdf = hist.cumsum()
        cdf_normalized = cdf * hist.max() / cdf.max()

        cdf_m = np.ma.masked_equal(cdf,  0)
        cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
        cdf = np.ma.filled(cdf_m, 0).astype('uint8')
        img_out = cdf[img]

        # iar = np.asarray(img)
        # print(iar)

        # cv2.imshow("Ekualisasi Histogram", img_out)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # simple code
        # img = cv2.imread('wiki.jpg', 0)
        # equ = cv2.equalizeHist(img)
        # res = np.hstack((img, equ))  # stacking images side-by-side
        # cv2.imwrite('res.png', res)

        print('-------------Threshold--------------------')

        T = 140
        h, w = img_out.shape[:2]
        for i in np.arange(h):
            for j in np.arange(w):
                a = img_out.item(i, j)
                if a > T:
                    b = 255
                elif a < T:
                    b = 0
                else:
                    b = b
                img_out.itemset((i, j), b)


        # img_final = cv2.medianBlur(img_out, 5)
        # img_final = cv2.GaussianBlur(img_out, (5, 5), 1)
        # pixel = img_out[5, 5]
        # print(pixel)


        iar = np.asarray(img_out)
        print(iar)

        # cv2.imshow("Threshold", img_out)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        pixArray = np.asarray(img_out)
        mean = np.mean(pixArray)

        print('Mean = ', mean)


        if 107 <= mean <= 108:
            print('kualitas daging nomer 1')
            self.label_kualitas.setText('Kualitas Marbling Ke-1 ')
        elif 109 <= mean <=124:
            print ('Kualitas daging nomer 2')
            self.label_kualitas.setText('Kualitas Marbling Ke-2')
        elif mean < 107 or mean > 124:
            print ('Kulitas daging nomer 3')
            self.label_kualitas.setText('Kualitas Marbling Ke-3')
        #Nilai range didapat dari data latih dengan berbagai jenis marbling pada daging

        print('cek')
        self.image = img_out
        self.displayImage(2)

    def Cek_Kualitas(self):
        #KUALITAS HSV

        img = self.image
        # Crop image
        r = cv2.selectROI(img)
        images = img[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]

        # converting from BGR to HSV color space
        hsv = cv2.cvtColor(images, cv2.COLOR_BGR2HSV)

        lower_blue = np.array([1, 50, 150])
        upper_blue = np.array([40, 215, 255])
        # Nilai Range didapat dari hasil percobaan dengan data latih berupa daging segar dan busuk

        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        result = cv2.bitwise_and(images,images, mask=mask)
        mean = np.mean(result)
        print(mean)

        if 45 <= mean <= 160:
            print('kualitas daging nomer 1 = daging segar')
            self.label_kualitas_daging.setText('Kualitas Daging Ke-1 = Daging Segar ')
            # self.mean.setText(str (mean))
        elif  25 <= mean <= 44.9:
            print('Kualitas daging nomer 2 = daging ')
            self.label_kualitas_daging.setText('Kualitas Daging Ke-2 = Daging ')
            # self.mean.setText(mean)
        elif mean == 0 or mean < 24.9:
            print('Kulitas daging nomer 3 = daging busuk')
            self.label_kualitas_daging.setText('Kualitas Daging Ke-3 = Busuk')
            # self.mean.setText(mean)

        self.image = hsv
        self.displayImage(3)


    @pyqtSlot()
    def loadClicked(self):
        flname, filter=QFileDialog.getOpenFileName(self, 'Open File','C:\\User\\FDLY\\Downloads\\',"Image Files(*.jpg)")
        if flname:
            self.loadImage(flname)
        else:
            print('Invalid Image')

    def loadImage(self, flname):
        self.image = cv2.imread(flname)
        self.displayImage()

    def displayImage(self, windows=1):
        qformat = QImage.Format_Indexed8

        if len(self.image.shape) == 3:
            if (self.image.shape[2]) == 4:
                qformat = QImage.Format_RGBA8888

            else:
                qformat = QImage.Format_RGB888
        img = QImage(self.image, self.image.shape[1], self.image.shape[0], self.image.strides[0], qformat)
        img = img.rgbSwapped()

        if windows == 1:
            self.imagelabel.setPixmap(QPixmap.fromImage(img))
            self.imagelabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.imagelabel.setScaledContents(True)
        if windows == 2:
            self.l1.setPixmap(QPixmap.fromImage(img))
            self.l1.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.l1.setScaledContents(True)
        if windows == 3:
            self.l2.setPixmap(QPixmap.fromImage(img))
            self.l2.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.l2.setScaledContents(True)

        return self.imagelabel

        self.imagelabel.setPixmap(QPixmap.fromImage(img))
        self.imagelabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

    def save_Button(self):
        flname, filter = QFileDialog.getSaveFileName(self, 'save file','D:\\',
                                                     "Images Files(*.jpg)")
        if flname:
            cv2.imwrite(flname, self.image)
        else:
            print('Saved')



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ShowImage()
    window.setWindowTitle('Show Image GUI')
    window.show()
    sys.exit(app.exec_())