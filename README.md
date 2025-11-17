##### Criado e testado em Ubuntu. Validado em WSL.

### ▶️ Rodar 

Na primeira vez que subir o container:

``
docker compose up -d
``

#### O MySQL vai:
* Criar o banco criptorace
* Rodar automaticamente o init.sql
* Popular as tabelas com os dados definidos

**Para testar:**

``
docker exec -it mysql_criptorace mysql -u criptoracer -p criptorace
``
E então:

``
SELECT * FROM contest;
``

**⚠️ Importante**

O script só roda na primeira inicialização, ou seja, se o volume mysql_data já existir, o MySQL não executa novamente o init.sql.
Se quiser testar novamente, basta remover o volume:


``
docker compose down -v
``

``
docker compose up -d
``


### ▶️ Execução da API
Primeiramente, inicialize o venv:

``
source .venv/bin/activate
``

Se não tiver o .venv (virtual environment), crie antes de rodar o comando anterior:

``
source .venv/bin/activate
``

**Instale dependências:**

``
pip install -r requirements.txt
``

**Rode a aplicação:**

``
python3 run.py
``

**Como saída, dando tudo certo, teremos algo como:**

````
tatuapu@LAPTOP-OEMBT6MA:~/criptoRaceV3$ python3 run.py
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.239.187:5000
````


Em caso de erros, revise os passos. Provavelmente pode ocorrer a falta de algum requisito a ser instalado.


