# API REST FOR WEATHER

  Esta é uma API feita em Python usando Flask que retorna as principais informações de clima de cada municipio do Brasil, de acordo com o codigo do municipio.

## Rotas

  Existem 3 rotas que a API fornece:
  -  Para o Clima

    /<codigo>

Retorna as informações de clima do município como temperatura máxima e mínima, umidade máxima e mínima, direção do vento, por e nascer do sol entre mais algumas outras. 

- Cidades
        
        /cities

Este retorna uma lista contendo o nome de 5570 municipios do Brasil, no qual pode-se usar para buscar o codigo na rota adequada ou usar em regexp.

- Código

        /cities/code/<city_name>

Este retorna o nome e o codigo da cidade dada como parâmetro na url.


## Como rodar

Para rodar o projeto, dentro da pasta raiz './api_clima', rode:

        flask --app flaskr run

A API estará disponivel em http://localhost:5000.


## Detalhes
Esta API foi feita usando uma outra API como base. Esta API é a mesma que fornece as informações para o site do INMET, cuja as informações são públicas e de grande credibilidade.