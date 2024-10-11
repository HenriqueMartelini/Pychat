def create_env():
    with open('.env', 'w') as env_file:
        env_file.write("MONGO_CONNECTION_STRING=mongodb://localhost:27017\\n")
        env_file.write("SECRET_KEY=mysecretkey12345678901234567890123456789012345678\\n")

if __name__ == "__main__":
    create_env()