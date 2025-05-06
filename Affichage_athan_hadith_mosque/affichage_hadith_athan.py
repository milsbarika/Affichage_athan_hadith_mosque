
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import *
#from PyQt5.QtCore import QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import *
import sqlite3
from unidecode import unidecode
import numpy as np
import pandas as pd
import sys
import os
from os import path
import datetime
import locale
import time
import pytz
from hijri_converter import Hijri, Gregorian
# global nomMois
# global noJours
# global nomJours
from sqliteDb import *
myFunc = SqliteDb("C:/allFiles/priere_csv.db")
global result
global article
global nomTable
global df


FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), 'C:/allFiles/affichage_hadith_athan.ui'))


class Etudiant(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(Etudiant, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)

        # self.maFenetre()
        self.selectTable()

        self.i = 0
        self.comptage2 = 0
        self.timer1 = QTimer(self)
        self.timer1.start(1000)
        self.timer1.timeout.connect(self.compteur)
        self.msg = QMessageBox()
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.afficher_le_Jours()
        timer = QTimer(self)
        timer.timeout.connect(self.displayTime)
        timer.start(1000)
 
        h = Gregorian.today().to_hijri()
        myDateH = h.day_name('ar')+" "+str(h.day)+" " + \
            h.month_name('ar')+" "+str(h.year)
        self.label_8.setText(myDateH)
   
        LaDate = QDate.currentDate().toString(Qt.DefaultLocaleLongDate)
        self.label_10.setText((LaDate.upper()))


        self.currentDate = datetime.date.today()
        myDayName = h.day_name('ar')
        dateJours = self.currentDate.strftime("%d")
        myDateM = self.currentDate.strftime("%B")
        annee = self.currentDate.strftime("%Y")

        nomMois = ""
        
        locale.setlocale(locale.LC_ALL, 'en_GB')
        myDate = datetime.date.today().strftime("%A %d %B %Y")

        if myDateM == "January":
            nomMonth = "جانفي"
        elif myDateM == "February":
            nomMonth = "فيفري"
        elif myDateM == "March":
            nomMonth = "مارس"
        elif myDateM == "April":
            nomMonth = "افريل"
        elif myDateM == "May":
            nomMonth = "ماي"
        elif myDateM == "June ":
            nomMonth = "جوان"
        elif myDateM == "July ":
            nomMonth = "جويلية"
        elif myDateM == "August":
            nomMonth = "أوت"
        elif myDateM == "September":
            nomMonth = "سبتمبر"
        elif myDateM == "October":
            nomMonth = "أكتوبر"
        elif myDateM == "November":
            nomMonth = "نوفمبر"
        elif myDateM == "December ":
            nomMonth = "ديسمبر"

        myDateAR = myDayName + " "+str(dateJours)+" "+nomMonth+" "+str(annee)
        self.label_9.setText(myDateAR)
        self.label_11.setText((myDate.upper()))

        self.minimizeButton.clicked.connect(lambda: self.showMinimized())
        self.closeButton.clicked.connect(lambda: self.close())
        
#*****************************AVEC PANDAS**********************************

    def selectTable(self):
        global df

        cnn = sqlite3.connect(r"C:/allFiles/priere_csv1.db")
        # rs=cnn.cursor()
        query = '''
        SELECT * FROM hadith
        '''
        self.dfa = pd.read_sql_query(query, cnn)
        df = self.dfa.copy()

        # **************************
    def compteur(self):
        global df
        print("")
        # print("********************************")
        # print("")
        # self.count_dict=0
        self.count_dict = len(df)
        # self.lineEdit_nb.setText(str(self.count_dict))
        # interv = int(self.lineEdit_nb.text())
        self.comptage2 = self.comptage2 + 1

        time.sleep(3)
        df_dict = df.to_dict("records")
        self.textEdit.setText(str(df_dict[self.i]["text_hadith"]))
        self.lineEdit_type.setText(str(df_dict[self.i]["type_ibada"]))
        self.lineEdit_titre.setText(str(df_dict[self.i]["titre"]))
        # print(df_dict[0]["titre"])
        self.i += 1
        if self.comptage2 == self.count_dict:
            
            self.comptage2 = 0
            self.timer1.stop()

#*************************FIN PANDAS*************************************

    def displayTime(self):
        time = QTime.currentTime()
        date = QDate.currentDate()
        temps = time.toString('hh:mm:ss')
        self.lcdNumber.display(temps)

    def afficher_le_Jours(self):
        # global nomMois
        # global noJours
        dt_mtn = datetime.datetime.now()
        mtn_tz = pytz.timezone('US/Mountain')
        dt_mtn = mtn_tz.localize(dt_mtn)

        nomMois = dt_mtn.strftime('%B')
        noJours = dt_mtn.strftime('%d')
        nomJours = dt_mtn.strftime("%A")

        resultat = myFunc.selectOne(
            "SELECT * FROM "+nomMois+" WHERE Day="+noJours+"")
        print(resultat)

        if resultat is False:
            self.msg_display("ERROR", "pas d'enregistrements!!")
            return
        # self.daytxt.setText(str(resultat[0]))
        self.fajrtxt.setText(str(resultat[1]))
        self.sunrisetxt.setText(str(resultat[2]))
        self.dhuhrtxt.setText(str(resultat[3]))
        self.asrtxt.setText(str(resultat[4]))
        self.maghribtxt.setText(str(resultat[5]))
        self.ishatxt.setText(str(resultat[6]))

def main():
    app = QApplication(sys.argv)
    window = Etudiant()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
