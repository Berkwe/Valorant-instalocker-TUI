import time, os, requests, json, asyncio, aioconsole, inspect, argparse
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

agentSelectHelpMessage = "Ajan Seçimi - Komutlar".center(60)+"""
-ajanlar/agents : Ajan listesini okunaklı biçimde döndürür.
-ajanlar-l/agents-l : Ajan listesini 'liste' biçiminde döndürür.
-güncelle/update : Ajan listesini günceller.
-yb/re : Uygulamayı hızlıca yeniden başlatır.
-liste-konumu/agents-folder : Ajan listesinin konumunu döndürür.
-kayıt-konumu/logs-folder : Kayıt dosyasının konumunu döndürür.
-yardım/help : bu mesajı görüntüler\n
"""
modeSelectHelpMessage = "Mod Seçimi - Komutlar".center(60)+"""
- 1  : Ajanı seçer ve kilitler, normal moddur. Hızlıca geçmek için entere basın.
- 2  : Ajanı sadece seçer, kilitlemez. Bu şekilde rekabetci maçlarda, seçim ekranlarında bilgisayar başında olmanıza gerek kalmaz.
- 3 yardım/help : bu mesajı gösterir.\n
"""


os.system("color a")
os.system("cls")

agentListPath = os.path.join(os.path.expandvars(r"%LocalAppData%\VALORANT"), "agents.json")
logPath = os.path.join(os.path.expandvars(r'%LocalAppData%\VALORANT'), "Instalocker.log")

parser = argparse.ArgumentParser()
parser.add_argument("--agent", help="ajan ismi")
parser.add_argument("--mode", help="seçim modu lock/select")
parser.add_argument("--region", help="region idsi (eu,na vb)")
parser.add_argument("--debug", help="hata ayıklama için true/false", type=bool)

debug = False
rebootFlag = False
isClientLoggedIn = False
matches = []
agents = {}
exitFlag = False
userBreakedGame = False
isShortcut = False


def controlShortcut(): # ? Kısayol kontrolü
    args = parser.parse_args()
    dict_args = vars(args)
    if len(dict_args.keys()) == 0:
        return
    else:
        return dict_args
  

def writeLog(message: str, level = "debug"): # ? Logları tutar
    try:
        if level.lower() == "debug" and not debug:
            return
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
        print("Loglar yazılırken bir hata oluştu Lütfen geliştiriciye iletin : ", str(f))
        time.sleep(4)


def createShortCut(array: dict): # ? Kısayol oluşturur
    global exitFlag
    try:
        userDir = os.path.join(os.path.expanduser("~"), "Desktop")
        current_file = os.path.abspath(__file__)

        agent = array.get("agent")
        mode = array.get("mode")
        region = array.get("region")

        shortcutDir = os.path.join(userDir, f"{agent}_{("kilitle" if mode == 0 else "göster")}.lnk")
        iconFolder = os.path.join(os.path.dirname(agentListPath), "agentImages")
        iconDir = os.path.join(iconFolder ,f"{agent}.ico")
        shell = Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(str(shortcutDir))
        shortcut.Targetpath = str(current_file)
        shortcut.Arguments = f"--agent {agent} --mode {mode} --region {region}"+(f" --debug {debug}" if debug else "")
        if not os.path.exists(iconDir):
            url = ("https://valorant-api.com/v1/agents/"+agents.get(agent))
            response = requests.get(url)
            if response.status_code == 200:
                agentInfoDict = dict(response.json())
                agentInfo = agentInfoDict.get("data")
                agentImage = agentInfo.get("displayIcon")
                agentImageResponse = requests.get(agentImage)
                img = Image.open(BytesIO(agentImageResponse.content))
                if not os.path.exists(iconFolder):
                    os.makedirs(iconFolder)
                img.save(str(iconDir))
                shortcut.IconLocation = str(iconDir)
            else:
                shortcut.IconLocation = str(current_file)
        else:
            shortcut.IconLocation = str(iconDir)
        shortcut.save()
        print(f"Kısayol '{os.path.dirname(shortcutDir)}' konumuna oluşturuldu.")
    except Exception as e:
        exitFlag = True
        writeLog("Kısayol oluşturulurken bir hata oluştu : "+str(e), "error")
        print("Kısayol oluşturulurken bir hata oluştu lütfen geliştiriciye iletin : "+str(e), "error")
        time.sleep(4)



