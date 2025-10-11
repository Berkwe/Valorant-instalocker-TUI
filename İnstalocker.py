import time, os, requests, json, asyncio, aioconsole, inspect, argparse, sys, winreg
from io import BytesIO
from PIL import Image
from urllib3.exceptions import MaxRetryError, NameResolutionError
from requests.exceptions import ConnectionError
from base64 import b64decode as bs
from valclient import *
from valclient.resources import regions
from valclient.exceptions import *
from win32com.client import Dispatch

# Coded by berkwe_


os.system("color a")
os.system("cls")


valorantPath = os.path.expandvars(r'%LocalAppData%\VALORANT')
agentListPath = os.path.join(valorantPath, "agents.json")
logPath = os.path.join(valorantPath, "Instalocker.log")
shooterLogFilePath = os.path.expandvars(r'%LocalAppData%\VALORANT\Saved\Logs\ShooterGame.log')
languageFilePath = os.path.join(valorantPath, "language.json")

valorantAPI = "https://valorant-api.com/v1/agents?isPlayableCharacter=true"
languageFileURL = "https://raw.githubusercontent.com/Berkwe/Valorant-instalocker/refs/heads/main/language.json"

parser = argparse.ArgumentParser()
parser.add_argument("--agent", help="ajan ismi")
parser.add_argument("--mode", help="seçim modu lock/select")
parser.add_argument("--region", help="region idsi (eu,na vb)")
parser.add_argument("--debug", help="hata ayıklama için true/false", type=bool)



languageFile = {}
debug = False
rebootFlag = False
isClientLoggedIn = False
matches = []
agents = {}
language = "english"
exitFlag = False
userBreakedGame = False
isShortcut = False


