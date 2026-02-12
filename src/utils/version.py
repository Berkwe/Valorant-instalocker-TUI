import requests
import re
from src.core.logger import Logger
from src.core.config import Config

class Version:
    def __init__(self):
        self.__version__ = "1.9.0--alpha-1.0"#?0$
        self.__author__ = "Berkwe_"
        self.REMOTE_VERSION_URL = "https://raw.githubusercontent.com/Berkwe/Valorant-instalocker/refs/heads/main/src/utils/version.py"
        self.config = Config()
        self.logger = Logger(self.config)
    

    def __getVersionFromAPI(self):
        returnedDict = {"ok": True, "response": 200, "isOld": False, "apiVersion": "1234", "currentVersion": self.__version__}
        response = requests.get(self.REMOTE_VERSION_URL)
        if response.status_code != 200:
            returnedDict["ok"] = False
            returnedDict["response"] = response.status_code
            return returnedDict
            
        pattern = r'__version__\s*=\s*"([^"]+)"\s*#\?0\$'
        match = re.search(pattern, response.text)

        if not match:
            returnedDict["ok"] = False
            returnedDict["exception"] = "Key Pattern Not Found"
            return returnedDict
            
        returnedDict["apiVersion"] = match.group(1)
        self.logger.write(f"Version Api dönüşü : {returnedDict}", "info")
        return returnedDict


    def __equalVersions(self, remote, local):
        priority_map = {
            'alpha': 1,
            'beta': 2
        }

        def parse(v):
            parts = []
            for part in re.split(r'[.-]+', v):
                if not part: continue
                
                if part.isdigit():
                    parts.append(int(part))
                else:
                    weight = priority_map.get(part.lower(), 0)
                    parts.append(weight)
            return parts
        
        return parse(remote) > parse(local)

    def versionControl(self):
        """githubdan yeni sürümü kontrol eder"""
        try:
            result = self.__getVersionFromAPI()
            
            if result and result.get("ok"):
                result["isOld"] = self.__equalVersions(result["apiVersion"], result["currentVersion"])
                result["currentVersion"] = self.__version__
            
            return result
            
        except Exception as e:
            self.logger.write(f"Version Kontrolünde hata : {e}", "error")
            return {"ok": False}
