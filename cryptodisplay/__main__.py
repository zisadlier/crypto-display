"""
Crypto Display
"""

import sys
import datetime
import os
import requests

from config import *

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from coinmarketcap import Market
from bs4 import BeautifulSoup

def get_weather_text(zipcode):
    page = requests.get('https://weather.com/weather/today/l/'+str(zipcode)+':4:US')
    soup = BeautifulSoup(page.content, 'html5lib')
    weather_str = ''
    
    temp_tag = soup.find('div', class_='today_nowcard-temp')
    if temp_tag is not None:
        weather_str += temp_tag.get_text() + '\n'
    phrase_tag = soup.find('div', class_='today_nowcard-phrase')
    if phrase_tag is not None:
        weather_str += phrase_tag.get_text() + '\n'
    location_tag = soup.find('h1', class_='today_nowcard-location')
    if location_tag is not None:
        loc = location_tag.get_text()
        weather_str += loc[:loc.find('(')] + '\n'

    return weather_str

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

    change_str = "$" + str(round(abs(change_usd), 2)) + " (" + str(abs(change_percent)) + "%)"
    label = QLabel(change_str, window)
    label.setFont(font)
    if float(change_percent) >= 0:
        label.setText("+ " + change_str)
        label.setStyleSheet('color: #32CD32')
    else:
        label.setText("- " + change_str)
        label.setStyleSheet('color: #F00')

    return label

def get_regular_label(text, font, color_code, window):
    label = QLabel(text, window)
    label.setFont(font)
    label.setStyleSheet('color: #' + color_code)

    return label

def update_change_label(label, currency):
    price_usd = float(get_currency_attribute(currency, 'price_usd'))
    change_percent = float(get_currency_attribute(currency, 'percent_change_24h'))
    change_usd = price_usd * (change_percent/100)

    change_str = "$" + str(round(abs(change_usd), 2)) + " (" + str(abs(change_percent)) + "%)"

    label.setText(change_str)
    if float(change_percent) >= 0:
        label.setText("+ " + change_str)
        label.setStyleSheet('color: #32CD32')
    else:
        label.setText("- " + change_str)
        label.setStyleSheet('color: #F00')

def clear_update_alts(window):
    for logo in window.altcoin_logos:
        logo.deleteLater()
        logo = None

    for price in window.altcoin_prices:
        price.deleteLater()
        price = None

    for change in window.altcoin_changes:
        change.deleteLater()
        change = None

    window.altcoin_logos = []
    window.altcoin_prices = []
    window.altcoin_changes = []

    num_sets = int(window.num_alts/window.alts_per_set)
    leftover = window.num_alts % window.alts_per_set

    if leftover:
        num_sets += 1
    else:
        leftover = window.alts_per_set

    if window.current_alt_set == num_sets:
        window.current_alt_set = 1
        window.current_alts = ALTCOINS[:window.alts_per_set]
    elif window.current_alt_set == num_sets - 1:
        index = window.alts_per_set * window.current_alt_set
        window.current_alts = ALTCOINS[index:index + leftover]
        window.current_alt_set += 1
    else:
        index = window.alts_per_set * window.current_alt_set
        window.current_alts = ALTCOINS[index:index + window.alts_per_set]
        window.current_alt_set += 1

