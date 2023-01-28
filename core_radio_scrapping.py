import re
import requests
from bs4 import BeautifulSoup, ResultSet
from logger import Logger


class CoreRadioWrapper:
    # Globarl URL by albums
    __URL__ = "https://coreradio.online/albums.html/page/"

    def __init__(self, quantity_to_get=1, apply_quantity=False) -> None:
        self.quantity_to_get = quantity_to_get
        self.apply_quantity = apply_quantity

    def load_page(self, page_number: int) -> str:
        return requests.get(self.__URL__ + str(page_number)).text

    @staticmethod
    def search_items(content_page: str) -> ResultSet:
        soup = BeautifulSoup(content_page, "lxml")
        return soup.find_all('li', class_='tcarusel-item main-news')

    def get_functional_data(self, items: ResultSet) -> list:
        results = []
        cont = 0
        for item in items:
            album_img_info = item.find('div', class_='tcarusel-item-image').find('a')
            image_link = album_img_info.find('img')['src']
            album_title = item.find('div', class_='tcarusel-item-title').find('a').get_text()
            download_songs = self.get_data_download_songs(album_img_info["href"])
            if len(download_songs) == 0:
                continue
            results.append({
                "album_image": image_link,
                "album_title": album_title,
                "album_info": download_songs
            })
            cont += 1
            if self.apply_quantity and self.quantity_to_get == cont:
                break
        return results

    @staticmethod
    def get_data_download_songs_3(info, index_genre, index_country, split_songs_genre):
        f_n_w_i_d_pre = info.get_text().split('Tracklist:')
        genre_country = f_n_w_i_d_pre[0].split('Quality')[0].split(split_songs_genre)
        tracklist = f_n_w_i_d_pre[1]
        return [genre_country[index_genre], genre_country[index_country], '', re.sub(r'[\d]+:\d[\d]?', '', tracklist).strip()]

    @staticmethod
    def get_data_download_songs_2(info, index_genre, index_country, split_songs_genre):
        info = info.find_all('div')[1]
        f_n_w_i_d_pre = info.get_text().split('Tracklist:')
        genre_country = f_n_w_i_d_pre[0].split('Quality')[0].split(split_songs_genre)
        tracklist = f_n_w_i_d_pre[1]
        return [genre_country[index_genre], genre_country[index_country], '', re.sub(r'[\d]+:\d[\d]?', '', tracklist).strip()]

    @staticmethod
    def get_data_download_songs_8(info, index_genre, index_country, split_songs_genre):
        if 'Tracklist:' in info[4].get_text():
            genre_country = info[3].get_text().split('Quality')[0].split(split_songs_genre)
            tracklist = info[5].get_text()
            return [genre_country[index_genre], genre_country[index_country], '', re.sub(r'[\d]+:\d[\d]?', '', tracklist).strip()]
        elif 'Genre' in info[1].get_text():
            genre_country = info[1].find_all('span')
            genre = genre_country[0].get_text().replace('\xa0', ' ')
            country = genre_country[1].get_text()
            tracklist = info[3].find_all('span')
            tracklist = ''.join(t.get_text().replace('\xa0', '') for t in tracklist)
            return [genre, country, '', re.sub(r'[\d]+:\d[\d]?', '', tracklist).strip()]
        else:
            genre_country = info[2].find_all('span')
            genre = genre_country[0].get_text().replace('\xa0', ' ')
            country = genre_country[1].get_text()
            tracklist = info[4].find_all('span')
            tracklist = ''.join(t.get_text().replace('\xa0', '') for t in tracklist)
            return [genre, country, '', re.sub(r'[\d]+:\d[\d]?', '', tracklist).strip()]

    @staticmethod
    def get_data_download_songs_6(info):
        if 'Country' in info[2].get_text():
            if '' == info[1].get_text():
                genre_country = info[2].find_all('span')
                genre = genre_country[0].get_text()
                country = genre_country[1].get_text()
                tracklist = info[4].find_all('span')
                tracklist = ''.join(t.get_text().replace('\xa0', '') for t in tracklist)
                return [genre, country, '', re.sub(r'[\d]+:\d[\d]?', '', tracklist).strip()]
            else:
                genre = info[1].get_text().strip()
                country_tracklist = info[2].get_text().split('Tracklist:')
                return [genre, country_tracklist[0].split('Quality')[0], '', re.sub(r'[\d]+:\d[\d]?', '', country_tracklist[1]).strip()]
        else:
            genre_country = info[1].find_all('span')
            genre = genre_country[0].get_text()
            country = genre_country[1].get_text()
            tracklist = info[3].find_all('span')
            tracklist = ''.join(t.get_text().replace('\xa0', '') for t in tracklist)
            return [genre, country, '', re.sub(r'[\d]+:\d[\d]?', '', tracklist).strip()]

    @staticmethod
    def get_data_download_songs_4(info):
        if '' == info[0].find_all('div')[12].get_text():
            all_data = info[0].find_all('div')[8].find_all('span')
            genre = all_data[0].get_text().replace(':', ': ', 1)
            country = all_data[1].get_text().replace(':', ': ', 1)
            tracklist = all_data[3].get_text()
            return [genre, country, '', re.sub(r'[\d]+:\d[\d]?', '', tracklist).strip()]
        else:
            info = info[0].find_all('div') #12 genre 13 country 17 tracklist
            genre = info[12].find('span').get_text().replace('\xa0', ' ')
            country = ': '
            tracklist = info[17].get_text()
            return [genre, country, '', re.sub(r'[\d]+:\d[\d]?', '', tracklist).strip()]

    @staticmethod
    def get_data_download_songs_0(info):
        info = info[1].find_all('div')[1].get_text().split('Tracklist:')
        if 'Bitrate' in info[0]:
            genre = info[0].split('Bitrate')[0].strip()
            country = ': '
        elif 'Quality' in info[0]:
            if info[0].split('Quality')[0].startswith('Country'):
                genre_country = info[0].split('Quality')[0].split('Genre')
                genre = genre_country[1].replace(' :', ': ', 1)
                country = ': '
                if len(genre_country) > 1:
                    country = genre_country[0].replace(' :', ': ')
            else:
                genre_country = info[0].split('Quality')[0].split('Country')
                genre = genre_country[0].replace(' :', ': ', 1)
                country = ': '
                if len(genre_country) > 1:
                    country = genre_country[1].replace(' :', ': ')
        elif 'Qiality' in info[0]:
            genre_country = info[0].split('Qiality')[0].split('Country')
            genre = genre_country[0].replace(' :', ': ', 1)
            country = ': '
            if len(genre_country) > 1:
                country = genre_country[1].replace(' :', ': ')
        elif 'Country' not in info[0]:
            genre_country = info[0].split('Genre')
            country = ': '
            genre = genre_country[1].replace(' :', ': ', 1)
        else:
            genre_country = info[0].split('Genre')
            country = genre_country[0].replace(' :', ': ', 1)
            genre = genre_country[1].replace(' :', ': ', 1)
        return [genre, country, '', re.sub(r'[\d]+:\d[\d]?', '', info[1]).strip()]

    def get_data_download_songs(self, link: str) -> dict:
        logger = Logger()
        variacion = -1
        data = requests.get(link).text
        soup = BeautifulSoup(data, 'lxml')
        full_news_pre = soup.find('div', class_='full-news-info')
        full_news_without_info = soup.find_all('div', class_='full-news')
        if full_news_pre is None:
            print("Album without full_news: ", link)
            return {}
        full_news = full_news_pre.find('td').get_text().strip().split('\n')
        if full_news is None or len(full_news) < 2:
            full_news_without_info_data = full_news_without_info[1].find_all('p')
            index_genre = 1
            index_country = 0
            split_songs_genre = 'Genre'
            try:
                match len(full_news_without_info_data):
                    case 0:
                        variacion = 0
                        full_news = self.get_data_download_songs_0(full_news_without_info)
                    case 2:
                        variacion = 2
                        full_news = self.get_data_download_songs_2(full_news_without_info[1], index_genre, index_country, split_songs_genre)
                    case 3:
                        variacion = 3
                        split_songs_genre = 'Country'
                        index_genre = 0
                        index_country = 1
                        full_news = self.get_data_download_songs_3(full_news_without_info_data[2], index_genre, index_country, split_songs_genre);
                    case 4:
                        variacion = 4
                        full_news = self.get_data_download_songs_4(full_news_without_info)
                    case 6: # Genero index 1 de full_news_without_info_data Country y tracklist en index 2
                        variacion = 6
                        full_news = self.get_data_download_songs_6(full_news_without_info_data)
                    case 8:
                        variacion = 8
                        split_songs_genre = 'Country'
                        index_genre = 0
                        index_country = 1
                        full_news = self.get_data_download_songs_8(full_news_without_info_data, index_genre, index_country, split_songs_genre)
                    case _:
                        print('Nueva variacion con otra cantidad no registrada:', len(full_news_without_info_data))
                        logger.print_log('Nueva variacion con otra cantidad no registrada: ' + str(len(full_news_without_info_data)))
                        logger.print_links_to_check("Variacion de: " + str(len(full_news_without_info_data)) + ', link: ' + link)
                        return {}
            except Exception as e:
                print('Nueva variacion de las ya registradas(', len(full_news_without_info_data), ')', ', error: ', str(e))
                logger.print_log('Nueva variacion de las ya registradas(' + str(len(full_news_without_info_data)) + ')' + ', error: ' + str(e))
                logger.print_links_to_check("Nueva variacion: " + str(len(full_news_without_info_data)) + ', link: ' + link)
                return {}
            
        try:
            songs_index = 3
            for songi, songitem in enumerate(full_news):
                if songitem.startswith('1.') or songitem.startswith('01.'):
                    songs_index = songi
                    break

            songs = re.split('\d[\d]?\. +', full_news[songs_index])
            songs.pop(0)
            quote_block = soup.find('div', class_='quoteblock').find('font').findChildren('div', class_='fullo-news-line')
            quote_block_dict = {
                "views": quote_block[0].get_text().strip().replace(' ', ''),
                "post_date": quote_block[2].get_text().strip(),
                "time_ago": quote_block[3].get_text().strip()
            }
            full_news_dict = {
                "genre": full_news[0].replace(': ', ':', 1).split(':')[1],
                "country": full_news[1].replace(': ', ':', 1).split(':')[1],
                "songs_list": songs,
                "quoteblock": quote_block_dict
            }
        except Exception as e:
            print("Error pasando a siguiente link: ", link)
            logger.print_log("Error pasando a siguiente link: " + link)
            print("Exception: ", str(e), ', variacion:', variacion)
            logger.print_log("Exception: " + str(e) + ', variacion: ' + str(variacion))
            print("Contenido erroneo: ", str(full_news))
            logger.print_log("Contenido erroneo: " + str(full_news))
            logger.print_links_to_check("Error parseando los datos finales, link: " + link)
            return {}
        return full_news_dict

    def get_all_data_from_page(self, page_number=1):
        page_content = self.load_page(page_number)
        items = self.search_items(page_content)
        return self.get_functional_data(items)
