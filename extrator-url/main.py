url_completa = "http://bytebank.com/cambio?moedaOrigem=real&moedaDestino=dolar&quantidade=100"

url = "bytebank.com/cambio?moedaOrigem=real"
print(url)

url_base = url[0:19]
print(url_base)

url_parametros = url[20:36]
print(url_parametros)

nome_completo = "Hudson Carlos"
print(nome_completo[0:6])
print(nome_completo[7:13])

## --------------------------------------------------------

ind_inter = url.find('?')
resultado1 = url[:ind_inter]
print(resultado1)

resultado2 = url[ind_inter+1:]
print(resultado2)