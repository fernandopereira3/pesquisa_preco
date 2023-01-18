import csv
import pandas as pd
import requests 
from bs4 import BeautifulSoup
import datetime
from rocketry import Rocketry
from rocketry.conds import (after_fail,after_success,hourly, daily,minutely,every)

app = Rocketry(config={'task_execution': 'async'})

def raspagem():
    zoom = requests.get('https://www.zoom.com.br/notebook/macbook-apple-pro-m1-13-8gb-ssd-256-gb-mac-os?_lc=88&searchterm=macbook%20pro')
    soup_zoom = BeautifulSoup(zoom.content, 'html.parser')
    preco = soup_zoom.find('div', class_='OfferPrice_PriceContent__MW3Ty')
    link = soup_zoom.find('div', class_='OfferCard_OfferCardFooter__9dsDN')
    enca_link = link.find('a', href=True)
    resultado = preco.find('span')
    url = enca_link.attrs['href']
    return [resultado.text, url]


@app.task(hourly) ### TAREFA DAS 6 AS 18 BACKUP DO SMB DO SERVIDOR .4
def cat_preco():
    preco = raspagem()
    now = datetime.datetime.now()
    time = now.strftime("%H:%M -- %d/%m/%Y")
    dado = open('/scripts/python/scraping/dados.csv', 'a')
    escrita = csv.writer(dado)
    escrita.writerow(['Data: ' + time,'preço: '+ preco[0],' Link: www.zoom.com.br'+preco[1]])
    #print('Data: ' + time + " Preco: " + preco[0], ' Link: www.zoom.com.br'+preco[1])
    dado.close()


if __name__ == '__main__':

    app.run()


