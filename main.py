import sys

import numpy as np
from Runnable import Runnable
from PyQt6.QtCore import  QThreadPool, pyqtSignal, pyqtSlot
import ui.dialogAddAuditoriya
from ui.MainWindow import Ui_MainWindow
from ui.DialogAddZdanie import Ui_Dialog
from PyQt6.QtWidgets import \
    (
    QApplication,
    QMainWindow,
    QMessageBox,
    QDialog,
    QTableWidgetItem,
    QInputDialog,
)

from Database.MyDatabase import Database


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("FaceCounter")
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.showMaximized()

        self.tableWidget.clear()
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.hideColumn(0)
        self.tableWidget.hideColumn(1)
        self.tableWidget.setHorizontalHeaderLabels(
            ['1', '2', 'Названия аудитории', 'Этаж', 'Описания аудитории', ' IP камера', 'Состояния'])

        self.mydb = Database()
        self.z_id_Zdaniye = []
        self.selectAllZdaniye()
        self.selectAllAuditoriya()

        self.pushBtn.clicked.connect(self.btn_click)
        self.pushButton.clicked.connect(self.btn_click_showAddAuditoriya)
        self.pushBtnDeleteAuditoriya.clicked.connect(self.deleteAuditoriyaById)
        self.comboBox.currentIndexChanged.connect(self.comboBoxSelectedIndexChanged)
        self.comboBox_Etaj.currentIndexChanged.connect(self.comboBoxEtajSelectedIndexChanged)
        self.tableWidget.itemDoubleClicked.connect(self.updateCellInTable)
        self.actionExit.triggered.connect(self.exitProgram)
        self.pushBtn_Start.clicked.connect(self.startWoker)

        # to run threads
        self.run_woker = True
        self.threadCount = QThreadPool.globalInstance().maxThreadCount()
        self.Threads = [0]*self.threadCount

    def comboBoxSelectedIndexChanged(self):
        print("list: ", self.z_id_Zdaniye)
        print("ok ", self.z_id_Zdaniye[self.comboBox.currentIndex() - 1])
        print("self.comboBox.currentIndex() ", self.comboBox.currentIndex())
        z_id = self.z_id_Zdaniye[self.comboBox.currentIndex() - 1]

        if self.comboBox.currentIndex() == 0:
            result = self.mydb.selectAllAuditoriya()
        else:
            result = self.mydb.selectAuditoriyaByZ_Id(z_id)

        self.tableWidget.setRowCount(len(result))
        i = 0
        for row in result:
            self.tableWidget.setItem(i, 0, QTableWidgetItem(str(row.id)))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(row.z_id)))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(row.aname))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(str(row.etaj)))
            self.tableWidget.setItem(i, 4, QTableWidgetItem(row.descr))
            self.tableWidget.setItem(i, 5, QTableWidgetItem(row.ipcam))
            self.tableWidget.setItem(i, 6, QTableWidgetItem(str(row.do_surv)))
            i = i + 1
        self.label_Zdaniye.setText(self.comboBox.currentText())

    def comboBoxEtajSelectedIndexChanged(self):
        z_id = self.z_id_Zdaniye[self.comboBox.currentIndex() - 1]
        etaj = self.comboBox_Etaj.currentText()

        if self.comboBox.currentIndex() == 0:
            result = self.mydb.selectAllAuditoriya()
        else:
            result = self.mydb.selectAuditoriyaByZ_Id_and_Etaj(z_id, etaj=etaj)

        self.tableWidget.setRowCount(len(result))
        i = 0
        for row in result:
            self.tableWidget.setItem(i, 0, QTableWidgetItem(str(row.id)))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(row.z_id)))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(row.aname))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(str(row.etaj)))
            self.tableWidget.setItem(i, 4, QTableWidgetItem(row.descr))
            self.tableWidget.setItem(i, 5, QTableWidgetItem(row.ipcam))
            self.tableWidget.setItem(i, 6, QTableWidgetItem(str(row.do_surv)))
            i = i + 1

    def selectAllZdaniye(self):
        result = self.mydb.selectAllZdaniye()
        self.comboBox.clear()
        self.comboBox.addItem('Все здания')
        self.z_id_Zdaniye.clear()
        for row in result:
            self.comboBox.addItem(row.zname)
            self.z_id_Zdaniye.append(row.id)

    def selectAllAuditoriya(self):
        result = self.mydb.selectAllAuditoriya()

        self.tableWidget.setRowCount(len(result))
        i = 0
        for row in result:
            self.tableWidget.setItem(i, 0, QTableWidgetItem(str(row.id)))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(row.z_id)))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(row.aname))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(str(row.etaj)))
            self.tableWidget.setItem(i, 4, QTableWidgetItem(row.descr))
            self.tableWidget.setItem(i, 5, QTableWidgetItem(row.ipcam))
            self.tableWidget.setItem(i, 6, QTableWidgetItem(str(row.do_surv)))
            i = i + 1

        self.tableWidget.setColumnWidth(0, 10)
        self.tableWidget.setColumnWidth(1, 10)
        self.tableWidget.setColumnWidth(2, 200)
        self.tableWidget.setColumnWidth(3, 60)
        self.tableWidget.setColumnWidth(4, 250)

    def updateCellInTable(self):
        id = int(self.tableWidget.item(self.tableWidget.selectionModel().currentIndex().row(), 0).text())
        colIndex = self.tableWidget.selectionModel().currentIndex().column()
        s = str(self.tableWidget.item(self.tableWidget.selectionModel().currentIndex().row(), colIndex).text())
        print(colIndex)
        text, ok = QInputDialog.getText(self, 'Значение', 'Введите значение:', text=s)
        if ok:
            b = self.mydb.updateAuditoriya(id, colIndex, str(text))
            if b:
                self.tableWidget.setItem(self.tableWidget.selectionModel().currentIndex().row(), colIndex,
                                         QTableWidgetItem(str(text)))

    def btn_click(self):
        dlg = AddZdanie()
        dlg.exec()
        self.selectAllZdaniye()

    def btn_click_showAddAuditoriya(self):
        dlg = AddAuditoriya()
        if dlg.exec():
            z_id = int(dlg.id[dlg.comboBoxZdaniye.currentIndex()])
            aname = dlg.lineEditAuditoriya.text()
            etaj = dlg.comboBoxEtaj.currentText()
            descr = dlg.lineEditDescription.text()
            ipcam = dlg.lineEditIPCamera.text()
            do_surv = int(0)
            if dlg.checkBoxDO_Surv.isChecked():
                do_surv = int(1)
            self.mydb.insertAuditoriya(z_id=z_id, aname=aname, etaj=etaj, descr=descr, ipcam=ipcam, do_surv=do_surv)
        self.selectAllAuditoriya()

    def startWoker(self):
        allAuditoriya = self.mydb.selectAllAuditoriya()
        divCamCount = len(allAuditoriya)/self.threadCount
        groupsIpCam = [allAuditoriya[i:i + int(len(allAuditoriya)/divCamCount)] for i in range(0, len(allAuditoriya), int(len(allAuditoriya)/divCamCount))]
        #print(len(groupsIpCam))
        #return

        if self.run_woker:
            for i in range(len(groupsIpCam)):  # len(groupsIpCam)<=self.threadCount !!!!
                self.ipCams = groupsIpCam[i] #['rtsp://admin:Qwerty123@192.168.1.64:554/Streaming/Channels/1']
                self.Threads[i] = Runnable(self.ipCams)
                self.Threads[i].t.connect(self.update_t)
                self.Threads[i].start()
            self.run_woker = False
            self.pushBtn_Start.setText('Стоп')
        else:
            try:
                for i in range(len(groupsIpCam)):
                    self.Threads[i].run_flag = False
                self.run_woker = True
                self.pushBtn_Start.setText('Старт')
            except IndexError:
                print('Index error')
            except:
                print('other error')


    @pyqtSlot(str)
    def update_t(self, s):
        self.textEdit.append(s+"\n")
        # self.textEdit.setText(self.textEdit.toPlainText()+"Кол. лиц: "+s)
        #if self.textEdit.>4:
        #    self.textEdit.clear()

    def exitProgram(self):
        msgBox = QMessageBox()
        # msgBox.setIcon(QMessageBox.Icon.Information)
        msgBox.setText("Вы действительно хотите выйти из приложения?")
        msgBox.setWindowTitle("Выход из приложения")
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.StandardButton.Ok:
            self.close()

    def deleteAuditoriyaById(self):
        if len(self.tableWidget.selectedItems()) > 0:
            id = int(self.tableWidget.item(self.tableWidget.currentItem().row(), 0).text())
            print(id)
            if id > 0:
                msgBox = QMessageBox()
                # msgBox.setIcon(QMessageBox.Icon.Information)
                msgBox.setText("Вы действительно хотите удалить?")
                msgBox.setWindowTitle("Удаление")
                msgBox.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

                returnValue = msgBox.exec()
                if returnValue == QMessageBox.StandardButton.Ok:
                    self.mydb.deleteAuditoriya(id)
                    self.selectAllAuditoriya()


