from database.database import conectar_banco

class Tarefa:
    def __init__(self, titulo:str, descricao:str, status:str, prioridade:str, data_conclusao:str, user_id:int):
        self.titulo = titulo
        self.descricao = descricao
        self.status = status
        self.prioridade = prioridade
        self.data_conclusao = data_conclusao
        self.user_id = user_id
    
    def __str__(self):
        return f"{self.titulo} | {self.descricao} | {self.status} | {self.prioridade} | {self.data_conclusao} | {self.user_id}"

    @staticmethod
    def adicionar_tarefa(titulo:str, descricao:str, status:str, prioridade:str, data_conclusao:str, user_id:int):
        conn = conectar_banco()
        cursor = conn.cursor()
    
        cursor.execute(
            """
                INSERT INTO tarefas (titulo, descricao, status, prioridade, data_conclusao, user_id)
                VALUES(%s,%s,%s,%s,%s,%s)        
            """,
            (titulo,descricao,status,prioridade,data_conclusao,user_id)
        )
    
        conn.commit()
        tarefa_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        return tarefa_id
    
    @staticmethod
    def deletar(user_id:int ,id_tarefa:int):
        conn = conectar_banco()
        cursor = conn.cursor()
    
        cursor.execute(
            """
                DELETE FROM tarefas
                WHERE user_id = %s AND id = %s
            """,
            (user_id, id_tarefa)
        )

        conn.commit()
        tarefa_id = cursor.rowcount
        if tarefa_id == 0:
            print("tarefa não existe!")
        cursor.close()
        conn.close()
        return tarefa_id
    
    @staticmethod
    def tarefas_usuario(user_id:int):
        conn = conectar_banco()
        cursor = conn.cursor()

        cursor.execute("""
                       SELECT * FROM tarefas
                        WHERE user_id = %s 
                       ORDER BY FIELD(status,'fazendo','fazer','feito'),
                       FIELD(prioridade,'grave','média','baixa')
                       """,
                        (user_id,))

        tarefas = cursor.fetchall()
        

        cursor.close()
        conn.close()
        return tarefas

    @staticmethod
    def mudar_status(user_id:int, status:str, tarefa_id:int):
        conn = conectar_banco()
        cursor = conn.cursor()

        cursor.execute(
            """
                UPDATE tarefas
                SET status = %s
                WHERE user_id = %s AND id = %s
            """,
            (status, user_id, tarefa_id)
        )
        conn.commit()
        
        linhas_afetadas = cursor.rowcount
        cursor.close()
        conn.close()
        return linhas_afetadas


    #METODO DE ADMIN
    @classmethod
    def ver_tarefas(cls):
        conn = conectar_banco()
        cursor = conn.cursor()
    
        cursor.execute("SELECT * FROM tarefas")  
    
        tarefas = cursor.fetchall()
    
        for id_tarefa, titulo, descricao, status, prioridade, data_criacao, data_conclusao, user_id in tarefas:
            print(f"""
                id: {id_tarefa}
                titulo: {titulo}
                descrição: {descricao}
                status: {status}
                prioridade: {prioridade}
                data de criação: {data_criacao}
                data de conclusão: {data_conclusao}
                user_id: {user_id}
                """, "-" * 50)
            
    
        cursor.close()
        conn.close()
    
        return tarefas
    
    
    
if __name__ == "__main__":

    # tarefas = Tarefa.ver_tarefas()
    # print(tarefas)
    print(Tarefa)

