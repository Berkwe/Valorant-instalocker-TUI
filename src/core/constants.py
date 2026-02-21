import os

class Constants:

    # ? main paths
    VALORANT_PATH = os.path.expandvars(r"%LocalAppData%\VALORANT")
    INSTALOCKER_PATH = os.path.join(VALORANT_PATH, "Instalocker")

    # ? control
    if not os.path.exists(INSTALOCKER_PATH):
        os.mkdir(INSTALOCKER_PATH)
    # ? Instalocker paths
    AGENT_LIST_PATH = os.path.join(INSTALOCKER_PATH, "agents.json")
    MAP_LIST_PATH = os.path.join(INSTALOCKER_PATH, "maps.json")
    LOG_PATH = os.path.join(INSTALOCKER_PATH, "Instalocker.log")
    SHOOTER_LOG_FILE_PATH = os.path.expandvars(r'%LocalAppData%\VALORANT\Saved\Logs\ShooterGame.log')
    LANGUAGE_FILE_PATH = os.path.join(INSTALOCKER_PATH, "language.json")
    PROFILE_SLOT_PATH = os.path.join(INSTALOCKER_PATH, "profile_shortcuts.json")

    # ? api urls
    VALORANT_AGENTS_API_URL = "https://valorant-api.com/v1/agents?isPlayableCharacter=true"
    VALORANT_MAPS_API_URL = "https://valorant-api.com/v1/maps"
    LANGUAGE_FILE_URL = "https://raw.githubusercontent.com/Berkwe/Valorant-instalocker/refs/heads/main/language.json"
    # ? default jsons
    PROFILE_FILE_DEFAULT_PROP_TR = {
        "ajan": "",
        "mod": ""
    }
    PROFILE_FILE_DEFAULT_PROP_EN = {
         "agent": "",
         "mode": ""
    }

    def clearOldFiles():
            """Eski sürümlerden kalan dosyaları temizler"""
            try:
                returnedBool = False
                oldLogPath = os.path.join(Constants.VALORANT_PATH, "Instalocker.log")
                oldAgentsPath = os.path.join(Constants.VALORANT_PATH, "agents.json")
                oldLanguagePath = os.path.join(Constants.VALORANT_PATH, "language.json")

                if os.path.exists(oldLogPath):
                    returnedBool = True
                    os.remove(oldLogPath)
                
                if os.path.exists(oldAgentsPath):
                    returnedBool = True
                    os.remove(oldAgentsPath)

                if os.path.exists(oldLanguagePath):
                    returnedBool = True
                    os.remove(oldLanguagePath)
                return returnedBool
            except Exception as e:
                print("eski dosyalar temizlenirken bir hata oluştu"+str(e))