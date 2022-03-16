import comic
import bs4
import requests
import os


class OPScraper(comic.Scraper):

    def __init__(self, chapter):
        self.chapter = chapter
        self.main_url = 'http://onepiece-tube.com/kapitel/' + str(chapter) + '/'
        self.page_url = self.main_url + str(self.site)

    def get_next_page(self):
        self.site += 1
        self.page_url = self.main_url + str(self.site)
        return

    def check_if_end(self):
        if self.site == 1:
            return

        end_tag = '<title>404 - Fehler: 404</title>'
        soup = bs4.BeautifulSoup(self.current_page.text)
        title_tag = soup.title

        if end_tag == str(title_tag):
            self.flag = -1
            return

        return

    def image_navigator(self):
        image_bs = bs4.BeautifulSoup(self.current_page.text)
        image_elem = image_bs.select('img')  # gets all html Tags with img
        image_url = image_elem[0]['src']  # link to img src
        self.image = requests.get(image_url)  # download actual image
        self.image.raise_for_status()
        return


class OPConverter(comic.Converter):

    def __init__(self, folder):
        self.cwd = os.path.join(os.getcwd(), 'One_Piece_Manga')
        self.name = str(folder) + '.pdf'
        self.folder = os.path.join(self.cwd, str(folder))
        os.chdir(self.cwd)


class OPMake(comic.Make):

    def __init__(self):
        self.folder = 'One_Piece_Manga'
        self.path = os.path.join(os.getcwd(), self.folder)
        os.makedirs(self.path, exist_ok=True)
        os.chdir(self.path)

    def make_chapter(self, chapter):
        OPScraper(chapter).download_chapter()
        OPConverter(chapter).img_to_pdf()
        return
