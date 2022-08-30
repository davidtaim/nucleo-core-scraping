import requests, re
from bs4 import BeautifulSoup, ResultSet

class CoreRadioWrapper:
    #Globarl URL by albums
    __URL__ = "https://coreradio.online/albums.html/page/"

    def __init__(self, quantity_to_get = 1, apply_quantity = False) -> None:
        self.quantity_to_get = quantity_to_get
        self.apply_quantity = apply_quantity

    def load_page(self, page_number: int) -> str:
        return requests.get(self.__URL__ + str(page_number)).text
    
    def search_items(self, content_page: str) -> ResultSet:
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
            album_info_dict = {}
            album_info_dict["album_title"] = album_title
            results.append({
                "album_image": image_link,
                "album_title": album_title,
                "album_info": download_songs
            })
            cont += 1
            if self.apply_quantity and self.quantity_to_get == cont:
                break
        return results
    
    def get_data_download_songs(self, link: str) -> dict:
        data = requests.get(link).text
        soup = BeautifulSoup(data, 'lxml')
        full_news = soup.find('div', class_='full-news-info').find('td').get_text().strip().split('\n')        
        songs = re.split('\d[\d]?\. +', full_news[3])
        songs.pop(0)
        download_links = soup.find('div', class_='quotel').find('font').children
        download_links_list = []
        for dl in download_links:
            dl_elem = dl.find('section')
            if (dl_elem != -1 and dl_elem != None):
                dl_a = dl_elem.find('a')
                download_links_list.append({"quality": dl_a.get_text(), "link": dl_a["href"]})
        quote_block = soup.find('div', class_='quoteblock').find('font').findChildren('div', class_='fullo-news-line')
        quote_block_dict = {
            "views": quote_block[0].get_text().strip(),
            "post_date": quote_block[2].get_text().strip(),
            "time_ago": quote_block[3].get_text().strip()
        }
        full_news_dict = {
            "genre": full_news[0].split(': ')[1],
            "country": full_news[1].split(': ')[1],
            "quality": full_news[2].split(': ')[1],
            "songs_list": songs,
            "download_links": download_links_list,
            "quoteblock": quote_block_dict
        }
        return full_news_dict

    def get_all_data_from_page(self, page_number = 1):
        page_content = self.load_page(page_number)
        items = self.search_items(page_content)
        return self.get_functional_data(items)