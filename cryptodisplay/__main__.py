"""
ZetCode PyQt5 tutorial 

In this example, we create a simple
window in PyQt5.

Author: Jan Bodnar
Website: zetcode.com 
Last edited: August 2017
"""

import sys
import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from coinmarketcap import Market

def get_currency_attribute(currency, attribute):
    attributes = Market().ticker(currency)[0]

    return attributes[attribute]

 
class CurrencyDisplay(QWidget):
 
    def __init__(self, updateTime=10):
        super().__init__()
        #self.layout = QGridLayout(self)
        self.title = 'Crypto display'
        self.updateTime = updateTime * 1000;

        self.logo_heights = {}
        self.logo_heights["btc"] = 192
        self.logo_heights["eth"] = 500

        self.initImages()
        self.initText()
        self.setWindowTitle(self.title)

        self.updateTimer = QTimer()
        self.updateTimer.timeout.connect(self.setText)
        self.updateTimer.start(self.updateTime)

        self.show()
 
    def initImages(self):
        self.geometry = app.desktop().availableGeometry()
        self.setGeometry(self.geometry)
        self.gh = self.geometry.height()
        self.gw = self.geometry.width()
 
        # Background
        bg = QLabel(self)
        bg.setPixmap(QPixmap('images/background.png'))
        
        # Bitcoin logo
        btc_logo = QLabel(self)
        btc_logo.setPixmap(QPixmap('images/bitcoin.png'))#.scaled(192, 192, Qt.KeepAspectRatio))
        btc_logo.move(self.gw/100, self.gh/2.5 - self.logo_heights["btc"]/2)
 
        # Ethereum logo
        eth_logo = QLabel(self)
        eth_logo.setPixmap(QPixmap('images/ethereum.png'))#.scaled(192, 192, Qt.KeepAspectRatio))
        eth_logo.move(self.gw/2, self.gh/2.5 - self.logo_heights["eth"]/2)



    def initText(self):
        date_font = QFont("Times", 32, QFont.Bold) 
        big_value_font = QFont("Ariel", 64, QFont.Bold) 

        self.date_lbl = QLabel(datetime.datetime.now().strftime("%B %d, %Y"), self)
        self.date_lbl.setFont(date_font)
        text_width = self.date_lbl.fontMetrics().boundingRect(self.date_lbl.text()).width()
        self.date_lbl.move(self.gw/2 - text_width/2, self.gh/30)

        self.time_lbl = QLabel(datetime.datetime.now().strftime("%H:%M"), self)
        self.time_lbl.setFont(date_font)
        text_width = self.time_lbl.fontMetrics().boundingRect(self.time_lbl.text()).width()
        self.time_lbl.move(self.gw/2 - text_width/2, self.gh/10)

        self.btc_price_lbl = QLabel("$"+get_currency_attribute('Bitcoin', 'price_usd'), self)
        self.btc_price_lbl.setFont(big_value_font)
        self.btc_price_lbl.move(self.gw/8, self.geometry.height()/3)

        self.eth_price_lbl = QLabel("$"+get_currency_attribute('Ethereum', 'price_usd'), self)
        self.eth_price_lbl.setFont(big_value_font)
        self.eth_price_lbl.move(self.gw/1.45, self.geometry.height()/3)

    def setText(self):
        self.date_lbl.setText(datetime.datetime.now().strftime("%B %d, %Y"))
        self.time_lbl.setText(datetime.datetime.now().strftime("%H:%M"))
        self.btc_price_lbl.setText("$"+get_currency_attribute('Bitcoin', 'price_usd'))
        self.eth_price_lbl.setText("$"+get_currency_attribute('Ethereum', 'price_usd'))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = CurrencyDisplay(10)
    sys.exit(app.exec_())