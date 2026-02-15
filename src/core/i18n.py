import json, os, requests, time
from .constants import Constants
from .logger import Logger
from .config import Config

class LanguageManager:
    def __init__(self, config: Config, logger: Logger):
        self.config = config
        self.logger = logger
        self.language_file = {}
        self.decode_error_count = 0

    def load_user_language(self, auto_mode=True):
        """Kullanıcı dilini logdan çekmeye çalışır"""
        try:
            if auto_mode:
                if not os.path.exists(Constants.SHOOTER_LOG_FILE_PATH):
                    self.logger.write("Otomatik dil belirlenemedi, kullanıcıya dil sorulacak.", "warning")
                    return self.load_user_language(auto_mode=False)

                with open(Constants.SHOOTER_LOG_FILE_PATH, "r", encoding="utf-8") as f:
                    data = f.read().lower()

                if "tr-tr" in data:
                    self.config.language = "turkish"
                    self.logger.write("Otomatik dil tespit edildi: Türkçe", "info")
                else:
                    self.config.language = "english"
                    self.logger.write("Otomatik dil tespit edildi: İngilizce", "info")
                return

            else:
                for _ in range(5):
                    print("Automatic language detection failed, Please select your language.")
                    language_input = input("Select Language (ingilizce/english/EN, türkçe/turkish/TR) : ").lower()

                    if language_input in ("help", "yardım"):
                        self.logger.write("Kullanıcı yardım istedi.", "info")
                        print("neyin yardımını istiyon amk")
                        continue

                    elif language_input in ("ingilizce", "english", "en"):
                        self.config.language = "english"
                        self.logger.write("Kullanıcı İngilizce dilini seçti.", "info")
                        return

                    elif language_input in ("türkçe", "turkish", "tr"):
                        self.config.language = "turkish"
                        self.logger.write("Kullanıcı Türkçe dilini seçti.", "info")
                        return

                    else:
                        self.logger.write(f"Yanlış dil girildi: {language_input}", "warning")
                        print("You wrote the language incorrectly, only English/EN, Turkish/TR")
                else:
                    self.logger.write("Kullanıcı 5 kez yanlış dil girdi, Instalocker kapanıyor.", "error")
                    print("Incorrect entry attempted 5 times, Instalocker is shutting down...")
                    self.config.exit_flag = True

        except Exception as e:
            self.logger.write(f"Hata oluştu getUserLang() : {e}", "error")
            print(f"An error occurred : {e}")
            self.config.exit_flag = True

    def update_language_file(self):
        """Dil dosyasını günceller"""
        try:
            self.logger.write("updateLanguageFile fonksiyonu çağrıldı.", "info")
            response = requests.get(Constants.LANGUAGE_FILE_URL, timeout=17)
            data = dict(response.json() or {})

            if response.status_code != 200:
                self.logger.write(f"Language file çekilemedi. Status code: {response.status_code}", "error")
                print("The language file could not be downloaded. Please check your internet connection.")
                return {"response": False, "data": data}

            self.logger.write(f"Language file başarıyla çekildi.\n\n{data}\n\n", "info")
            
            with open(Constants.LANGUAGE_FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            self.logger.write(f"Language file {Constants.LANGUAGE_FILE_PATH} içine yazıldı.", "info")
            self.load_language_file()
            return {"response": True, "data": data}

        except requests.exceptions.RequestException as req_err:
            self.logger.write(f"Request hatası oluştu : {req_err}", "error")
            print(f"A request error occurred : {req_err}")
            return {"response": False, "data": {}}

        except Exception as e:
            self.logger.write(f"updateLanguageFile sırasında beklenmeyen hata: {e}", "error")
            print(f"An error occurred during updateLanguageFile : {e}")
            return {"response": False, "data": {}}

    def load_language_file(self):
        """Dil dosyasını diskten çeker"""
        try:
            self.logger.write("getLanguageFile() çağrıldı.", "info")

            if not os.path.exists(Constants.LANGUAGE_FILE_PATH):
                print("Language file not found, downloading remotely...")
                self.logger.write("Dil dosyası mevcut değil, updateLanguageFile() çağrılıyor.", "warning")

                response = self.update_language_file()
                if not response.get("response"):
                    print(f"Language file could not be retrieved. HTTP code : {response.get('data', {}).get('status_code', 'Unknown')}")
                    time.sleep(4)
                    return

            with open(Constants.LANGUAGE_FILE_PATH, "r", encoding="utf-8") as f:
                self.language_file = json.load(f)
                self.logger.write("Dil dosyası başarıyla yüklendi.", "info")
            
            self.decode_error_count = 0

        except json.JSONDecodeError:
            self.decode_error_count += 1
            self.logger.write(f"JSONDecodeError yakalandı, deneme sayısı: {self.decode_error_count}", "warning")

            if self.decode_error_count == 1:
                os.remove(Constants.LANGUAGE_FILE_PATH)
                self.logger.write("Bozuk dil dosyası silindi, yeniden indiriliyor...", "warning")
                self.load_language_file()
            else:
                self.logger.write("JSONDecodeError iki kez tekrarlandı, program sonlandırılıyor.", "critical")
                print("The language file was found to be incorrect twice, the program is terminating.")
                time.sleep(4)
                self.config.exit_flag = True

        except Exception as e:
            print(f"An error occurred while reading the language file : {e}")
            self.logger.write(f"Dil dosyası okunurken hata: {e}", "error")

    def print_lang(self, key_path: str, **kwargs):
        """Dile göre yazdırma fonksyonu"""
        try:
            inline = False
            if not self.language_file:
                self.load_language_file()
            
            lang_data = self.language_file.get(self.config.language, self.language_file.get("english", {}))
            
            if "INPUT" in key_path:
                inline = True
                
            keys = key_path.split('.')
            text = lang_data
            
            for key in keys:
                text = text.get(key)
                if text is None:
                    self.logger.write(f"printLang: '{key_path}' bulunamadı!", "error")
                    print(f"Key missing: {key_path}, updating language file...")
                    if self.update_language_file().get("response"):
                        self.load_language_file()
                        print("Updated. Please restart if issue persists.")
                    return
            
            if kwargs:
                try:
                    text = text.format(**kwargs)
                except KeyError as e:
                    self.logger.write(f"printLang format hatası: {e} - key: {key_path}", "error")
                    print(f"missing variable {e} - {text}")
                    return
            
            if inline:
                print(text, end="")
            else:
                print(text)
            
            self.logger.write(f"printLang: {key_path} -> {text}", "info")
            
        except Exception as e:
            self.logger.write(f"printLang genel hatası: {e}", "error")
            print(f"error : {e}")
