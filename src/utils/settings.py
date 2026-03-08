import traceback, os, time, json
from src.core.constants import Constants
from src.core.config import Config
from src.core.logger import Logger

class SettingsManager:
    def __init__(self, config: Config, logger: Logger):
        self.config = config
        self.logger = logger
        pass
    
    def createSettings(self):
        try:
            with open(Constants.SETTINGS_PATH, "w", encoding="utf-8") as f:
                json.dump(Constants.SETTINGS_DEFAULT_PROP, f, ensure_ascii=False, indent=4)
        except Exception as e:
            detailed_traceback = traceback.exc()
            self.logger.write(f"Ayar dosyası oluşturulurken bir hata oluştu : {detailed_traceback}", "error")
            self.config.exit_flag = True
            time.sleep(4)
            return

    def setSetting(self, settingKey, settingValue):
        try:
            if not self.config.settings:
                self.getSettings()
            
            if self.config.settings.get(settingKey) is None or settingValue is None:
                self.logger.write(f"patlama yanlış anahtar girdin eşşek, : {settingKey} : {settingValue}", "info")
                return -1

            self.config.settings[settingKey] = settingValue
            with open(Constants.SETTINGS_PATH, "w", encoding="utf-8") as f:
                json.dump(self.config.settings, f, ensure_ascii=False, indent=4)
        except Exception as e:
            detailed_traceback = traceback.exc()
            self.logger.write(f"Ayarlar çekilirken bir hata oluştu : {detailed_traceback}", "error")
            self.config.exit_flag = True
            time.sleep(4)
            return

    def getSettings(self):
        try:
            if not os.path.exists(Constants.SETTINGS_PATH):
                self.createSettings()
            
            with open(Constants.SETTINGS_PATH, "r", encoding="utf-8") as f:
                tempJson = json.load(f)

            self.config.settings = tempJson
        except Exception as e:
            detailed_traceback = traceback.exc()
            self.logger.write(f"Ayarlar çekilirken bir hata oluştu : {detailed_traceback}", "error")
            self.config.exit_flag = True
            time.sleep(4)
            return