class AddZdanie(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.insertZdaniye)
        self.pushButton_2.clicked.connect(self.deleteZdaniyeById)
        self.tableWidget.itemDoubleClicked.connect(self.updateCellInTable)

        self.mydb = Database()
        self.selectAllZdaniye()

    def selectAllZdaniye(self):
        result = self.mydb.selectAllZdaniye()

        self.tableWidget.clear()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(3)
        self.tableWidget.hideColumn(0)
        self.tableWidget.setHorizontalHeaderLabels(['1', 'Названия аудитории', 'Описания аудитории'])
        i = 0
        for row in result:
            self.tableWidget.setItem(i, 0, QTableWidgetItem(str(row.id)))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(row.zname))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(row.descr))
            i = i + 1
        self.tableWidget.setColumnWidth(1, 260)
        self.tableWidget.setColumnWidth(2, 340)

    def insertZdaniye(self):
        if len(str(self.lineEdit.text()).strip()) > 0:
            self.mydb.insertZdaniye(str(self.lineEdit.text().strip()), str(self.lineEdit_2.text()).strip())
        self.selectAllZdaniye()

    def deleteZdaniyeById(self):
        if len(self.tableWidget.selectedItems()) > 0:
            id = int(self.tableWidget.item(self.tableWidget.currentItem().row(), 0).text())

            if id > 0:
                msgBox = QMessageBox()
                # msgBox.setIcon(QMessageBox.Icon.Information)
                msgBox.setText("Вы действительно хотите удалить?")
                msgBox.setWindowTitle("Удаление")
                msgBox.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

                returnValue = msgBox.exec()
                if returnValue == QMessageBox.StandardButton.Ok:
                    self.mydb.deleteZdaniye(id)
                self.selectAllZdaniye()

    def updateCellInTable(self):
        id = int(self.tableWidget.item(self.tableWidget.selectionModel().currentIndex().row(), 0).text())
        colIndex = self.tableWidget.selectionModel().currentIndex().column()
        s = str(self.tableWidget.item(self.tableWidget.selectionModel().currentIndex().row(), colIndex).text())
        print(colIndex)
        text, ok = QInputDialog.getText(self, 'Значение', 'Введите значение:', text=s)
        if ok:
            print('ok')
            b = self.mydb.updateZdaniye(id, colIndex, str(text))
            if b:
                self.tableWidget.setItem(self.tableWidget.selectionModel().currentIndex().row(), colIndex,
                                         QTableWidgetItem(str(text)))


class AddAuditoriya(QDialog, ui.dialogAddAuditoriya.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.pushButton.clicked.connect(self.insertZdaniye)
        # self.pushButton_2.clicked.connect(self.deleteZdaniyeById)

        self.mydb = Database()
        result = self.mydb.selectAllZdaniye()
        self.comboBoxZdaniye.clear()
        self.id = []
        for row in result:
            self.comboBoxZdaniye.addItem(row.zname)
            self.id.append(int(row.id))


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