def updateLanguageFile(): # ? dil dosyasını internet ile günceller
    global languageFile
    try:
        writeLog("updateLanguageFile fonksiyonu çağrıldı.", "info")
        response = requests.get(languageFileURL, timeout=17)
        data = dict(response.json() or {})

        if response.status_code != 200:
            writeLog(f"Language file çekilemedi. Status code: {response.status_code}", "error")
            print("The language file could not be downloaded. Please check your internet connection.")
            returnedArray = {"response": False, "data": data}
            return returnedArray

        writeLog("Language file başarıyla çekildi.", "info")

        with open(languageFilePath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        writeLog(f"Language file {languageFilePath} içine yazıldı.", "info")

        returnedArray = {"response": True, "data": data}
        return returnedArray

    except requests.exceptions.RequestException as req_err:
        writeLog(f"Request hatası oluştu : {req_err}", "error")
        print(f"A request error occurred : {req_err}")
        return {"response": False, "data": {}}

    except Exception as e:
        writeLog(f"updateLanguageFile sırasında beklenmeyen hata: {e}", "error")
        print(f"An error occurred during updateLanguageFile : {e}")
        return {"response": False, "data": {}}


def getUserLang(autoMode : bool = True): # ? kullanıcının dilini belirler
    global language
    global exitFlag
    try:
        if autoMode:
            if not os.path.exists(shooterLogFilePath):
                writeLog("Otomatik dil belirlenemedi, kullanıcıya dil sorulacak.", "warning")
                resp = getUserLang(autoMode=False)
                return resp

            with open(shooterLogFilePath, "r", encoding="utf-8") as f:
                data = f.read().lower()

            if "tr-tr" in data:
                language = "turkish"
                writeLog("Otomatik dil tespit edildi: Türkçe", "info")
            else:
                language = "english"
                writeLog("Otomatik dil tespit edildi: İngilizce", "info")

            return

        else:
            for _ in range(5):
                print("Automatic language detection failed, Please select your language.")
                languageInput = input("Select Language (ingilizce/english/EN, türkçe/turkish/TR) : ").lower()

                if languageInput in ("help", "yardım"):
                    writeLog("Kullanıcı yardım istedi.", "info")
                    print("neyin yardımını istiyon amk")
                    continue

                elif languageInput in ("ingilizce", "english", "en"):
                    language = "english"
                    writeLog("Kullanıcı İngilizce dilini seçti.", "info")
                    break

                elif languageInput in ("türkçe", "turkish", "tr"):
                    language = "turkish"
                    writeLog("Kullanıcı Türkçe dilini seçti.", "info")
                    break

                else:
                    writeLog(f"Yanlış dil girildi: {languageInput}", "warning")
                    print("You wrote the language incorrectly, only English/EN, Turkish/TR")

            else:
                writeLog("Kullanıcı 5 kez yanlış dil girdi, Instalocker kapanıyor.", "error")
                print("Incorrect entry attempted 5 times, Instalocker is shutting down...")
                exitFlag = True
                return

            writeLog(f"Dil ayarlandı: {language}", "info")
            return

    except Exception as e:
        writeLog(f"Hata oluştu getUserLang()  : {e}", "error")
        print(f"An error occurred : {e}")
        exitFlag = True
        return


def getLanguageFile():  # ? dil dosyasını localden çeker
    global languageFile, exitFlag
    if not hasattr(getLanguageFile, "decodeErrorCount"):
        getLanguageFile.decodeErrorCount = 0

    try:
        writeLog("getLanguageFile() çağrıldı.", "info")

        if not os.path.exists(languageFilePath):
            print("Language file not found, downloading remotely...")
            writeLog("Dil dosyası mevcut değil, updateLanguageFile() çağrılıyor.", "warning")

            response = updateLanguageFile()
            writeLog(f"updateLanguageFile() dönüşü: {response}", "debug")

            if not response.get("response"):
                print(f"Language file could not be retrieved. HTTP code : {response.get('data').status_code}")
                writeLog(f"Dil dosyası alınamadı, response: {response}", "error")
                time.sleep(4)
                return

        with open(languageFilePath, "r", encoding="utf-8") as f:
            readedText = f.read()
            languageFile = json.loads(readedText)
            writeLog("Dil dosyası başarıyla yüklendi.", "info")

        getLanguageFile.decodeErrorCount = 0

    except json.JSONDecodeError as e:
        getLanguageFile.decodeErrorCount += 1
        writeLog(f"JSONDecodeError yakalandı, deneme sayısı: {getLanguageFile.decodeErrorCount}", "warning")

        if getLanguageFile.decodeErrorCount == 1:
            os.remove(languageFilePath)
            writeLog("Bozuk dil dosyası silindi, yeniden indiriliyor...", "warning")
            getLanguageFile()
        else:
            writeLog("JSONDecodeError iki kez tekrarlandı, program sonlandırılıyor.", "critical")
            print("The language file was found to be incorrect twice, the program is terminating.")
            time.sleep(4)
            exitFlag = True
            return

    except Exception as e:
        print(f"An error occurred while reading the language file : {e}")
        writeLog(f"Dil dosyası okunurken hata: {e}", "error")
    


def printLang(key_path: str, **kwargs):
    global exitFlag
    try:
        inline = False
        if not languageFile:
            getLanguageFile()
        
        lang_data = languageFile.get(language, languageFile.get("english", {}))
        if "INPUT" in key_path:
            inline = True
        keys = key_path.split('.')
        text = lang_data
        
        for key in keys:
            text = text.get(key)
            if text is None:
                writeLog(f"printLang: '{key_path}' bulunamadı!", "error")
                print(f"There's a problem with printing, probably because the language file is outdated and is being updated. Key : {key_path}")
                response = updateLanguageFile()
                if response.get("response"):
                    getLanguageFile()
                    print("The language file successfully updated.")
                else:
                    print("The language file could not be retrieved. Please forward the log file to the developer. The program is closing...")
                    writeLog(f"Dil dosyası eskiyken çekilemedi response : {response}")
                    exitFlag = True
                return
        
        if kwargs:
            try:
                text = text.format(**kwargs)
            except KeyError as e:
                writeLog(f"printLang format hatası: {e} - key: {key_path}", "error")
                print(f"missing varible {e} - {text}")
                return
        if inline:
            print(text, end="")
        else:
            print(text)
        writeLog(f"printLang: {key_path} -> {text}", "info")
        
    except Exception as e:
        writeLog(f"printLang genel hatası: {e}", "error")
        print(f"error : {e}")


def controlShortcut(): # ? Kısayol kontrolü
    writeLog("controlShortcut fonksiyonu çağrıldı argüman kontrolü yapılıyor", "info")
    args = parser.parse_args()
    dict_args = vars(args)
    writeLog(f"Argümanlar parse edildi: {dict_args}")
    if len(dict_args.keys()) == 0:
        writeLog("Hiçbir argüman bulunamadı kısayol modunda değil", "info")
        return None
    else:
        has_values = any(value is not None for value in dict_args.values())
        if not has_values:
            writeLog("Argümanlar var ama hepsi None kısayol modunda değil", "info")
            return None
        writeLog(f"Kısayol modu tespit edildi. Parametreler: Agent={dict_args.get('agent')}, Mode={dict_args.get('mode')}, Region={dict_args.get('region')}, Debug={dict_args.get('debug')}", "info")
        return dict_args


def writeLog(message: str, level = "debug"): # ? Logları tutar
    global exitFlag
    try:
        if level.lower() == "debug" and not debug:
            return
        if level.lower() == "info":
            level == "ınfo"
        if (os.path.getsize(logPath)/1024**2) > 20:
            f = open(logPath, "w", encoding="utf-8")
            f.close()
        now = time.localtime()
        frame = inspect.currentframe().f_back
        with open(logPath, "a", encoding="utf-8") as f:
            f.write(f"[{now.tm_mon}/{now.tm_mday}:{now.tm_hour}:{now.tm_min}:{now.tm_sec}] - [{frame.f_code.co_name}:{frame.f_lineno}]:[{level.upper()}] : {message}\n")
    except FileNotFoundError:
        with open(logPath, "w", encoding="utf-8") as f:
            writeLog(message, level)
    except Exception as f:
        exitFlag = True
        printLang("errors.log_write_error")
        print(str(f))
        time.sleep(4)


def createShortCut(array: dict): # ? Kısayol oluşturur
    global exitFlag
    try:
        writeLog("createShortCut fonksiyonu başlatıldı", "info")
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders") as reg_key:
            desktop_path, _ = winreg.QueryValueEx(reg_key, "Desktop")
        
        userDir = os.path.expandvars(desktop_path)
        if not os.path.exists(userDir):
            userDir = os.path.expanduser("~")
        writeLog(f"Masaüstü konumu çekildi : {userDir}")
        current_file = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
        agent = array.get("agent")
        mode = array.get("mode")
        region = array.get("region")
        writeLog(f"Kısayol parametreleri alındı - Ajan: {agent}, Mod: {mode}, Bölge: {region}")
        mode_text = "göster" if mode == 2 else "kilitle"
        shortcutDir = os.path.join(userDir, f"{agent}_{mode_text}.lnk")
        writeLog(f"Kısayol hedef yolu belirlendi: {shortcutDir}")
        iconFolder = os.path.join(os.path.dirname(agentListPath), "agentImages")
        iconDir = os.path.join(iconFolder, f"{agent}.ico")
        writeLog(f"İkon klasörü: {iconFolder}, İkon dosyası: {iconDir}")
        writeLog(f"Hedef exe dosyası: {current_file}")
        shell = Dispatch("WScript.Shell")
        writeLog("WScript.Shell COM nesnesi oluşturuldu")
        shortcut = shell.CreateShortcut(str(shortcutDir))
        writeLog("Kısayol nesnesi oluşturuldu")
        shortcut.TargetPath = str(current_file)
        shortcut.Arguments = f"--agent {agent} --mode {mode} --region {region}"+(f" --debug {debug}" if debug else "")
        writeLog(f"Kısayol argümanları ayarlandı: {shortcut.Arguments}")
        if not os.path.exists(iconDir):
            writeLog(f"İkon dosyası bulunamadı, API'den indiriliyor: {iconDir}")
            url = (valorantAPI+agents.get(agent))
            writeLog(f"API isteği gönderiliyor: {url}")
            response = requests.get(url)
            writeLog(f"API yanıtı alındı. Status code: {response.status_code}")
            if response.status_code == 200:
                agentInfoDict = dict(response.json())
                agentInfo = agentInfoDict.get("data")
                agentImage = agentInfo.get("displayIcon")
                writeLog(f"Ajan görseli URL'si alındı: {agentImage}")
                agentImageResponse = requests.get(agentImage)
                writeLog(f"Ajan görseli indirildi. Boyut: {len(agentImageResponse.content)} bytes")
                img = Image.open(BytesIO(agentImageResponse.content))
                writeLog(f"Görsel PIL ile açıldı. Format: {img.format}, Boyut: {img.size}")
                if not os.path.exists(iconFolder):
                    os.makedirs(iconFolder)
                    writeLog(f"İkon klasörü oluşturuldu: {iconFolder}")
                img.save(str(iconDir))
                writeLog(f"İkon dosyası kaydedildi: {iconDir}")
                shortcut.IconLocation = str(iconDir)
                writeLog("Kısayol ikonu özel ikon olarak ayarlandı")
            else:
                writeLog(f"API isteği başarısız, varsayılan ikon kullanılacak. Status: {response.status_code}", "warn")
                shortcut.IconLocation = str(current_file)
                writeLog("Kısayol ikonu exe dosyası olarak ayarlandı")
        else:
            writeLog(f"İkon dosyası zaten mevcut: {iconDir}")
            shortcut.IconLocation = str(iconDir)
            writeLog("Mevcut ikon dosyası kısayola atandı")
        shortcut.save()
        writeLog(f"Kısayol başarıyla kaydedildi: {shortcutDir}", "info")
        printLang("success.shortcut_created", path=shortcutDir)
        return 0
    except Exception as e:
        writeLog(f"Kısayol oluşturulurken hata: {str(e)}", "error")
        writeLog(f"Hata detayları - Ajan: {array.get('agent')}, Mod: {array.get('mode')}, Bölge: {array.get('region')}", "error")
        printLang("errors.shortcut_creation_error")
        print(str(e))
        return 1


async def questShortCut(agentInfo: dict): # ? Kısayol oluşturmak için kullanıcıya sorar
    global exitFlag
    writeLog("questShortCut task'ı başlatıldı", level="info")
    try:
        while True:
            userInput = await aioconsole.ainput("Bu ajan için masaüstüne kısayol oluşturmak ister misiniz? E/H : ")
            writeLog(f"Kullanıcı ShortCut için giriş yaptı: '{userInput}'")
            if userInput.lower() == "e" or userInput.lower() == "y":
                returnedVal = createShortCut(agentInfo)
                if returnedVal == 0:
                    break
            elif userInput.lower() == "h" or userInput.lower() == "n":
                break
    except Exception as e:
        exitFlag = True
        writeLog("Kısayolda hata : "+ str(e), "error")
        printLang("errors.shortcut_creation_error")
        print(str(e))
        time.sleep(4)



def getAgentList(offline=True): # ? Ajan listesini çeken ana görev
    global agents, exitFlag
    writeLog(f"Ajan listesi alma işlemi başlatıldı. Offline mod: {offline}")
    try:
        if offline:
            if not os.path.exists(agentListPath):
                writeLog("Local ajan dosyası bulunamadı, APIden güncelleniyor.", level="info")
                printLang("info.agent_file_not_found")
                agentList = update()
                if agentList.get("returned", True):
                    with open(agentListPath, "w", encoding="utf-8") as f:
                        json.dump(agentList, f, ensure_ascii=False, indent=4)
                    agents = agentList
                    writeLog("Offline modda ajanlar dosyadan çekildi (API'den güncellendi).", level="info")
                    printLang("success.agents_loaded")
                    return
                else:
                    writeLog("Offline modda Ajan listesi çekilirken hata oluştu. : HTTP Hata kodu : "+str(agentList.get("status", "hata kodu alınamadı")), level="error")
                    printLang("errors.valorant_folder_not_found", path=agentListPath)
                    print(f"HTTP Hata kodu : {agentList.get('status', 'hata kodu alınamadı')}")
                    time.sleep(3)
                    exitFlag = True
                    return
            else:
                with open(agentListPath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if "jett" not in data.keys() or "kayo" not in data.keys(): 
                        writeLog("Varsayılan ajan listesi bozuk. Güncelleniyor. Ajan Listesi : "+str(data), level="error")
                        printLang("info.agent_list_corrupted")
                        getAgentList(offline=False)
                        return
                    agents = data
                    writeLog("Ajanlar offline olarak lokal agents.json dosyasından başarıyla çekildi.", level="info")
                    return
        writeLog("Online modda ajan listesi güncelleniyor.", level="info")
        agentList = update()
        printLang("info.agent_list_updating")
        if not os.path.exists(agentListPath):
            if agentList.get("returned", True):
                with open(agentListPath, "w", encoding="utf-8") as f:
                    json.dump(obj=agentList, fp=f, ensure_ascii=False, indent=4)
                agents = agentList
                writeLog("Online modda Ajan listesi güncellendi.", level="info")
                printLang("success.agent_list_updated")
            else:
                writeLog("Online modda Ajan listesi çekilirken hata oluştu (agents.json yoktu). : HTTP Hata kodu : "+str(agentList.get("status", "hata kodu alınamadı")), level="error")
                printLang("errors.valorant_folder_not_found", path=agentListPath)
                print(f"HTTP hata kodu : {agentList.get('status', 'hata kodu alınamadı')}")
                time.sleep(3)
                exitFlag = True
                return
        else:
            if agentList.get("returned", True):
                with open(agentListPath, "w", encoding="utf-8") as f:
                    json.dump(obj=agentList, fp=f, ensure_ascii=False, indent=4)
                agents = agentList
                writeLog("Online Modda Ajan listesi güncellendi.", level="info")
                printLang("success.agent_list_updated_short")
            else:
                writeLog("Güncel ajan listesi çekilemedi, varsayılan liste çekilmeye çalışılıyor. Hata: "+str(agentList.get("status", "hata kodu alınamadı")), "error")
                print(f"Güncel ajan listesi çekilemedi, varsayılan liste çekilmeye çalışılıyor.... HTTP Hata kodu : {agentList.get('status', 'hata kodu alınamadı')}")
                with open(agentListPath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if "jett" not in data.keys() or "kayo" not in data.keys():
                    writeLog("Varsayılan ajan listesi de bozuk.", "error")
                    print(f"Ajan listesi bozulmuş, onarmak için manuel olarak indirin veya hatanın geçmesini bekleyin. varsayılan ajan listesi yolu : {agentListPath}")
                    time.sleep(3)
                    exitFlag = True
                    return
                writeLog("Varsayılan ajan listesi başarıyla yüklendi, güncelleme başarısız oldu.", level="info")
                printLang("success.agent_list_default_updated")
                agents = data
    except FileNotFoundError:
        writeLog(f"'{os.path.dirname(agentListPath)}' veya 'agents.json' bulunamadı. Valorant indirilmemiş veya AppData kısmı erişilebilir değil.", level="error")
        printLang("errors.valorant_folder_not_found", path=os.path.dirname(agentListPath))
        time.sleep(3)
        exitFlag = True
        return
    except Exception as e:
        writeLog(f"Ajan listesi çekilirken bir hata oluştu: {str(e)}", level="error")
        printLang("errors.general_error", e=str(e))
        exitFlag = True
        return


def update(): # ? Api'den ajan listesini çeker
    writeLog("Valorant API'sinden ajan listesi çekilmeye başlanıyor.")
    try:
        agentsTemp = {}
        data = requests.get(valorantAPI, verify=False, timeout=4) 
        dataDict = dict(data.json())
        if data.status_code == 200 and dataDict.get("status") == 200:
            for agent in dataDict.get("data"):
                displayName = agent.get("displayName").lower()
                uuid = agent.get("uuid")
                if displayName == "kay/o":
                    displayName = "kayo"
                agentsTemp[displayName] = uuid
                writeLog(f"API'den ajan eklendi: {displayName} - {uuid}")
            writeLog(f"API'den {len(agentsTemp)} ajan başarıyla çekildi.", level="info")
            return agentsTemp
        else:
            writeLog(f"Valorant API hatası, HTTP Status: {data.status_code}, API Status: {dataDict.get('status')}", level="error")
            return {"status": data.status_code if data.status_code != 200 else dataDict.get("status"), "returned": False}
    except ConnectionError as e_conn:
        writeLog(f"Bağlantı hatası oluştu: {str(e_conn)}", level="error")
        return {"status": 0, "returned": False}
    except requests.exceptions.Timeout as e_timeout:
        writeLog(f"Zaman aşımı hatası oluştu: {str(e_timeout)}", level="error")
        return {"status": "Timeout", "returned": False}
    except requests.exceptions.RequestException as e_req:
        writeLog(f"API isteği sırasında hata oluştu: {str(e_req)}", level="error")
        return {"status": "RequestException", "returned": False}
    except Exception as e_gen:
        writeLog(f"Ajan listesi güncellenirken bilinmeyen bir hata oluştu: {str(e_gen)}", level="error")
        return {"status": "UnknownErrorInUpdate", "returned": False}


def writeAnmiatedText(header, footer=""): # ? Ekrana fırlayan yazılar için
    writeLog(f"yaz fonksiyonu çağrıldı. header1: '{header}', footer: '{footer}'")
    randoms = "01"
    for i in range(len(header)):
        for k in randoms:
            print((header[:i] + k).center(150).removesuffix(" "))
            os.system("cls")
    print(header.center(150)+"\n")
    time.sleep(0.3)
    print(footer.center(150))
    writeLog(f"yaz fonksiyonu tamamlandı. Ekrana '{header}' ve '{footer}' yazdırıldı.", level="info")


def findRegion(autoMod = True): # ? Kullanıcının sunucusunu algılar
    global exitFlag
    writeLog(f"Bölge arama işlemi başlatıldı. mod: {autoMod}")
    try:
        if autoMod:
            
            writeLog(f"ShooterGame.log okunuyor: {shooterLogFilePath}")
            with open(shooterLogFilePath, "r", encoding="utf-8") as f:
                regionLine = None
                for line in f.readlines():
                    if "https://glz-" in line:
                        regionLine = line
                        writeLog(f"Bölge içeren satır bulundu: {regionLine.strip()}")
                        break
                region = regionLine.split("https://glz-")[1].split("-")[0].lower()
                writeLog(f"Bölge kodu: {region}")
                if region in regions:
                    writeLog(f"Bölge otomatik olarak bulundu: {region}", level="info")
                    return region
                else:
                    writeLog(f"Otomatik olarak bulunan bölge '{region}' geçerli değil. Manuel giriş isteniyor.", level="warn")
                    pass
        writeLog("Manuel bölge girişi bekleniyor.")
        while True:
            printLang("prompts.INPUT_select_server")
            regionInput = input("").lower()
            writeLog(f"Kullanıcı bölge girdi: {regionInput}")
            if regionInput == "yardım" or regionInput == "help":
                os.system("cls")
                print(", ".join(regions))
                writeLog("Kullanıcı bölge kodları için yardım istedi.")
                continue
            elif regionInput not in regions:
                os.system("cls")
                printLang("prompts.invalid_server")
                writeLog(f"Kullanıcı geçersiz bölge girdi: {regionInput}", level="info")
                continue
            else:
                os.system("cls")
                writeLog(f"Kullanıcı geçerli bölge seçti: {regionInput}", level="info")
                return regionInput
    except FileNotFoundError:
        writeLog("ShooterGame.log dosyası bulunamadı. Manuel sunucu belirleme moduna geçiliyor.", level="error")
        printLang("info.log_file_not_found")
        return findRegion(False)
    except Exception as f:
        if not autoMod:
            writeLog(f"Bölge bulunurken bir hata oluştu, manuel sunucu da belirlenemedi: {str(f)}", level="error")
            exitFlag = True
            printLang("errors.general_error", e=str(f))
        else:
            writeLog(f"Bölge bulunurken bir hata oluştu: {str(f)}. Manuel sunucu belirlemeye geçiliyor.", level="error")
            printLang("errors.general_error", e=str(f))
            return findRegion(False)


async def state(mode: int = 1, agent: str = "jett", region: str = "eu"): # ? Seçim ekranı durum kontrolü için
    while not userBreakedGame and not exitFlag:
        writeLog(f"State fonksiyonu çalıştı. Mod: {'Seç ve Kilitle' if mode == 1 else 'Sadece Seç'}, Ajan: {agent.capitalize()}", level="info") 
        if language == "english": # ? dil dosyasına eklemeye fenasal üşendim
            mode_text = "select and lock" if mode == 1 else "only select"
        else:
            mode_text = "seç ve kilitle" if mode == 1 else "sadece seç"
        printLang("game.waiting_for_selection", agent=agent, mode_text=mode_text)
        breakProtectionTask = None
        breakGameTask = None
        questShortCutTask = None
        if not isShortcut:
            questShortCutTask = asyncio.create_task(questShortCut({"agent": agent, "mode": mode, "region": region}))
        try:
            while True:
                try:
                    fetchedState = client.fetch_presence(client.puuid)['matchPresenceData']['sessionLoopState']
                    await asyncio.sleep(0)
                    if (fetchedState == "PREGAME" and client.pregame_fetch_match()['ID'] not in matches and isClientLoggedIn):
                        os.system("cls")
                        printLang("game.selection_screen_detected")
                        client.pregame_select_character(agents.get(agent))
                        if bs("YmVya3dl").decode() not in client.player_name.lower():
                            await asyncio.sleep(0.3)
                        if mode == 1:
                            client.pregame_lock_character(agents.get(agent))
                        writeLog(f"Ajan '{agent.capitalize()}' (UUID: {agents.get(agent)}) kilitlendi.", level="info")
                        matches.append(client.pregame_fetch_match()['ID'])
                        printLang("game.agent_selected", agent=agent.capitalize())
                        printLang("game.crash_protection_active")
                        writeLog("Bozulma koruması (breakGame ve checkBreakProtection task'ları) başlatılacak.")
                        break
                except KeyError:
                    if debug:
                        pass
                except TypeError:
                    writeLog("State döngüsünde TypeError.")
                    pass
                except Exception as e:
                    writeLog(f"Ajan kitlerken bir hata oluştu (iç döngü): {str(e)}", level="error")
                    raise Exception(f"Ajan kitlerken bir hata oluştu geliştiriciye iletin : {e}")        
            if questShortCutTask and not questShortCutTask.done():
                writeLog("questShortCut task'ı sonlandırılıyor", "info")
                questShortCutTask.cancel()
            if exitFlag: 
                break
            writeLog("breakGame ve checkBreakProtection taskları oluşturuluyor.")
            breakGameTask = asyncio.create_task(breakGame())
            breakProtectionTask = asyncio.create_task(checkBreakProtection(breakGameTask))
            await asyncio.gather(breakGameTask, breakProtectionTask, return_exceptions=True)
            writeLog("breakGame ve checkBreakProtection task'ları tamamlandı veya iptal edildi.")
        except asyncio.CancelledError:
            writeLog("State fonksiyonu iptal edildi.", level="info")
            pass
        finally:
            writeLog("State fonksiyonu finally bloğuna girildi.")
            if breakProtectionTask and not breakProtectionTask.done():
                breakProtectionTask.cancel()
                writeLog("breakProtectionTask iptal ediliyor.")
            if breakGameTask and not breakGameTask.done():
                breakGameTask.cancel()
                writeLog("breakGameTask iptal ediliyor.")
            if questShortCutTask and not questShortCutTask.done():
                questShortCutTask.cancel()
                writeLog("questShortCutTask iptal ediliyor (finally).")
        if userBreakedGame or exitFlag :
            writeLog(f"State fonksiyonu sonlanıyor. userBreakedGame: {userBreakedGame}, exitFlag: {exitFlag}", level="info")
            break
        


async def breakGame(): # ? Oyunu bozar
    global exitFlag, userBreakedGame
    writeLog("breakGame task'ı başlatıldı.", level="info")
    try:
        while True:
            userInput = await aioconsole.ainput("Oyunu bozmak için e/y yazın: ")
            writeLog(f"Kullanıcı breakGame için giriş yaptı: '{userInput}'")
            if userInput.lower() == "e" or userInput.lower() == "y":
                writeLog("Kullanıcı oyunu bozuyor.", level="info")
                fetchedState = client.fetch_presence(client.puuid)['matchPresenceData']['sessionLoopState']
                if debug:
                    writeLog(f"Oyun bozma komutu sonrası mevcut durum: {fetchedState}") 
                if fetchedState == "PREGAME":
                    client.pregame_quit_match()
                    writeLog("Maç PREGAME durumundayken başarıyla bozuldu.", level="info")
                    printLang("game.match_disrupted")
                    await asyncio.sleep(0.5)
                    writeAnmiatedText("Instalocker For Valorant", "By Berkwe_")
                    userBreakedGame = True
                    exitFlag = False
                    break
                elif fetchedState == "INGAME":
                    writeLog("Oyun zaten başlamış (INGAME). Maç manuel olarak bozulamadı.", level="info")
                    printLang("game.game_already_started")
                    exitFlag = True
                    break
                else:
                    writeLog("Oyun zaten bozulmuş veya ana menüde. Yeniden başlatılıyor.", level="info")
                    printLang("game.game_already_disrupted")
                    userBreakedGame = False
                    exitFlag = False
                    break
            else:
                writeLog(f"Bilinmeyen komut girildi: '{userInput}'. 'e' veya 'y' bekleniyordu.")
                printLang("prompts.invalid_disrupt_command")
    except asyncio.CancelledError:
        writeLog("breakGame task'ı iptal edildi.")
        pass
    except Exception as f:
        writeLog(f"Manuel oyun bozucuda bir hata oluştu: {str(f)}", level="error")
        printLang("errors.general_error", e=str(f))
        exitFlag = True


async def checkBreakProtection(breakGameTask): # ? Oyunun bozulup bozulmadığını algılar
    global exitFlag, userBreakedGame
    writeLog("checkBreakProtection task'ı başlatıldı.")
    try:
        while True:
            try:
                fetchedState = await asyncio.to_thread(client.fetch_presence, client.puuid)
                fetchedState = fetchedState['matchPresenceData']['sessionLoopState']
                if fetchedState == "INGAME":
                    os.system("cls")
                    writeAnmiatedText("Instalocker For Valorant","By Berkwe_")
                    writeLog("Oyun başladı. Oyun bozulmadı, Instalocker kapanıyor.", level="info")
                    printLang("game.game_not_disrupted")
                    await asyncio.sleep(3)
                    if breakGameTask and not breakGameTask.done():
                        breakGameTask.cancel()
                        writeLog("INGAME durumu: breakGameTask iptal edildi.")
                    userBreakedGame = False
                    exitFlag = True
                    break 
                elif fetchedState == "MENUS":
                    if userBreakedGame:
                        writeLog("Kullanıcı oyunu bozdu ve MENUS durumuna geçildi. checkBreakProtection sonlanıyor.")
                        break
                    os.system("cls")
                    writeLog("Oyun bozuldu. Instalocker aynı ajanı tekrar seçmek için hazırlanıyor.", level="info")
                    printLang("game.game_disrupted_reselecting")
                    exitFlag = False
                    if breakGameTask and not breakGameTask.done():
                        breakGameTask.cancel()
                        writeLog("BreakGameTask iptal edildi.")
                    break
                await asyncio.sleep(0.2) 
            except asyncio.CancelledError:
                writeLog("checkBreakProtection task'ı (iç döngüde) iptal edildi.")
                break
            except Exception as f_check_inner:
                writeLog(f"Bozulma korumasında (iç döngü) bir hata oluştu: {str(f_check_inner)}", level="error")
                printLang("errors.general_error", e=str(f_check_inner))
                if breakGameTask and not breakGameTask.done():
                    breakGameTask.cancel()
                exitFlag = True
                break
    except asyncio.CancelledError: 
        writeLog("checkBreakProtection task'ı (ana döngü) iptal edildi.")


async def main(): # ? Ana işlev fonksiyonu
    global debug, client, exitFlag, userBreakedGame, rebootFlag, isClientLoggedIn, isShortcut, language
    region = None
    getUserLang()
    getLanguageFile()
    while not exitFlag:
        writeLog("Ana döngü başlatılıyor.", level="info")
        try:
            writeLog(f"Debug modu: {'Açık' if debug else 'Kapalı'}", level="info")
            userBreakedGame = False
            exitFlag = False
            if not isShortcut:
                writeLog("Kısayol tespiti başlatılıyor.")
                args = controlShortcut()
                writeLog("Kısayol tespiti bitti : "+str(args))
                if not args is None:
                    debug = args.get("debug", False)
                    region = args.get("region")
                    selectedAgent = args.get("agent")
                    mode = int(args.get("mode"))
                    if region is None or mode is None or selectedAgent is None:
                        pass
                    else:
                        isShortcut = True
                        continue
            writeLog("Bölge belirleme fonksiyonu çağrılıyor.")
            if region is None:
                region = findRegion()
            if exitFlag:
                writeLog("findRegion sonrası exitFlag True, ana döngüden çıkılıyor.")
                break 
            writeLog(f"Bölge '{region}' olarak ayarlandı.", level="info")
            writeLog("Ajan listesi alma fonksiyonu çağrılıyor.")
            getAgentList() 
            if exitFlag:
                writeLog("getAgentList sonrası exitFlag True, ana döngüden çıkılıyor.")
                break 
            if not agents:
                writeLog("Ajan listesi alınamadı veya boş, Instalocker sonlandırılıyor.", level="error")
                printLang("errors.agent_list_load_failed")
                exitFlag = True
                break
            writeLog(f"Ajan listesi yüklendi. {len(agents.keys())} ajan bulundu.", level="info")
            mode = 0
            while not isShortcut:
                printLang("mode.options_header")
                printLang("mode.options")
                printLang("mode.INPUT_get_mode")
                modeInput = input("").lower()
                writeLog(f"Kullanıcı mod seçimi yaptı: '{modeInput}'")
                if modeInput == "debug":
                    debug = True
                    os.system("cls")
                    writeLog("Debug mod açıldı.", "info")
                    continue
                if modeInput == "":
                    os.system("cls")
                    printLang("mode.set_to_lock")
                    writeLog("Mod: Ajan Kitleme (varsayılan) olarak ayarlandı.", level="info")
                    mode = 1
                    break
                elif modeInput == "help" or modeInput == "yardım":
                    os.system("cls")
                    printLang("help.mode_select_message")
                    writeLog("Kullanıcı mod seçimi için yardım istedi.")
                    continue
                elif not modeInput.isdecimal():
                    os.system("cls")
                    printLang("prompts.enter_number")
                    writeLog(f"Kullanıcı geçersiz mod girişi yaptı, rakam girilmedi: '{modeInput}'")
                    continue
                modeInt = int(modeInput)
                if modeInt == 1:
                    os.system("cls")
                    printLang("mode.set_to_lock")
                    writeLog("Mod: Ajan Kitleme olarak ayarlandı.", level="info")
                    mode = 1
                    break
                elif modeInt == 2:
                    os.system("cls")
                    printLang("mode.set_to_select")
                    writeLog("Mod: Sadece Ajan Seçme olarak ayarlandı.", level="info")
                    mode = 2
                    break
                else:
                    os.system("cls")
                    printLang("prompts.enter_1_or_2")
                    writeLog(f"Kullanıcı geçersiz mod numarası girdi: {modeInt}")
                    continue
            writeLog(f"Client bölge '{region}' için başlatılıyor.")
            client = Client(region=region)
            try:
                client.activate()
                isClientLoggedIn = True
                writeLog(f"Client başarıyla aktive edildi. Kullanıcı: {client.player_name}, PUUID: {client.puuid}", level="info") 
            except HandshakeError:
                isClientLoggedIn = False
                writeLog("Valorant açık değil veya Riot Client ile bağlantı kurulamadı (HandshakeError).", level="error")
                if debug:
                    printLang("debug.valorant_not_open_skipping")
                    writeLog("Debug modu aktif, HandshakeErrora rağmen devam ediliyor.", level="warn")
                    pass
                else:
                    os.system("cls")
                    printLang("debug.valorant_not_open")
                    await asyncio.sleep(3)
                    exitFlag = True
                    break
            while not isShortcut:
                printLang("prompts.INPUT_select_agent")
                agentInput = input("").lower()
                writeLog(f"Kullanıcı ajan girişi yaptı: '{agentInput}'")
                if agentInput == "yardım" or agentInput == "help":
                    os.system("cls")
                    printLang("help.agent_select_message")
                    writeLog("Kullanıcı ajan seçimi için yardım istedi.")
                    continue
                elif agentInput == "güncelle" or agentInput == "update":
                    os.system("cls")
                    writeLog("Kullanıcı ajan listesini manuel olarak güncelleme komutu verdi.", level="info")
                    getAgentList(offline=False)
                    if exitFlag:
                        writeLog("Ajan listesi güncellenirken hata oluştu, ana döngüden çıkılıyor.", level="error")
                        break
                    printLang("success.agent_list_updated")
                    response = updateLanguageFile()
                    if response.get("response"):
                        printLang("info.language_file_manuel_updated")
                        getLanguageFile()
                    continue
                elif agentInput == "yb" or agentInput == "re":
                    rebootFlag = True
                    writeLog("Kullanıcı Instalockeri yeniden başlatıyor...", "info")
                    printLang("info.restarting")
                    time.sleep(0.5)
                    break
                elif agentInput == "ajanlar" or agentInput == "agents":
                    writeLog("Kullanıcı ajan listesini düzgün şekilde çekti.", "debug")
                    print(", ".join(agents.keys()))
                    continue
                elif agentInput == "ajanlar-l" or agentInput == "agents-l":
                    writeLog("Kullanıcı ajan listesini 'liste' şeklinde çekti.", "debug")
                    print(str(list(agents.keys())))
                    continue
                elif agentInput == "liste-konumu" or agentInput == "agents-folder":
                    writeLog("Kullanıcı ajan listesinin konumunu çekti.", "debug")
                    print(agentListPath)
                    continue
                elif agentInput == "kayıt-konumu" or agentInput == "logs-folder":
                    writeLog("Kullanıcı kayıt dosyasının konumunu çekti.", "debug")
                    print(logPath)
                    continue
                selectedAgent = ""
                if agentInput in agents.keys():
                    selectedAgent = agentInput
                elif len(agentInput) >= 4:
                    for agentsNameKey in agents.keys():
                        if agentsNameKey.startswith(agentInput) and len(agentsNameKey) > 5: 
                            selectedAgent = agentsNameKey
                            writeLog(f"Kısmi eşleşme: '{agentInput}' -> '{selectedAgent}' bulundu.")
                            os.system("cls")
                            break 
                if selectedAgent:
                    writeLog(f"Ajan '{selectedAgent.capitalize()}' olarak ayarlandı.", level="info")
                    os.system("cls")
                    break
                elif agentInput == "english":
                    language = "english"
                    os.system("cls")
                    printLang("info.language_changed", language=language)
                    continue
                elif agentInput == "türkçe":
                    language = "turkish"
                    os.system("cls")
                    printLang("info.language_changed", language=language)
                    continue
                else:
                    os.system("cls")
                    printLang("prompts.invalid_agent")
                    writeLog(f"Geçersiz ajan adı girildi veya bulunamadı: '{agentInput}'")
                    continue
            if exitFlag:
                break
            if rebootFlag:
                rebootFlag = False
                os.system("cls")
                continue
            writeLog(f"State task'ı ajan '{selectedAgent}' ve mod '{mode}' ile oluşturuluyor.")
            stateTask = asyncio.create_task(state(mode, selectedAgent, region))
            userBreakedGame = False
            try:
                await stateTask
                writeLog("State task'ı normal bir şekilde tamamlandı veya iptal edildi.")
            except asyncio.CancelledError:
                writeLog("Main iptal edildi.")
            except Exception as f_state_task:
                writeLog(f"StateTask çalıştırılırken bir hata oluştu: {str(f_state_task)}", level="error")
                printLang("errors.state_task_error", error=str(f_state_task))
                exitFlag = True 
            if userBreakedGame:
                writeLog("Oyun kullanıcı tarafından bozuldu, Instalocker yeniden başlatılıyor.", level="info")
                writeAnmiatedText("Instalocker For Valorant", "By Berkwe_")
                continue
            elif exitFlag:
                writeLog("Exit flag aktif ana döngü sonlandırılıyor.", level="info")
                break
        except asyncio.CancelledError:
            writeLog("Main task (ana döngü) iptal edildi.", level="info")
            exitFlag = True
        except Exception as f:
            writeLog(f"Ana döngüde beklenmedik bir hata oluştu: {str(f)}", level="error")
            print(f"Ana programda bir sorun oluştu, lütfen geliştiriciye iletin : {str(f)}")
            await asyncio.sleep(3)
            exitFlag = True
        finally:
            writeLog("Main fonksiyonunun 'finally' bloğu çalışıyor. Aktif async tasklar iptal ediliyor.")
            current_task = asyncio.current_task()
            tasks = [t for t in asyncio.all_tasks() if t is not current_task and not t.done()]
            if tasks:
                writeLog(f"İptal edilecek {len(tasks)} aktf async task var.")
                for t in tasks:
                    writeLog(f"Task '{t.get_name()}' iptal ediliyor.")
                    t.cancel()
                await asyncio.gather(*tasks, return_exceptions=True)
                writeLog("Tüm aktif async tasklar iptal edildi.")
            else:
                writeLog("İptal edilecek aktif async task bulunamadı.")
    writeLog("main() sonlandı, Instalocker kapatılıyor.", level="info")
    await asyncio.sleep(0.5)


if __name__ == "__main__":
    writeLog("\n\n\nInstalocker başlatılıyor (__main__).", level="info")
    writeAnmiatedText("Instalocker For Valorant", "By Berkwe_")
    try:
        asyncio.run(main())
    except Exception as e_run_main:
        writeLog(f"asyncio.run(main) seviyesinde 'beklenmedik' bir hata oluştu : {str(e_run_main)}", level="critical")
        printLang("errors.startup_error", error=str(e_run_main))
    finally:
        writeLog("Instalocker tüm işlemler tamamladı.", level="info")
