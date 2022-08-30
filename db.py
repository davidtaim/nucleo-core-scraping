import mysql.connector

class DbMySql:
    def __init__(self) -> None:
        self.mydb = mysql.connector.connect(host='108.179.194.28', user='lovenoti_core', password='polaris260', db='lovenoti_core_radio')

    def execute_insert_album(self, album: tuple) -> str:
        query = "insert into Album (title, country, genre, qualityAvailable, imageLink, views, postDate, timeAgo, updatedAt) values (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
        cursor = self.mydb.cursor()
        cursor.execute(query, album)
        self.mydb.commit()
        id_row = cursor.lastrowid
        cursor.close()
        return str(id_row)

    def execute_insert_download_link(self, download_link) -> None:
        query = "insert into DownloadLink (idAlbum, quality, link, updatedAt) values (%s, %s, %s, %s);"
        cursor = self.mydb.cursor()
        cursor.execute(query, download_link)
        self.mydb.commit()
        cursor.close()


    def execute_insert_song(self, song) -> None:
        query = "insert into Song (idAlbum, name, updatedAt) values (%s, %s, %s);"
        cursor = self.mydb.cursor()
        cursor.execute(query, song)
        self.mydb.commit()
        cursor.close()

    def close_connection(self) -> None:
        self.mydb.close()