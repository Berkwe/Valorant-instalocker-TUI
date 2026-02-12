import requests, json, os, time
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

    def update_apidata(self):
        """API den ajanları çeker"""
        self.logger.write("Valorant API'sinden ajan listesi çekilmeye başlanıyor.")
        try:
            agents_temp = {}
            data = requests.get(Constants.VALORANT_API_URL, verify=False, timeout=4)
            data_dict = dict(data.json())
            
            if data.status_code == 200 and data_dict.get("status") == 200:
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
            else:
                self.logger.write(f"Valorant API hatası, HTTP Status: {data.status_code}, API Status: {data_dict.get('status')}", level="error")
                return {"status": data.status_code if data.status_code != 200 else data_dict.get("status"), "returned": False}
                
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
            self.logger.write(f"Ajan listesi güncellenirken bilinmeyen bir hata oluştu: {str(e_gen)}", level="error")
            return {"status": "UnknownErrorInUpdate", "returned": False}

    def load_agents(self, offline=True):
        """Ajanları dosyadan yükler dosya bozuksa veya yoksa günceller"""
        self.logger.write(f"Ajan listesi alma işlemi başlatıldı. Offline mod: {offline}")
        try:
            if offline:
                if not os.path.exists(Constants.AGENT_LIST_PATH):
                    self.logger.write("Local ajan dosyası bulunamadı, APIden güncelleniyor.", level="info")
                    self.i18n.print_lang("info.agent_file_not_found")
                    agent_list = self.update_apidata()
                    
                    if isinstance(agent_list, dict) and agent_list.get("returned") is False:
                        self.logger.write("Offline modda Ajan listesi çekilirken hata oluştu. : HTTP Hata kodu : "+str(agent_list.get("status", "hata kodu alınamadı")), level="error")
                        self.i18n.print_lang("errors.valorant_folder_not_found", path=Constants.AGENT_LIST_PATH)
                        print(f"HTTP Hata kodu : {agent_list.get('status', 'hata kodu alınamadı')}")
                        time.sleep(3)
                        self.config.exit_flag = True
                        return
                    else:
                        with open(Constants.AGENT_LIST_PATH, "w", encoding="utf-8") as f:
                            json.dump(agent_list, f, ensure_ascii=False, indent=4)
                        self.agents = agent_list
                        self.logger.write("Offline modda ajanlar dosyadan çekildi (API'den güncellendi).", level="info")
                        self.i18n.print_lang("success.agents_loaded")
                        return
                else:
                    with open(Constants.AGENT_LIST_PATH, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if "jett" not in data.keys() or "kayo" not in data.keys() or "lastCheck" not in data.keys(): # ? yalandan bi kontrol
                            self.logger.write("Varsayılan ajan listesi bozuk. Güncelleniyor.", level="error")
                            self.i18n.print_lang("info.agent_list_corrupted")
                            self.load_agents(offline=False)
                            return
                        self.lastCheck = data.get("lastCheck", "1.1.1")
                        self.agents = data
                        self.logger.write("Ajanlar offline olarak lokal agents.json dosyasından başarıyla çekildi.", level="info")
                        return

            self.logger.write("Online modda ajan listesi güncelleniyor.", level="info")
            agent_list = self.update_apidata()
            self.i18n.print_lang("info.agent_list_updating")
            
            success = not (isinstance(agent_list, dict) and agent_list.get("returned") is False)
            
            if success:
                with open(Constants.AGENT_LIST_PATH, "w", encoding="utf-8") as f:
                    json.dump(obj=agent_list, fp=f, ensure_ascii=False, indent=4)
                self.agents = agent_list
                self.logger.write("Online modda Ajan listesi güncellendi.", level="info")
                
                if not os.path.exists(Constants.AGENT_LIST_PATH):
                     self.i18n.print_lang("success.agent_list_updated")
                else:
                     self.i18n.print_lang("success.agent_list_updated_short")
            else:
                 self.logger.write("Güncel ajan listesi çekilemedi, varsayılan liste çekilmeye çalışılıyor.", "error")
                 if not os.path.exists(Constants.AGENT_LIST_PATH):
                      self.config.exit_flag = True
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
             self.logger.write(f"Ajan listesi çekilirken bir hata oluştu: {str(e)}", level="error")
             self.i18n.print_lang("errors.general_error", e=str(e))
             self.config.exit_flag = True
