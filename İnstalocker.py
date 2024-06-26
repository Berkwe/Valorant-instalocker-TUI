import sys, time, os
from valclient import *
from valclient.resources import regions
from valclient.exceptions import *

os.system("color a")

# Debug ayarı
debug = False


# Oyunun tekrar tekrar seçmemesi için
maçlar = []

# Thread için yardımcı fonksiyon
thrd = False

# Ajan listesi
ajanlar = { 
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
    "clove": "1dbf2edd-4729-0984-3115-daa5eed44993"
}


def yaz(yazı, yazı2=""): # Şekilli Şukullu yazılar için
    randoms = "0101"
    for i in range(len(yazı)):
        for k in randoms:
          print((yazı[:i] + k).center(150).removesuffix(" "))
          os.system("cls")
    print(yazı.center(150)+"\n")
    time.sleep(0.3)
    print(yazı2.center(150))

def kontrol(): # Oyuna girilip girilmediğini kontrol eder
    global thrd
    print(f"Ajan seçme ekranı bekleniyor, seçilecek ajan : {ajan}")

    while True:
        try:
            oyunDurumu = client.fetch_presence(client.puuid)['sessionLoopState'] # Oyun durumunu çeker
            if (oyunDurumu == "PREGAME" and client.pregame_fetch_match()['ID'] not in maçlar): # Seçme ekranını kontrol eder
                os.system("cls")
                print('Ajan seçme ekranı belirlendi')
                client.pregame_select_character(ajanlar[ajan]) # Ajanı seç
                if not debug: # :)))))
                    time.sleep(0.3)
                client.pregame_lock_character(ajanlar[ajan]) # Ajanı kilitle
                maçlar.append(client.pregame_fetch_match()['ID'])
                print('Ajan başarıyla seçildi : \n' + ajan.capitalize())
                print("Bozulma koruması devrede, oyuna girilince instalocker kapanacak.")
                break
        except Exception as e:
                print("Bir hata oluştu! : ",e)
    while True:
            oyunDurumu = client.fetch_presence(client.puuid)['sessionLoopState']
            if  (oyunDurumu == "MENUS") or (oyunDurumu == "INGAME"): # Bozulma koruması
                if oyunDurumu == "INGAME":
                    os.system("cls")
                    yaz("İnstalocker For Valorant","By Berkwe_")
                    print("Oyun bozulmadı instalocker kapanıyor...")
                    time.sleep(3)
                    break
                else:
                    os.system("cls")
                    print("Oyun bozuldu, İnstalocker aynı ajanı tekrardan seçiyor.")
                    kontrol()

def main(): # Ana program
    global debug, client, ajan
    while True:
        pregion = input("Sunucunuzu girin : ").lower() # Sunucu kodu

        if pregion == "debug" and not debug: # Debug modunu etkinleştir
            os.system("cls")
            print("Debug açıldı!")
            debug = True
            continue

        elif pregion == "yardım": # Yardım menüsü
            os.system("cls")
            print(", ".join(regions))
            continue

        elif pregion not in regions: # Sunucu kodu yanlışsa
            os.system("cls")
            print("Lütfen geçerli bir sunucu girin, kodları bilmiyorsanız yardım yazın!")
            continue
        
        client = Client(region=pregion) # Client ata

        try:
            client.activate() # Oyuna bağlanmaya çalış
            os.system("cls")

        except HandshakeError: # Bağlanılamadı hatası
            if debug:
                pass
            else:
                os.system("cls")
                print("Valorant açık değil veya İnternete bağlı değilsiniz!")
                time.sleep(3)
                sys.exit()

        except Exception as f:
            os.system("cls")
            print("Bilinmeyen bir hata oluştu! : ", f)
            time.sleep(3)
            sys.exit()
        os.system("cls")

        while True:
            ajan = input("Seçilecek ajan : ").lower() # Ajan seçimi
            
            if ajan == "yardım": # Yardım menüsü
                os.system("cls")
                print(",\n".join(ajanlar.keys())+"\n")
                continue

            elif ajan not in ajanlar.keys(): # Ajan doğru yazıldımı
                os.system("cls")
                print("Lütfen ajan ismini doğru girin! Ajan isimleri için yardım yazın.")
                continue
            os.system("cls")
            break
        break
    kontrol()

yaz("İnstalocker For Valorant", "By Berkwe")
main()
       
