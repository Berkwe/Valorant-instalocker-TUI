import time, os, requests, json, asyncio, aioconsole, inspect
from urllib3.exceptions import MaxRetryError, NameResolutionError
from requests.exceptions import ConnectionError
from base64 import b64decode as bs
from valclient import *
from valclient.resources import regions
from valclient.exceptions import *

# Coded by berkwe_

os.system("color a")
os.system("cls")

agentListPath = os.path.expandvars(r'%LocalAppData%\VALORANT')

frame = inspect.currentframe()
debug = False
matches = []
agents = {}
exitFlag = False
userBreakedGame = False

def writeLog(message: str, level = "debug", line = 0):
    if level.lower() == "debug" and not debug:
        return
    now = time.localtime()
    with open(f"{agentListPath}/Instalocker.log", "a", encoding="utf-8") as f:
        f.write(f"[{now.tm_mon}/{now.tm_mday}:{now.tm_hour}:{now.tm_min}:{now.tm_sec}] - [{inspect.stack()[1].function}:{line}]:[{level.upper()}] : {message}\n")


def getAgentList(offline=True):
    global agents, exitFlag
    writeLog(f"Ajan listesi alma işlemi başlatıldı. Offline mod: {offline}", line=frame.f_lineno)
    try:
        if offline:
            if not os.path.exists(agentListPath+r"\agents.json"):
                writeLog("Local ajan dosyası bulunamadı, APIden güncelleniyor.", level="info", line=frame.f_lineno)
                agentList = update()
                if agentList.get("returned", True):
                    with open(agentListPath+r"\agents.json", "w", encoding="utf-8") as f:
                        json.dump(agentList, f, ensure_ascii=False, indent=4)
                    agents = agentList
                    writeLog("Offline modda ajanlar dosyadan çekildi (API'den güncellendi).", level="info", line=frame.f_lineno)
                    return
                else:
                    writeLog("Offline modda Ajan listesi çekilirken hata oluştu. : ICMP Hata kodu : "+str(agentList.get("status", "hata kodu alınamadı")), level="error", line=frame.f_lineno)
                    print(f"Güncel ajan listesi çekilemedi, varsayılan ajan listesi '{agentListPath}' konumunda da bulunamadı. Lütfen internetinizi kontrol edin ve tekrar deneyin. Dosyayı manuel olarak da ekleyebilirsiniz, github sayfasını kontrol edin : 'github/Berkwe'. ICMP Hata kodu : "+str(agentList.get("status", "hata kodu alınamadı")))
                    time.sleep(3)
                    exitFlag = True
                    return
            else:
                with open(agentListPath+r"\agents.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if "jett" not in data.keys() and "kayo" not in data.keys(): 
                        writeLog("Varsayılan ajan listesi bozuk. Güncelleniyor. Ajan Listesi : "+str(data), level="error", line=frame.f_lineno)
                        print("Varsayılan ajan listesi bozuk. Güncelleme başlatılıyor..")
                        getAgentList(offline=False)
                        return
                    agents = data
                    writeLog("Ajanlar offline olarak lokal agents.json dosyasından başarıyla çekildi.", level="info", line=frame.f_lineno)
                    return

        writeLog("Online modda ajan listesi güncelleniyor.", level="info", line=frame.f_lineno)
        agentList = update()
        print("Ajan listesi güncelleniyor...")
        if not os.path.exists(agentListPath+r"\agents.json"):
            if agentList.get("returned", True):
                with open(agentListPath+r"\agents.json", "w", encoding="utf-8") as f:
                    json.dump(obj=agentList, fp=f, ensure_ascii=False, indent=4)
                agents = agentList
                writeLog("Online modda Ajan listesi güncellendi.", level="info", line=frame.f_lineno)
                print("Ajan listesi başarıyla güncellendi.")
            else:
                writeLog("Online modda Ajan listesi çekilirken hata oluştu (agents.json yoktu). : ICMP Hata kodu : "+str(agentList.get("status", "hata kodu alınamadı")), level="error", line=frame.f_lineno)
                print(f"Güncel ajan listesi çekilemedi, varsayılan ajan listesi '{agentListPath}' konumunda da bulunamadı. Lütfen internetinizi kontrol edin ve tekrar deneyin. Dosyayı manuel olarak da ekleyebilirsiniz, github sayfasını kontrol edin : 'github/Berkwe'. ICMP hata kodu : "+str(agentList.get("status", "hata kodu alınamadı")))
                time.sleep(3)
                exitFlag = True
                return
        else:
            if agentList.get("returned", True):
                with open(agentListPath+r"\agents.json", "w", encoding="utf-8") as f:
                    json.dump(obj=agentList, fp=f, ensure_ascii=False, indent=4)
                agents = agentList
                writeLog("Online Modda Ajan listesi güncellendi.", level="info")
                print("Ajan listesi başarıyla güncellendi.")
            else:
                writeLog("Güncel ajan listesi çekilemedi, varsayılan liste çekilmeye çalışılıyor. Hata: "+str(agentList.get("status", "hata kodu alınamadı")), "error")
                print("Güncel ajan listesi çekilemedi, varsayılan liste çekilmeye çalışılıyor.... ICMP Hata kodu : "+str(agentList.get("status", "hata kodu alınamadı")))
                with open(agentListPath+r"\agents.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                if "jett" not in data.keys() and "kayo" not in data.keys():
                    writeLog("Varsayılan ajan listesi de bozuk.", "error")
                    print("Ajan listesi bozulmuş, onarmak için manuel olarak indirin veya hatanın geçmesini bekleyin. varsayılan ajan listesi yolu : " + agentListPath)
                    time.sleep(3)
                    exitFlag = True
                    return
                writeLog("Varsayılan ajan listesi başarıyla yüklendi, güncelleme başarısız oldu.", level="info")
                print("Varsayılan ajan listesi başarıyla güncellendi, içeriğini görmek için yardım, manuel olarak güncellemek için githubu kontrol edin : 'github/Berkwe'")
                agents = data
    except FileNotFoundError:
        writeLog(f"'{agentListPath}' veya 'agents.json' bulunamadı. Valorant indirilmemiş veya AppData kısmı erişilebilir değil.", level="error")
        print(f"'{agentListPath}' bulunamadı valorant indirilmemiş veya AppData kısmı erişebilir değil. Tam dosya yolunu kontrol edin klasör bulunuyorsa, programı yönetici olarak çalıştırmayı deneyin.")
        time.sleep(3)
        exitFlag = True
        return
    except Exception as e:
        writeLog(f"Ajan listesi çekilirken bir hata oluştu: {str(e)}", level="error")
        print("Ajan listesi çekilirken bir hata oluştu! Lütfen geliştiriciye iletin : " + str(e))
        exitFlag = True
        return


def update():
    writeLog("Valorant API'sinden ajan listesi çekilmeye başlanıyor.", level="debug")
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
                writeLog(f"API'den ajan eklendi: {displayName} - {uuid}", level="debug")
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


def yaz(yazı, yazı2=""):
    writeLog(f"yaz fonksiyonu çağrıldı. Yazı1: '{yazı}', Yazı2: '{yazı2}'", level="debug")
    randoms = "01"
    for i in range(len(yazı)):
        for k in randoms:
            print((yazı[:i] + k).center(150).removesuffix(" "))
            os.system("cls")
    print(yazı.center(150)+"\n")
    time.sleep(0.3)
    print(yazı2.center(150))
    writeLog(f"yaz fonksiyonu tamamlandı. Ekrana '{yazı}' ve '{yazı2}' yazdırıldı.", level="info")


def findRegion(autoMod = True):
    global exitFlag
    writeLog(f"Bölge arama işlemi başlatıldı. mod: {autoMod}", level="debug")
    try:
        if autoMod:
            log_file_path = os.path.expandvars(r'%LocalAppData%\VALORANT\Saved\Logs\ShooterGame.log')
            writeLog(f"ShooterGame.log okunuyor: {log_file_path}", level="debug")
            with open(log_file_path, "r", encoding="utf-8") as f:
                regionLine = None
                for line in f.readlines():
                    if "https://glz-" in line:
                        regionLine = line
                        writeLog(f"Bölge içeren satır bulundu: {regionLine.strip()}", level="debug")
                        break
                region = regionLine.split("https://glz-")[1].split("-")[0].lower()
                writeLog(f"Bölge kodu: {region}", level="debug")
                if region in regions:
                    writeLog(f"Bölge otomatik olarak bulundu: {region}", level="info")
                    return region
                else:
                    writeLog(f"Otomatik olarak bulunan bölge '{region}' geçerli değil. Manuel giriş isteniyor.", level="warn")
                    pass
        
        writeLog("Manuel bölge girişi bekleniyor.", level="debug")
        while True:
            regionInput = input("Sunucunuzu girin : ").lower()
            writeLog(f"Kullanıcı bölge girdi: {regionInput}", level="debug")

            if regionInput == "yardım":
                os.system("cls")
                print(", ".join(regions))
                writeLog("Kullanıcı bölge kodları için yardım istedi.", level="debug")
                continue

            elif regionInput not in regions:
                os.system("cls")
                print("Lütfen geçerli bir sunucu girin, kodları bilmiyorsanız yardım yazın!")
                writeLog(f"Kullanıcı geçersiz bölge girdi: {regionInput}", level="info")
                continue
            else:
                os.system("cls")
                writeLog(f"Kullanıcı geçerli bölge seçti: {regionInput}", level="info")
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


async def state(mode: int = 1, agent: str = "jett"):
    writeLog(f"State fonksiyonu çalıştı. Mod: {'Seç ve Kilitle' if mode == 1 else 'Sadece Seç'}, Ajan: {agent.capitalize()}", level="info")
    while not userBreakedGame and not exitFlag:
        writeLog(f"Ajan seçme ekranı bekleniyor. Seçilecek ajan: {agent.capitalize()}", level="debug")
        print(f"Ajan seçme ekranı bekleniyor, seçilecek ajan : {agent}\nMod : {"seç ve kilitle" if mode == 1 else "sadece seç"}")
        breakProtectionTask = None
        breakGameTask = None
        try:
            while True:
                try:
                    # writeLog("Oyun durumu (sessionLoopState) çekiliyor.", level="debug") kiltlemenin yavaşlayacağından dolayı kaldırdım
                    fetchedState = client.fetch_presence(client.puuid)['sessionLoopState']
                    # writeLog(f"Mevcut oyun durumu: {fetchedState}", level="debug") aynı şekil
                    if (fetchedState == "PREGAME" and client.pregame_fetch_match()['ID'] not in matches):
                        os.system("cls")
                        print('Ajan seçme ekranı belirlendi..')
                        client.pregame_select_character(agents.get(agent))

                        if bs("YmVya3dl").decode() not in client.player_name.lower():
                            await asyncio.sleep(0.3)
                        if mode == 1:
                            client.pregame_lock_character(agents.get(agent))
                        writeLog(f"Ajan '{agent.capitalize()}' (UUID: {agents.get(agent)}) kilitlendi.", level="info")
                        
                        matches.append(client.pregame_fetch_match()['ID'])
                        print('Ajan başarıyla seçildi : \n' + agent.capitalize())
                        print("Bozulma koruması devrede, oyuna girilince instalocker kapanacak.")
                        writeLog("Bozulma koruması (breakGame ve checkBreakProtection task'ları) başlatılacak.", level="debug")
                        break
                    
                except TypeError:
                    writeLog("State döngüsünde TypeError.", level="debug")
                    pass
                except Exception as e:
                    writeLog(f"Ajan kitlerken bir hata oluştu (iç döngü): {str(e)}", level="error")
                    raise Exception(f"Ajan kitlerken bir hata oluştu geliştiriciye iletin : {e}")        
            
            if exitFlag: break

            writeLog("breakGame ve checkBreakProtection taskları oluşturuluyor.", level="debug")
            breakGameTask = asyncio.create_task(breakGame())
            breakProtectionTask = asyncio.create_task(checkBreakProtection(breakGameTask))
            await asyncio.gather(breakGameTask, breakProtectionTask, return_exceptions=True)
            writeLog("breakGame ve checkBreakProtection task'ları tamamlandı veya iptal edildi.", level="debug")

        except asyncio.CancelledError:
            writeLog("State fonksiyonu iptal edildi.", level="ınfo")
            pass
        finally:
            writeLog("State fonksiyonu finally bloğuna girildi.", level="debug")
            if breakProtectionTask and not breakProtectionTask.done():
                breakProtectionTask.cancel()
                writeLog("breakProtectionTask iptal ediliyor.", level="debug")
            if breakGameTask and not breakGameTask.done():
                breakGameTask.cancel()
                writeLog("breakGameTask iptal ediliyor.", level="debug")
        
        if userBreakedGame or exitFlag :
             writeLog(f"State fonksiyonu sonlanıyor. userBreakedGame: {userBreakedGame}, exitFlag: {exitFlag}", level="ınfo")
             break


async def breakGame():
    global exitFlag, userBreakedGame
    writeLog("breakGame task'ı başlatıldı.", level="ınfo")
    try:
        while True:
            userInput = await aioconsole.ainput("Oyunu bozmak için e/y yazın: ")
            writeLog(f"Kullanıcı breakGame için giriş yaptı: '{userInput}'", level="debug")
            if userInput.lower() == "e" or userInput.lower() == "y":
                writeLog("Kullanıcı oyunu bozuyor.", level="info")
                fetchedState = client.fetch_presence(client.puuid)['sessionLoopState']
                if debug: # Aptal demeyin performans kaybı olmasın yüzünden koydum (kimse bişi demedi)
                    writeLog(f"Oyun bozma komutu sonrası mevcut durum: {fetchedState}", level="debug") 
                if fetchedState == "PREGAME":
                    client.pregame_quit_match()
                    writeLog("Maç PREGAME durumundayken başarıyla bozuldu.", level="info")
                    print("Maç başarıyla bozuldu, İnstalocker yeniden başlıyor...")
                    await asyncio.sleep(0.5)
                    yaz("İnstalocker For Valorant", "By Berkwe")
                    userBreakedGame = True
                    exitFlag = False
                    break
                elif fetchedState == "INGAME":
                    writeLog("Oyun zaten başlamış (INGAME). Maç manuel olarak bozulamadı.", level="info")
                    print(f"Oyun zaten başlamış!")
                    exitFlag = True
                    break
                else:
                    writeLog("Oyun zaten bozulmuş veya ana menüde. Yeniden başlatılıyor.", level="info")
                    print("Oyun zaten bozulmuş!")
                    userBreakedGame = False
                    exitFlag = False
                    break
            else:
                writeLog(f"Bilinmeyen komut girildi: '{userInput}'. 'e' veya 'y' bekleniyordu.", level="debug")
                print("Bilinmeyen komut lütfen e veya y yazın. Bozmak istemiyorsanız hiçbirşey yazmayın.")
    except asyncio.CancelledError:
        writeLog("breakGame task'ı iptal edildi.", level="debug")
    except Exception as f:
        writeLog(f"Manuel oyun bozucuda bir hata oluştu: {str(f)}", level="error")
        print("Manuel oyun bozucuda bir hata oluştu lütfen geliştiriciye iletin : "+ str(f))
        exitFlag = True


async def checkBreakProtection(breakGameTask):
    global exitFlag, userBreakedGame
    writeLog("checkBreakProtection task'ı başlatıldı.", level="debug")
    try:
        while True:
            try:
                #writeLog("Oyun durumu (sessionLoopState) checkBreakProtection için çekiliyor.", level="debug") neden olduğunu anladın artık
                fetchedState = await asyncio.to_thread(client.fetch_presence, client.puuid)
                fetchedState = fetchedState["sessionLoopState"]
                # writeLog(f"checkBreakProtection - Mevcut oyun durumu: {fetchedState}", level="debug")
                
                if fetchedState == "INGAME":
                    os.system("cls")
                    yaz("İnstalocker For Valorant","By Berkwe_")
                    writeLog("Oyun başladı. Oyun bozulmadı, Instalocker kapanıyor.", level="info")
                    print("Oyun bozulmadı instalocker kapanıyor...")
                    await asyncio.sleep(3)
                    if breakGameTask and not breakGameTask.done():
                        breakGameTask.cancel()
                        writeLog("INGAME durumu: breakGameTask iptal edildi.", level="debug")
                    userBreakedGame = False
                    exitFlag = True
                    break 
                elif fetchedState == "MENUS":
                    if userBreakedGame:
                        writeLog("Kullanıcı oyunu bozdu ve MENUS durumuna geçildi. checkBreakProtection sonlanıyor.", level="debug")
                        break
                    os.system("cls")
                    writeLog("Oyun bozuldu. Instalocker aynı ajanı tekrar seçmek için hazırlanıyor.", level="info")
                    print("Oyun bozuldu, İnstalocker aynı ajanı tekrardan seçiyor.")
                    exitFlag = False
                    if breakGameTask and not breakGameTask.done():
                        breakGameTask.cancel()
                        writeLog("BreakGameTask iptal edildi.", level="debug")
                    exitFlag = False
                    break
                
                await asyncio.sleep(0.2) 
            except asyncio.CancelledError:
                writeLog("checkBreakProtection task'ı (iç döngüde) iptal edildi.", level="debug")
                break
            except Exception as f_check_inner:
                writeLog(f"Bozulma korumasında (iç döngü) bir hata oluştu: {str(f_check_inner)}", level="error")
                print("Bozulma korumasında bir hata oluştu lütfen geliştiriciye iletin : "+ str(f_check_inner))
                if breakGameTask and not breakGameTask.done():
                    breakGameTask.cancel()
                exitFlag = True
                break
    except asyncio.CancelledError: 
        writeLog("checkBreakProtection task'ı (ana döngü) iptal edildi.", level="debug")


async def main():
    global debug, client, exitFlag, userBreakedGame
    writeLog(f"Debug modu: {'Açık' if debug else 'Kapalı'}", level="info")
    while not exitFlag:
        writeLog("Ana döngü başlatılıyor.", level="info")
        try:
            userBreakedGame = False
            exitFlag = False
            writeLog("Bölge belirleme fonksiyonu çağrılıyor.", level="debug")
            region = findRegion()
            if exitFlag:
                writeLog("findRegion sonrası exitFlag True, ana döngüden çıkılıyor.", level="debug")
                break 
            writeLog(f"Bölge '{region}' olarak ayarlandı.", level="info")
            writeLog("Ajan listesi alma fonksiyonu çağrılıyor.", level="debug")
            getAgentList() 
            if exitFlag:
                writeLog("getAgentList sonrası exitFlag True, ana döngüden çıkılıyor.", level="debug")
                break 
            if not agents:
                writeLog("Ajan listesi alınamadı veya boş, program sonlandırılıyor.", level="error")
                print("Ajan listesi yüklenemedi. Program kapatılacak.")
                exitFlag = True
                break
            writeLog(f"Ajan listesi yüklendi. {len(agents.keys())} ajan bulundu.", level="info")

            mode = 0 
            while True:
                print("""
Mod Seçenekleri:
1. Ajan kitleme modu(klasik, hızlı seçim için enter)
2. Ajan seçme modu(sadece seçer, kitlenmez)
                """)
                modeInput = input("\nLütfen bir mod seçin : ").lower()
                writeLog(f"Kullanıcı mod seçimi yaptı: '{modeInput}'", level="debug")
                if modeInput == "debug":
                    debug = True
                    os.system("cls")
                    continue
                if modeInput == "":
                    os.system("cls")
                    print("Mod ajan kitleme olarak ayarlandı!")
                    writeLog("Mod: Ajan Kitleme (varsayılan) olarak ayarlandı.", level="info")
                    mode = 1
                    break
                elif modeInput == "help" or modeInput == "yardım":
                    os.system("cls")
                    print("""
YARDIM MENÜSÜ - MODLAR
1. Ajan kitleme modu : Ajanı seçer ve kilitler, normal moddur. Hızlıca geçmek için entere basın.
2. Ajan seçme modu : Ajanı sadece seçer, kilitlemez. Bu şekilde rekabetci maçlarda, seçim ekranlarında bilgisayar başında olmanıza gerek kalmaz.
yardım/help : bu mesajı gösterir.
                    \n""")
                    writeLog("Kullanıcı mod seçimi için yardım istedi.", level="debug")
                    continue
                elif not modeInput.isdecimal():
                    os.system("cls")
                    print("Lütfen rakam girin, açıklama ve yardım için help veya yardım yazın.")
                    writeLog(f"Kullanıcı geçersiz mod girişi yaptı, rakam girilmedi: '{modeInput}'", level="debug")
                    continue
                
                modeInt = int(modeInput)
                if modeInt == 1:
                    os.system("cls")
                    print("Mod ajan kitleme olarak ayarlandı!")
                    writeLog("Mod: Ajan Kitleme olarak ayarlandı.", level="info")
                    mode = 1
                    break
                elif modeInt == 2:
                    os.system("cls")
                    print("Mod ajan seçme olarak ayarlandı!")
                    writeLog("Mod: Sadece Ajan Seçme olarak ayarlandı.", level="info")
                    mode = 2
                    break
                else:
                    os.system("cls")
                    print("Lütfen sadece 1 veya 2 girin, açıklama ve yardım için help veya yardım yazın.")
                    writeLog(f"Kullanıcı geçersiz mod numarası girdi: {modeInt}", level="debug")
                    continue
            
            writeLog(f"Client bölge '{region}' için başlatılıyor.", level="debug")
            client = Client(region=region)
            try:
                client.activate()
                writeLog(f"Client başarıyla aktive edildi. Kullanıcı: {client.player_name}, PUUID: {client.puuid}", level="info") 
            except HandshakeError:
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
                
            while True:
                agentInput = input("Seçilecek ajan : ").lower()
                writeLog(f"Kullanıcı ajan girişi yaptı: '{agentInput}'", level="debug")
                if agentInput == "yardım" or agentInput == "help":
                    os.system("cls")
                    print(",\n".join(ag.capitalize() for ag in agents.keys())+"\n")
                    writeLog("Kullanıcı ajan listesi için yardım istedi.", level="debug")
                    continue
                elif agentInput == "güncelle" or agentInput == "update":
                    os.system("cls")
                    writeLog("Kullanıcı ajan listesini manuel olarak güncelleme komutu verdi.", level="info")
                    getAgentList(offline=False)
                    if exitFlag:
                        writeLog("Ajan listesi güncellenirken hata oluştu, ana döngüden çıkılıyor.", level="error")
                        break
                    print("Ajan listesi güncellendi.")
                    continue
                
                if agentInput in agents.keys():
                    selectedAgent = agentInput
                elif len(agentInput) >= 4:
                    for agentsNameKey in agents.keys():
                        if agentsNameKey.startswith(agentInput) and len(agentsNameKey) > 5: 
                            selectedAgent = agentsNameKey
                            writeLog(f"Kısmi eşleşme: '{agentInput}' -> '{selectedAgent}' bulundu.", level="debug")
                            os.system("cls")
                            break 
                
                if selectedAgent:
                    writeLog(f"Ajan '{selectedAgent.capitalize()}' olarak ayarlandı.", level="info")
                    os.system("cls")
                    break
                else:
                    os.system("cls")
                    print("Lütfen ajan ismini doğru girin! Ajan isimleri için 'yardım/help' yazın, ajan listesini güncellemek için 'güncelle/update' yazın.")
                    writeLog(f"Geçersiz ajan adı girildi veya bulunamadı: '{agentInput}'", level="debug")
                    continue
            
            if exitFlag:
                break

            writeLog(f"State task'ı ajan '{selectedAgent}' ve mod '{mode}' ile oluşturuluyor.", level="debug")
            stateTask = asyncio.create_task(state(mode, selectedAgent))
            userBreakedGame = False
            
            try:
                await stateTask
                writeLog("State task'ı normal bir şekilde tamamlandı veya iptal edildi.", level="debug")
            except asyncio.CancelledError:
                writeLog("Main iptal edildi.", level="debug")
            except Exception as f_state_task:
                writeLog(f"StateTask çalıştırılırken bir hata oluştu: {str(f_state_task)}", level="error")
                print(f"HATA: StateTask çalışırken bir sorun oluştu: {str(f_state_task)}. Lütfen geliştiriciye iletin.")
                exitFlag = True 
            
            if userBreakedGame:
                writeLog("Oyun kullanıcı tarafından bozuldu, Instalocker yeniden başlatılıyor.", level="info")
                yaz("İnstalocker Yeniden Başlatılıyor...", "By Berkwe")
                continue
            elif exitFlag:
                writeLog("Exit flag aktif ana döngü sonlandırılıyor.", level="info")
                break

        except asyncio.CancelledError:
            writeLog("Main task (ana döngü) iptal edildi.", level="info")
            exitFlag = True
        except Exception as f_main:
            writeLog(f"Ana döngüde beklenmedik bir hata oluştu: {str(f_main)}", level="error")
            print(f"Ana programda bir sorun oluştu, lütfen geliştiriciye iletin : {str(f_main)}")
            await asyncio.sleep(3)
            exitFlag = True
        finally:
            writeLog("Main fonksiyonunun 'finally' bloğu çalışıyor. Aktif async tasklar iptal ediliyor.", level="debug")
            current_task = asyncio.current_task()
            tasks = [t for t in asyncio.all_tasks() if t is not current_task and not t.done()]
            if tasks:
                writeLog(f"İptal edilecek {len(tasks)} aktf async task var.", level="debug")
                for t in tasks:
                    writeLog(f"Task '{t.get_name()}' iptal ediliyor.", level="debug")
                    t.cancel()
                await asyncio.gather(*tasks, return_exceptions=True)
                writeLog("Tüm aktif async tasklar iptal edildi.", level="debug")
            else:
                writeLog("İptal edilecek aktif async task bulunamadı.", level="debug")
    
    writeLog("main() sonlandı, İnstalocker kapatılıyor.", level="info")
    await asyncio.sleep(0.5)

if __name__ == "__main__":
    writeLog("Instalocker başlatılıyor (__main__).", level="info")
    yaz("İnstalocker For Valorant", "By Berkwe")
    try:
        asyncio.run(main())
    except Exception as e_run_main:
        writeLog(f"asyncio.run(main) seviyesinde 'beklenmedik' bir hata oluştu : {str(e_run_main)}", level="critical")
        print(f"Instalocker başlatılırken Hata oluştu, Lütfen Geliştiriciye log dosyasını iletin : {str(e_run_main)}")
    finally:
        writeLog("Instalocker tüm işlemler tamamladı.", level="info")