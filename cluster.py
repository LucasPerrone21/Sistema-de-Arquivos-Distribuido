import argparse
import subprocess

def igualdade_lista(lista):
    primeiro_elemento = lista[0]
    for elemento in lista:
        if elemento != primeiro_elemento:
            return False
    return True


numero_nodes = 2

# Criação do parser
parser = argparse.ArgumentParser(description='Exemplo de script com argumentos e opções.')

# Argumento posicional
parser.add_argument('comando', help='comando')
parser.add_argument('-lact', help='Local atual')
parser.add_argument('-ldest', help='Local destino')


args = parser.parse_args()


if args.comando == 'list':
    '''
    lista todos os arquivos dentro da pasta shared ou subpastas da pasta shared

    Ex1: dfs list
    Ex2: dfs list -lact caminho/da/subpasta

    '''
    node_output = []
    for c in range(1, numero_nodes + 1):
        if args.lact is None:
            node_output.append(subprocess.check_output(f'ssh node{c} "ls ~/shared"', shell=True).decode('utf-8'))
        elif args.lact is not None:
            node_output.append(subprocess.check_output(f'ssh node{c} "ls ~/shared/{args.lact}"', shell=True).decode('utf-8'))
    if igualdade_lista(node_output):
            print(node_output[0])
    else:
        print("Erro: os arquivos estão dessincronizados")


elif (args.comando == 'copy'):
    '''
    copia um arquivo/diretorio de um local para outro

    Ex: dfs copy -lact caminho/da/subpasta/origem -ldest caminho/da/subpasta/destino
    '''
    loc_atual = args.lact
    loc_destino = args.ldest
    for c in range (1, numero_nodes + 1):
        subprocess.check_output(f'ssh node{c} "cp shared/{loc_atual} shared/{loc_destino}"', shell=True)

elif (args.comando == 'move'):
    '''
    move um arquivo/diretorio de um local para outro

    Ex: dfs move -lact caminho/da/subpasta/origem -ldest caminho/da/subpasta/destino
    '''
    loc_atual = args.lact
    loc_destino = args.ldest
    for c in range (1, numero_nodes + 1):
        subprocess.check_output(f'ssh node{c} "mv shared/{loc_atual} shared/{loc_destino}"', shell=True)

elif (args.comando == 'newdir'):
    '''
    cria um novo diretorio

    Ex: dfs newdir -lact caminho/da/subpasta/nome_do_diretorio
    '''
    loc = args.lact
    for c in range (1, numero_nodes + 1):
        subprocess.check_output(f'ssh node{c} "mkdir shared/{loc}"', shell=True)

elif args.comando == 'del':
    '''
    deleta um arquivo/diretorio

    Ex: dfs del -lact caminho/da/subpasta/nome_do_diretorio

    '''
    file_to_delete = args.lact
    for c in range(1, numero_nodes + 1):
        subprocess.check_output(f'ssh node{c} "rm -rf shared/{file_to_delete}"', shell=True)

elif args.comando == 'sync':
    '''
    sincroniza os arquivos entre os nós

    Ex: dfs sync
    '''
    for c in range(1, numero_nodes):
        subprocess.check_output(f'ssh node{c} "scp -r ~/shared/ node{c+1}:~/"', shell=True)
        print(f'node{c} sincronizado com node{c+1}')

else:
    print(f'dfs: comando "{args.comando}" não encontrado')
