import asyncio, os, argparse, time, random

from src.core.constants import Constants
from src.core.config import Config
from src.core.logger import Logger
from src.core.i18n import LanguageManager
from src.services.api import AgentService, MapService, ProfileService
from src.utils.shortcuts import ShortcutManager
from src.utils.utils import AnimateText
from src.utils.version import Version
from src.game.client import GameSession
from src.game.controller import GameController
from valclient.resources import regions

class InstalockerApp:
    def __init__(self):
        self.config = Config()
        self.logger = Logger(self.config)
        self.i18n = LanguageManager(self.config, self.logger)
        self.agent_service = AgentService(self.config, self.logger, self.i18n)
        self.map_service = MapService(self.config, self.logger, self.i18n)
        self.shortcut_mgr = ShortcutManager(self.config, self.logger, self.i18n, self.agent_service)
        self.profile_service = ProfileService(self.config, self.logger, self.i18n, self.map_service)
        self.session = GameSession(self.config, self.logger, self.i18n)
        self.write_animated_text = AnimateText().write_animated_text
        self.clear = AnimateText().clear
        self.parser = argparse.ArgumentParser()
        self.dt = self.agent_service.dt
        self.version = Version()
        self.versionResponse = self.version.versionControl()
        self.parser.add_argument("--agent", help="ajan ismi")
        self.parser.add_argument("--mode", help="seçim modu lock/select")
        self.parser.add_argument("--region", help="region idsi (eu,na vb)")
        self.parser.add_argument("--debug", help="hata ayıklama için true/false", type=bool)

    def find_region(self, auto_mode=True):
        """Loglardan kullanıcının regionunu arar"""
        self.logger.write(f"Bölge arama işlemi başlatıldı. mod: {auto_mode}")
        try:
            if auto_mode:
                self.logger.write(f"ShooterGame.log okunuyor: {Constants.SHOOTER_LOG_FILE_PATH}")
                with open(Constants.SHOOTER_LOG_FILE_PATH, "r", encoding="utf-8") as f:
                    region_line = None
                    for line in f.readlines():
                        if "https://glz-" in line:
                            region_line = line
                            break
                
                if region_line:
                    region = region_line.split("https://glz-")[1].split("-")[0].lower()
                    if region in regions:
                        self.logger.write(f"Bölge otomatik olarak bulundu: {region}", level="info")
                        return region
                else:
                    self.logger.write("Log dosyasında bölge bilgisi bulunamadı.", level="warn")

            self.logger.write("Manuel bölge girişi bekleniyor.")
            while True:
                self.i18n.print_lang("prompts.INPUT_select_server")
                region_input = input("").lower()
                
                if region_input in ("yardım", "help"):
                    self.clear()
                    print(", ".join(regions))
                    continue
                elif region_input not in regions:
                    self.clear()
                    self.i18n.print_lang("prompts.invalid_server")
                    continue
                else:
                    self.clear()
                    return region_input

        except FileNotFoundError:
             self.logger.write("ShooterGame.log bulunamadı.", level="error")
             self.i18n.print_lang("info.log_file_not_found")
             return self.find_region(False)
        except Exception as e:
            if not auto_mode:
                self.logger.write(f"Bölge hatası: {e}", "error")
                self.config.exit_flag = True
                self.i18n.print_lang("errors.general_error", e=str(e))
            else:
                return self.find_region(False)


    async def main_loop(self):
        self.i18n.load_user_language()
        self.i18n.load_language_file()
        
        while not self.config.exit_flag:
            self.logger.write("Ana döngü başlatılıyor.", level="info")
            try:
                self.config.user_broke_game = False
                self.config.exit_flag = False
                
                if not self.config.is_shortcut:
                    args = self.shortcut_mgr.parse_arguments(self.parser)
                    self.config.set_args(args)
                
                if self.config.region is None:
                    self.config.region = self.find_region()
                    
                if self.config.exit_flag:
                    break
                    
                self.logger.write(f"Bölge '{self.config.region}' olarak ayarlandı.", level="info")
                
                if Constants.clearOldFiles():
                    self.i18n.print_lang("success.clear_old_files")


                self.agent_service.loadAgents()
                if self.config.exit_flag:
                    break
                if not self.agent_service.agents:
                    self.i18n.print_lang("errors.agent_list_load_failed")
                    self.config.exit_flag = True
                    break
                self.logger.write(f"Ajan listesi yüklendi. {len(self.agent_service.agents)} ajan.", level="info")
                
                self.map_service.loadMaps()
                if self.config.exit_flag:
                    break
                if not self.map_service.maps:
                    self.i18n.print_lang("errors.map_list_load_failed")
                    self.config.exit_flag = True
                    break
                self.logger.write(f"Harita listesi yüklendi. {len(self.map_service.maps)} harita.", level="info")

                while not self.config.is_shortcut:
                    if self.versionResponse.get("isOld"):
                        self.i18n.print_lang("info.update_app_warn", version=self.versionResponse.get("apiVersion"))
                    self.i18n.print_lang("mode.options_header")
                    self.i18n.print_lang("mode.options")
                    self.i18n.print_lang("mode.INPUT_get_mode")
                    mode_input = input("").lower()
                    
                    if mode_input == "debug":
                        self.config.debug = True
                        self.clear()
                        continue
                    if mode_input == "":
                        self.clear()
                        self.i18n.print_lang("mode.set_to_lock")
                        self.config.mode = 1
                        break
                    elif mode_input in ("help", "yardım"):
                        self.clear()
                        self.i18n.print_lang("help.mode_select_message")
                        continue
                    elif not mode_input.isdecimal():
                        self.clear()
                        self.i18n.print_lang("prompts.enter_number")
                        continue
                        
                    mode_int = int(mode_input)
                    if mode_int == 1:
                        self.clear()
                        self.i18n.print_lang("mode.set_to_lock")
                        self.config.mode = 1
                        break
                    elif mode_int == 2:
                        self.clear()
                        self.i18n.print_lang("mode.set_to_select")
                        self.config.mode = 2
                        break
                    elif mode_int == 3:
                        self.clear()
                        self.i18n.print_lang("mode.set_to_macro")
                        self.config.mode = 3
                        break
                    else:
                        self.clear()
                        self.i18n.print_lang("prompts.enter_correct_mode")
                        continue

                success = self.session.start_client()
                if not success:
                    self.clear()
                    self.i18n.print_lang("debug.valorant_not_open")
                    await asyncio.sleep(3)
                    self.config.exit_flag = True
                    break
                    
                while not self.config.is_shortcut:
                    last = self.dt.today() - self.dt.strptime(self.agent_service.lastCheck, "%d.%m.%Y")
                    if last.days > 3:
                        self.i18n.print_lang("info.last_update_check", day=last.days)

                    if self.config.mode == 3:
                        if self.config.profilePath != "":
                            self.i18n.print_lang("prompts.INPUT_macro_profile_path_default", path=self.config.profilePath)
                        else: 
                            self.i18n.print_lang("prompts.INPUT_macro_profile_path")
                    else:
                        self.i18n.print_lang("prompts.INPUT_select_agent")
                    agent_input = input("").lower()
                    agent_input = agent_input.replace("'", "").replace("\"", "") # ? bu bişiyi etkilicek ve unutcam sonra hatayı bulmak için delircem eminim
                    self.logger.write(f"{"ajan inputu" if self.config.mode != 3 else "profil dosyası yolu"} : {agent_input}", "info")

                    if agent_input in ("yardım", "help"):
                        self.clear()
                        self.i18n.print_lang("help.agent_select_message")
                        continue
                    elif agent_input in ("güncelle", "update"):
                        self.clear()
                        self.agent_service.loadAgents(offline=False)
                        if self.config.exit_flag: break
                        self.map_service.loadMaps(offline=False)
                        if self.config.exit_flag: break
                        self.i18n.update_language_file()
                        if self.config.exit_flag: break
                        continue
                    elif agent_input in ("yb", "re"):
                        self.config.reboot_flag = True
                        self.logger.write("Kullanıcı yeniden başlatma istedi.")
                        self.i18n.print_lang("info.restarting")
                        time.sleep(0.5)
                        break
                    elif agent_input in ("ajanlar", "agents"):
                        self.clear()
                        agent_list = list(self.agent_service.agents.keys())
                        agent_list.remove("lastCheck")
                        print(", ".join(agent_list)+"\n\n")
                        continue
                    elif agent_input in ("ajanlar-l", "agents-l"):
                        self.clear()
                        agent_list = list(self.agent_service.agents.keys())
                        agent_list.remove("lastCheck")
                        print(agent_list, "\n\n")
                        continue
                    elif agent_input in ("liste-konumu", "agents-folder"):
                        self.clear()
                        print(Constants.AGENT_LIST_PATH, "\n\n")
                        continue
                    elif agent_input in ("kayıt-konumu", "logs-folder"):
                        self.clear()
                        print(Constants.LOG_PATH, "\n\n")
                        continue
                    elif agent_input in ("english", "türkçe"):
                        self.config.language = "english" if agent_input == "english" else "turkish"
                        self.clear()
                        self.i18n.print_lang("info.language_changed", language=self.config.language)
                        continue
                    elif agent_input in ("profil-oluştur", "create-profile", "cp", "po"):
                        returnedProfilePath = self.profile_service.createProfile()
                        self.config.profilePath = os.path.abspath(returnedProfilePath)
                        self.i18n.print_lang("success.profile_file_created", path=returnedProfilePath)
                        continue
                    elif agent_input in ("clear", "temizle", "cls"):
                        self.clear()
                    if self.config.mode == 3:
                        self.clear()
                        if (agent_input == "" or agent_input.isspace()) and self.config.profilePath != "":
                            path = self.config.profilePath
                        else:
                            path = agent_input
                        if path == "" or path.isspace():
                            continue
                        isValidProfile = self.profile_service.loadProfile(path)
                        
                        if not isValidProfile:
                            self.i18n.print_lang("errors.profile_file_not_loaded")
                            continue
                        self.i18n.print_lang("success.profile_file_loaded", path=path)
                        break
                    else:
                        selected_agent = ""
                        if agent_input in self.agent_service.agents and agent_input != "lastCheck":
                            selected_agent = agent_input
                        elif len(agent_input) >= 4:
                            for name in self.agent_service.agents:
                                if name.startswith(agent_input) and len(name) >len(agent_input): 
                                    selected_agent = name
                                    self.clear()
                                    break
                        elif agent_input in ("rastgele", "random", "r", "Kendimi Bok Gibi Hissediyorum :)"):
                            agent_list = list(self.agent_service.agents.keys()) # ? üşendiğimden 5 yere aynı yapıyı kopyaladım kim uğraşcak 
                            agent_list.remove("lastCheck")
                            selected_agent = random.choice(agent_list)
                        if selected_agent:
                            self.config.agent = selected_agent
                            self.logger.write(f"Ajan seçildi: {selected_agent}")
                            self.clear()
                            break
                        else:
                            self.clear()
                            self.i18n.print_lang("prompts.invalid_agent")
                            continue
                
                if self.config.exit_flag: break
                if self.config.reboot_flag:
                    self.config.reboot_flag = False
                    self.clear()
                    continue
                
                self.logger.write(f"State task'ı başlatılıyor: {self.config.agent}")
                controller = GameController(self.config, self.logger, self.i18n, self.session, self.shortcut_mgr, self.agent_service, self.map_service)
                await controller.mainInstalocker()
                
                if self.config.user_broke_game:
                    self.write_animated_text("Instalocker For Valorant")
                    continue
                elif self.config.exit_flag:
                     break
                     
            except asyncio.CancelledError:
                 self.logger.write("Main loop iptal edildi.")
                 self.config.exit_flag = True
            except Exception as e:
                 self.logger.write(f"Ana döngü hatası: {e}", "error")
                 print(f"Hata: {e}")
                 await asyncio.sleep(3)
                 self.config.exit_flag = True

    def run(self):
        os.system("color a")
        print("\033[H\033[J", end="")
        self.write_animated_text("Instalocker For Valorant")
        try:
            asyncio.run(self.main_loop())
        except Exception as e:
            self.logger.write(f"Ana fonksyionda kritik hata: {e}", "critical")
            print(f"Critical error: {e}")
