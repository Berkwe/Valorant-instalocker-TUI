import time
from src.core.logger import Logger
from src.core.config import Config
from src.utils.version import Version


class AnimateText:
    def __init__(self):
        self.config = Config()
        self.logger = Logger(self.config)
        self.version = Version()
        self.__author__ = self.version.__author__
        self.__version__ = self.version.__version__

    def write_animated_text(self, header, footer="author"):
        """Güzide bir açılış ekranı"""
        self.logger.write(f"yaz fonksiyonu çağrıldı. header1: '{header}', footer: '{footer}'")
        randoms = "01"
        if footer.lower() == "author":
            footer = f"    By {self.__author__}\n".center(150) # ? ayıp olmasın diye boşluk
            footer += f"{self.__version__}"
        for i in range(len(header)):
            for k in randoms:
                print((header[:i] + k).center(150).removesuffix(" "))
                time.sleep(0.005)
                print("\033[H\033[J", end="")
        print(header.center(150)+"\n")
        time.sleep(0.3)
        print(footer)
        self.logger.write(f"yaz fonksiyonu tamamlandı. Ekrana '{header}' ve '{footer}' yazdırıldı.", level="info")
