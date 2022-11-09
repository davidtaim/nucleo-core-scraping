from datetime import datetime
from core_radio_scrapping import CoreRadioWrapper
from db import DbMySql

class MySqlSaver:

    def __init__(self) -> None:
        pass

    def get_data_to_save(self, quantity = 1, page = 1, apply_q = True):
        app = CoreRadioWrapper(quantity_to_get=quantity, apply_quantity = apply_q)
        return app.get_all_data_from_page(page_number=page)

    def save_data(self):
        counter = 0
        page_number = 1
        data_to_save = self.get_data_to_save(1, page_number, False)
        db = DbMySql()
        for elem in data_to_save:
            album = (
            elem["album_title"],
            elem["album_info"]["country"],
            elem["album_info"]["genre"],
            elem["album_info"]["quality"],
            elem["album_image"],
            elem["album_info"]["quoteblock"]["views"],
            elem["album_info"]["quoteblock"]["post_date"],
            datetime.now())
            id_album = db.execute_insert_album(album)
            for dl in elem["album_info"]["download_links"]:
                download_link = (
                    id_album,
                    dl["quality"],
                    dl["link"],
                    datetime.now()
                )
                db.execute_insert_download_link(download_link)
            for song in elem["album_info"]["songs_list"]:
                song_tuple = (id_album, song, datetime.now())
                db.execute_insert_song(song_tuple)
            counter = counter + 1
        print("Datos guardados: ", counter)
        db.close_connection()
        

if __name__ == '__main__':
    app = MySqlSaver()
    app.save_data()