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
import urllib, os
from time import sleep 
from matplotlib import pyplot as plt
from tqdm import tqdm


import pyfiglet

ascii_banner = pyfiglet.figlet_format("DataCrypto Analytics")
print(ascii_banner)
#########################################################################################
#=========  Esolhe a Criptomoedas e valores de negociação
########################################################################################
criptomoeda = input(' | Algoritmo: forex-rl '
					'\n | Versão: v0.2-PT ' 
                    '\n\n | Twitter @DataCryptoML '
                    '\n | Github @datacrypto-analytics '
					'\n | https://datacryptoanalytics.com/ '
                    '\n \nDigite o par Forex listada na ALPHA VANTAGE: ')

print('O par Forex informada foi: %s' %(criptomoeda))
#######################################################################################
#========   Cria URL da API Binance
#######################################################################################
apikey = 'XLRRSVFGQJLI7S4W'
root_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED'
symbol = criptomoeda
url = root_url + '&symbol=' + symbol + "&outputsize=full&apikey="+apikey+ '&datatype=csv'
response = getattr(urllib, 'request', urllib).urlopen(url)
with tqdm.wrapattr(open(os.devnull, "wb"), "write",
                   miniters=1, desc="DataCrypto Analytics recuperando dados",
                   total=getattr(response, 'length', None)) as fout:
    for chunk in response:
        fout.write(chunk)
#print(url)

r = requests.get(url)
for i in tqdm((r), desc ="DataCrypto Analytics preparando dados"): 
    sleep(.01) 
df = pd.read_csv(url, index_col=0, parse_dates=True)
tqdm.pandas(desc="DataCrypto Analytics preparando dados")
df.progress_apply(lambda x: x**2)

df.head
df.shape
df.index 
df.columns
df.describe
#print(df.shape)
#print(df.columns)
#print(df.describe)


forex_fechamento = df['close'].astype('float').values
forex_abertura = df['open'].astype('float').values
forex_alta = df['high'].astype('float').values
forex_baixa = df['low'].astype('float').values
#forex_date = df['timestamp'].values
#date = df['index']

forex_close = df['close'].astype('float')
closeprice = forex_close.iloc[1]

#print(forex_date)

#######################################################################################
# Média movel de 14 dias do Fechamento
#######################################################################################
forex_fechamento_mediamovel = df['close'].rolling(100).mean()
#######################################################################################
# Média movel de 30 dias do Fechamento
#######################################################################################
forex_fechamento_mediamovel100 = df['close'].rolling(200).mean()
#######################################################################################


import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from matplotlib import rcParams
#=========
criptomoeda_regressao = forex_abertura
#=========   Treinar X
criptomoeda_X_train = forex_abertura
criptomoeda_X_test = forex_abertura
X_train = np.reshape(criptomoeda_X_train, (-1,1))
X_test = np.reshape(criptomoeda_X_test, (-1,1))
#==========   Treinar Y
criptomoeda_y_train = forex_fechamento
criptomoeda_y_test = forex_fechamento
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
print('\n Preço de fechamento: ', closeprice)
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
plt.plot(forex_close, '-', color="black", linewidth=1)
plt.plot(forex_fechamento_mediamovel, '-', color="red", linewidth=1)
plt.plot(forex_fechamento_mediamovel100, '-', color="black", linewidth=1)
#plt.plot(midpoint, '--', color="red", linewidth=1, alpha=0.4)
#plt.text(10000, 3000, "@DataCryptoML", family="serif")
plt.legend(['Close %.2f'%(closeprice), 'MA30', 'MA100'], loc=0)
plt.title('DataCrypto Analytics (@DataCryptoML) - %s' %(criptomoeda))
#plt.xlabel('DataCrypto Analytics (@DataCryptoML)', labelpad=1)
plt.ylabel('Price')

plt.subplot(2, 1, 2)
plt.scatter(X_test, y_test, color="black", linewidth=2, alpha=0.5, s=.8)
plt.scatter(media, media,color="red", linewidth=3, alpha=0.6)
plt.plot(X_test, criptomoeda_y_pred, color='blue', linewidth=1)

plt.legend(['Linear Regression', 'Close', 'Prediction Price %.2f'%(media)], loc=0)
plt.xlabel('GitHub: @datacrypto-analytics', fontsize=9)
plt.ylabel('Linear Regression')
plt.show()
