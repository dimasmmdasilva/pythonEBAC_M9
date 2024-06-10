import os
import time
import json
import csv
import pandas as pd
import seaborn as sns

from sys import argv
from random import random
from datetime import datetime

import requests

URL = 'https://www2.cetip.com.br/ConsultarTaxaDi/ConsultarTaxaDICetip.aspx'

for _ in range(0, 10):

    data_e_hora = datetime.now()
    data = datetime.strftime(data_e_hora, '%Y/%m/%d')
    hora = datetime.strftime(data_e_hora, '%H:%M:%S')

    try:
        response = requests.get(URL)
        response.raise_for_status()
    except requests.HTTPError as exc:
        print("Dado não encontrado, continuando.")
        cdi = None
    except Exception as exc:
        print("Erro, parando a execução.")
        raise exc
    else:
        dado = json.loads(response.text)
        cdi = float(dado['taxa'].replace(',', '.')) + (random() - 0.5)

    if os.path.exists('./taxa-cdi.csv') == False:

        with open(file='./taxa-cdi.csv', mode='w', encoding='utf8') as fp:
            fp.write('data,hora,taxa\n')

    with open(file='./taxa-cdi.csv', mode='a', encoding='utf8') as fp:
        fp.write(f'{data},{hora},{cdi}\n')

    time.sleep(2 + (random() - 0.5))

df = pd.read_csv('./taxa-cdi.csv')

grafico = sns.lineplot(x=df['hora'], y=df['taxa'])
_ = grafico.set_xticks(range(len(df['hora'])))
_ = grafico.set_xticklabels(labels=df['hora'], rotation=90)

# Usar um argumento padrão se nenhum for fornecido
output_filename = argv[1] if len(argv) > 1 else 'grafico.png'
grafico.get_figure().savefig(output_filename)

print("Sucesso")