class CurrencyDisplay(QWidget):
 
    def __init__(self, app, altcoin_size=150, update_time=10, size_ratio=1):
        super().__init__()
        self.title = 'Crypto display'
        self.update_time = update_time * 1000;
        self.size_ratio = size_ratio
        self.altcoin_size = altcoin_size * size_ratio
        self.app = app
        self.alts_per_set = 3
        self.num_alts = len(ALTCOINS)
        self.current_alt_set = 1
        self.current_alts = []
        self.single_set = True

        self.btc_size = 192 * self.size_ratio
        self.eth_size = 500 * self.size_ratio

        if self.num_alts > self.alts_per_set:
            self.current_alts = ALTCOINS[:self.alts_per_set]
            self.single_set = False
        else:
            self.current_alts = ALTCOINS[:self.num_alts]

        self.altcoin_logos = []
        self.altcoin_prices = []
        self.altcoin_changes = []

        self.initImages()
        self.initText()
        self.setWindowTitle(self.title)

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update)
        self.update_timer.start(self.update_time)

        self.show()
 
    def initImages(self, only_alts=False):
 
        if not only_alts:
            self.geometry = self.app.desktop().availableGeometry()
            self.setGeometry(self.geometry)
            self.gh = self.geometry.height()
            self.gw = self.geometry.width()
            self.spacing = self.gw/3

            # Background
            bg = QLabel(self)
            bg.setPixmap(QPixmap(os.path.join(IMAGE_DIR, 'background.png')).scaled(self.gw, self.gh))

            banner = QLabel(self)
            banner.setPixmap(QPixmap(os.path.join(IMAGE_DIR, 'banner.png')).scaled(self.gw, self.gh/5))          
            banner.move(0, self.gh/1.3)        
        
            # Bitcoin logo
            btc_logo = QLabel(self)
            btc_logo.setPixmap(QPixmap(os.path.join(IMAGE_DIR, 'bitcoin.png')).scaled(self.btc_size, self.btc_size, Qt.KeepAspectRatio))
            btc_logo.move(self.gw/100, self.gh/2.5 - self.btc_size/2)
 
            # Ethereum logo
            eth_logo = QLabel(self)
            eth_logo.setPixmap(QPixmap(os.path.join(IMAGE_DIR, 'ethereum.png')).scaled(self.eth_size, self.eth_size, Qt.KeepAspectRatio))
            eth_logo.move(self.gw/2.2, self.gh/2.5 - self.eth_size/2)

        # Altcoin logos
        for i, altcoin in enumerate(self.current_alts):
            alt_label = QLabel(self)
            alt_label.setPixmap(QPixmap(os.path.join(IMAGE_DIR, altcoin.lower()+'.png')).scaled(self.altcoin_size, self.altcoin_size, Qt.KeepAspectRatio))
            alt_label.move(self.gw/100 + i*self.spacing, self.gh/1.15 - self.altcoin_size/2)
            alt_label.show()
            self.altcoin_logos.append(alt_label)


    def initText(self, only_alts=False):
        # Font declarations
        date_font = QFont("Times", 48 * self.size_ratio, QFont.Bold)
        big_value_font = QFont("Ariel", 64 * self.size_ratio, QFont.Bold)
        small_value_font = QFont("Ariel", 24 * self.size_ratio, QFont.Bold)
        change_font = QFont("Ariel", 28 * self.size_ratio, QFont.Bold)  
        small_change_font = QFont("Ariel", 16 * self.size_ratio, QFont.Bold)  

        if not only_alts:
            # Date and time labels
            self.date_lbl = get_regular_label(datetime.datetime.now().strftime("%B %d, %Y"), date_font, '101261', self)
            text_width = self.date_lbl.fontMetrics().boundingRect(self.date_lbl.text()).width()
            self.date_lbl.move(self.gw/3 - text_width/2, self.gh/30)

            self.time_lbl = get_regular_label(datetime.datetime.now().strftime("%H:%M"), big_value_font, '101261', self)
            text_width = self.time_lbl.fontMetrics().boundingRect(self.time_lbl.text()).width()
            self.time_lbl.move(self.gw/3 - text_width/2, self.gh/8)

            # Weather labels
            self.weather_lbl = get_regular_label(get_weather_text(ZIPCODE), change_font, '101261', self)
            self.weather_lbl.move(self.gw/1.5, self.gh/15)

            # BTC labels
            self.btc_price_lbl = get_regular_label("$"+get_currency_attribute('Bitcoin', 'price_usd', rounded_usd=True), big_value_font, '000', self)
            self.btc_price_lbl.move(self.gw/6, self.geometry.height()/3)

            self.btc_change_lbl = get_change_label('Bitcoin', change_font, self)
            self.btc_change_lbl.move(self.gw/6, self.geometry.height()/2.2)

            # ETH labels
            self.eth_price_lbl = get_regular_label("$"+get_currency_attribute('Ethereum', 'price_usd', rounded_usd=True), big_value_font, '000', self)
            self.eth_price_lbl.move(self.gw/1.47, self.geometry.height()/3)

            self.eth_change_lbl = get_change_label('Ethereum', change_font, self)
            self.eth_change_lbl.move(self.gw/1.47, self.geometry.height()/2.2)

        # Altcoin labels
        for i, altcoin in enumerate(self.current_alts):
            alt_price_lbl = get_regular_label("$"+get_currency_attribute(altcoin, 'price_usd', rounded_usd=True, btc=True), small_value_font, 'FFF', self)
            alt_price_lbl.move(self.gw/9 + i*self.spacing, self.geometry.height()/1.25)
            alt_change_lbl = get_change_label(altcoin, small_change_font, self)
            alt_change_lbl.move(self.gw/9 + i*self.spacing, self.geometry.height()/1.15)

            alt_price_lbl.show()
            alt_change_lbl.show()

            self.altcoin_prices.append(alt_price_lbl)
            self.altcoin_changes.append(alt_change_lbl)


    def update(self):
        self.date_lbl.setText(datetime.datetime.now().strftime("%B %d, %Y"))
        self.time_lbl.setText(datetime.datetime.now().strftime("%H:%M"))
        self.btc_price_lbl.setText("$"+get_currency_attribute('Bitcoin', 'price_usd'))
        self.eth_price_lbl.setText("$"+get_currency_attribute('Ethereum', 'price_usd'))
        self.weather_lbl.setText(get_weather_text(ZIPCODE))
        update_change_label(self.btc_change_lbl, 'Bitcoin')
        update_change_label(self.eth_change_lbl, 'Ethereum')

        clear_update_alts(self)

        if self.single_set:
            for i, altcoin_price in enumerate(self.altcoin_prices):
                altcoin_price.setText("$"+get_currency_attribute(self.current_alts[i], 'price_usd', rounded_usd=True, btc=True))

            for i, altcoin_change in enumerate(self.altcoin_changes):
                update_change_label(altcoin_change, self.current_alts[i])
        else:
            self.initImages(only_alts=True)
            self.initText(only_alts=True)

def main():
    app = QApplication(sys.argv)
    ex = CurrencyDisplay(app, altcoin_size=ALTCOIN_SIZE, size_ratio=SIZE_RATIO, update_time=UPDATE_TIME)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()