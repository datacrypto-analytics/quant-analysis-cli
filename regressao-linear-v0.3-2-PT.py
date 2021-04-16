#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Felipe Soares
"""
import requests
import json
import random
import talib
import pandas as pd
import datetime as dt
from matplotlib import pyplot as plt
import pyfiglet

ascii_banner = pyfiglet.figlet_format("DataCrypto Analytics")
print(ascii_banner)
#########################################################################################
#=========  Esolhe a Criptomoedas e valores de negociação
########################################################################################
criptomoeda = input(' | Algoritmo: Regressão Linear '
					'\n | Versão: v0.3-2-PT ' 
                    '\n\n | Twitter @DataCryptoML '
                    '\n | Github @datacrypto-analytics '
					'\n | https://datacryptoanalytics.com/ '
                    '\n \nDigite o par de criptomoedas listada na Binance: ')

print('O par de criptomoeda informada foi: %s' %(criptomoeda))
#######################################################################################
#========   Cria URL da API Binance
#######################################################################################
root_url = 'https://api.binance.com/api/v1/klines'
symbol = criptomoeda
interval = input('Digite o Timeframe (Exemplo: 15m, 30m, 1h, 1d, 1M): ')
url = root_url + '?symbol=' + symbol + '&interval=' + interval
#print(url)
#######################################################################################
#========   Monta URL e o Gráfico e DataFrame
#######################################################################################
def get_bars(symbol, interval = interval):
   url = root_url + '?symbol=' + symbol + '&interval=' + interval
   data = json.loads(requests.get(url).text)
   df = pd.DataFrame(data)
   df.columns = ['open_time',
                 'o', 'h', 'l', 'c', 'v',
                 'close_time', 'qav', 'num_trades',
                 'taker_base_vol', 'taker_quote_vol', 'ignore']
   df.index = [dt.datetime.fromtimestamp(x/1000.0) for x in df.close_time]
   return df
#######################################################################################
#========   Organizando Variaveis
#######################################################################################
criptomoeda = get_bars(criptomoeda)
criptomoeda_fechamento = criptomoeda['c'].astype('float').values
criptomoeda_close = criptomoeda['c'].astype('float')
criptomoeda_abertura = criptomoeda['o'].astype('float').values
criptomoeda_num_trades = criptomoeda['num_trades'].astype('float')
criptomoeda_maxima = criptomoeda['h'].astype('float')
criptomoeda_minima = criptomoeda['l'].astype('float')
criptomoeda_volume = criptomoeda['v'].astype('float')
criptomoeda_datas_fechamento = criptomoeda['close_time'].astype('float')
criptomoeda_datas_abertura = criptomoeda['open_time'].astype('float')
taker_base_vol = criptomoeda['taker_base_vol'].astype('float')
taker_quote_vol = criptomoeda['taker_quote_vol'].astype('float')
closeprice = criptomoeda_close.iloc[-1]
cci = talib.CCI(criptomoeda_maxima, criptomoeda_minima, criptomoeda_close, timeperiod=14)
atr = talib.ATR(criptomoeda_maxima, criptomoeda_minima, criptomoeda_close, timeperiod=14)

midpoint = talib.MIDPOINT(criptomoeda_close, timeperiod=30)

sma6 = talib.SMA(criptomoeda_close, timeperiod=6)
sma9 = talib.SMA(criptomoeda_close, timeperiod=9)

real = talib.T3(criptomoeda_close, timeperiod=14)
print('________________________________________________________________________________')
print('\n \n Preço de Fechamento: $%.2f'%(closeprice))

from tqdm import tqdm 
from time import sleep 
for i in tqdm(range(0, 100), desc =" DataCrypto Analytics recuperando dados"): 
    sleep(.1) 
#print('\n \n DataCrypto Analytics buscando dados...'
#	  '\n Aguarde alguns segundos, algoritmo treinando e fazendo previsões!')
for i in tqdm(range(0, 100), desc =" Algoritmo treinando com dados recuperados"): 
    sleep(.2) 

for i in tqdm(range(0, 100), desc =" Aguarde mais alguns segundos. Algoritmo fazendo previsões"): 
    sleep(.5) 


#######################################################################################
# Média movel de 14 dias do Fechamento
#######################################################################################
criptomoeda_fechamento_mediamovel = criptomoeda['c'].rolling(30).mean()
#######################################################################################
# Média movel de 30 dias do Fechamento
#######################################################################################
criptomoeda_fechamento_mediamovel100 = criptomoeda['c'].rolling(100).mean()
#######################################################################################
#======== Importar biblioteca SKLEARN
#######################################################################################
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from matplotlib import rcParams
#=========
criptomoeda_regressao = criptomoeda_abertura
#=========   Treinar X
criptomoeda_X_train = criptomoeda_abertura
criptomoeda_X_test = criptomoeda_abertura
X_train = np.reshape(criptomoeda_X_train, (-1,1))
X_test = np.reshape(criptomoeda_X_test, (-1,1))
#==========   Treinar Y
criptomoeda_y_train = criptomoeda_fechamento
criptomoeda_y_test = criptomoeda_fechamento
y_train = np.reshape(criptomoeda_y_train, (-1,1))
y_test = np.reshape(criptomoeda_y_test, (-1,1))
#######################################################################################
#=========   Criar modelo de regressão linear
#######################################################################################
regr = linear_model.LinearRegression(fit_intercept=True, normalize=True, copy_X=True, n_jobs=15, positive=False)
#######################################################################################
#=========   Treine o modelo usando os conjuntos de treinamento
#######################################################################################
regr.fit(X_train, y_train)
#######################################################################################
#========   Faça previsões usando o conjunto de teste
#######################################################################################
criptomoeda_y_pred = regr.predict(X_test)
#######################################################################################
#========   The coefficients
#######################################################################################
print('________________________________________________________________________________')
print('________________________________Resultados______________________________________')
print('\n Coefficients: ', regr.coef_)
print('________________________________________________________________________________')
#######################################################################################
#========   The mean squared error
#######################################################################################
print("\n Mean squared error (MSE): %.2f"
      % mean_squared_error(y_test, criptomoeda_y_pred))
print('________________________________________________________________________________')
#######################################################################################
# ========   Explained variance score: 1 is perfect prediction
#######################################################################################
print('\n Score de variância (próximo de 1.0 bom > ruim): %.2f'
      % r2_score(y_test, criptomoeda_y_pred))
print('________________________________________________________________________________')
print('\n Média previsões:', criptomoeda_y_pred.mean())
print('________________________________________________________________________________')
media = criptomoeda_y_pred.mean()
#######################################################################################
#============  Criar Gráfico
#######################################################################################
plt.style.use('bmh')
plt.rcParams['figure.figsize'] = (12,7)
plt.rcParams['font.family'] = 'serif'

plt.subplot(2, 1, 1)
plt.plot(criptomoeda_close, '-', color="black", linewidth=1)
plt.plot(criptomoeda_fechamento_mediamovel, '-', color="red", linewidth=1)
plt.plot(criptomoeda_fechamento_mediamovel100, '-', color="black", linewidth=1)
plt.plot(midpoint, '--', color="red", linewidth=1, alpha=0.4)
#plt.text(10000, 3000, "@DataCryptoML", family="serif")
plt.legend(['Close $%.2f'%(closeprice), 'MA30', 'MA100', 'Midpoint'], loc=0)
plt.title('DataCrypto Analytics (@DataCryptoML)')
#plt.xlabel('DataCrypto Analytics (@DataCryptoML)', labelpad=1)
plt.ylabel('Price')

plt.subplot(2, 1, 2)
plt.scatter(X_test, y_test, color="black", linewidth=2, alpha=0.5, s=.8)
plt.scatter(media, media,color="red", linewidth=3, alpha=0.6)
plt.plot(X_test, criptomoeda_y_pred, color='blue', linewidth=1)

plt.legend(['Linear Regression', 'Close', 'Prediction Price $%.2f'%(media)], loc=0)
plt.xlabel('GitHub: @datacrypto-analytics', fontsize=9)
plt.ylabel('Linear Regression')
plt.show()
#######################################################################################
#------   Salvando o modelo -----------------
#######################################################################################
# importa o pickle
import pickle
# Define o nome do arquivo em disco que irá
# guardar o nosso modelo
filename='regressor_model.sav'
# salva o modelo no disco
pickle.dump(regr, open(filename, 'wb'))
# Carregando o modelo do disco
loaded_model = pickle.load(open(filename, 'rb'))
# Atribui a variável result o score do modelo
result = loaded_model.score(X_test, y_test)
#Imprime o resultado
print('\n Score do modelo salvo:', result)
print('________________________________________________________________________________')
