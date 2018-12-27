# poc-mobilis-metabase

Uma aplicação como POC do Metabase usando os meus dados do Mobilis

## Como usar esse repositório?

### Pre-requisitos

* Tenha instalado o Postgres
* Crie duas bases, uma chamada metabase, e outra de sua escolha. Sugira-se usar a do docker
* Edite o código em `parser.main.py` para estabelecer a conexão ao banco de dados
* Edite o docker-compose com os dados de variáveis de ambiente, como acesso ao banco de dados pelo metabase.

### Rodar o cli.py

Tenha em sua máquina, como dependências:

* pandas
* click
* psycopg2

É possível instalá-las usando o pip ou usando docker e instalando manualmente em uma imagem

Tendo as dependências instaladas, é só rodar o comando:

```
python cli.py --csv<csv_path>
```

Em que `csv_path` pode ser mapeado para a pasta reports. Como segue:

```
python cli.py --csv=reports/data.csv
```

O arquivo CSV deverá ser o que o aplicativo do Mobilis no telefone exporta, não a versão web, pois é diferente

### Rodando o banco e a aplicação do Metabase

Para rodar as aplicação do metabase via docker, é só rodar o comando:

```
docker-compose up
```

Haverá inúmeros logs do metabase, na primeira vez que ele for executado.

Não havendo erros nos logs, é só acessar a aplicação, em `localhost:3000`.
