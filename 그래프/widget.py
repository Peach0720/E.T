# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 19:12:29 2022

@author: mcxru
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 18:33:52 2022

@author: mcxru
"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvas as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import pymysql
import pandas as pd
import matplotlib.pyplot as plt

class MyApp(QMainWindow):

  def __init__(self):
      super().__init__()

      self.main_widget = QWidget()
      self.setCentralWidget(self.main_widget)

      canvas = FigureCanvas(Figure(figsize=(11, 8)))
      vbox = QVBoxLayout(self.main_widget)
      vbox.addWidget(canvas)

      self.addToolBar(NavigationToolbar(canvas, self))
      myMyConn = pymysql.connect(user='SW', password='1234', host = '203.234.62.112',port = 3306 ,charset='utf8mb4', database='stock')
      
      sql = """
              select *
              from ohlcv

      
          """

      df = pd.read_sql(sql, myMyConn)
      samsung = df[df['Ticker']=='066570']
      samsung_close = samsung['Close']
      samsung_close.index = samsung['Date']
      
      self.ax = canvas.figure.subplots()
      self.ax.plot(samsung_close)
      
      self.setWindowTitle('Matplotlib in PyQt5')
      self.setGeometry(300, 100, 600, 400)
      self.show()

if __name__ == '__main__':
  app = QApplication(sys.argv)
  ex = MyApp()
  sys.exit(app.exec_())