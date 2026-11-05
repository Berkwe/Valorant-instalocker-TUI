import base64, json, requests
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
        # ? valclient her istekte yeni bağlantı açıyor, bu oturum bağlantıyı açık tutar
        self.http = requests.Session()

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
        port = self.client.lockfile['port']
        response = self.http.get(f"https://127.0.0.1:{port}/chat/v4/presences",
                                 headers=self.client.local_headers, verify=False, timeout=5)
        try:
            for presence in response.json()['presences']:
                if presence['puuid'] == self.client.puuid:
                    return json.loads(base64.b64decode(presence['private']))
        except (KeyError, TypeError, ValueError):
            return None

    def _glz_request(self, method, path):
        """Riot pregame sunucusuna açık bağlantı üzerinden istek atar, token bittiyse yeniler"""
        url = f"{self.client.base_url_glz}{path}"
        response = self.http.request(method, url, headers=self.client.headers, json={}, timeout=5)
        if response.status_code in (400, 401):
            self.logger.write(f"{path} için {response.status_code} alındı, token yenileniyor.", "warn")
            self.client.activate()
            response = self.http.request(method, url, headers=self.client.headers, json={}, timeout=5)
        return response

    def warm_connection(self):
        """Ajan seçimi başlamadan bağlantıyı ve tokeni hazır tutar"""
        try:
            self._glz_request("GET", f"/pregame/v1/players/{self.client.puuid}")
        except Exception as e:
            self.logger.write(f"Bağlantı ısıtılamadı: {e}", "warn")

    def pregame_fetch_match_id(self):
        """Maç idsini döner, pregame'de değilse None"""
        response = self._glz_request("GET", f"/pregame/v1/players/{self.client.puuid}")
        if response.status_code != 200:
            return None
        return response.json().get("MatchID")

    def pregame_pick_agent(self, agent_id, match_id, lock):
        """Ajanı seçer veya kitler, HTTP durum kodunu döner"""
        action = "lock" if lock else "select"
        return self._glz_request("POST", f"/pregame/v1/matches/{match_id}/{action}/{agent_id}").status_code

    def pregame_quit_match(self):
        return self.client.pregame_quit_match()
