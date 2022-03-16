from abc import abstractmethod
import requests
import os
import img2pdf
import shutil
import abc
from PIL import Image
from PyPDF2 import PdfFileMerger


class Scraper(abc.ABC):
    """Responsible to scrape images from a website that are part of a chapter in a comic.

    Attributes:
    -----------
        site : int
            Gives the page number for the current chapter and is also name of the current image.
        chapter : int
            Holds the chapter number, this value does not get changed after Object creation.
        image : Response object from requests
            Is the Object that contains the image from a website
        current_page : Response object from requests
            Is the object that contains the complete html structure of the current page from page_url
        page_url : str
            Holds the current_page url
        main_url : str
            Holds the domain name of the website
        flag : int
            Indication for the methods download_chapter(self) and download_page(self) to stop
        cwd : str
            Contains the path to our current working directory
    """

    site = 1
    chapter = ''
    image = None
    current_page = ''
    page_url = ''
    main_url = ''
    flag = 0
    cwd = os.getcwd()

    def download_chapter(self):
        """downloads a whole chapter from a comic in a folder
        """
        self.create_folder()

        while self.flag != -1:
            self.download_page()

        os.chdir(self.cwd)
        return

    def download_page(self):
        """downloads the image from current_page
        """
        self.get_current_page()
        self.check_if_end()

        if self.flag == -1:
            return

        self.image_navigator()
        self.save_page()
        self.get_next_page()
        return

    def get_current_page(self):
        """Gets the html website from page_url and save the Response object in the class attribute current_page
        """
        self.current_page = requests.get(self.page_url)
        return

    @abstractmethod
    def get_next_page(self):
        """Contains the logic to navigate us to the next page. Method needs to increment the class variable
        site after invoking
        """
        pass

    @abstractmethod
    def image_navigator(self):
        """Extracts the image link and downloads the image. When downloading the image the response object
        gets saved in the class attribute image
        """
        pass

    def save_page(self):
        """Downloads the class attribute image in the chapter folder and names it after the class attribute site"""
        filename = str(self.site) + '.jpg'
        with open(filename, 'wb') as image_file:
            for chunk in self.image.iter_content(100000):
                image_file.write(chunk)
            return

    @abstractmethod
    def check_if_end(self):
        """Checks if current chapter has another site

        Returns
        -------
        -1 : int
            Stop, no more pages
        0 : int
            continue, at least one more page
        """
        pass

    def create_folder(self):
        """Creates a folder named by the chapter in the current working directory
        """
        os.makedirs(str(self.chapter), exist_ok=True)
        path = os.path.join(os.getcwd(), str(self.chapter))
        os.chdir(path)
        return


"""----- END OF SCRAPER -----"""


class Converter(abc.ABC):
    """Responsible to replace a folder of images with a single pdf file that contains all images in order

    Attributes
    ----------
    directory : string
        Contains the path to the comic directory
    folder : string
        Contains the path to the chapter
    name : string
        Contains the pdf name, which is the str(folder) + '.pdf'
    images : [string]
        List of all paths to the images in the folder
    """

    directory = ''
    folder = ''
    name = ''
    images = []

    def img_to_pdf(self):
        self.get_images()

        with open(self.name, "wb") as pdf:
            try:
                pdf.write(img2pdf.convert(self.images))
                shutil.rmtree(self.folder)
            except:
                self.convert_to_pdf()

    def get_images(self):
        self.images = []
        folder = os.listdir(self.folder)

        for i in range(1, len(folder) + 1):
            self.images.append(os.path.join(self.folder, str(i)))

        return

    def convert_to_pdf(self):
        i = 1
        path = os.path.join(self.cwd, self.folder)
        for img_path in self.images:
            try:
                img = Image.open(img_path + '.jpg')
            except FileNotFoundError:
                break
            rgb_im = img.convert('RGB')
            rgb_im.save(os.path.join(path, str(i) + '.pdf'))
            i += 1

        tmp_images = []
        for img in os.listdir(path):
            if img[-1] != 'f':
                continue
            else:
                tmp_images.append(os.path.join(path, img))

        # sort by order
        order_images = ['placeholder'] * (len(tmp_images))
        for img in tmp_images:
            current = img.split('\\')[-1]
            current = current.split('.')[0]
            current = int(current) - 1
            order_images[current] = img

        merger = PdfFileMerger()

        for pdf in order_images:
            merger.append(pdf)

        merger.write(self.folder + ".pdf")
        merger.close()

        shutil.rmtree(self.folder)

        return


"""----- END OF CONVERTER -----"""


class Make(abc.ABC):
    """"Responsible to wrap the functionality of Scraper and Converter. It creates a chapter or multiple chapters
    with only one method.

    Attributes
    ----------
    path : string
        Contains path to the comic folder
    """

    path = ''
    comic_name = ''

    @ abc.abstractmethod
    def make_chapter(self, chapter):
        """
        calls the concrete implementation of the scraper and converter

        Parameters
        ----------
        chapter : int

        Examples
        --------
        concreteComic(chapter).download_chapter()
        concteteComic(chapter).img_to_pdf()
        """
        pass

    def make_chapters(self, begin, end):
        end += 1
        for i in range(begin, end):
            self.make_chapter(i)
            print('Making Chapter: ' + str(i))
        return


"""----- END OF MAKE -----"""
