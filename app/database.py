import sqlite3

class ConectaBanco:
    
    
    # --- Criando a conexão com banco de dados "kivy_data.db"
    def __init__(self, name = 'kivy_data.db') -> None:
        self.name = name

    def connect(self): 
        self.connection = sqlite3.connect(self.name)
    
    def create_table(self):

        cursor = self.connection.cursor() # --- Gerando um cursor"

        # --- Criando a tabela "usuario"
        cursor.execute("""CREATE TABLE IF NOT EXISTS usuario (
            idUser INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL)
            """)

    def inserir_dados(self,dados):
        campos = ('username','email','password')
        itens = ('?,?,?')
        
        self.connect()
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"""INSERT INTO usuario {campos} VALUES ({itens}) """, dados)
            self.record_data()
            
        except Exception as e:
            print('Erro, dados nao gravados\n',e)
        
        self.close_connection()

    def record_data(self):
        try:
            self.connection.commit() # --- Gravar dados na tabela"
        except:
            pass

    def close_connection(self): 
        try:
            self.connection.close() # --- Fecha conexão com banco"
        except:
            pass
    
    def listar_dados(self,usuarios=''):
        
        self.connect()
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM usuario")
            usuarios = cursor.fetchall()
        except:
            pass
        
        return usuarios

    def valida_login(self,user,senha):
        logado = False
    
        self.connect()
        try:
            cursor = self.connection.cursor()
            busca = (f"SELECT password FROM usuario WHERE username = '{user}'")
            cursor.execute(busca)            
            results = cursor.fetchall()
        except:
            pass

        print(results[0][0])
        if senha == results[0][0]:
            logado = True
        
        return logado
    

            
        