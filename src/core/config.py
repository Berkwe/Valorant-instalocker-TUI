class Config:
    def __init__(self):
        self.debug = False
        self.region = None
        self.mode = 0  # ? 1: Kitleme 2: seçme 3: makro
        self.agent = None
        self.profile = {
            "ascent": "jett",
            "haven": "brimstone"

        }
        self.profilePath = "/home/berkwe/profile.json"
        
        self.reboot_flag = False
        self.exit_flag = False
        self.is_shortcut = False
        self.user_broke_game = False
        
        self.language = "english" 

    def set_args(self, args_dict):
        """verilen dicten argümanları pars eder"""
        if not args_dict:
            return
            
        self.debug = args_dict.get("debug", False)
        self.region = args_dict.get("region")
        self.agent = args_dict.get("agent")
        if args_dict.get("mode"):
            self.mode = int(args_dict.get("mode"))
        self.is_shortcut = True
