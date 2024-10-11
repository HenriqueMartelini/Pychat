from cryptography.fernet import Fernet
from dotenv import load_dotenv
from databases.mongohandler import MongoHandler, SECRET_KEY
import os

load_dotenv()

if __name__ == '__main__':
    print("\n" * 130)
    mongo = MongoHandler()
    mongo.connect()
    print("Bem-vindo ao Pychat!\n")

    while True:
        option = input("1 - Fazer Login\n2 - Criar uma conta\nEscolha a opção desejada: ")
        if option in ["1", "2"]:
            option = int(option)
            break
        else:
            print("\n" * 130)
            print("Opção inválida, tente novamente com uma das opções fornecidas (1 / 2)")

    print("\n")

    if option == 1:
        user = input("Digite o email para acesso: ")
        password = input("Digite a senha para acesso: ")
        if mongo.authenticate(user, password):
            print("Login válido!")

            subject = input("Digite o assunto da mensagem: ")
            body = input("Digite o corpo da mensagem: ")
            mongo.send_message(user, user, subject, body)

            last_message = mongo.get_last_message(user)

            if last_message:
                print("Assunto:", last_message.subject)
                print("Mensagem criptografada recebida. Para descriptografar, insira a senha.")

                decryption_key = input("Digite a chave de decriptação: ")

                try:
                    fernet = Fernet(decryption_key)
                    decrypted_body = fernet.decrypt(last_message.body.encode()).decode()
                    print("Mensagem descriptografada:", decrypted_body)
                except Exception as e:
                    print(f"Erro ao descriptografar: {e}")
            else:
                print("Nenhuma mensagem encontrada.")

        else:
            print("Login inválido.")
    else:
        name = input("Digite seu nome: ")
        email = input("Digite seu email: ")
        password = input("Digite sua senha: ")
        mongo.add_user(name, email, password)
        print("Conta criada com sucesso!")

        subject = input("Digite o assunto da mensagem: ")
        body = input("Digite o corpo da mensagem: ")
        mongo.send_message(email, email, subject, body)

        input_password = input("Digite a chave secreta para ler a mensagem: ").strip()

        if input_password == os.getenv("SECRET_KEY"):
            last_message = mongo.get_last_message(email)
            if last_message:
                try:
                    decrypted_body = mongo.fernet.decrypt(last_message['body'].encode()).decode()
                    print("Mensagem descriptografada:")
                    print(decrypted_body)
                except Exception as e:
                    print(f"Erro ao descriptografar: {e}")
        else:
            print("Chave secreta incorreta!")