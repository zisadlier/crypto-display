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

def get_currency_attribute(currency, attribute, rounded_usd=False, btc=False):
    attributes = Market().ticker(currency)[0]

    if rounded_usd:
        if btc:
            return str(round(float(attributes[attribute]), 2)) + " (" + attributes['price_btc'] + ")"

        return str(round(float(attributes[attribute]), 2))

    return attributes[attribute]

def get_change_label(currency, font, window):
    price_usd = float(get_currency_attribute(currency, 'price_usd'))
    change_percent = float(get_currency_attribute(currency, 'percent_change_24h'))
    change_usd = price_usd * (change_percent/100)

    change_str = "$" + str(round(change_usd, 2)) + " (" + str(change_percent) + "%)"
    label = QLabel(change_str, window)
    label.setFont(font)
    if float(change_percent) >= 0:
        label.setText("+ " + change_str)
        label.setStyleSheet('color: #32CD32')
    else:
        label.setText("- " + change_str)
        label.setStyleSheet('color: #F00')

    return label

def get_regular_label(text, font, window):
    label = QLabel(text, window)
    label.setFont(font)
    label.setStyleSheet('color: #000')

    return label

def update_change_label(label, currency):
    price_usd = float(get_currency_attribute(currency, 'price_usd'))
    change_percent = float(get_currency_attribute(currency, 'percent_change_24h'))
    change_usd = price_usd * (change_percent/100)

    change_str = "$" + str(round(change_usd, 2)) + " (" + str(change_percent) + "%)"

    label.setText(change_str)
    if float(change_percent) >= 0:
        label.setText("+ " + change_str)
        label.setStyleSheet('color: #32CD32')
    else:
        label.setText("- " + change_str)
        label.setStyleSheet('color: #F00')

class CurrencyDisplay(QWidget):
 
    def __init__(self, app, altcoin_size=150, update_time=10, size_ratio=1):
        super().__init__()
        self.title = 'Crypto display'
        self.update_time = update_time * 1000;
        self.size_ratio = size_ratio
        self.altcoin_size = altcoin_size * size_ratio
        self.app = app

        self.logo_sizes = {}
        self.logo_sizes["btc"] = 192 * self.size_ratio
        self.logo_sizes["eth"] = 500 * self.size_ratio

        self.altcoin_logos = []
        self.altcoin_prices = []
        self.altcoin_changes = []

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
        self.spacing = self.gw/3
 
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

        # Altcoin logos
        for i, altcoin in enumerate(ALTCOINS):
            alt_label = QLabel(self)
            alt_label.setPixmap(QPixmap(os.path.join(IMAGE_DIR, altcoin.lower()+'.png')).scaled(self.altcoin_size, self.altcoin_size, Qt.KeepAspectRatio))
            alt_label.move(self.gw/100 + i*self.spacing, self.gh/1.15 - self.altcoin_size/2) 
            self.altcoin_logos.append(alt_label)


    def initText(self):
        # Font declarations
        date_font = QFont("Times", 48 * self.size_ratio, QFont.Bold) 
        big_value_font = QFont("Ariel", 64 * self.size_ratio, QFont.Bold)
        small_value_font = QFont("Ariel", 24 * self.size_ratio, QFont.Bold)
        change_font = QFont("Ariel", 28 * self.size_ratio, QFont.Bold)  
        small_change_font = QFont("Ariel", 16 * self.size_ratio, QFont.Bold)  

        # Date and time labels
        self.date_lbl = get_regular_label(datetime.datetime.now().strftime("%B %d, %Y"), date_font, self)
        text_width = self.date_lbl.fontMetrics().boundingRect(self.date_lbl.text()).width()
        self.date_lbl.move(self.gw/2 - text_width/2, self.gh/30)

        self.time_lbl = get_regular_label(datetime.datetime.now().strftime("%H:%M"), date_font, self)
        text_width = self.time_lbl.fontMetrics().boundingRect(self.time_lbl.text()).width()
        self.time_lbl.move(self.gw/2 - text_width/2, self.gh/8)

        # BTC labels
        self.btc_price_lbl = get_regular_label("$"+get_currency_attribute('Bitcoin', 'price_usd', rounded_usd=True), big_value_font, self)
        self.btc_price_lbl.move(self.gw/6, self.geometry.height()/3)

        self.btc_change_lbl = get_change_label('Bitcoin', change_font, self)
        self.btc_change_lbl.move(self.gw/6, self.geometry.height()/2.2)

        # ETH labels
        self.eth_price_lbl = get_regular_label("$"+get_currency_attribute('Ethereum', 'price_usd', rounded_usd=True), big_value_font, self)
        self.eth_price_lbl.move(self.gw/1.47, self.geometry.height()/3)

        self.eth_change_lbl = get_change_label('Ethereum', change_font, self)
        self.eth_change_lbl.move(self.gw/1.47, self.geometry.height()/2.2)

        # Altcoin labels
        for i, altcoin in enumerate(ALTCOINS):
            alt_price_lbl = get_regular_label("$"+get_currency_attribute(altcoin, 'price_usd', rounded_usd=True, btc=True), small_value_font, self)
            alt_price_lbl.move(self.gw/10 + i*self.spacing, self.geometry.height()/1.25)
            alt_change_lbl = get_change_label(altcoin, small_change_font, self)
            alt_change_lbl.move(self.gw/10 + i*self.spacing, self.geometry.height()/1.15)

            self.altcoin_prices.append(alt_price_lbl)
            self.altcoin_changes.append(alt_change_lbl)

    def setText(self):
        self.date_lbl.setText(datetime.datetime.now().strftime("%B %d, %Y"))
        self.time_lbl.setText(datetime.datetime.now().strftime("%H:%M"))
        self.btc_price_lbl.setText("$"+get_currency_attribute('Bitcoin', 'price_usd'))
        self.eth_price_lbl.setText("$"+get_currency_attribute('Ethereum', 'price_usd'))
        update_change_label(self.btc_change_lbl, 'Bitcoin')
        update_change_label(self.eth_change_lbl, 'Ethereum')


def main():
    app = QApplication(sys.argv)
    ex = CurrencyDisplay(app, altcoin_size=ALTCOIN_SIZE, size_ratio=SIZE_RATIO, update_time=UPDATE_TIME)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()