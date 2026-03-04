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
    print('4. Adicionar avaliação')
    print('5. Sair')
    print()

#cadastrando um novo disco no sistema
def cadastrar_discos():
    '''
    Pede as infos para cadastro de um novo album
    '''
    print('\n📀 CADASTRAR NOVO DISCO\n')

    nome = input('Nome do album: ')
    artista = input('Nome do artista')
    while True:
        try:
            quant_musicas = int(input('Quantidade de músicas: '))
            break
        except ValueError:
            print ('❌ Favor inserir apenas números. ')

    #criação do album
    novo_album = Albums(nome, artista, quant_musicas)

    #está em estoque?
    em_estoque = input('Está em estoque? (s/n): ').lower()
    if em_estoque == 's':
        novo_album.estoque_alt()
    print(f'\n✅ Álbum "{nome}" cadastrado com sucesso!')

def listar_discos():
    '''
    Lista todos os discos cadastrados no sistema
    '''
    print('\n📚 CATÁLOGO COMPLETO\n')
    Albums.listar_albums()

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
        print (f'{i+1}. {album.nome} - {album.ativo}')

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
    if not Albums.album:
            print ('Não há nenhum album cadastrado...')
    #mostrando tds os albums
    print('Álbuns cadastrados:')
    for i, album in enumerate(Albums.album):
        print(f'{i+1}. {album._nome}')

    #usuário escolhe o album:
    cliente = input ('Digite seu nome: ')

    while True:
        try:
            nota = float(input('Nota (0 a 5): '))
            if Albums.album[escolha].receber_avaliacao(cliente, nota):
                print('Avaliaçao registrada.')
            else:
                print ('❌ Nota deve estar entre 0 e 5.')
        except ValueError:
            print('❌ Digite um número válido!')

def main():
    while True:
        to_menu()
        opcao = input('Escolha uma opção: ')
        
        #menu principal do usuário
        if opcao == '1':
            cadastrar_disco()
        
        elif opcao == '2':
            listar_discos()
        
        elif opcao == '3':
            alterar_estoque()
        
        elif opcao == '4':
            adicionar_avaliacao()
        
        elif opcao == '5':
            print('\n👋 Obrigado por usar o Darkmoon Records!')
            break
        
        else:
            print ('❌ Opção inválida, tente novamente.')
        input('\nPressione ENTER para continuar...')

if __name__ == '__main__':
    main()

cd1 = Albums('The Dark Side of the Moon', 'Pink Floyd', 10)
cd2 = Albums('Abbey Road', 'The Beatles', 17)
cd3 = Albums('Notes on a Conditional Form', 'The 1975', 22)