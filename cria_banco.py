import sqlite3

connection = sqlite3.connect('banco.db')

cursor = connection.cursor()

cria_tabela = 'CREATE TABLE IF NOT EXISTS hoteis (id text PRIMARY KEY,\
                                                    name text,\
                                                    stars real,\
                                                    rate real,\
                                                    city text)'

cria_hotel = 'INSERT OR REPLACE INTO hoteis VALUES ("alpha", "Alpha Hotel", 4.3, 345.30, "São Paulo")'

cursor.execute(cria_tabela)

cursor.execute(cria_hotel)

connection.commit()

connection.close()


