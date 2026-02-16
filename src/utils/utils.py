import time, os, winreg, json
from src.core.logger import Logger
from src.core.config import Config
from src.utils.version import Version
from src.core.constants import Constants


class AnimateText:
    def __init__(self, map_service):
        self.config = Config()
        self.logger = Logger(self.config)
        self.version = Version()
        self.map_service = map_service
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
                os.system("cls")
        print(header.center(150)+"\n")
        time.sleep(0.3)
        print(footer)
        self.logger.write(f"yaz fonksiyonu tamamlandı. Ekrana '{header}' ve '{footer}' yazdırıldı.", level="info")

    def createProfile(self):
        """Masaüstüne profil dosyası oluşturur"""
        profile_file = {}
        profile_file_name = "Instalocker_profile_1"
        self.logger.write("createProfile çağrıldı", "info")
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders") as reg_key:
            desktop_path, _ = winreg.QueryValueEx(reg_key, "Desktop")
            
        user_dir = os.path.expandvars(desktop_path)
        if not os.path.exists(user_dir):
            user_dir = os.path.expanduser("~")
        if self.config.language == "turkish":
            for _, map in self.map_service.maps:
                profile_file[map] = Constants.PROFILE_FILE_DEFAULT_PROP_TR
        else:
            for _, map in self.map_service.maps:
                profile_file[map] = Constants.PROFILE_FILE_DEFAULT_PROP_EN


        self.logger.write(f"Varsayılan profil dosyası oluşturuldu : {profile_file}")
        for i in range(1, 30):
            if os.path.exists(os.path.join(user_dir, profile_file_name)):
                profile_file_name = profile_file_name[:2]
                profile_file_name += "_"+str(i)
                continue
            with open(os.path.join(user_dir, profile_file_name), "w", encoding="utf-8") as f:
                json.dump(profile_file, f, ensure_ascii=False, indent=4)
            self.logger.write(f"{os.path.join(user_dir, profile_file_name)} yoluna profil dosyası oluşturuldu.", "info")
            return os.path.join(user_dir, profile_file_name)
        self.config.exit_flag = True
        raise TimeoutError("Profil dosyası 30 dan çok olduğundan Instalocker kapanıyor..")
