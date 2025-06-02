import pandas as pd
import numpy as np
import datetime

#Configura todas as colunas float de uma dataframe para terem o formato de duas casas decimais.
pd.options.display.float_format = '{:.2f}'.format

#################################################################################################################################################################################

dados_vendas = pd.read_json("dados_locacao_imoveis.json")
dados_vendas_normalizados = pd.json_normalize(dados_vendas['dados_locacao'])

dados_vendas_normalizados = dados_vendas_normalizados.explode(['datas_combinadas_pagamento', 'datas_de_pagamento', 'valor_aluguel'])
dados_vendas_normalizados.reset_index(inplace = True, drop = True)

#Tratamento dos dados numéricos para realizar a conversão posteriormente:

dados_vendas_normalizados['valor_aluguel'] = dados_vendas_normalizados['valor_aluguel'].str.replace('$', '', regex=False).replace('(\,\w\s\w\w\w\w\w)', '', regex=True)
dados_vendas_normalizados['valor_aluguel'] = dados_vendas_normalizados['valor_aluguel'].astype(np.float32)

#Tokenização das strings:

dados_vendas_normalizados['apartamento'] = dados_vendas_normalizados['apartamento'].str.replace('(blocoAP)', '')

#Conversão de datetime:

dados_vendas_normalizados['datas_combinadas_pagamento'] = dados_vendas_normalizados['datas_combinadas_pagamento'].str.split('/')
dados_vendas_normalizados['datas_combinadas_pagamento'] = dados_vendas_normalizados['datas_combinadas_pagamento'].map(lambda x : datetime.datetime(int(x[2]), int(x[1]), int(x[0])))
dados_vendas_normalizados['datas_de_pagamento'] = dados_vendas_normalizados['datas_de_pagamento'].str.split('/')
dados_vendas_normalizados['datas_de_pagamento'] = dados_vendas_normalizados['datas_de_pagamento'].map(lambda x : datetime.datetime(int(x[2]), int(x[1]), int(x[0])))

#print(dados_vendas_normalizados['datas_combinadas_pagamento'])
#print(dados_vendas_normalizados['datas_de_pagamento'])
#print(dados_vendas_normalizados['valor_aluguel'])
#print(dados_vendas_normalizados['apartamento'])

dados_agrupamento = dados_vendas_normalizados.groupby(['apartamento', 'datas_combinadas_pagamento' ,'datas_de_pagamento'])[['valor_aluguel']].sum()

print(dados_agrupamento)


#################################################################################################################################################################################

dados_condominio = pd.read_json("dados_vendas_clientes.json")
dados_condominio_normalizados = pd.json_normalize(dados_condominio['dados_vendas'])


dados_condominio_normalizados = dados_condominio_normalizados.explode(['Cliente', 'Valor da compra'])
dados_condominio_normalizados.reset_index(inplace = True, drop = True)

dados_condominio_normalizados['Valor da compra'] = dados_condominio_normalizados['Valor da compra'].str.replace('R$', '').str.replace(',', '.')
dados_condominio_normalizados['Valor da compra'] = dados_condominio_normalizados['Valor da compra'].astype(np.float32)

#Tokenização das strings:

dados_condominio_normalizados['Cliente'] = dados_condominio_normalizados['Cliente'].str.lower()
dados_condominio_normalizados['Cliente'] = dados_condominio_normalizados['Cliente'].replace('[^a-zA-Z\-\']', ' ', regex=True)


#Datas das compras:
dados_condominio_normalizados['Data de venda'] = dados_condominio_normalizados['Data de venda'].str.split('/')
dados_condominio_normalizados['Data de venda'] = dados_condominio_normalizados['Data de venda'].map(lambda x : datetime.datetime(int(x[2]), int(x[1]), int(x[0])))
dados_agrupados = dados_condominio_normalizados.groupby('Data de venda')[['Valor da compra']].sum()
print(dados_agrupados)
