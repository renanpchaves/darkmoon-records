"""
DEPRECADO - Versão CLI original (v1.0)
Este arquivo não é mais usado.
A nova versão é uma API REST em /api/main.py

Mantido apenas para referência histórica.
Data de descontinuação: 20/03/2026
"""

from modelo.darkmoon import Albums

def to_menu():
    '''
    Mostra as possibilidades no menu para o usuário. Menu principal
    '''
    print('\n' + '='*50)
    print('🎵 DARKMOON RECORDS - SISTEMA DE ESTOQUE 🎵'.center(50))
    print('='*50)
    print('\n1. Cadastrar novo disco')
    print('2. Listar todos os discos')
    print('3. Alterar status de estoque')
    print('4. Deletar álbums da base de dados')
    print('5. Adicionar avaliação')
    print('6. Salvar dados no banco')
    print('7. Sair')
    print()

#cadastrando um novo disco no sistema
def cadastrar_discos():
    '''
    Pede as infos para cadastro de um novo album
    '''
    print('\n📀 CADASTRAR NOVO DISCO\n')

    nome = input('Nome do album: ')
    artista = input('Nome do artista: ')
    while True:
        try:
            quant_musicas = int(input('Quantidade de músicas: '))
            break
        except ValueError:
            print ('❌ Favor inserir apenas números. ')

    #criação do album
    novo_album = Albums(nome, artista, quant_musicas)

    #está em estoque?
    while True:
        em_estoque = input('Está em estoque? (s/n): ').lower()

        if em_estoque in ['s', 'n']:
            break
        else:
            print('❌ Digite apenas "s" ou "n".')

    if em_estoque == 's':
        novo_album.estoque_alt()
    print(f'\n✅ Álbum "{nome}" cadastrado com sucesso!')

def listar_discos():
    '''
    Lista todos os discos cadastrados no sistema
    '''
    print('\n📚 CATÁLOGO COMPLETO\n')
    Albums.listar_albums()

def deletar_discos():
    '''
    Exclui um album do sistema por ID
    '''
    print('\n🗑️ DELETAR DISCO\n')

    if not Albums.album:
        print('❌ Não há nenhum álbum cadastrado...')
        return
    
    #iterando para mostrar todos os albums cadastrados
    print('Álbuns cadastrados:')
    for i, album in enumerate(Albums.album):
        print(f'{i+1}. {album._nome} - {album._artista}')

    #escolher o album
    while True:
        try:
            escolha = int(input('\número do álbum a deletar: (digite 0 para cancelar)'))

            if escolha == 0:
                print('❌ Operação cancelada.')
                return
            
            escolha -= 1 #ajustando o valor pra relacionar ao indice

            if 0 <= escolha < len(Albums.album):
                album = Albums.album[escolha]

                confirma = input(f'\n⚠️ Tem certeza que deseja deletar "{album._nome}"? (s/n): ').lower()

                if confirma == 's':
                    album.deletar_album()
                    print(f'\n✅ Álbum "{album._nome}" deletado com sucesso!')
                else:
                    print('❌ Operação cancelada.')
                break
            else:
                print('❌Número inválido!')
        except ValueError:
            print('❌ Digite um número válido!')

def alterar_estoque():
    '''
    Altera o status de estoque
    '''
    print('\n📦 ALTERAR ESTOQUE\n')

    if not Albums.album:
        print('Não há nenhum album cadastrado...')
        return
    print ('Álbuns cadastrados: ')
    for i, album in enumerate(Albums.album):
        print (f'{i+1}. {album._nome} - {album.ativo}')

    while True:
        try:
            escolha = int(input('\nEscolha o número do álbum: ')) - 1
            if 0 <= escolha < len(Albums.album):
                Albums.album[escolha].estoque.alt()
                print(f'Status alterado para: {Albums.album[escolha].ativo}')
                break
            else:
                print ('❌ Número inválido')
        except ValueError:
            print ('❌ Digite um número!')

def add_avaliacao():
    '''
    Adiciona avaliação a um album
    '''
    print('\n⭐ ADICIONAR AVALIAÇÃO\n')

    #sem albuns registrados na base de dados
    if not Albums.album:
            print ('Não há nenhum album cadastrado...')
            return
    
    #mostrando todos os albums registrados
    print('Álbuns cadastrados:')
    for i, album in enumerate(Albums.album):
        print(f'{i+1}. {album._nome}')

    #loop que recebe input do usuario para escolher o album que vai avaliar
    while True:
        try:
            escolha = int(input('\nEscolha o número do álbum: ')) - 1
            if 0 <= escolha < len(Albums.album):
                break
            else:
                print('❌ Album inválido!')
        except ValueError:
            print('❌ Digite um número válido!')
    cliente = input ('Digite seu nome: ')
            
    #loop que recebe a avaliação de fato
    while True:
        try:
            nota = float(input('Nota (0 a 5): '))
            if Albums.album[escolha].receber_avaliacao(cliente, nota):
                print('Avaliaçao registrada.')
                break
            else:
                print ('❌ Nota deve estar entre 0 e 5.')
        except ValueError:
            print('❌ Digite um número válido!')

def salvar_todos():
    '''
    salva os dados na base
    '''
    print('\n💾 SALVANDO NO BANCO DE DADOS...\n')
    for album in Albums.album:
        album.salvar_db()
    print('\n✅ Todos os dados foram salvos!')


#main
def main():

    print('Carregando dados...')
    Albums.carregar_db()

    while True:
        to_menu()
        opcao = input('Escolha uma opção: ')
        
        #menu principal do usuário
        if opcao == '1':
            cadastrar_discos()
        
        elif opcao == '2':
            listar_discos()
        
        elif opcao == '3':
            alterar_estoque()

        elif opcao == '4':
            deletar_discos()
        
        elif opcao == '5':
            add_avaliacao()

        elif opcao == '6':
            salvar_todos()
        
        elif opcao == '7':
            salvar = input('\n Deseja salvar antes de sair? (s/n): ').lower()
            if salvar == 's':
                salvar_todos()
            print('\n👋 Obrigado por usar o Darkmoon Records!')
            break
        else:
            print ('❌ Opção inválida, tente novamente.')
        input('\nPressione ENTER para continuar...')

if __name__ == '__main__':
    main()