# Solução de Integração

Solução de integração para corte da gravação inicial em trechos que correspondam a cada programa
da grade de programação que entrega os conteúdos separadamente para a API do Globo Play.

## Instruções de utilização

Opcionalmente, para rodar a aplicação, crie e ative o ambiente virtual com os comandos abaixo:

```
python3 -m venv env
source env/bin/activate
```

na pasta raiz do projeto execute o comando abaixo para instalar as dependências:

```
pip3 install -r requirements.txt
```

Para simular as APIs da Globo, criei uma API com Hug com as chamadas para simulação. Para executar a API execute o 
comando abaixo:

Para o correto funcionamento, a API 'mock_apis_globo.py' deve estar rodando.
```
hug -f mock_apis_globo.py
```



Para executar a aplicação execute o comando no diretório raiz da aplicação:

```
python3 run.py 'arquivos-para-leitura'
```

Substituir "python3" pela chamada do python correspondente e 'arquivos-para-leitura' pelo diretório a ser monitorado
 a espera de arquivos.

A aplicação ficará monitorando novos arquivos no diretório 'arquivos-para-leitura' e sempre que um novo arquivo for 
adicionado, a aplicação executará as intruções de corte contidas no arquivo.

```
/arquivos-para-leitura
```
 
## Informações importantes

As informações dos arquivos são salvas no banco de dados (sqlite)
```
Start Time (time code)
End Time (time code)
Title (string)
Duration (Time Code)
Reconcile Key (number)
```

Para fim de simulação, criei um aquivo chamado 'arquivo_de_video.mp4' dentro do diretório 'videos-cortados' que simula 
o vídeo entregue pela API de Corte.

```
/videos-cortados/arquivo_de_video.mp4
```

Quando a API de Corte retornar o status 'completed' o sistema irá copiar este vídeo para a pasta 'videos-entregues' e 
consumir a API da GloboPlay efetuando a entrega do vídeo.
O nome do vídeo entregue será o ID do registro no banco de dados concatenado com a informação Reconcile Key
```
/videos-entregues/{ID}_{RECONCILE_KEY}.mp4
```