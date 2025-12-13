import os

class Constants:
    VALORANT_PATH = os.path.expandvars(r'%LocalAppData%\VALORANT')
    AGENT_LIST_PATH = os.path.join(VALORANT_PATH, "agents.json")
    LOG_PATH = os.path.join(VALORANT_PATH, "Instalocker.log")
    SHOOTER_LOG_FILE_PATH = os.path.expandvars(r'%LocalAppData%\VALORANT\Saved\Logs\ShooterGame.log')
    LANGUAGE_FILE_PATH = os.path.join(VALORANT_PATH, "language.json")
    
    VALORANT_API_URL = "https://valorant-api.com/v1/agents?isPlayableCharacter=true"
    LANGUAGE_FILE_URL = "https://raw.githubusercontent.com/Berkwe/Valorant-instalocker/refs/heads/main/language.json"
