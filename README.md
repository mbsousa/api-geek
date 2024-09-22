<h1> API GEEK </h1>

> Status: Finalizado ✅

## Descrição 
Esta API GEEK foi desenvolvida exclusivamente para o estudo de back-end utilizando FastAPI, SQLModel e SQLAlchemy. O objetivo da aplicação é gerenciar um sistema de vendas de artigos voltados para jovens de 18 a 24 anos, com foco em produtos de cultura pop, como séries, mangás, games e filmes.

## Funcionalidades Implementadas:

1. Criação de Produto: Permite cadastrar produtos com atributos como nome, descrição, preço, quantidade em estoque, categoria e franquia.
2. Listagem de Produtos: Retorna uma lista de produtos cadastrados com filtros opcionais por nome, preço, categoria ou franquia.
3. Atualização de Produto: Possibilita a atualização de informações de um produto específico e a atualização do estoque por meio de venda ou reposição.
4. Exclusão de Produto: Permite excluir produtos, desde que o estoque esteja zerado.

## Tecnologias Utilizadas:

* FastAPI: Framework para construção de APIs web rápidas e modernas.
* SQLModel: Modelo de dados baseado em SQLAlchemy e Pydantic para gerenciar a persistência de dados.
* SQLAlchemy: Ferramenta de ORM para interagir com o banco de dados relacional.
* SQLite: Banco de dados relacional simples e leve para o armazenamento dos dados da aplicação.
* Docker: Contêinerização da aplicação para facilitar o deploy e a execução.

### Como executar o projeto: 

1. Clone o repositório.
2. Instale as dependências do projeto
`pip install -r requirements.txt`
3. Execute a aplicação localmente:
`uvicorn server:app --reload`
4. Acesse a documentação interativa no Swagger UI em:
`http://localhost:8000/docs`

## Rotas Principais:

* POST /api/geek/produtos/: Cria um novo produto.
* GET /api/geek/produtos/: Lista todos os produtos com filtros opcionais.
* GET /api/geek/produtos/{id}: Exibe os detalhes de um produto específico.
* PUT /api/geek/produtos/{produto_id}/att/: Atualiza um produto.
* PUT /api/geek/produtos/{produto_id}/estoque/: Atualiza o estoque de um produto.
* DELETE /api/geek/produtos/{produto_id}/: Exclui um produto (somente se o estoque for zero).
