from extensions import OPManga
from opmangabot import manga_email


chapter = 1035

OPManga.OPMake().make_chapter(chapter)

manga_email.main(chapter)
