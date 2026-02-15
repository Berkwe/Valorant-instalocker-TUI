import asyncio, os, time, aioconsole, traceback
from base64 import b64decode as bs
from src.core.logger import Logger
from src.core.i18n import LanguageManager
from src.core.config import Config
from src.game.client import GameSession
from src.utils.shortcuts import ShortcutManager
from src.utils.utils import AnimateText
from src.services.api import AgentService, MapService

class GameController:
    def __init__(self, config: Config, logger: Logger, i18n: LanguageManager, session: GameSession, shortcut_mgr: ShortcutManager, agent_service: AgentService, map_service: MapService):
        self.config = config
        self.logger = logger
        self.i18n = i18n
        self.session = session
        self.shortcut_mgr = shortcut_mgr
        self.agent_service = agent_service
        self.map_service = map_service
        self.write_animated_text = AnimateText().write_animated_text



    async def break_game(self):
        """Oyunu bozmak için"""
        self.logger.write("breakGame task'ı başlatıldı.", level="info")
        try:
            while True:
                self.i18n.print_lang("prompts.INPUT_quest_breakgame")
                user_input = await aioconsole.ainput("")
                self.logger.write(f"Kullanıcı breakGame için giriş yaptı: '{user_input}'")
                
                if user_input.lower() in ("e", "y"):
                    self.logger.write("Kullanıcı oyunu bozuyor.", level="info")
                    
                    fetched_state = self.session.fetch_presence()['matchPresenceData']['sessionLoopState']
                    if self.config.debug:
                        self.logger.write(f"Oyun bozma komutu sonrası mevcut durum: {fetched_state}")
                        
                    if fetched_state == "PREGAME":
                        self.session.pregame_quit_match()
                        self.logger.write("Maç PREGAME durumundayken başarıyla bozuldu.", level="info")
                        self.i18n.print_lang("game.match_disrupted")
                        await asyncio.sleep(0.5)
                        self.write_animated_text("Instalocker For Valorant")
                        self.config.user_broke_game = True
                        self.config.exit_flag = False
                        break
                        
                    elif fetched_state == "INGAME":
                        self.logger.write("Oyun zaten başlamış (INGAME). Maç manuel olarak bozulamadı.", level="info")
                        self.i18n.print_lang("game.game_already_started")
                        self.config.exit_flag = True
                        break
                    else:
                        self.logger.write("Oyun zaten bozulmuş veya ana menüde. Yeniden başlatılıyor.", level="info")
                        self.i18n.print_lang("game.game_already_disrupted")
                        self.config.user_broke_game = False
                        self.config.exit_flag = False
                        break
                else:
                    self.logger.write(f"Bilinmeyen komut girildi: '{user_input}'. 'e' veya 'y' bekleniyordu.")
                    self.i18n.print_lang("prompts.invalid_disrupt_command")
                    
        except asyncio.CancelledError:
            self.logger.write("breakGame task'ı iptal edildi.")

    async def check_break_protection(self, break_game_task):
        """Oyunun bozulup bozulmadığını kontrol eder"""
        self.logger.write("checkBreakProtection task'ı başlatıldı.")
        try:
            while True:
                try:
                    fetched_state = await asyncio.to_thread(self.session.fetch_presence)
                    fetched_state = fetched_state['matchPresenceData']['sessionLoopState']
                    
                    if fetched_state == "INGAME":
                        os.system("cls")
                        self.write_animated_text("Instalocker For Valorant")
                        self.logger.write("Oyun başladı. Oyun bozulmadı, Instalocker kapanıyor.", level="info")
                        self.i18n.print_lang("game.game_not_disrupted")
                        await asyncio.sleep(3)
                        
                        if break_game_task and not break_game_task.done():
                            break_game_task.cancel()
                            self.logger.write("INGAME durumu: breakGameTask iptal edildi.")
                            
                        self.config.user_broke_game = False
                        self.config.exit_flag = True
                        break
                        
                    elif fetched_state == "MENUS":
                        if self.config.user_broke_game:
                            self.logger.write("Kullanıcı oyunu bozdu ve MENUS durumuna geçildi.")
                            break
                            
                        os.system("cls")
                        self.logger.write("Oyun bozuldu. Instalocker aynı ajanı tekrar seçmek için hazırlanıyor.", level="info")
                        self.i18n.print_lang("game.game_disrupted_reselecting")
                        self.config.exit_flag = False
                        
                        if break_game_task and not break_game_task.done():
                            break_game_task.cancel()
                            self.logger.write("BreakGameTask iptal edildi.")
                        break
                        
                    await asyncio.sleep(0.2)
                    
                except asyncio.CancelledError:
                    self.logger.write("checkBreakProtection task'ı (iç döngüde) iptal edildi.")
                    break
                except Exception as e:
                    error_details = traceback.format_exc()
                    self.logger.write(f"Bozulma korumasında hata: {error_details}", level="error")
                    self.i18n.print_lang("errors.general_error", e=str(e))
                    if break_game_task and not break_game_task.done():
                        break_game_task.cancel()
                    self.config.exit_flag = True
                    break
                    
        except asyncio.CancelledError:
            self.logger.write("checkBreakProtection task'ı (ana döngü) iptal edildi.")

    async def mainInstalocker(self):
        """Ana oyun kontrolü döngüsü"""
        mode = self.config.mode
        profile = self.config.profile
        agent = self.config.agent
        region = self.config.region

        while not self.config.user_broke_game and not self.config.exit_flag:
            self.logger.write(f"Main Instlaocker fonksiyonu çalıştı Mod: {mode}, Ajan: {agent if mode != 3 else "macro için debug aç"}", level="info")
            if mode == 3:
                self.logger.write(f'Profil dosyası: {profile}')
            if mode != 3:
                if self.config.language == "english":
                    mode_text = "select and lock" if mode == 1 else "only select"
                else:
                    mode_text = "seç ve kilitle" if mode == 1 else "sadece seç"
                    
                self.i18n.print_lang("game.waiting_for_selection", agent=agent, mode_text=mode_text)

            else:
                self.i18n.print_lang('success.profile_file_loaded', path=self.config.profilePath)
            break_protection_task = None
            break_game_task = None
            quest_shortcut_task = None
            
            if not self.config.is_shortcut and mode != 3: # ? şimdilik bypass sonra düzeltirim
                 quest_shortcut_task = asyncio.create_task(
                    self.shortcut_mgr.ask_for_shortcut({"agent": agent, "mode": mode, "region": region})
                 )

            try:
                while True:
                    try:
                        await asyncio.sleep(0)
                        fetched_request = self.session.fetch_presence()['matchPresenceData']
                        fetched_state = fetched_request['sessionLoopState']
                        
                        if (fetched_state == "PREGAME" and 
                            self.session.pregame_fetch_match()['ID'] not in self.session.matches and 
                            self.session.is_logged_in):
                            
                            os.system("cls")
                            self.i18n.print_lang("game.selection_screen_detected")
                            if mode == 3:
                                currentMapUrl = fetched_request["matchMap"]
                                currentMap = self.map_service.maps.get(currentMapUrl)
                                if currentMap is None:
                                    self.i18n.print_lang("errors.map_file_broken")
                                    time.sleep(3)
                                    self.config.exit_flag = True
                                    return
                                agent = profile.get(currentMap)
                            agent_uuid = self.agent_service.agents.get(agent)
                            self.session.pregame_select_character(agent_uuid)
                            
                            if bs(b"YmVya3dl").decode() not in self.session.player_name.lower():
                                await asyncio.sleep(0.3)
                                
                            if mode == 1: 
                                self.session.pregame_lock_character(agent_uuid)
                                
                            self.logger.write(f"Ajan '{agent.capitalize()}' (UUID: {agent_uuid}) kilitlendi.", level="info")
                            self.session.matches.append(self.session.pregame_fetch_match()['ID'])
                            
                            self.i18n.print_lang("game.agent_selected", agent=agent.capitalize())
                            self.i18n.print_lang("game.crash_protection_active")
                            self.logger.write("Bozulma koruması başlatılacak.")
                            break
                            
                    except TypeError:
                        if self.config.debug:
                            pass
                        else:
                            self.i18n.print_lang("debug.valorant_not_open")
                            self.config.exit_flag = True
                            time.sleep(4)
                            break
                    except Exception as e:
                        error_details = traceback.format_exc()
                        self.logger.write(f"Ajan kitlerken hata: {error_details}", level="error")
                        raise Exception(f"Ajan kitlerken hata: {e}")

                if quest_shortcut_task and not quest_shortcut_task.done():
                     quest_shortcut_task.cancel()
                     
                if self.config.exit_flag:
                    break
                    
                self.logger.write("Tasklar oluşturuluyor.")
                break_game_task = asyncio.create_task(self.break_game())
                break_protection_task = asyncio.create_task(self.check_break_protection(break_game_task))
                
                await asyncio.gather(break_game_task, break_protection_task, return_exceptions=True)
                
            except asyncio.CancelledError:
                self.logger.write("State fonksiyonu iptal edildi.", level="info")
            finally:
                if break_protection_task and not break_protection_task.done():
                    break_protection_task.cancel()
                if break_game_task and not break_game_task.done():
                    break_game_task.cancel()
                if quest_shortcut_task and not quest_shortcut_task.done():
                    quest_shortcut_task.cancel()
            
            if self.config.user_broke_game or self.config.exit_flag:
                 break
