import time, os, requests, json, asyncio, aioconsole
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

debug = False
matches = []
agents = {}
exitFlag = False
userBreakedGame = False

def getAgentList(offline=True):
    global agents, exitFlag
    try:
        if offline:
            if not os.path.exists(agentListPath+r"\agents.json"):
                agentList = update()
                if agentList.get("returned", True):
                    with open(agentListPath+r"\agents.json", "w", encoding="utf-8") as f:
                        json.dump(agentList, f, ensure_ascii=False, indent=4)
                    agents = agentList
                    return
                else:
                    print(f"Güncel ajan listesi çekilemedi, varsayılan ajan listesi '{agentListPath}' konumunda da bulunamadı. Lütfen internetinizi kontrol edin ve tekrar deneyin. Dosyayı manuel olarak da ekleyebilirsiniz, github sayfasını kontrol edin : 'github/Berkwe'. ICMP Hata kodu : "+str(agentList.get("status", "hata kodu alınamadı")))
                    time.sleep(3)
                    exitFlag = True
                    return
            else:
                with open(agentListPath+r"\agents.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if "jett" not in data.keys():
                        print("Varsayılan ajan listesi bozuk. Güncelleme başlatılıyor..")
                        getAgentList(offline=False)
                        return
                    agents = data
                return

        agentList = update()
        print("Ajan listesi güncelleniyor...")
        if not os.path.exists(agentListPath+r"\agents.json"):
            if agentList.get("returned", True):
                with open(agentListPath+r"\agents.json", "w", encoding="utf-8") as f:
                    json.dump(obj=agentList, fp=f, ensure_ascii=False, indent=4)
                agents = agentList
                print("Ajan listesi başarıyla güncellendi.")
            else:
                print(f"Güncel ajan listesi çekilemedi, varsayılan ajan listesi '{agentListPath}' konumunda da bulunamadı. Lütfen internetinizi kontrol edin ve tekrar deneyin. Dosyayı manuel olarak da ekleyebilirsiniz, github sayfasını kontrol edin : 'github/Berkwe'. ICMP hata kodu : "+str(agentList.get("status", "hata kodu alınamadı")))
                time.sleep(3)
                exitFlag = True
                return
        else:
            if agentList.get("returned", True):
                with open(agentListPath+r"\agents.json", "w", encoding="utf-8") as f:
                    json.dump(obj=agentList, fp=f, ensure_ascii=False, indent=4)
                agents = agentList
                print("Ajan listesi başarıyla güncellendi.")
            else:
                print("Güncel ajan listesi çekilemedi, varsayılan liste çekilmeye çalışılıyor.... ICMP Hata kodu : "+str(agentList.get("status", "hata kodu alınamadı")))
                with open(agentListPath+r"\agents.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                if "jett" not in data.keys():
                    print("Ajan listesi bozulmuş, onarmak için manuel olarak indirin veya hatanın geçmesini bekleyin. varsayılan ajan listesi yolu : " + agentListPath)
                    time.sleep(3)
                    exitFlag = True
                    return
                print("Varsayılan ajan listesi başarıyla güncellendi, içeriğini görmek için yardım, manuel olarak güncellemek için githubu kontrol edin : 'github/Berkwe'")
                agents = data
    except FileNotFoundError:
        print(f"'{agentListPath}' bulunamadı valorant indirilmemiş veya AppData kısmı erişebilir değil. Tam dosya yolunu kontrol edin klasör bulunuyorsa, programı yönetici olarak çalıştırmayı deneyin.")
        time.sleep(3)
        exitFlag = True
        return
    except Exception as e:
        print("Ajan listesi çekilirken bir hata oluştu! Lütfen geliştiriciye iletin : " + str(e))
        exitFlag = True
        return
    

def update():
    try:
        agents = {}
        data = requests.get("https://valorant-api.com/v1/agents?isPlayableCharacter=true", verify=False, timeout=4)
        dataDict = dict(data.json())
        if data.status_code == 200 and dataDict.get("status") == 200:
            for agent in dataDict.get("data"):
                agents[agent.get("displayName").lower() if agent.get("displayName").lower() != "kay/o" else "kayo"] = agent.get("uuid")
            return agents
        else:
            return {"status": data.status_code if data.status_code != 200 else dataDict.get("status"), "returned": False}
    except ConnectionError:
        return {"status": 0, "returned": False}


def yaz(yazı, yazı2=""): 
    randoms = "01"
    for i in range(len(yazı)):
        for k in randoms:
          print((yazı[:i] + k).center(150).removesuffix(" "))
          os.system("cls")
    print(yazı.center(150)+"\n")
    time.sleep(0.3)
    print(yazı2.center(150))


def findRegion(autoMod = True):
    try:
        if autoMod:
            with open(os.path.expandvars(r'%LocalAppData%\VALORANT\Saved\Logs\ShooterGame.log'), "r", encoding="utf-8") as f:
                for line in f.readlines():
                    if "https://glz-" in line:
                        regionLine = line
                        break
                region = regionLine.split("https://glz-")[1].split("-")[0].lower()
                if region in regions:
                    return region
                else:
                    while True:
                        region = input("Sunucunuzu girin : ").lower()

                        if region == "yardım":
                            os.system("cls")
                            print(", ".join(regions))
                            continue

                        elif region not in regions:
                            os.system("cls")
                            print("Lütfen geçerli bir sunucu girin, kodları bilmiyorsanız yardım yazın!")
                            continue
                        else:
                            os.system("cls")
                            return region
        else:
            while True:
                        region = input("Sunucunuzu girin : ").lower()

                        if region == "yardım":
                            os.system("cls")
                            print(", ".join(regions))
                            continue

                        elif region not in regions:
                            os.system("cls")
                            print("Lütfen geçerli bir sunucu girin, kodları bilmiyorsanız yardım yazın!")
                            continue
                        else:
                            os.system("cls")
                            return region
    except FileNotFoundError:
        print("Log dosyası bulunamadı manuel sunucu belirleniyor...")
        return findRegion(False)
    except Exception as f:
        print("bir hata oluştu : "+str(f))
        return findRegion(False)
    

async def state(mode: int = 1, agent: str = "jett"):
    while not userBreakedGame and not exitFlag:
        print(f"Ajan seçme ekranı bekleniyor, seçilecek ajan : {agent}\nMod : {"seç ve kilitle" if mode == 1 else "sadece seç"}")
        breakProtectionTask = None
        breakGameTask = None
        try:
            while True:
                try:
                    fetchedState = client.fetch_presence(client.puuid)['sessionLoopState']
                    if (fetchedState == "PREGAME" and client.pregame_fetch_match()['ID'] not in matches):
                        os.system("cls")
                        print('Ajan seçme ekranı belirlendi..')
                        client.pregame_select_character(agents[agent])
                        if bs("YmVya3dl").decode() not in client.player_name.lower():
                            await asyncio.sleep(0.3)
                        if mode == 1:
                            client.pregame_lock_character(agents[agent])
                        matches.append(client.pregame_fetch_match()['ID'])
                        print('Ajan başarıyla seçildi : \n' + agent.capitalize())
                        print("Bozulma koruması devrede, oyuna girilince instalocker kapanacak.")
                        break
                except TypeError:
                    pass
                except Exception as f:
                    raise Exception(f"Ajan kitlerken bir hata oluştu geliştiriciye iletin : {f}")
            breakGameTask = asyncio.create_task(breakGame())
            breakProtectionTask = asyncio.create_task(checkBreakProtection(breakGameTask))
            await asyncio.gather(breakGameTask, breakProtectionTask, return_exceptions=True)
        except asyncio.CancelledError:
            pass
        finally:
            if breakProtectionTask:
                breakProtectionTask.cancel()
            if breakGameTask:
                breakGameTask.cancel()
            
       
async def breakGame():
    global exitFlag, userBreakedGame
    while True:
        try:
            userInput = await aioconsole.ainput("Oyunu bozmak için e/y yazın: ")
            if userInput.lower() == "e" or userInput.lower() == "y":
                fetchedState = client.fetch_presence(client.puuid)['sessionLoopState']
                if fetchedState == "PREGAME":
                    client.pregame_quit_match()
                    print("Maç başarıyla bozuldu, İnstalocker yeniden başlıyor...")
                    await asyncio.sleep(0.5)
                    yaz("İnstalocker For Valorant", "By Berkwe")
                    userBreakedGame = True
                    exitFlag = False
                    break
                elif fetchedState == "INGAME":
                    print(f"Oyun zaten başlamış!")
                    exitFlag = True
                    break
                else:
                    print("Oyun zaten bozulmuş!")
                    userBreakedGame = False
                    break
            else: 
                print("Bilinmeyen komut lütfen e veya y yazın. Bozmak istemiyorsanız hiçbirşey yazmayın.")
        except asyncio.CancelledError:
            break
        except Exception as f:
            print("Manuel oyun bozucuda bir hata oluştu lütfen geliştiriciye iletin : "+ str(f))


async def checkBreakProtection(breakGameTask):
    global exitFlag, userBreakedGame
    while True:
        try:
            fetchedState = await asyncio.to_thread(client.fetch_presence, client.puuid)
            fetchedState = fetchedState["sessionLoopState"]
            if fetchedState == "INGAME":
                os.system("cls")
                yaz("İnstalocker For Valorant","By Berkwe_")
                print("Oyun bozulmadı instalocker kapanıyor...")
                await asyncio.sleep(3)
                if breakGameTask:
                    breakGameTask.cancel()
                userBreakedGame = False
                exitFlag = True
                break
            elif fetchedState == "MENUS":
                if userBreakedGame:
                    break
                os.system("cls")
                print("Oyun bozuldu, İnstalocker aynı ajanı tekrardan seçiyor.")
                exitFlag = False
                if breakGameTask:
                    breakGameTask.cancel()
                break
            await asyncio.sleep(0.2)
        except asyncio.CancelledError:
            break
        except Exception as f:
            print("Bozulma korumasında bir hata oluştu lütfen geliştiriciye iletin : "+ str(f))



async def main():
    global debug, client, exitFlag, userBreakedGame
    while not exitFlag:
        try:
            region = findRegion()
            getAgentList()
            while True:
                print("""
                    1. Ajan kitleme modu(klasik, hızlı seçim için enter)
                    2. Ajan seçme modu(sadece seçer, kitlenmez)
                """)
                mode = input("\nLütfen bir mod seçin : ")

                if mode == "":
                    os.system("cls")
                    print("Mod ajan kitleme olarak ayarlandı!")
                    mode = 1
                elif mode == "help" or mode == "yardım":
                    os.system("cls")
                    print("""
                                                    YARDIM MENÜSÜ
                    1. Ajan kitleme modu : Ajanı seçer ve kilitler, normal moddur. Hızlıca geçmek için entere basın.
                    2. Ajan seçme modu : Ajanı sadece seçer, kilitlemez. Bu şekilde rekabetci maçlarda, seçim ekranlarında bilgisayar başında olmanıza gerek kalmaz.
                    yardım/help : bu mesajı gösterir.
                \n""")
                    continue
                elif not mode.isdecimal():
                    os.system("cls")
                    print("Lütfen rakam girin, açıklama ve yardım için help veya yardım yazın.")
                    continue

                elif int(mode) == 1:
                    os.system("cls")
                    print("Mod ajan kitleme olarak ayarlandı!")
                    
                elif int(mode) == 2:
                    os.system("cls")
                    print("Mod ajan seçme olarak ayarlandı!")
                else:
                    os.system("cls")
                    print("Lütfen sadece 1 veya 2 girin, açıklama ve yardım için help veya yardım yazın.")
                    continue

                
                client = Client(region)
                try:
                    client.activate()

                except HandshakeError:
                    if debug:
                        print("valorant açık değil fakat debug açık olduğundan atlanıyor..")
                        pass
                    else:
                        os.system("cls")
                        print("Valorant açık değil, açıksa Riot Client uygulamasını tekrar açın.") 
                        await asyncio.sleep(3)
                        exitFlag = True
                        return

                while True:
                    agent = input("Seçilecek ajan : ").lower()
                    if agent == "yardım" or agent == "help":
                        os.system("cls")
                        print(",\n".join(agents.keys())+"\n")
                        continue
                    elif agent == "güncelle" or agent == "update":
                        os.system("cls")
                        getAgentList(offline=False)
                        continue
                    elif agent not in agents.keys():
                        if len(agent) >= 4:
                            for agentsName in agents.keys():
                                if agentsName.startswith(agent) and len(agentsName) > 5:
                                    agent = agentsName
                                    os.system("cls")
                                    break
                            if agent in agents.keys():
                                break
                        os.system("cls")
                        print("Lütfen ajan ismini doğru girin! Ajan isimleri için 'yardım/help' yazın, ajan listesini güncellemek için 'güncelle/update' yazın.")
                        continue
                    os.system("cls")
                    break
                break
            
            stateTask = asyncio.create_task(state(mode, agent))
            userBreakedGame = False
            try:
                await stateTask
            except asyncio.CancelledError:
                pass
            except Exception as f:
                print(f"StateTask oluşturulurken Bir hata oluştu lütfen geliştiriciye iletin : "+str(f))
            
            finally:
                current_task = asyncio.current_task()
                tasks = [t for t in asyncio.all_tasks() if t is not current_task]
                for t in tasks:
                    t.cancel()
                await asyncio.gather(*tasks, return_exceptions=True)
        except asyncio.CancelledError:
            pass
        except Exception as f:
            print(f"Bir hata oluştu lütfen geliştiriciye iletin : "+str(f))
            await asyncio.sleep(3)
            exitFlag = True
            return
        
if __name__ == "__main__":
    yaz("İnstalocker For Valorant", "By Berkwe")
    asyncio.run(main())
