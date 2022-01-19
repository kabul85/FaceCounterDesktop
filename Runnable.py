import time
import numpy as np
import cv2
from mtcnn import MTCNN

from PyQt6.QtCore import QRunnable, QThread, pyqtSignal


class Runnable(QThread):
    t = pyqtSignal(str)
    def __init__(self, ipCams):
        super().__init__()
        self.run_flag = True
        self.ipCams = ipCams

    def run(self):
        detector = MTCNN()
        while self.run_flag:
            try:
                for aIpCam in self.ipCams:
                    #time.sleep(1)
                    #net = cv2.dnn.readNetFromCaffe('models/deploy.prototxt.txt', 'models/res10_300x300_ssd_iter_140000.caffemodel')
                    cap = cv2.VideoCapture(aIpCam.ipcam)
                    #image = cv2.imread(aIpCam)
                    if cap.isOpened():
                        isOk, image = cap.read()
                        if isOk:
                           # (h, w) = image.shape[:2]
                           # blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
                           # net.setInput(blob)
                           # detections = net.forward()
                           # faceCount = 0
                           # for i in range(0, detections.shape[2]):
                           #     confidence = detections[0, 0, i, 2]
                           #     if confidence > 0.5:
                           #         faceCount = faceCount + 1
                            detections = detector.detect_faces(image)
                            faceCount = len(detections)
                            self.t.emit("аудитория: " + aIpCam.aname+", этаж: "+str(aIpCam.etaj)+"     кол. лиц: "+str(faceCount)+" ")
                    cap.release()


            except:
                self.t.emit(" error ")

    def stop(self):
        self.run_flag = False
        self.wait()
