from database.database import conectar_banco

class User:
    def __init__(self, nome:str, ultimo_nome:str, email:str, senha:str):
        self.nome = nome
        self.ultimo_nome = ultimo_nome
        self.email = email
        self.senha = senha

    def adicionar(self):
        conn = conectar_banco()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO users (nome, ultimo_nome, email, senha)
            VALUES(%s,%s,%s,%s)
            """,
            (self.nome, self.ultimo_nome, self.email, self.senha)
        )

        conn.commit()
        user_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return user_id

    @staticmethod
    def deletar(user_id:int):
        conn = conectar_banco()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))

        conn.commit()
        user_deletado = cursor.rowcount
        cursor.close()
        conn.close()
        return user_deletado

    @classmethod
    def ver_tabelas(cls):
        conn = conectar_banco()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users")

        usuarios= cursor.fetchall()

        for id_user, nome, ultimo_nome, email, senha in usuarios:
            print(f"""
                id: {id_user},
                nome: {nome},
                ultimo_nome: {ultimo_nome},
                email: {email},
                senha: {senha}
                """, "-" * 50)

        cursor.close()
        conn.close()
        return usuarios

    @classmethod
    def verificar_login(cls,email:str, senha:str):
        conn = conectar_banco()
        cursor = conn.cursor()
    
        cursor.execute(
                """
                    SELECT id,nome,email,senha FROM users
                    WHERE email = %s AND senha = %s
                """,
                (email, senha)
            )
    
        resultado = cursor.fetchone()
        cursor.close()
        conn.close()
        if resultado:
            return {"id": resultado[0], "nome": resultado[1], "email": resultado[2]}
        else:
            return None
    
    
    