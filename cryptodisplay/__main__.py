"""
Crypto Display
"""

import sys
import datetime
import os

from config import *

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from coinmarketcap import Market

def get_currency_attribute(currency, attribute):
    attributes = Market().ticker(currency)[0]

    return attributes[attribute]

def get_change_label(currency, window):
    price_usd = float(get_currency_attribute(currency, 'price_usd'))
    change_percent = float(get_currency_attribute(currency, 'percent_change_24h'))
    change_usd = price_usd * (change_percent/100)

    change_str = "$" + str(round(change_usd, 2)) + " (" + str(change_percent) + "%)"

    label = QLabel(change_str, window)
    if float(change_percent) >= 0:
        label.setStyleSheet('color: #32CD32')
    else:
        label.setStyleSheet('color: #F00')

    return label
 
class CurrencyDisplay(QWidget):
 
    def __init__(self, app, update_time=10, size_ratio=1):
        super().__init__()
        #self.layout = QGridLayout(self)
        self.title = 'Crypto display'
        self.update_time = update_time * 1000;
        self.size_ratio = size_ratio
        self.app = app

        self.logo_sizes = {}
        self.logo_sizes["btc"] = 192 * self.size_ratio
        self.logo_sizes["eth"] = 500 * self.size_ratio

        self.initImages()
        self.initText()
        self.setWindowTitle(self.title)

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.setText)
        self.update_timer.start(self.update_time)

        self.show()
 
    def initImages(self):
        self.geometry = self.app.desktop().availableGeometry()
        self.setGeometry(self.geometry)
        self.gh = self.geometry.height()
        self.gw = self.geometry.width()
 
        # Background
        bg = QLabel(self)
        bg.setPixmap(QPixmap(os.path.join(IMAGE_DIR, 'background.png')).scaled(self.gw, self.gh))
        
        # Bitcoin logo
        btc_logo = QLabel(self)
        btc_logo.setPixmap(QPixmap(os.path.join(IMAGE_DIR, 'bitcoin.png')).scaled(self.logo_sizes["btc"], self.logo_sizes["btc"], Qt.KeepAspectRatio))
        btc_logo.move(self.gw/100, self.gh/2.5 - self.logo_sizes["btc"]/2)
 
        # Ethereum logo
        eth_logo = QLabel(self)
        eth_logo.setPixmap(QPixmap(os.path.join(IMAGE_DIR, 'ethereum.png')).scaled(self.logo_sizes["eth"], self.logo_sizes["eth"], Qt.KeepAspectRatio))
        eth_logo.move(self.gw/2.2, self.gh/2.5 - self.logo_sizes["eth"]/2)



    def initText(self):

        date_font = QFont("Times", 48 * self.size_ratio, QFont.Bold) 
        big_value_font = QFont("Ariel", 64 * self.size_ratio, QFont.Bold)
        change_font = QFont("Ariel", 24 * self.size_ratio, QFont.Bold)  

        # Date and time labels
        self.date_lbl = QLabel(datetime.datetime.now().strftime("%B %d, %Y"), self)
        self.date_lbl.setFont(date_font)
        self.date_lbl.setStyleSheet('color: #000')
        text_width = self.date_lbl.fontMetrics().boundingRect(self.date_lbl.text()).width()
        self.date_lbl.move(self.gw/2 - text_width/2, self.gh/30)

        self.time_lbl = QLabel(datetime.datetime.now().strftime("%H:%M"), self)
        self.time_lbl.setFont(date_font)
        self.time_lbl.setStyleSheet('color: #000')
        text_width = self.time_lbl.fontMetrics().boundingRect(self.time_lbl.text()).width()
        self.time_lbl.move(self.gw/2 - text_width/2, self.gh/8)

        # BTC labels
        self.btc_price_lbl = QLabel("$"+get_currency_attribute('Bitcoin', 'price_usd'), self)
        self.btc_price_lbl.setFont(big_value_font)
        self.btc_price_lbl.setStyleSheet('color: #000')
        self.btc_price_lbl.move(self.gw/6, self.geometry.height()/3)

        self.btc_change_lbl = get_change_label('Bitcoin', self)
        self.btc_change_lbl.setFont(change_font)
        text_width = self.btc_change_lbl.fontMetrics().boundingRect(self.btc_change_lbl.text()).width()
        self.btc_change_lbl.move(self.gw/6 + text_width/4, self.geometry.height()/2.25)

        # ETH labels
        self.eth_price_lbl = QLabel("$"+get_currency_attribute('Ethereum', 'price_usd'), self)
        self.eth_price_lbl.setFont(big_value_font)
        self.eth_price_lbl.setStyleSheet('color: #000')
        self.eth_price_lbl.move(self.gw/1.47, self.geometry.height()/3)

        self.eth_change_lbl = get_change_label('Ethereum', self)
        self.eth_change_lbl.setFont(change_font)
        text_width = self.eth_change_lbl.fontMetrics().boundingRect(self.eth_change_lbl.text()).width()
        self.eth_change_lbl.move(self.gw/1.47 + text_width/4, self.geometry.height()/2.25)

    def setText(self):
        self.date_lbl.setText(datetime.datetime.now().strftime("%B %d, %Y"))
        self.time_lbl.setText(datetime.datetime.now().strftime("%H:%M"))
        self.btc_price_lbl.setText("$"+get_currency_attribute('Bitcoin', 'price_usd'))
        self.eth_price_lbl.setText("$"+get_currency_attribute('Ethereum', 'price_usd'))


def main():
    app = QApplication(sys.argv)
    ex = CurrencyDisplay(app, size_ratio=SIZE_RATIO, update_time=UPDATE_TIME)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()