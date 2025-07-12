
## API com Python e Flask:
API completa que simula um sistema de e-commerce, com rotas, integração com um banco de dados, 
autenticação de usuário e funcionalidades essenciais, como listar produtos, adicionar itens ao 
carrinho de compras e realizar o checkout.

- Para baixar as bibliotecas necessárias digite no terminal:
```
pip3 install -r requirements.txt
```
- Comandos no terminal para o banco:
    - `flask shell` -> Abre o terminal flask shell.
    - `db.create_all()` -> Transforma os modelos em tabelas.
    - `db.drop_all()` -> Deleta todas as tabelas.
    - `user = User(username="", password="")` -> Cria um usuário.
    - `db.session.add(user)` -> Adiciona o usuário.
    - `db.session.commit()` -> Efetiva as mudanças no banco.
    - `exit()` -> Sai do flask shell.

- Instale a extensão SQLite Viewer do VS Code para poder visualizar o banco de dados.