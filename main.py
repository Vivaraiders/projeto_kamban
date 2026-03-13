from models.users import User
from models.tarefas import Tarefa

def main():
    verifador = None
    print("PROJETO KAMBAN")
    while verifador is None:
        input_email = input("Digite seu email:\n")
        input_senha = input("Digite sua senha: \n")
        verifador = User.verificar_login(input_email, input_senha)                              
        if verifador is None:                                               #Verifica email, se email e senha não existir, ele passa None
            print("email ou senha errados!!")
    usuario_conectado = verifador                                           #Recebe id, nome e email para conseguir adicionar coisas a esse email
    print(f"Seja bem vindo {usuario_conectado['nome']}, id {usuario_conectado['id']}")          #printa nome e id(apenas teste pode tirar depois)
    while True:
        print("\ntarefas:")
        tarefas = Tarefa.tarefas_usuario(usuario_conectado['id'])                                   #tarefas pega id do usuario para puxar no banco as tarefas desse id
        if not tarefas:
            print("Usuário ainda não tem tarefas!")
        else:
            for tarefa in tarefas:
                if tarefa[4] == "grave":
                    gravidade = "GRAVE | "           ##COMENTÁRIO: no banco tem uma função que printa primeiro a tarefa que esta em fazendo, então primeiro mostra FAZENDO (STATUS), depois FAZER(STATUS), FEITO(STATUS)
                elif tarefa[4] == "média":
                    gravidade = "MÉDIA | "
                else:
                    gravidade = "BAIXA | "
                print(f"{gravidade} ID: {tarefa[0]} | TAREFA: {tarefa[1]} | STATUS: {tarefa[3]} | DATA PARA CONCLUIR: {tarefa[6]}")            #esses numeros são as respectivas colunas do banco


        print("\nSelecione o serviço que deseja fazer:")
        try:
            escolha = int(input("1. Adicionar tarefas\n2. Deletar tarefa\n3. Para atualizar status de uma tarefa\n4. Parar execução\n"))
        except ValueError:
            print("Digite apenas numeros!")
            continue
        if escolha == 1:
            titulo = input("Digite qual é a tarefa:\n").lower()
            descricao = input("descrição dessa tarefa:\n").lower()

            status = input("esta fazendo, vai fazer ou ja terminou a tarefa: (fazer, fazendo, feito)\n").lower()
            if status not in ["fazer", "fazendo", "feito"]:                                                                 #Verifica se status é algum desses 3
                print("Status inválido!")
                continue

            prioridade = input("Qual prioridade da tarefa: (baixa, média, grave)\n").lower()
            if prioridade not in ["baixa", "média", "grave"]:
                print("Prioridade inválida!")
                continue

            data_conclusao = input("Quando pretende terminar a tarefa: (ano-mês-dia  horas-minutos-segundos)\n")
            Tarefa.adicionar_tarefa(titulo,descricao,status,prioridade,data_conclusao, usuario_conectado["id"])               #Adiciona a tarefa ao respectivo id

        elif escolha == 2:
            try:
                deletar = int(input("Digite o id de qual tarefa deseja deletar: "))                                         #Deleta se houver esse id no banco
            except ValueError:
                print("Apenas numeros!")
                continue
            Tarefa.deletar(usuario_conectado["id"], deletar)
        
        elif escolha == 3:
            try:
                tarefa_id = int(input("Digite o id de qual tarefa deseja atualizar: "))                                     
            except ValueError:
                print("Apenas numeros!")
                continue
            
            status = input("Qual status deseja colocar: (fazer, fazendo, feito): ")
            if status not in ["fazer", "fazendo", "feito"]:
                print("Status inválido!")
                continue

            resultado = Tarefa.mudar_status(usuario_conectado["id"], status, tarefa_id)                         #muda status se o usuario tiver tarefa com o respectivo id
            if resultado == 0:
                print("tarefa não encontrada")
            else:
                print("Tarefa atualizada")
            
        elif escolha == 4:
            break
        else:
            print("Escolha inválida!!")

if __name__ == "__main__":
    main()