import os, time, inspect
from .constants import Constants
from .config import Config

class Logger:
    def __init__(self, config: Config):
        self.config = config
        self.log_path = Constants.LOG_PATH

    def write(self, message: str, level: str = "debug"):
        try:
            if level.lower() == "debug" and not self.config.debug:
                return
            
            if os.path.exists(self.log_path) and (os.path.getsize(self.log_path) / 1024**2) > 20:
                with open(self.log_path, "w", encoding="utf-8") as f:
                    pass

            now = time.localtime()
            frame = inspect.currentframe().f_back
            caller_info = f"{frame.f_code.co_name}:{frame.f_lineno}" if frame else "unknown"

            log_entry = f"[{now.tm_mon}/{now.tm_mday}:{now.tm_hour}:{now.tm_min}:{now.tm_sec}] - [{caller_info}]:[{level.upper()}] : {message}\n"
            
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(log_entry)
                
        except Exception as e:
            print(f"Logger Error: {e}")
            if hasattr(self.config, 'exit_flag'):
                self.config.exit_flag = True
                time.sleep(4)

