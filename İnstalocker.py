import sys
import time
from valclient.client import *
from valclient.resources import regions
import threading
#coded by berkwe_

print("\n                                                                          INSTALOCKER FOR VALORANT")
print('Made by:Berkwe_\n')
s_h = False
while not s_h:
    try:
        playerRegion: str = input("Sunucunuzu girin (Istanbul 'EU' olarak kodlanmıştır): ").lower() # Region
        if playerRegion in regions: # Regionun doğruluğunu kontrol eder
            s_h = True
        else:
            os.system("cls")
            print("HATA : Bilinmeyen sunucu kodu. Sunucu kodları= ", ", ".join(regions))
    except:
        pass
client = Client(region=playerRegion)
try:
    client.activate() # Valorantın açık olduğunu kontrol et
    os.system("cls")
except HandshakeError:
    os.system("cls")
    print("HATA : Valorant açık değil.")
    time.sleep(3)
    sys.exit()
except Exception:
    os.system("cls")
    print("HATA : Bilinmeyen bir hata oluştu.")
    time.sleep(3)
    sys.exit()
deger = False
maclar = []

ajanlar = {
    "agents": {
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
        "ıso": "0e38b510-41a8-5780-5e8f-568b2a4f2d6c"
    }
}


def oyun_kontrol(): # Oyunun bozulup bozulmadığını kontrol eder
    global whil2
    whil2 = 1
    while True:
        try:
            sessionState = client.fetch_presence(client.puuid)['sessionLoopState']
            if sessionState == "INGAME":
                whil2 = 0
                print("Oyun bozulmadı, instalocker kapanıyor...")

                time.sleep(3)
                sys.exit()
        except Exception as e:
            print(f"Bir hata meydana geldi: {e}")


while not deger:
    try:
        preferredAgent = input("Seçilecek ajan: ").lower() 
        if preferredAgent in ajanlar['agents'].keys(): # Seçilen ajan ajanlar sözlüğünün keylerinden biriyse dögüyü kır
            deger = True
        else:
            print("HATA : Bilinmeyen ajan")
    except:
        print("Bilinmeyen bir hata oluştu")
os.system("cls")
print(f"Ajan seçme ekranı bekleniyor, seçilecek ajan : {preferredAgent}")
def main():
    ingame_thread = threading.Thread(target=oyun_kontrol) # Eş zamanlı olarak oyun_kontrol fonksiyonunu çalıştır
    ingame_thread.start()
    whil = 1
    while whil == 1:
        try:
            sessionState = client.fetch_presence(client.puuid)['sessionLoopState']
            if (sessionState == "PREGAME") and (client.pregame_fetch_match()['ID'] not in maclar): # Eğer session state(oyun durumu) PREGAME(Seçim ekranı) olursa devam
                os.system("cls")
                print('Ajan secilme ekranı belirlendi.')
                client.pregame_select_character(ajanlar['agents'][preferredAgent]) # Yazılan karakteri seç
		time.sleep(2)
                client.pregame_lock_character(ajanlar['agents'][preferredAgent]) # Yazılan karakteri kilitle
                maclar.append(client.pregame_fetch_match()['ID']) # Karışmaması için bu listeye ekle 
                print('Ajan başarıyla seçildi : \n' + preferredAgent.capitalize())
                print("\n                                                                                       iyi "
                    "oyunlar!!")
                whil = 0
        except Exception as e:
            print('', end='')
    while whil2 == 1:
        sessionState = client.fetch_presence(client.puuid)['sessionLoopState']
        if (sessionState == "MENUS"): # Eğer session state oyun başlamadan MENUs(menüye girildiğinde olan durum) olursa oyun bozulmuştur
            os.system('cls')
            print(
                f'\nOyun bozuldu, instalocker tekrar aynı ajanı seçiyor. Seçilecek ajan : ' + preferredAgent.capitalize())
            time.sleep(5)
            main()
main()
