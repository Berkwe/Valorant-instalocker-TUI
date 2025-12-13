import asyncio, os, argparse, sys, time

from src.core.constants import Constants
from src.core.config import Config
from src.core.logger import Logger
from src.core.i18n import LanguageManager
from src.services.api import AgentService
from src.utils.shortcuts import ShortcutManager
from src.utils.utils import AnimateText
from src.game.client import GameSession
from src.game.controller import GameController
from valclient.resources import regions

class InstalockerApp:
    def __init__(self):
        self.config = Config()
        self.logger = Logger(self.config)
        self.i18n = LanguageManager(self.config, self.logger)
        self.agent_service = AgentService(self.config, self.logger, self.i18n)
        self.shortcut_mgr = ShortcutManager(self.config, self.logger, self.i18n, self.agent_service)
        self.session = GameSession(self.config, self.logger, self.i18n)
        self.write_animated_text = AnimateText().write_animated_text
        self.parser = argparse.ArgumentParser()
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
                    os.system("cls")
                    print(", ".join(regions))
                    continue
                elif region_input not in regions:
                    os.system("cls")
                    self.i18n.print_lang("prompts.invalid_server")
                    continue
                else:
                    os.system("cls")
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
                
                self.agent_service.load_agents()
                if self.config.exit_flag: 
                    break
                if not self.agent_service.agents:
                    self.i18n.print_lang("errors.agent_list_load_failed")
                    self.config.exit_flag = True
                    break
                    
                self.logger.write(f"Ajan listesi yüklendi. {len(self.agent_service.agents)} ajan.", level="info")

                while not self.config.is_shortcut:
                    self.i18n.print_lang("mode.options_header")
                    self.i18n.print_lang("mode.options")
                    self.i18n.print_lang("mode.INPUT_get_mode")
                    mode_input = input("").lower()
                    
                    if mode_input == "debug":
                        self.config.debug = True
                        os.system("cls")
                        continue
                    if mode_input == "":
                        os.system("cls")
                        self.i18n.print_lang("mode.set_to_lock")
                        self.config.mode = 1
                        break
                    elif mode_input in ("help", "yardım"):
                        os.system("cls")
                        self.i18n.print_lang("help.mode_select_message")
                        continue
                    elif not mode_input.isdecimal():
                        os.system("cls")
                        self.i18n.print_lang("prompts.enter_number")
                        continue
                        
                    mode_int = int(mode_input)
                    if mode_int == 1:
                        os.system("cls")
                        self.i18n.print_lang("mode.set_to_lock")
                        self.config.mode = 1
                        break
                    elif mode_int == 2:
                        os.system("cls")
                        self.i18n.print_lang("mode.set_to_select")
                        self.config.mode = 2
                        break
                    else:
                        os.system("cls")
                        self.i18n.print_lang("prompts.enter_1_or_2")
                        continue

                success = self.session.start_client()
                if not success:
                    os.system("cls")
                    self.i18n.print_lang("debug.valorant_not_open")
                    await asyncio.sleep(3)
                    self.config.exit_flag = True
                    break
                    
                while not self.config.is_shortcut:
                    self.i18n.print_lang("prompts.INPUT_select_agent")
                    agent_input = input("").lower()
                    
                    if agent_input in ("yardım", "help"):
                        os.system("cls")
                        self.i18n.print_lang("help.agent_select_message")
                        continue
                    elif agent_input in ("güncelle", "update"):
                        os.system("cls")
                        self.agent_service.load_agents(offline=False)
                        if self.config.exit_flag: break
                        self.i18n.print_lang("success.agent_list_updated")
                        self.i18n.update_language_file()
                        continue
                    elif agent_input in ("yb", "re"):
                        self.config.reboot_flag = True
                        self.logger.write("Kullanıcı yeniden başlatma istedi.")
                        self.i18n.print_lang("info.restarting")
                        time.sleep(0.5)
                        break
                    elif agent_input in ("ajanlar", "agents"):
                         print(", ".join(self.agent_service.agents.keys()))
                         continue
                    
                    selected_agent = ""
                    if agent_input in self.agent_service.agents:
                        selected_agent = agent_input
                    elif len(agent_input) >= 4:
                        for name in self.agent_service.agents:
                            if name.startswith(agent_input) and len(name) >len(agent_input): 
                                selected_agent = name
                                os.system("cls")
                                break
                    
                    if selected_agent:
                        self.config.agent = selected_agent
                        self.logger.write(f"Ajan seçildi: {selected_agent}")
                        os.system("cls")
                        break
                    elif agent_input in ("english", "türkçe"):
                         self.config.language = "english" if agent_input == "english" else "turkish"
                         os.system("cls")
                         self.i18n.print_lang("info.language_changed", language=self.config.language)
                         continue
                    else:
                        os.system("cls")
                        self.i18n.print_lang("prompts.invalid_agent")
                        continue
                
                if self.config.exit_flag: break
                if self.config.reboot_flag:
                    self.config.reboot_flag = False
                    os.system("cls")
                    continue
                
                self.logger.write(f"State task'ı başlatılıyor: {self.config.agent}")
                controller = GameController(self.config, self.logger, self.i18n, self.session, self.shortcut_mgr, self.agent_service)
                await controller.run_state()
                
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
        os.system("cls")
        self.write_animated_text("Instalocker For Valorant")
        try:
            asyncio.run(self.main_loop())
        except Exception as e:
            self.logger.write(f"Ana fonksyionda kritik hata: {e}", "critical")
            print(f"Critical error: {e}")
