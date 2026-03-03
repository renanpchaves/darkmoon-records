from modelo.darkmoon import Albums

cd1 = Albums('The Dark Side of the Moon', 'Pink Floyd', 10)
cd1.estoque_alt()

cd2 = Albums('Abbey Road', 'The Beatles', 17)
cd2.estoque_alt()

cd3 = Albums('Notes on a Conditional Form', 'The 1975', 22)

def main():
    Albums.listar_albums()

if __name__ == '__main__':
    main()