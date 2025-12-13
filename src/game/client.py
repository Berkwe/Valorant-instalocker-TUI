import os, asyncio
from valclient.client import Client as ValClient
from valclient.exceptions import HandshakeError
from src.core.logger import Logger
from src.core.i18n import LanguageManager
from src.core.config import Config

class GameSession:
    def __init__(self, config: Config, logger: Logger, i18n: LanguageManager):
        self.config = config
        self.logger = logger
        self.i18n = i18n
        self.client = None
        self.is_logged_in = False
        self.matches = []
        self.player_name = ""
        self.puuid = ""

    def start_client(self):
        """Valclienti başlatır"""
        self.logger.write(f"Client bölge '{self.config.region}' için başlatılıyor.")
        self.client = ValClient(region=self.config.region)
        try:
            self.client.activate()
            self.is_logged_in = True
            self.player_name = self.client.player_name
            self.puuid = self.client.puuid
            self.logger.write(f"Client başarıyla aktive edildi. Kullanıcı: {self.player_name}, PUUID: {self.puuid}", level="info")
            return True
        except HandshakeError:
            self.is_logged_in = False
            self.logger.write("Valorant açık değil veya Riot Client ile bağlantı kurulamadı (HandshakeError).", level="error")
            if self.config.debug:
                self.i18n.print_lang("debug.valorant_not_open_skipping")
                self.logger.write("Debug modu aktif, HandshakeErrora rağmen devam ediliyor.", level="warn")
                return True
            else:
                 return False

    ## ? basit yer tutucular
    def fetch_presence(self):
         return self.client.fetch_presence(self.client.puuid)

    def pregame_fetch_match(self):
        return self.client.pregame_fetch_match()
    
    def pregame_select_character(self, agent_id):
        return self.client.pregame_select_character(agent_id)

    def pregame_lock_character(self, agent_id):
        return self.client.pregame_lock_character(agent_id)
    
    def pregame_quit_match(self):
        return self.client.pregame_quit_match()
