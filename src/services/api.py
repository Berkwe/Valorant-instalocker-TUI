import requests, json, os, time, traceback, winreg
from datetime import date
from requests.exceptions import ConnectionError
from src.core.constants import Constants
from src.core.logger import Logger
from src.core.i18n import LanguageManager
from src.core.config import Config

class AgentService:
    def __init__(self, config: Config, logger: Logger, i18n: LanguageManager):
        self.config = config
        self.logger = logger
        self.i18n = i18n
        self.agents = {}
        self.lastCheck = ""
        self.dt = date

    def updateApiData(self):
        """API den ajanları çeker"""
        self.logger.write("Valorant apisinden ajan listesi çekilmeye başlanıyor.")
        try:
            agents_temp = {}
            data = requests.get(Constants.VALORANT_AGENTS_API_URL, verify=False, timeout=4)
            data_dict = dict(data.json())

            if data.status_code != 200 or data_dict.get("status") != 200:
                self.logger.write(f"Valorant API hatası, HTTP Status: {data.status_code}, API Status: {data_dict.get('status')}", level="error")
                return {"status": data.status_code if data.status_code != 200 else data_dict.get("status"), "returned": False}

            for agent in data_dict.get("data"):
                display_name = agent.get("displayName").lower()
                uuid = agent.get("uuid")
                if display_name == "kay/o":
                    display_name = "kayo"
                agents_temp[display_name] = uuid
                self.logger.write(f"API'den ajan eklendi: {display_name} - {uuid}")
            self.logger.write(f"API'den {len(agents_temp)} ajan başarıyla çekildi.", level="info")
            self.lastCheck = self.dt.today().strftime("%d.%m.%Y")
            agents_temp["lastCheck"] = self.lastCheck
            return agents_temp
        
        except ConnectionError as e_conn:
            self.logger.write(f"Bağlantı hatası oluştu: {str(e_conn)}", level="error")
            return {"status": 0, "returned": False}
        except requests.exceptions.Timeout as e_timeout:
            self.logger.write(f"Zaman aşımı hatası oluştu: {str(e_timeout)}", level="error")
            return {"status": "Timeout", "returned": False}
        except requests.exceptions.RequestException as e_req:
            self.logger.write(f"API isteği sırasında hata oluştu: {str(e_req)}", level="error")
            return {"status": "RequestException", "returned": False}
        except Exception as e_gen:
            self.i18n.print_lang("errors.general_error", e=str(e_gen))
            error_details = traceback.format_exc()
            self.logger.write(f"Ajan listesi güncellenirken bilinmeyen bir hata oluştu: {error_details}", level="error")
            return {"status": "UnknownErrorInUpdate", "returned": False}

    def loadAgents(self, offline=True):
        """Ajanları dosyadan yükler dosya bozuksa veya yoksa günceller"""
        self.logger.write(f"Ajan listesi alma işlemi başlatıldı. Offline mod: {offline}")
        try:
            if offline:
                if not os.path.exists(Constants.AGENT_LIST_PATH):
                    self.logger.write("Local ajan dosyası bulunamadı, APIden güncelleniyor.", level="info")
                    self.i18n.print_lang("info.agent_file_not_found")
                    agent_list = self.updateApiData()
                    
                    if agent_list.get("returned") is False:
                        self.logger.write("Offline modda Ajan listesi çekilirken hata oluştu. : HTTP Hata kodu : "+str(agent_list.get("status", "hata kodu alınamadı")), level="error")
                        self.i18n.print_lang("errors.valorant_folder_not_found", path=Constants.AGENT_LIST_PATH)
                        time.sleep(3)
                        self.config.exit_flag = True
                        return

                    with open(Constants.AGENT_LIST_PATH, "w", encoding="utf-8") as f:
                        json.dump(agent_list, f, ensure_ascii=False, indent=4)
                    self.agents = agent_list
                    self.logger.write("Offline modda ajanlar dosyadan çekildi (API'den güncellendi).", level="info")
                    self.i18n.print_lang("success.agents_loaded")
                    return
                

                with open(Constants.AGENT_LIST_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if "jett" not in data.keys() or "kayo" not in data.keys() or "lastCheck" not in data.keys(): # ? yalandan bi kontrol
                        self.logger.write("Varsayılan ajan listesi bozuk. Güncelleniyor.", level="error")
                        self.i18n.print_lang("info.agent_list_corrupted")
                        self.loadAgents(offline=False)
                        return
                    self.lastCheck = data.get("lastCheck", "1.1.1")
                    self.agents = data
                    self.logger.write("Ajanlar offline olarak lokal agents.json dosyasından başarıyla çekildi.", level="info")
                    return

            self.logger.write("Online modda ajan listesi güncelleniyor.", level="info")
            agent_list = self.updateApiData()
            self.i18n.print_lang("info.agent_list_updating")
            
            success = not (isinstance(agent_list, dict) and agent_list.get("returned") is False)
            
            if success:
                with open(Constants.AGENT_LIST_PATH, "w", encoding="utf-8") as f:
                    json.dump(obj=agent_list, fp=f, ensure_ascii=False, indent=4)
                self.agents = agent_list
                self.logger.write("Online modda Ajan listesi güncellendi.", level="info")
                
                self.i18n.print_lang("success.agent_list_updated")
                return
            

            self.logger.write("Güncel ajan listesi çekilemedi, varsayılan liste çekilmeye çalışılıyor.", "warn")
            if not os.path.exists(Constants.AGENT_LIST_PATH):
               self.config.exit_flag = True
               self.logger.write("Varsayılan ajan listesi de çekilemedi, çıkılıyor", "error")
               return
                 
            with open(Constants.AGENT_LIST_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            if "jett" not in data.keys() or "lastCheck" not in data.keys():
                self.logger.write("Varsayılan ajan listesi de bozuk.", "error")
                self.config.exit_flag = True
                return
                     
            self.i18n.print_lang("success.agent_list_default_updated")
            self.agents = data


        except FileNotFoundError:
             self.logger.write(f"'{os.path.dirname(Constants.AGENT_LIST_PATH)}' bulunamadı.", level="error")
             self.i18n.print_lang("errors.valorant_folder_not_found", path=os.path.dirname(Constants.AGENT_LIST_PATH))
             time.sleep(3)
             self.config.exit_flag = True
        except Exception as e:
             error_details = traceback.format_exc()
             self.logger.write(f"Ajan listesi çekilirken bir hata oluştu: {error_details}", level="error")
             self.i18n.print_lang("errors.general_error", e=str(e))
             self.config.exit_flag = True


class MapService:
    def __init__(self, config: Config, logger: Logger, i18n: LanguageManager):
        self.config = config
        self.logger = logger
        self.i18n = i18n
        self.maps = {}
        self.excluded_maps = ["district", "kasbah", "drift", "piazza"]
    
    def updateApiData(self):
        """Valorant apisinden harita listesini çeker"""
        self.logger.write("Valorant apisinden map çekiliyor.")
        try:
            maps_temp = {}
            data = requests.get(Constants.VALORANT_MAPS_API_URL, verify=False, timeout=3)
            data_dict = dict(data.json())
            if data.status_code != 200 or data_dict.get("status") != 200:
                self.logger.write(f"Valorant API hatası, HTTP Status: {data.status_code}, API Status: {data_dict.get('status')}", level="error")
                return {"status": data.status_code if data.status_code != 200 else data_dict.get("status"), "returned": False}
            
            for map in data_dict.get("data"):
                displayName = map.get("displayName").lower()
                if displayName in self.excluded_maps:
                    continue
                mapUrl = map.get("mapUrl").lower()
                maps_temp[mapUrl] = displayName
                self.logger.write(f"Map eklendi : {displayName} - {mapUrl}")
                
            return maps_temp
        
        except ConnectionError as e_conn:
            self.logger.write(f"Bağlantı hatası oluştu: {str(e_conn)}", level="error")
            return {"status": 0, "returned": False}
        except requests.exceptions.Timeout as e_timeout:
            self.logger.write(f"Zaman aşımı hatası oluştu: {str(e_timeout)}", level="error")
            return {"status": "Timeout", "returned": False}
        except requests.exceptions.RequestException as e_req:
            self.logger.write(f"API isteği sırasında hata oluştu: {str(e_req)}", level="error")
            return {"status": "RequestException", "returned": False}
        except Exception as e_gen:
            self.i18n.print_lang("errors.general_error", e=str(e_gen))
            error_details = traceback.format_exc()
            self.logger.write(f"Ajan listesi güncellenirken bilinmeyen bir hata oluştu: {error_details}", level="error")
            return {"status": "UnknownErrorInUpdate", "returned": False}
        
    def loadMaps(self, offline = True):
        try:
            if offline:
                if not os.path.exists(Constants.MAP_LIST_PATH):
                    self.logger.write("Offline modda Map listesi bulunamadı. Apiden güncelleniyor..", "warn")
                    self.i18n.print_lang("info.map_file_not_found")
                    maps_list = self.updateApiData()

                    if maps_list.get("returned") is False:
                        self.logger.write("Offline modda Ajan listesi çekilirken hata oluştu. : HTTP Hata kodu : "+str(maps_list.get("status", "hata kodu alınamadı")), level="error")
                        self.i18n.print_lang("errors.valorant_folder_not_found", path=Constants.MAP_LIST_PATH)
                        time.sleep(3)
                        self.config.exit_flag = True
                        return
                    self.i18n.print_lang("success.map_list_updated")


                    with open(Constants.MAP_LIST_PATH, "w", encoding="utf-8") as f:
                        json.dump(maps_list, f, ensure_ascii=False, indent=4)
                    self.maps = maps_list
                    self.logger.write("Haritalar offline olarak lokal maps.json dosyasından yüklendi", "info")
                    return
            
                with open(Constants.MAP_LIST_PATH, "r", encoding="utf-8") as f:
                    maps_list = json.load(f)
                    if len(maps_list.keys()) < 5 or "ascent" not in maps_list.values():
                        self.i18n.print_lang("errors.map_file_broken")
                        self.loadMaps(False)
                        return
                    self.maps = maps_list
                    self.logger.write("Harita listesi lokalden çekildi.", "info")
                    return

            self.logger.write("Online modda harita listesi güncelleniyor", "info")
            maps_list = self.updateApiData()
            self.i18n.print_lang("info.map_list_updating")

            success = not (maps_list.get("returned") is False)
            
            if success:
                with open(Constants.MAP_LIST_PATH, "w", encoding="utf-8") as f:
                    json.dump(maps_list, f, ensure_ascii=False, indent=4)
                self.maps = maps_list
                self.logger.write("Online modda harita listesi güncellendi", "info")

                self.i18n.print_lang("success.map_list_updated")

            else:
                self.logger.write("Güncel map listesi çekilemedi, varsayılan liste çekiliyor", "warn")
                if not os.path.exists(Constants.MAP_LIST_PATH):
                    self.config.exit_flag = True
                    self.logger.write("Varsayılan map listesi de çekilemedi, çıkılıyor", "error")
                    return
                
                with open(Constants.MAP_LIST_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)

                if "ascent" not in data.keys():
                    self.logger.write("varsayılan map listesi de bozuk", "error")
                    self.config.exit_flag = True
                    return
                
                self.i18n.print_lang("success.map_list_default_updated")
                self.maps = data
        except FileNotFoundError:
            self.logger.write(f"'{os.path.dirname(Constants.MAP_LIST_PATH)}' bulunamadı.", level="error")
            self.i18n.print_lang("errors.valorant_folder_not_found", path=os.path.dirname(Constants.AGENT_LIST_PATH))
            time.sleep(3)
            self.config.exit_flag = True
        except Exception as e:
            error_details = traceback.format_exc()
            self.logger.write(f"Map listesi çekilirken bir hata oluştu: {error_details}", level="error")
            self.i18n.print_lang("errors.general_error", e=str(e))
            time.sleep(3)
            self.config.exit_flag = True

class ProfileService:
    def __init__(self, config: Config, logger: Logger, language_manager: LanguageManager, map_service):
        self.config = config
        self.logger = logger
        self.i18n = language_manager
        self.map_service = map_service

    def createProfile(self):
        """Masaüstüne profil dosyası oluşturur"""
        try:
            profile_file = {}
            profile_file_name = "Instalocker_profile"
            profile_file_name_ext = "_1"
            final_profile_file_name = ""
            self.logger.write("createProfile çağrıldı", "info")
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders") as reg_key:
                desktop_path, _ = winreg.QueryValueEx(reg_key, "Desktop")
                
            user_dir = os.path.expandvars(desktop_path)
            if not os.path.exists(user_dir):
                user_dir = os.path.expanduser("~")
            if self.config.language == "turkish":
                for _, map in self.map_service.maps.items():
                    profile_file[map] = Constants.PROFILE_FILE_DEFAULT_PROP_TR
            else:
                for _, map in self.map_service.maps.items():
                    profile_file[map] = Constants.PROFILE_FILE_DEFAULT_PROP_EN


            self.logger.write(f"Varsayılan profil dosyası oluşturuldu : {profile_file}")
            for i in range(1, 30):
                if os.path.exists(os.path.join(user_dir, final_profile_file_name)):
                    profile_file_name_ext = profile_file_name_ext[0]
                    profile_file_name_ext = "_"+str(i)
                    final_profile_file_name = profile_file_name+profile_file_name_ext
                    continue
                with open(os.path.join(user_dir, final_profile_file_name), "w", encoding="utf-8") as f:
                    json.dump(profile_file, f, ensure_ascii=False, indent=4)
                self.logger.write(f"{os.path.join(user_dir, final_profile_file_name)} yoluna profil dosyası oluşturuldu.", "info")
                return os.path.join(user_dir, final_profile_file_name)
            self.config.exit_flag = True
            raise TimeoutError("Profil dosyası 30 dan çok olduğundan Instalocker kapanıyor..")
        except Exception as e:
            detailed_exception = traceback.format_exc()
            self.logger.write(f"Hata : {detailed_exception}", "error")
            self.i18n.print_lang("errors.general_error", e=e)
            raise e





