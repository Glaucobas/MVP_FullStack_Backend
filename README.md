# API

O objetida da API é servir como uma camada de controle entre o frontend e a base de dados.

---
## Como executar 


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

Após a criação do ambiente virtual execute o comando:

```
env\Scripts\activate
```
para ativar o ambiente.

em seguida o comando:

```
(env)$ pip install -r requirements.txt
```
para instalar as bibliotecas necessárias.

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Abra o http://localhost:5000/#/ no navegador para verificar o status da API em execução e ter acesso a documentação.
