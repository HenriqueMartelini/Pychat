# Projeto Pychat

Este é um projeto de exemplo para o envio de mensagens criptografadas utilizando MongoDB, bcrypt para autenticação de senhas e cryptography para criptografia/descriptografia de mensagens.

## Requisitos

Para rodar este projeto, certifique-se de ter o Python instalado e as bibliotecas necessárias. Você pode instalá-las utilizando o `requirements.txt`:
pip install -r requirements.txt

## Configuração do Ambiente
Também se faz necessário criar um arquivo .env, que pode ser criado de maneira mais fácil atraves do `generate_env.py`

Note que a `senha para descriptografar a mensagem` deve ser de exatos `44 caracteres`, uma vez que a senha deve ser em 32 bytes e em base 64.

Exemplo de conteúdo do `.env`:

MONGO_CONNECTION_STRING="mongodb://localhost:27017"
SECRET_KEY="mysecretkey123456789012345678901234567890123"