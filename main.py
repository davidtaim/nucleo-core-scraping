import time
from datetime import datetime
from core_radio_scrapping import CoreRadioWrapper
from db import DbMySql
from logger import Logger

class MySqlSaver:

    def __init__(self) -> None:
        pass

    @staticmethod
    def get_data_to_save(quantity=1, page=1, apply_q=True):
        wrapper = CoreRadioWrapper(quantity_to_get=quantity, apply_quantity=apply_q)
        return wrapper.get_all_data_from_page(page_number=page)

    def save_data(self):
        logger = Logger()
        counter = 0  # Cuantos datos se guardaron en total
        counter_page = 0
        page_number = 499  # a 26 de enero del 2023 son 607 se ira restando how_many_pages
        how_many_pages = 50  # Cuantas paginas leer 607 - 57 = 550
        how_many_pages_counter = 0  # Para saber cuantas lleva
        for pn in range(page_number, page_number - how_many_pages, -1):
            counter_page = 0
            print("Pagina #", pn, sep='')
            data_to_save = self.get_data_to_save(1, pn, False)
            how_many_pages_counter = how_many_pages_counter + 1
            db = DbMySql()
            for elem in data_to_save:
                album = (
                    elem["album_title"],
                    elem["album_info"]["country"],
                    elem["album_info"]["genre"],
                    elem["album_image"],
                    elem["album_info"]["quoteblock"]["views"],
                    elem["album_info"]["quoteblock"]["post_date"],
                    datetime.now())
                id_album = db.execute_insert_album(album)
                for song in elem["album_info"]["songs_list"]:
                    song_tuple = (id_album, song.strip(), datetime.now())
                    db.execute_insert_song(song_tuple)
                counter = counter + 1
                counter_page = counter_page + 1
            db.close_connection()
            print("Datos guardados de la pagina: ", pn, ", #", counter_page, ', total: ', counter, sep='')
            logger.print_log("Datos guardados de la pagina: " + str(pn) + ", #" + str(counter_page) + ', total: ' + str(counter))
            time.sleep(30)
        print("Datos guardados en total: ", counter)
        logger.print_log("Datos guardados en total: " + str(counter))


if __name__ == '__main__':
    app = MySqlSaver()
    app.save_data()
