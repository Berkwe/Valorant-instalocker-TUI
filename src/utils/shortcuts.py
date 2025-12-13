import os, sys, winreg, requests, asyncio, aioconsole, time
from io import BytesIO
from PIL import Image
from win32com.client import Dispatch

from src.core.constants import Constants
from src.core.logger import Logger
from src.core.i18n import LanguageManager
from src.core.config import Config
from src.services.api import AgentService

class ShortcutManager:
    def __init__(self, config: Config, logger: Logger, i18n: LanguageManager, agent_service: AgentService):
        self.config = config
        self.logger = logger
        self.i18n = i18n
        self.agent_service = agent_service
        self.parser = None

    def parse_arguments(self, parser):
        """Kısayol argümanlarını kontrol eder"""
        self.logger.write("controlShortcut fonksiyonu çağrıldı argüman kontrolü yapılıyor", "info")
        args = parser.parse_args()
        dict_args = vars(args)
        self.logger.write(f"Argümanlar parse edildi: {dict_args}")
        
        if len(dict_args.keys()) == 0:
            self.logger.write("Hiçbir argüman bulunamadı kısayol modunda değil", "info")
            return None
        else:
            has_values = any(value is not None for value in dict_args.values())
            if not has_values:
                self.logger.write("Argümanlar var ama hepsi None kısayol modunda değil", "info")
                return None
            
            self.logger.write(f"Kısayol modu tespit edildi. Parametreler: {dict_args}", "info")
            return dict_args

    def create_shortcut(self, array: dict):
        """Msaüstü kısayolu oluşturur"""
        try:
            self.logger.write("createShortCut fonksiyonu başlatıldı", "info")
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders") as reg_key:
                desktop_path, _ = winreg.QueryValueEx(reg_key, "Desktop")
            
            user_dir = os.path.expandvars(desktop_path)
            if not os.path.exists(user_dir):
                user_dir = os.path.expanduser("~")
            
            self.logger.write(f"Masaüstü konumu çekildi : {user_dir}")
            
            current_file = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(sys.argv[0])
            
            agent = array.get("agent")
            mode = array.get("mode")
            region = array.get("region")
            
            self.logger.write(f"Kısayol parametreleri alındı - Ajan: {agent}, Mod: {mode}, Bölge: {region}", "info")

            if self.config.language == "turkish":
                mode_text = "kilitle" if mode == 1 else "göster"
            else:
                mode_text = "lock" if mode == 1 else "select"
                
            shortcut_dir = os.path.join(user_dir, f"{agent}_{mode_text}.lnk")
            
            icon_folder = os.path.join(os.path.dirname(Constants.AGENT_LIST_PATH), "agentImages")
            icon_dir = os.path.join(icon_folder, f"{agent}.ico")
            
            shell = Dispatch("WScript.Shell")
            shortcut = shell.CreateShortcut(str(shortcut_dir))
            shortcut.TargetPath = str(current_file)
            
            debug_arg = f" --debug {self.config.debug}" if self.config.debug else ""
            shortcut.Arguments = f"--agent {agent} --mode {mode} --region {region}{debug_arg}"
            
            if not os.path.exists(icon_dir):
                self.logger.write(f"İkon dosyası bulunamadı, API'den indiriliyor: {icon_dir}", "info")
                agent_uuid = self.agent_service.agents.get(agent)
                if not agent_uuid:
                    self.logger.write(f"Ajan UUID bulunamadı: {agent}", "error")
                    shortcut.IconLocation = str(current_file)
                else:
                    url = f"https://valorant-api.com/v1/agents/{agent_uuid}"
                    response = requests.get(url)
                    
                    if response.status_code == 200:
                        data = response.json().get("data", {})
                        icon_url = data.get("displayIcon")
                        
                        img_resp = requests.get(icon_url)
                        img = Image.open(BytesIO(img_resp.content))
                        
                        if not os.path.exists(icon_folder):
                            os.makedirs(icon_folder)
                            
                        img.save(str(icon_dir))
                        shortcut.IconLocation = str(icon_dir)
                    else:
                         shortcut.IconLocation = str(current_file)
            else:
                shortcut.IconLocation = str(icon_dir)

            shortcut.save()
            self.logger.write(f"Kısayol başarıyla kaydedildi: {shortcut_dir}", "info")
            self.i18n.print_lang("success.shortcut_created", path=shortcut_dir)
            return 0
            
        except Exception as e:
            self.logger.write(f"Kısayol oluşturulurken hata: {str(e)}", "error")
            self.i18n.print_lang("errors.shortcut_creation_error")
            print(str(e))
            return 1

    async def ask_for_shortcut(self, agent_info: dict):
        """Asynchronously asks the user if they want to create a shortcut."""
        self.logger.write("questShortCut task'ı başlatıldı", level="info")
        try:
            while True:
                self.i18n.print_lang("prompts.INPUT_quest_shortcut")
                user_input = await aioconsole.ainput("")
                self.logger.write(f"Kullanıcı ShortCut için giriş yaptı: '{user_input}'")
                
                if user_input.lower() in ("e", "y"):
                    if self.create_shortcut(agent_info) == 0:
                        break
                elif user_input.lower() in ("h", "n"):
                    break
        except Exception as e:
            self.config.exit_flag = True
            self.logger.write("Kısayolda hata : "+ str(e), "error")
            self.i18n.print_lang("errors.shortcut_creation_error")
            print(str(e))
            time.sleep(4)
