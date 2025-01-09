import sys, time, os
from valclient import *
from valclient.resources import regions
from valclient.exceptions import *
os.system("color a")
os.system("cls")


debug = False
matches = []
agents = { 
    "jett": "add6443a-41bd-e414-f6ad-e58d267f4e95",
    "reyna": "a3bfb853-43b2-7238-a4f1-ad90e9e46bcc",
    "raze": "f94c3b30-42be-e959-889c-5aa313dba261",
    "yoru": "7f94d92c-4234-0a36-9646-3a87eb8b5c89",
    "phoenix": "eb93336a-449b-9c1b-0a54-a891f7921d69",
    "neon": "bb2a4828-46eb-8cd1-e765-15848195d751",
    "breach": "5f8d3a7f-467b-97f3-062c-13acf203c006",
    "skye": "6f2a04ca-43e0-be17-7f36-b3908627744d",
    "sova": "320b2a48-4d9b-a075-30f1-1f93a9b638fa",
    "kayo": "601dbbe7-43ce-be57-2a40-4abd24953621",
    "killjoy": "1e58de9c-4950-5125-93e9-a0aee9f98746",
    "cypher": "117ed9e3-49f3-6512-3ccf-0cada7e3823b",
    "sage": "569fdd95-4d10-43ab-ca70-79becc718b46",
    "chamber": "22697a3d-45bf-8dd7-4fec-84a9e28c69d7",
    "omen": "8e253930-4c05-31dd-1b6c-968525494517",
    "brimstone": "9f0d8ba9-4140-b941-57d3-a7ad57c6b417",
    "astra": "41fb69c1-4189-7b37-f117-bcaf1e96f1bf",
    "viper": "707eab51-4836-f488-046a-cda6bf494859",
    "fade": "dade69b4-4f5a-8528-247b-219e5a1facd6",
    "gekko": "e370fa57-4757-3604-3648-499e1f642d3f",
    "harbor": "95b78ed7-4637-86d9-7e41-71ba8c293152",
    "deadlock": "cc8b64c8-4b25-4ff9-6e7f-37b4da43d235",
    "ıso": "0e38b510-41a8-5780-5e8f-568b2a4f2d6c",
    "clove": "1dbf2edd-4729-0984-3115-daa5eed44993",
    "vyse": "efba5359-4016-a1e5-7626-b1ae76895940",
    "tejo": "b444168c-4e35-8076-db47-ef9bf368f384"
}

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
        findRegion(False)
    except Exception as f:
        print("bir hata oluştu : "+f)
        findRegion(False)
    

def state(mode: int = 1):
    print(f"Ajan seçme ekranı bekleniyor, seçilecek ajan : {agent}\nMod : {"seç ve kilitle" if mode == 1 else "sadece seç"}")
    while True:
        try:
            fetchedState = client.fetch_presence(client.puuid)['sessionLoopState']
            if (fetchedState == "PREGAME" and client.pregame_fetch_match()['ID'] not in matches):
                os.system("cls")
                print('Ajan seçme ekranı belirlendi..')
                client.pregame_select_character(agents[agent])
                if not debug:
                    time.sleep(0.3)
                if mode == 1:
                    client.pregame_lock_character(agents[agent])
                matches.append(client.pregame_fetch_match()['ID'])
                print('Ajan başarıyla seçildi : \n' + agent.capitalize())
                print("Bozulma koruması devrede, oyuna girilince instalocker kapanacak.")
                break
        except TypeError:
            pass
        except Exception as f:
            raise Exception(f"Bir hata oluştu geliştiriciye iletin : {f}")

    while True:
            fetchedState = client.fetch_presence(client.puuid)['sessionLoopState']
            if  (fetchedState == "MENUS") or (fetchedState == "INGAME"):
                if fetchedState == "INGAME":
                    os.system("cls")
                    yaz("İnstalocker For Valorant","By Berkwe_")
                    print("Oyun bozulmadı instalocker kapanıyor...")
                    time.sleep(3)
                    break
                else:
                    os.system("cls")
                    print("Oyun bozuldu, İnstalocker aynı ajanı tekrardan seçiyor.")
                    state(mode)


def main():
    global debug, client, agent
    try:
        region = findRegion()
        while True:
            print("""
                1. Ajan kitleme modu(default, hızlı seçim için enter)
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
                    pass
                else:
                    os.system("cls")
                    print("Valorant açık değil veya İnternete bağlı değilsiniz!")
                    time.sleep(3)
                    sys.exit()

            if "berkwe" in client.player_name.lower():
                debug = True

            while True:
                agent = input("Seçilecek ajan : ").lower()
                
                if agent == "yardım" or agent == "help":
                    os.system("cls")
                    print(",\n".join(agents.keys())+"\n")
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
                    print("Lütfen ajan ismini doğru girin! Ajan isimleri için yardım yazın.")
                    continue
                os.system("cls")
                break
            break
        
        state(mode)
    except Exception as f:
        raise Exception(f"Bir hata oluştu geliştiriciye iletin : {f}")

yaz("İnstalocker For Valorant", "By Berkwe")
main()
