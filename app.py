import sqlite3

# --- Configuração do Banco ---
def conectar():
    return sqlite3.connect("sistema.db")

def inicializar_banco():
    conn = conectar()
    cursor = conn.cursor()
    # Cria as tabelas
    cursor.execute('CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS clientes (id INTEGER PRIMARY KEY, nome TEXT, email TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS produtos (id INTEGER PRIMARY KEY, nome TEXT, preco REAL)')
    cursor.execute('CREATE TABLE IF NOT EXISTS vendas (id INTEGER PRIMARY KEY, cliente_id INTEGER, total REAL)')
   
    # Cria um usuário padrão se não existir nenhum
    cursor.execute("SELECT count(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", ('admin', '1234'))
   
    conn.commit()
    conn.close()

# --- Funções do Sistema ---
def autenticar(user, pwd):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE username=? AND password=?", (user, pwd))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None

def cadastrar_cliente(nome, email):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clientes (nome, email) VALUES (?, ?)", (nome, email))
    conn.commit()
    conn.close()
    print("Cliente cadastrado com sucesso!")

def cadastrar_produto(nome, preco):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO produtos (nome, preco) VALUES (?, ?)", (nome, preco))
    conn.commit()
    conn.close()
    print("Produto cadastrado com sucesso!")

def registrar_venda(cliente_id, total):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO vendas (cliente_id, total) VALUES (?, ?)", (cliente_id, total))
    conn.commit()
    conn.close()
    print("Venda registrada com sucesso!")

# --- Menu Principal ---
if __name__ == "__main__":
    inicializar_banco()
   
    print("--- Bem-vindo ao SisVenda ---")
    user = input("Usuário: ")
    pwd = input("Senha: ")

    if autenticar(user, pwd):
        print("\nLogin realizado com sucesso!")
        while True:
            print("\n--- MENU ---")
            print("1. Cadastrar Cliente")
            print("2. Cadastrar Produto")
            print("3. Registrar Venda")
            print("4. Sair")
            opcao = input("Escolha uma opção: ")
           
            if opcao == '1':
                cadastrar_cliente(input("Nome: "), input("Email: "))
            elif opcao == '2':
                cadastrar_produto(input("Nome do produto: "), float(input("Preço: ")))
            elif opcao == '3':
                registrar_venda(input("ID do Cliente: "), float(input("Total da venda: ")))
            elif opcao == '4':
                print("Saindo...")
                break
            else:
                print("Opção inválida!")
    else:
        print("Acesso negado! Usuário ou senha incorretos.")