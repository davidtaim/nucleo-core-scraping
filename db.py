import mysql.connector


class DbMySql:
    def __init__(self) -> None:
        # DATABASE_URL="mysql://radicore_user:radiocore260@localhost:3306/radiocore"
        self.mydb = mysql.connector.connect(host='localhost', user='radicore_user', password='radiocore260',
                                            db='radiocore')

    def execute_insert_album(self, album: tuple) -> str:
        query = "insert into Album (title, country, genre, imageLink, views, postDate, updatedAt, idBand) " \
                "values (%s, %s, %s, %s, %s, %s, %s, 1);"
        cursor = self.mydb.cursor()
        cursor.execute(query, album)
        self.mydb.commit()
        id_row = cursor.lastrowid
        cursor.close()
        return str(id_row)

    def execute_insert_song(self, song) -> None:
        query = "insert into Song (idAlbum, name, updatedAt) values (%s, %s, %s);"
        cursor = self.mydb.cursor()
        cursor.execute(query, song)
        self.mydb.commit()
        cursor.close()

    def close_connection(self) -> None:
        self.mydb.close()