async def questShortCut(agentInfo: dict): # ? Kısayol oluşturmak için kullanıcıya sorar
    global exitFlag
    writeLog("questShortCut task'ı başlatıldı", level="ınfo")
    try:
        while True:
            userInput = await aioconsole.ainput("Bu ajan için masaüstüne kısayol oluşturmak istermisiniz? E/H : ")
            writeLog(f"Kullanıcı ShortCut için giriş yaptı: '{userInput}'")
            if userInput.lower() == "e" or userInput.lower() == "y":
                createShortCut(agentInfo)
                break
            elif userInput.lower() == "h" or userInput.lower() == "n":
                break
    except Exception as e:
        exitFlag = True
        writeLog("Kısayolda hata : "+ str(e), "error")
        print("Kısayol oluşturulurken bir hata oluştu Lütfen geliştiriciye iletin : ", str(e))
        time.sleep(4)



def getAgentList(offline=True): # ? Ajan listesini çeken ana görev
    global agents, exitFlag
    writeLog(f"Ajan listesi alma işlemi başlatıldı. Offline mod: {offline}")
    try:
        if offline:
            if not os.path.exists(agentListPath):
                writeLog("Local ajan dosyası bulunamadı, APIden güncelleniyor.", level="ınfo")
                print("Local ajan dosyası bulunamadı, APIden güncelleniyor.")
                agentList = update()
                if agentList.get("returned", True):
                    with open(agentListPath, "w", encoding="utf-8") as f:
                        json.dump(agentList, f, ensure_ascii=False, indent=4)
                    agents = agentList
                    writeLog("Offline modda ajanlar dosyadan çekildi (API'den güncellendi).", level="ınfo")
                    print("Ajanlar başarıyla yüklendi")
                    return
                else:
                    writeLog("Offline modda Ajan listesi çekilirken hata oluştu. : HTTP Hata kodu : "+str(agentList.get("status", "hata kodu alınamadı")), level="error")
                    print(f"Güncel ajan listesi çekilemedi, varsayılan ajan listesi '{agentListPath}' konumunda da bulunamadı. Lütfen internetinizi kontrol edin ve tekrar deneyin. Dosyayı manuel olarak da ekleyebilirsiniz, github sayfasını kontrol edin : 'github/Berkwe'. HTTP Hata kodu : "+str(agentList.get("status", "hata kodu alınamadı")))
                    time.sleep(3)
                    exitFlag = True
                    return
            else:
                with open(agentListPath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if "jett" not in data.keys() or "kayo" not in data.keys(): 
                        writeLog("Varsayılan ajan listesi bozuk. Güncelleniyor. Ajan Listesi : "+str(data), level="error")
                        print("Varsayılan ajan listesi bozuk. Güncelleme başlatılıyor..")
                        getAgentList(offline=False)
                        return
                    agents = data
                    writeLog("Ajanlar offline olarak lokal agents.json dosyasından başarıyla çekildi.", level="ınfo")
                    return

        writeLog("Online modda ajan listesi güncelleniyor.", level="ınfo")
        agentList = update()
        print("Ajan listesi güncelleniyor...")
        if not os.path.exists(agentListPath):
            if agentList.get("returned", True):
                with open(agentListPath, "w", encoding="utf-8") as f:
                    json.dump(obj=agentList, fp=f, ensure_ascii=False, indent=4)
                agents = agentList
                writeLog("Online modda Ajan listesi güncellendi.", level="ınfo")
                print("Ajan listesi başarıyla güncellendi.")
            else:
                writeLog("Online modda Ajan listesi çekilirken hata oluştu (agents.json yoktu). : HTTP Hata kodu : "+str(agentList.get("status", "hata kodu alınamadı")), level="error")
                print(f"Güncel ajan listesi çekilemedi, varsayılan ajan listesi '{agentListPath}' konumunda da bulunamadı. Lütfen internetinizi kontrol edin ve tekrar deneyin. Dosyayı manuel olarak da ekleyebilirsiniz, github sayfasını kontrol edin : 'github/Berkwe'. HTTP hata kodu : "+str(agentList.get("status", "hata kodu alınamadı")))
                time.sleep(3)
                exitFlag = True
                return
        else:
            if agentList.get("returned", True):
                with open(agentListPath, "w", encoding="utf-8") as f:
                    json.dump(obj=agentList, fp=f, ensure_ascii=False, indent=4)
                agents = agentList
                writeLog("Online Modda Ajan listesi güncellendi.", level="ınfo")
                print("Ajan listesi güncellendi.")
            else:
                writeLog("Güncel ajan listesi çekilemedi, varsayılan liste çekilmeye çalışılıyor. Hata: "+str(agentList.get("status", "hata kodu alınamadı")), "error")
                print("Güncel ajan listesi çekilemedi, varsayılan liste çekilmeye çalışılıyor.... HTTP Hata kodu : "+str(agentList.get("status", "hata kodu alınamadı")))
                with open(agentListPath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if "jett" not in data.keys() or "kayo" not in data.keys():
                    writeLog("Varsayılan ajan listesi de bozuk.", "error")
                    print("Ajan listesi bozulmuş, onarmak için manuel olarak indirin veya hatanın geçmesini bekleyin. varsayılan ajan listesi yolu : " + agentListPath)
                    time.sleep(3)
                    exitFlag = True
                    return
                writeLog("Varsayılan ajan listesi başarıyla yüklendi, güncelleme başarısız oldu.", level="ınfo")
                print("Varsayılan ajan listesi başarıyla güncellendi, içeriğini görmek için yardım, manuel olarak güncellemek için githubu kontrol edin : 'github/Berkwe'")
                agents = data
    except FileNotFoundError:
        writeLog(f"'{os.path.dirname(agentListPath)}' veya 'agents.json' bulunamadı. Valorant indirilmemiş veya AppData kısmı erişilebilir değil.", level="error")
        print(f"'{os.path.dirname(agentListPath)}' bulunamadı valorant indirilmemiş veya AppData kısmı erişebilir değil. Tam dosya yolunu kontrol edin. Klasör bulunuyorsa, Instalocker'ı yönetici olarak çalıştırmayı deneyin.")
        time.sleep(3)
        exitFlag = True
        return
    except Exception as e:
        writeLog(f"Ajan listesi çekilirken bir hata oluştu: {str(e)}", level="error")
        print("Ajan listesi çekilirken bir hata oluştu! Lütfen geliştiriciye iletin : " + str(e))
        exitFlag = True
        return


def update(): # ? Api'den ajan listesini çeker
    writeLog("Valorant API'sinden ajan listesi çekilmeye başlanıyor.")
    try:
        agentsTemp = {}
        data = requests.get("https://valorant-api.com/v1/agents?isPlayableCharacter=true", verify=False, timeout=4) 
        dataDict = dict(data.json())
        if data.status_code == 200 and dataDict.get("status") == 200:
            for agent in dataDict.get("data"):
                displayName = agent.get("displayName").lower()
                uuid = agent.get("uuid")
                if displayName == "kay/o":
                    displayName = "kayo"
                agentsTemp[displayName] = uuid
                writeLog(f"API'den ajan eklendi: {displayName} - {uuid}")
            writeLog(f"API'den {len(agentsTemp)} ajan başarıyla çekildi.", level="ınfo")
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
    writeLog(f"yaz fonksiyonu tamamlandı. Ekrana '{header}' ve '{footer}' yazdırıldı.", level="ınfo")


def findRegion(autoMod = True): # ? Kullanıcının sunucusunu algılar
    global exitFlag
    writeLog(f"Bölge arama işlemi başlatıldı. mod: {autoMod}")
    try:
        if autoMod:
            log_file_path = os.path.expandvars(r'%LocalAppData%\VALORANT\Saved\Logs\ShooterGame.log')
            writeLog(f"ShooterGame.log okunuyor: {log_file_path}")
            with open(log_file_path, "r", encoding="utf-8") as f:
                regionLine = None
                for line in f.readlines():
                    if "https://glz-" in line:
                        regionLine = line
                        writeLog(f"Bölge içeren satır bulundu: {regionLine.strip()}")
                        break
                region = regionLine.split("https://glz-")[1].split("-")[0].lower()
                writeLog(f"Bölge kodu: {region}")
                if region in regions:
                    writeLog(f"Bölge otomatik olarak bulundu: {region}", level="ınfo")
                    return region
                else:
                    writeLog(f"Otomatik olarak bulunan bölge '{region}' geçerli değil. Manuel giriş isteniyor.", level="warn")
                    pass
        writeLog("Manuel bölge girişi bekleniyor.")
        while True:
            regionInput = input("Sunucunuzu girin : ").lower()
            writeLog(f"Kullanıcı bölge girdi: {regionInput}")

            if regionInput == "yardım":
                os.system("cls")
                print(", ".join(regions))
                writeLog("Kullanıcı bölge kodları için yardım istedi.")
                continue

            elif regionInput not in regions:
                os.system("cls")
                print("Lütfen geçerli bir sunucu girin, kodları bilmiyorsanız yardım yazın!")
                writeLog(f"Kullanıcı geçersiz bölge girdi: {regionInput}", level="ınfo")
                continue
            else:
                os.system("cls")
                writeLog(f"Kullanıcı geçerli bölge seçti: {regionInput}", level="ınfo")
                return regionInput

    except FileNotFoundError:
        writeLog("ShooterGame.log dosyası bulunamadı. Manuel sunucu belirleme moduna geçiliyor.", level="error")
        print("Log dosyası bulunamadı manuel sunucu belirleniyor...")
        return findRegion(False)
    except Exception as f:
        if not autoMod:
            writeLog(f"Bölge bulunurken bir hata oluştu, manuel sunucu da belirlenemedi: {str(f)}", level="error")
            exitFlag = True
            print("bir hata oluştu : "+str(f))
        else:
            writeLog(f"Bölge bulunurken bir hata oluştu: {str(f)}. Manuel sunucu belirlemeye geçiliyor.", level="error")
            print("bir hata oluştu : "+str(f))
            return findRegion(False)


async def state(mode: int = 1, agent: str = "jett", region: str = "eu"): # ? Seçim ekranı durum kontrolü için
    while not userBreakedGame and not exitFlag:
        writeLog(f"State fonksiyonu çalıştı. Mod: {'Seç ve Kilitle' if mode == 1 else 'Sadece Seç'}, Ajan: {agent.capitalize()}", level="ınfo") 
        print(f"Ajan seçme ekranı bekleniyor, seçilecek ajan : {agent}\nMod : {"seç ve kilitle" if mode == 1 else "sadece seç"}")
        breakProtectionTask = None
        breakGameTask = None
        if not isShortcut:
            await questShortCut({"agent": agent, "mode": mode, "region": region})
        try:
            while True:
                try:
                    # * writeLog("Oyun durumu (sessionLoopState) çekiliyor.") kiltlemenin yavaşlayacağından dolayı kaldırdım
                    fetchedState = client.fetch_presence(client.puuid)['sessionLoopState']
                    # * writeLog(f"Mevcut oyun durumu: {fetchedState}") aynı şekil
                    if (fetchedState == "PREGAME" and client.pregame_fetch_match()['ID'] not in matches and isClientLoggedIn):
                        os.system("cls")
                        print('Ajan seçme ekranı belirlendi..')
                        client.pregame_select_character(agents.get(agent))
                        if bs("YmVya3dl").decode() not in client.player_name.lower():
                            await asyncio.sleep(0.3)
                        if mode == 1:
                            client.pregame_lock_character(agents.get(agent))
                        writeLog(f"Ajan '{agent.capitalize()}' (UUID: {agents.get(agent)}) kilitlendi.", level="ınfo")
                        
                        matches.append(client.pregame_fetch_match()['ID'])
                        print('Ajan başarıyla seçildi : \n' + agent.capitalize())
                        print("Bozulma koruması devrede, oyuna girilince instalocker kapanacak.")
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
            
            if exitFlag: break

            writeLog("breakGame ve checkBreakProtection taskları oluşturuluyor.")
            breakGameTask = asyncio.create_task(breakGame())
            breakProtectionTask = asyncio.create_task(checkBreakProtection(breakGameTask))
            await asyncio.gather(breakGameTask, breakProtectionTask, return_exceptions=True)
            writeLog("breakGame ve checkBreakProtection task'ları tamamlandı veya iptal edildi.")
        except asyncio.CancelledError:
            writeLog("State fonksiyonu iptal edildi.", level="ınfo")
            pass
        finally:
            writeLog("State fonksiyonu finally bloğuna girildi.")
            if breakProtectionTask and not breakProtectionTask.done():
                breakProtectionTask.cancel()
                writeLog("breakProtectionTask iptal ediliyor.")
            if breakGameTask and not breakGameTask.done():
                breakGameTask.cancel()
                writeLog("breakGameTask iptal ediliyor.")
        
        if userBreakedGame or exitFlag :
            writeLog(f"State fonksiyonu sonlanıyor. userBreakedGame: {userBreakedGame}, exitFlag: {exitFlag}", level="ınfo")
            break


async def breakGame(): # ? Oyunu bozar
    global exitFlag, userBreakedGame
    writeLog("breakGame task'ı başlatıldı.", level="ınfo")
    try:
        while True:
            userInput = await aioconsole.ainput("Oyunu bozmak için e/y yazın: ")
            writeLog(f"Kullanıcı breakGame için giriş yaptı: '{userInput}'")
            if userInput.lower() == "e" or userInput.lower() == "y":
                writeLog("Kullanıcı oyunu bozuyor.", level="ınfo")
                fetchedState = client.fetch_presence(client.puuid)['sessionLoopState']
                if debug: # Abtal demeyin performans kaybı olmasın diye koydum (kimse bişi demedi)
                    writeLog(f"Oyun bozma komutu sonrası mevcut durum: {fetchedState}") 
                if fetchedState == "PREGAME":
                    client.pregame_quit_match()
                    writeLog("Maç PREGAME durumundayken başarıyla bozuldu.", level="ınfo")
                    print("Maç başarıyla bozuldu, Instalocker yeniden başlıyor...")
                    await asyncio.sleep(0.5)
                    writeAnmiatedText("Instalocker For Valorant", "By Berkwe_")
                    userBreakedGame = True
                    exitFlag = False
                    break
                elif fetchedState == "INGAME":
                    writeLog("Oyun zaten başlamış (INGAME). Maç manuel olarak bozulamadı.", level="ınfo")
                    print(f"Oyun zaten başlamış!")
                    exitFlag = True
                    break
                else:
                    writeLog("Oyun zaten bozulmuş veya ana menüde. Yeniden başlatılıyor.", level="ınfo")
                    print("Oyun zaten bozulmuş!")
                    userBreakedGame = False
                    exitFlag = False
                    break
            else:
                writeLog(f"Bilinmeyen komut girildi: '{userInput}'. 'e' veya 'y' bekleniyordu.")
                print("Bilinmeyen komut lütfen e veya y yazın. Bozmak istemiyorsanız hiçbirşey yazmayın.")
    except asyncio.CancelledError:
        writeLog("breakGame task'ı iptal edildi.")
        pass
    except Exception as f:
        writeLog(f"Manuel oyun bozucuda bir hata oluştu: {str(f)}", level="error")
        print("Manuel oyun bozucuda bir hata oluştu lütfen geliştiriciye iletin : "+ str(f))
        exitFlag = True


async def checkBreakProtection(breakGameTask): # ? Oyunun bozulup bozulmadığını algılar
    global exitFlag, userBreakedGame
    writeLog("checkBreakProtection task'ı başlatıldı.")
    try:
        while True:
            try:
                #writeLog("Oyun durumu (sessionLoopState) checkBreakProtection için çekiliyor.") neden olduğunu anladın artık
                fetchedState = await asyncio.to_thread(client.fetch_presence, client.puuid)
                fetchedState = fetchedState["sessionLoopState"]
                # writeLog(f"checkBreakProtection - Mevcut oyun durumu: {fetchedState}")
                
                if fetchedState == "INGAME":
                    os.system("cls")
                    writeAnmiatedText("Instalocker For Valorant","By Berkwe_")
                    writeLog("Oyun başladı. Oyun bozulmadı, Instalocker kapanıyor.", level="ınfo")
                    print("Oyun bozulmadı instalocker kapanıyor...")
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
                    writeLog("Oyun bozuldu. Instalocker aynı ajanı tekrar seçmek için hazırlanıyor.", level="ınfo")
                    print("Oyun bozuldu, Instalocker aynı ajanı tekrardan seçiyor.")
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
                print("Bozulma korumasında bir hata oluştu lütfen geliştiriciye iletin : "+ str(f_check_inner))
                if breakGameTask and not breakGameTask.done():
                    breakGameTask.cancel()
                exitFlag = True
                break
    except asyncio.CancelledError: 
        writeLog("checkBreakProtection task'ı (ana döngü) iptal edildi.")


async def main(): # ? Ana işlev fonksiyonu
    global debug, client, exitFlag, userBreakedGame, rebootFlag, isClientLoggedIn, isShortcut
    region = None
    while not exitFlag:
        writeLog("Ana döngü başlatılıyor.", level="ınfo")
        try:
            writeLog(f"Debug modu: {'Açık' if debug else 'Kapalı'}", level="ınfo")
            userBreakedGame = False
            exitFlag = False
            if not isShortcut:
                writeLog("Kısayol tespiti başlatılıyor.") # * levelsiz debug oluyor
                args = controlShortcut()
                writeLog("Kısayol tespiti bitti : "+str(args))
                if not args is None:
                    debug = args.get("debug", False)
                    region = args.get("region")
                    selectedAgent = args.get("agent")
                    mode = args.get("mode")
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
            writeLog(f"Bölge '{region}' olarak ayarlandı.", level="ınfo")
            writeLog("Ajan listesi alma fonksiyonu çağrılıyor.")
            getAgentList() 
            if exitFlag:
                writeLog("getAgentList sonrası exitFlag True, ana döngüden çıkılıyor.")
                break 
            if not agents:
                writeLog("Ajan listesi alınamadı veya boş, Instalocker sonlandırılıyor.", level="error")
                print("Ajan listesi yüklenemedi. Instalocker kapatılacak.")
                exitFlag = True
                break
            writeLog(f"Ajan listesi yüklendi. {len(agents.keys())} ajan bulundu.", level="ınfo")
            mode = 0
            while not isShortcut:
                print("\nMod Seçenekleri : \n".center(60))
                print("""
1. Ajan kitleme modu(klasik, hızlı seçim için enter)
2. Ajan seçme modu(sadece seçer, kitlenmez)
                """)
                modeInput = input("\nLütfen bir mod seçin : ").lower()
                writeLog(f"Kullanıcı mod seçimi yaptı: '{modeInput}'")
                if modeInput == "debug":
                    debug = True
                    os.system("cls")
                    writeLog("Debug mod açıldı.", "ınfo")
                    continue
                if modeInput == "":
                    os.system("cls")
                    print("Mod ajan kitleme olarak ayarlandı!")
                    writeLog("Mod: Ajan Kitleme (varsayılan) olarak ayarlandı.", level="ınfo")
                    mode = 1
                    break
                elif modeInput == "help" or modeInput == "yardım":
                    os.system("cls")
                    print(modeSelectHelpMessage)
                    writeLog("Kullanıcı mod seçimi için yardım istedi.")
                    continue
                elif not modeInput.isdecimal():
                    os.system("cls")
                    print("Lütfen rakam girin, açıklama ve yardım için help veya yardım yazın.")
                    writeLog(f"Kullanıcı geçersiz mod girişi yaptı, rakam girilmedi: '{modeInput}'")
                    continue
                
                modeInt = int(modeInput)
                if modeInt == 1:
                    os.system("cls")
                    print("Mod ajan kitleme olarak ayarlandı!")
                    writeLog("Mod: Ajan Kitleme olarak ayarlandı.", level="ınfo")
                    mode = 1
                    break
                elif modeInt == 2:
                    os.system("cls")
                    print("Mod ajan seçme olarak ayarlandı!")
                    writeLog("Mod: Sadece Ajan Seçme olarak ayarlandı.", level="ınfo")
                    mode = 2
                    break
                else:
                    os.system("cls")
                    print("Lütfen sadece 1 veya 2 girin, açıklama ve yardım için help veya yardım yazın.")
                    writeLog(f"Kullanıcı geçersiz mod numarası girdi: {modeInt}")
                    continue
            
            writeLog(f"Client bölge '{region}' için başlatılıyor.")
            client = Client(region=region)
            try:
                client.activate()
                isClientLoggedIn = True
                writeLog(f"Client başarıyla aktive edildi. Kullanıcı: {client.player_name}, PUUID: {client.puuid}", level="ınfo") 
            except HandshakeError:
                isClientLoggedIn = False
                writeLog("Valorant açık değil veya Riot Client ile bağlantı kurulamadı (HandshakeError).", level="error")
                if debug:
                    print("valorant açık değil fakat debug açık olduğundan atlanıyor..")
                    writeLog("Debug modu aktif, HandshakeErrora rağmen devam ediliyor.", level="warn")
                    pass
                else:
                    os.system("cls")
                    print("Valorant açık değil, açıksa Riot Client uygulamasını tekrar açın.") 
                    await asyncio.sleep(3)
                    exitFlag = True
                    break
                
            while not isShortcut:
                agentInput = input("Seçilecek ajan : ").lower()
                writeLog(f"Kullanıcı ajan girişi yaptı: '{agentInput}'")
                if agentInput == "yardım" or agentInput == "help":
                    os.system("cls")
                    print(agentSelectHelpMessage)
                    writeLog("Kullanıcı ajan seçimi için yardım istedi.")
                    continue
                elif agentInput == "güncelle" or agentInput == "update":
                    os.system("cls")
                    writeLog("Kullanıcı ajan listesini manuel olarak güncelleme komutu verdi.", level="ınfo")
                    getAgentList(offline=False)
                    if exitFlag:
                        writeLog("Ajan listesi güncellenirken hata oluştu, ana döngüden çıkılıyor.", level="error")
                        break
                    print("Ajan listesi başarıyla güncellendi.")
                    continue
                elif agentInput == "yb" or agentInput == "re":
                    rebootFlag = True
                    writeLog("Kullanıcı Instalockeri yeniden başlatıyor...", "ınfo")
                    print("Yeniden başlatılıyor...")
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
                    writeLog(f"Ajan '{selectedAgent.capitalize()}' olarak ayarlandı.", level="ınfo")
                    os.system("cls")
                    break
                else:
                    os.system("cls")
                    print("Lütfen ajan ismini doğru girin! Ajan isimleri ve diğer komutlar için 'yardım/help' yazın.")
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
                print(f"HATA: StateTask çalışırken bir sorun oluştu: {str(f_state_task)}. Lütfen geliştiriciye iletin.")
                exitFlag = True 
            
            if userBreakedGame:
                writeLog("Oyun kullanıcı tarafından bozuldu, Instalocker yeniden başlatılıyor.", level="ınfo")
                writeAnmiatedText("Instalocker For Valorant", "By Berkwe_")
                continue
            elif exitFlag:
                writeLog("Exit flag aktif ana döngü sonlandırılıyor.", level="ınfo")
                break

        except asyncio.CancelledError:
            writeLog("Main task (ana döngü) iptal edildi.", level="ınfo")
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
    
    writeLog("main() sonlandı, Instalocker kapatılıyor.", level="ınfo")
    await asyncio.sleep(0.5)

if __name__ == "__main__":
    writeLog("\n\n\nInstalocker başlatılıyor (__main__).", level="ınfo")
    writeAnmiatedText("Instalocker For Valorant", "By Berkwe_")
    try:
        asyncio.run(main())
    except Exception as e_run_main:
        writeLog(f"asyncio.run(main) seviyesinde 'beklenmedik' bir hata oluştu : {str(e_run_main)}", level="critical")
        print(f"Instalocker başlatılırken Hata oluştu, Lütfen Geliştiriciye log dosyasını iletin : {str(e_run_main)}")
    finally:
        writeLog("Instalocker tüm işlemler tamamladı.", level="ınfo")