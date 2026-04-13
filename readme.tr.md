<p align="center">
      🌐 <a href=https://github.com/Berkwe/Valorant-instalocker-TUI/blob/main/README.md>English</a>  |  Türkçe
</p>

# 🛠️ Valorant Instalocker V1.9.0

## Tanıtım Videosu
<video src="https://github.com/user-attachments/assets/ff1e1677-f2c0-43a8-bd70-e4cf0cd09c0b" autoplay loop muted playsinline></video>
<a href="https://www.youtube.com/watch?v=BUttrI9untI">**TÜM VİDEO**</a>



Valorant Instalocker, Riot Games’in Valorant oyunu için hızlı ve güvenilir bir otomatik ajan kilitleme aracıdır. Genellikle Valorant instalock aracı veya ajan seçici olarak adlandırılır. Seçtiğiniz ajanı resmi Valorant API’sini kullanarak otomatik olarak seçer ve kilitler. Ban riski çok düşüktür(3-4 yıldır ban yemedim) Program Python ile yazılmıştır, basit bir CLI (konsol arayüzü) içerir ve ajan seçme aşamasını önemli ölçüde hızlandıran hafif bir instalocker betiği olarak çalışır. (ve evet bu yazı ai ile yazıldı)

# ❗ÖNEMLİ
**Bu sürüm hala deneme aşamasındadır hatalarınız veya isteklerinizi [sorunlar](https://github.com/Berkwe/Valorant-instalocker-TUI/issues) kısmından iletin lütfen.**

---

## 🆕 Yeni Özellikler v1.9

### 🌟 Önemli Güncellemeler (Harita Bazlı Seçim Sistemi)
* **Haritaya Göre Ajan Seçme/Kilitleme:** Her harita için özel ajan belirlemenizi sağlayan gelişmiş makro sistemi eklendi.
* **Profil Oluşturma Özelliği:** Harita bazlı seçimlerinizi kaydedebileceğiniz özelleştirilebilir profil sistemi eklendi.
* **Hızlı Profil Seçici & Kısayollar:** Kayıtlı profiller arasında anında geçiş yapmanızı sağlayan hızlı erişim mekanizması eklendi.
* **Otomatik Harita Güncelleyici:** Harita listesini sunucudan otomatik olarak çeken ve her zaman güncel tutan fonksiyon eklendi.
* **Ayarlar Güncellemesi:** Dil Değiştirdiğinizde instalocker bunu kaydedebilecek (gereksizdi ama içimde kalırdı eklemesem)

### 🔧 Genel İyileştirmeler & Sistem Optimizasyonu
* **Sürüm Kontrolü :** Instalocker sürümünü sürekli olarak kontrol edip yeni sürüm varsa sizi uyarır
* **İnatcı Veled :** Instalocker artık oyun başladıkdan sonra kapanmıyor, yeniden başlıyor. Haritaya göre sçeim modundaysa otomatik olarak aynı profili tekrar uyguluyor.
* **Hata Onarımları:** Uygulamanın stabilitesini bozan tüm kritik ve genel hatalar giderildi.
* **Dosya Yapısı Düzenlemesi:** Dosya karışıklığını önlemek için tüm veriler `VALORANT/Instalocker` klasörü altında toplandı.
* **Akıllı Temizleyici:** Eski sürümlerden kalan gereksiz "çöp" dosyaları otomatik olarak temizleyen sistem eklendi.
* **Güncelleme Hatırlatıcı:** Ajan listesi güncelliğini yitirdiğinde kullanıcıyı bilgilendiren yeni mekanizma eklendi.
* **Ayrıntılı Debug Kayıtları:** Sorun giderme sürecini hızlandırmak için hata ayıklama (log) kayıtları detaylandırıldı.

---

## 🚀 Öne Çıkan Özellikler

* **[Komutlar](#%EF%B8%8F-komutlar%C4%B1n-kullan%C4%B1m%C4%B1):** Instalocker bazı özel komutların kullanılmasına izin verir.
* **[Harita Bazlı Seçim (Makro) Modu](#%EF%B8%8F-harita-bazl%C4%B1-se%C3%A7im-kullan%C4%B1m%C4%B1):** Oyuna gelen haritaya göre önceden belirlediğiniz ajanı otomatik seçmenizi sağlayan gelişmiş profil sistemi.
* **[Hızlı Profil Seçici & Kısayollar](#%EF%B8%8F-harita-bazl%C4%B1-se%C3%A7im-kullan%C4%B1m%C4%B1):** Kayıtlı harita profilleriniz (son 3 profil) arasında anında geçiş yapmanızı sağlayan hızlı erişim.
* **[Otomatik Harita Güncelleyici](#%EF%B8%8F-komutlar%C4%B1n-kullan%C4%B1m%C4%B1):** Oyuna yeni haritalar eklendiğinde listeyi sunucudan otomatik tazeleyen altyapı.
* **[Ajan Kilitleme Modu](#%EF%B8%8F-ajan-se%C3%A7imi-ve-modlar%C4%B1n-kullan%C4%B1m%C4%B1):** Seçilen ajanı kilitler, klasik instalock.
* **[Sadece Seçme Modu](#%EF%B8%8F-ajan-se%C3%A7imi-ve-modlar%C4%B1n-kullan%C4%B1m%C4%B1):** Ajanı seçer fakat kilitlemez. Maç sırasında bilgisayar başında olmanıza gerek yok.
* **Oyun Bozulma Koruması:** Maç bozulursa Instalocker, aynı ajan ve modu tekrardan seçecektir.
* **[Bozma Mekaniği](#-ma%C3%A7-bozma-mekani%C4%9Fi-kullan%C4%B1m%C4%B1):** Ajan kitlendikten sonra tek tuşla maç bozabilir, ana menüye dönülür.
* **[Masaüstü Kısayol Oluşturma](#-k%C4%B1sayol-kullan%C4%B1m%C4%B1):** Belirli ajanlar ve modlar için masaüstüne kısayol oluşturabilirsiniz. Kısayolu çalıştırarak hızlıca instalock atabilirsiniz.
* **Dil Desteği:** Instalocker artık birden fazla dil destekliyor, yalnız deneysel bir özellik bu sebeple hataları [Issues](https://github.com/Berkwe/Valorant-instalocker-TUI/issues) kısmından bildirebilirsiniz.
* **Otomatik Dil Algılama:** Dil desteği için otomatik dili algılar, valorant ayarlarına göre değişebilir. Yine de [belirli komutlarla](#-komutlar%C4%B1n-kullan%C4%B1m%C4%B1) değiştirebilirsiniz.
* **[Ajan İsim Kısaltma](#%EF%B8%8F-ajan-i%CC%87sim-k%C4%B1saltmalar%C4%B1-kullan%C4%B1m%C4%B1):** Uzun isimlere sahip ajanların isimlerini kısaltarak hızlı seçim yapabilirsiniz.
* **[Otomatik Ajan Güncellemesi](#%EF%B8%8F-otomatik-ajan-g%C3%BCncellemesi-kullan%C4%B1m%C4%B1):** Yeni ajanlar eklendiğinde otomatik olarak eklenir.
* **[Log Sistemi](#-log-sistemi-a%C3%A7%C4%B1klamas%C4%B1):** Hataları kaydeder ve geliştiriciye bildirme kolaylığı sağlar.

---

## 📦 Kurulum

### 💾 Exe ile:

1. **Exe'yi İndirin:**
   [Instalocker.exe](https://github.com/Berkwe/Valorant-instalocker-TUI/releases/latest/download/Instalocker.exe)
2. **Çalıştırın:** İki kez tıkla ve çalıştır?

### 🐍 Python ile:

#### Gereksinimler

* Python 3.9+
* Ek modüller (requirements.txt)
* **_Not : Bazı özellikler çalışmayabilir_**
#### Adımlar

1. **Projeyi İndirin:**

   - **[Zip Dosyasını İndirin](https://github.com/Berkwe/Valorant-instalocker-TUI/archive/refs/heads/main.zip)**  

   **VEYA**  

   - **Git ile Klonlayın:**
   ```
   git clone https://github.com/Berkwe/Valorant-instalocker-TUI
   cd Valorant-instalocker-TUI
   ```
2. **Modülleri Kurun:**

   ```bash
   pip install -r requirements.txt
   ```
3. **Çalıştırın:**

   ```bash
   python instalocker.py
   ```

---

## 🛠️ Kullanım

### ⚙️ Ajan Seçimi ve Modların Kullanımı

##### - Ajan Kitleme Modu:
- Ajanı kilitler, klasik instalock.
  
##### - Sadece Seçme Modu: 
- Ajanı seçer fakat kitlemez. Bu şekilde rekabetci maçlarda instalock atmak istemeseniz bile Instalocker'i kullanabilirsiniz.

##### - Haritaya Bazlı Seçim Modu:
- Instalocker artık oluşturacağınız profil dosyalarıyla haritaya göre özelleştirdiğiniz seçim modlarıyla (sadece seçme/kilitleme modları) ajan seçebiliyor. Önceden kullandığınız son 3 profil dosyanız kayıt ediliyor ve hızlıca profil dosyalarınıza erişebiliyorsunuz. **[Nasıl Profil Dosyası Oluşturulur?](https://a.com)**

---
### 🗺️ Harita Bazlı Seçim Kullanımı
#### - Harita Bazlı Seçim Özelliği : 
- Yoğun istek üzerine (siyah, y ekseninde fazlalığı olan birinin tavsiyesi) Instalockere Haritalara göre özelleştirilebilen ajan seçim mekaniği eklendi. Bu mekanik girdiğiniz maçtaki gelen haritaya göre ajan ve mod(sadece seçme veya kilitleme modu) seçebiliyor. Bunu profil dosyaları sayesinde yapabiliyor.

#### - Profil Dosyası Kullanımı :
- Profil dosyası Instalocker'in komutlarıyla masaüstüne otomatik olarak oluşturulur. Sonrasında sağ tıklayıp birlikte aç kısmından not defteri ile düzenleyebilirsiniz. Sadece ajan ve mod yazmanız yeterlidir. **AJAN İSİMLERİ EKSİKSİZ GİRİLMELİDİR VE BAŞKA BİR ALANA DOKUNULMAMALIDIR YOKSA INSTALOCKER ÇALIŞMAZ!** Bir profil dosyasındaki haritalar aşağıdaki gibi görünür : 
```
{
    "ascent": {
        "ajan": "", # ? seçilecek ajan
        "mod": "" # ? kullanılacak mod (1 veya 2 girin girilmezse varsayılan olarak 1. modu(kilitleme modu) kullanır)
    },
    "split": {
        "ajan": "", 
        "mod": ""
    },
```
#### - Örnek Doldurma :
```
{
    "ascent": {
        "ajan": "jett", 
        "mod": "1"
    },
    "split": {
        "ajan": "brimstone", # ? burada brim yazamasınız tam isim girmelisiniz. Muhtemelen kısaltma özelliğini ilerde eklemeyeceğim. 
        "mod": "2"
    },
```

#### - Doldurulan Profil Dosyasını Kullanma : 
- **DİKKAT : DOSYALAR KAYIT ETTİKDEN SONRA KULLANILMALIDIR**. ctrl+s ile veya not defterini kapatarak kaydedebilirsiniz.
- Bu çok kolay bir süreçtir 3 şekilde yapılabilir. 
1. -  Eğer Instalocker üzerinden komutlarla yeni oluşturduğunuz bir profil dosyasını doldurduysanız Instalocker size parantez içinde (varsayılan=c:/profil/yolu/sallamasyon/) şeklinde bir uyarı verecektir. O uyarı görünüyorsa dosyanızı kaydettiğinizden emin oldukdan sonra Enter tuşuna basmanız yeterlidir.
2. - Eğer önceden oluşturduğunuzdan farklı bir dosya kullanacaksanız dosyanın yolunu, dosyaya sağ tıklayıp 'dosya yolunu kopyala' seçeneği ile kopyaladıkdan sonra Instalocker'e verebilirsiniz.
3. - Instalocker kullanılan son 3 profili kaydeder ve profil seçim ekranında gösterir. Listelenen profillerinizi numaralarından seçip (1,2,3) hızlıca kullanabilirsiniz.
---

### ⏩ Kısayol Kullanımı

##### - Kısayol Mekaniği :
- Instalocker istediğiniz ajanı ve modu (Harita Bazlı Seçim dışında) hızlıca seçmeniz için bir kısayol oluşturabilir. Bu şekilde sıfırdan uygulamayı açıp bilgileri girmek yerine kısayolunu çalıştırmanız yeterlidir.
  
##### - Kullanım :
- Ajan seçim ekranı beklenirken Instalocker size Kısayol oluşturmak isteyip istemediğinizi sorar. E/Y karakterlerini (büyük küçük duyarsızdır) girerseniz masaüstünüze ajan isminde kullanım modunuzda ve ajanın resmini içeren bir Instalocker kısayolu belirir.

##### - Çalıştırma :
- Oluşan kısayolu çalıştırdığınızda hiçbir ayar girmenize gerek kalmadan oluşturduğunuz ayarlarda Instalocker başlayacaktır.
---
### 🚫 Maç Bozma Mekaniği Kullanımı
##### - Maç Bozma Mekaniği :
-  Instalocker ajan seçim ekranında oyunu bozmak için oyunu kapatmanıza gerek kalmadan bozmanızı sağlayacak bir fonksiyon sunar. Tek yapmanız gereken ajan seçildikten sonra Instalocker'de sorulan 'bozmak ister misiniz?' sorusuna E/Y demektir.

##### - Bozma Sonrası : 
- Maç bozulduktan sonra ana menüye dönersiniz ve maç bozma cezanız verilir, bu mekanik cezayı bypasslamaz sadece oyunu bozmak için oyundan çıkmanıza gerek kalmaz.
 ---
### ⚙️ Komutların Kullanımı
#### **Aşağıdaki komutları mod seçimi kısmında kullanabilirsiniz :**

```
- 1 : Ajanı seçer ve kilitler, normal (varsayılan) moddur. 
      Hızlı geçmek için Enter’a basabilirsiniz.

- 2 : Ajanı sadece seçer, kilitlemez. Bu şekilde rekabetçi maçlarda instalock atmak istemeseniz bile Instalocker'in otomatik ajan seçme özelliğini kullanabilirsiniz. (ajan seçim ekranındaki süre sonunda seçtiğiniz ajan valorant tarafından kilitlenir bu sayede maç bozulmaz ve oyuna girersiniz.)

- 3 : Profil dosyalarını kullanarak oyundaki haritalara göre istediğiniz ajanı ve modu seçersiniz. Profil dosyaları Instalocker tarafından belirli komutlarla oluşturulabilir. (daha fazla bilgi için ajan ismi belirleme komutlarına bakın)

- 4 yardım / help : Bu yardım mesajını gösterir.
```
#### **Aşağıdaki komutları ajan ismi belirleme kısmında kullanabilirsiniz :**
```
#### 🦸 Ajan Seçim Komutları
- -profil-oluştur / create-profile / cp / po
  → Yeni bir profil dosyası oluşturur ve dosya yolunu döndürür.
- -r / rastgele / random
  → Listeden rastgele bir ajan seçer.
- -ajanlar / agents
  → Mevcut ajan listesini okunaklı ve düzenli bir formatta görüntüler.
- -ajanlar-l / agents-l**
  → Ajan listesini ham liste biçiminde döndürür.

#### 🛠️ Genel Sistem Komutları
- -clear / temizle / cls
  → Terminal ekranını temizleyerek karmaşayı giderir.
- -güncelle / update
  → Ajan listesi, harita listesi ve dil dosyalarını sunucudan tazeleyerek günceller.
- -yb / re
  → Uygulamayı kapatmadan hızlıca yeniden başlatır.
- -türkçe / english
  → Uygulama arayüz dilini anında değiştirir.
- -liste-konumu / agents-folder
  → Ajan verilerinin saklandığı klasörün yolunu gösterir.
- -kayıt-konumu / logs-folder
  → Uygulama kayıtlarının (log) tutulduğu klasörü açar.
- -yardım / help
  → Bu yardım menüsünü ve komut detaylarını görüntüler.
```
---
### ✂️ Ajan İsim Kısaltmaları Kullanımı
##### - Ajan İsmi Kısaltma Mekaniği : 
- Valorant ajanlarının boktan ve uzun isimlerini sürekli sürekli girmek can sıkıcı olabiliyor. Instalocker bu uzun isimleri kısaltarak daha iyi bir deneyim sunmak için bir mekaniğe sahip. 5 karakter üstü isimlere sahip ajanların isimleri kısaltılarak yazıldığında (kısaltma en az 4 harf olmalı) Instalocker ajanı seçer.

### Kafan mı karıştı? işte bir örnek : 
  ```text
  ✅ brim → geçerli
  ❌ reyn → geçersiz
  ```
---
### 🔄 Sunucu algılama Özelliği Açıklaması

##### - Otomatik Sunucu Algılama Özelliği : 
- Instalocker yapısı gereği çalışabilmek için kullanıcının sunucusunu bilmek zorundadır. Fakat her seferinde kullanıcının sunucusunu girmesini istemek ayakkabıya giren kumlar kadar sinir bozucu olabiliyor(ki ilk Instalocker sürümlerinde bu yöntem kullanılıyordu). Bu sebeple Instalocker kullanıcının hangi sunucuya bağlı olduğunu otomatik olarak algılayabiliyor. Tabii algılanmazsa ayakkabınıza o kum yine de girecek.
---
### ⬇️ Otomatik ajan güncellemesi Kullanımı

##### - Otomatik Ajan Güncelleme Mekaniği :
- Önceki sürümlerde olmayan ve cehennem yarat diğer bir mekanik ise yeni ajanların **güncellemeden güncellemeye** Instalockere eklenmesiydi. Bu her yeni gelen ajan için yeni güncellemeye gerek duyulmasını sağlıyordu, fakat şuan tek komutla güncellenebiliyor.([Daha fazla bilgi için komutlara bakın]())

##### - Manuel Güncelleme :
- Instalocker'i de bir insan evladı yazdığından, illaki yeni ajanlar eklenirken hata çıkacaktır. Bu durumda aşağıdaki adımları uygulayıp manuel olarak güncelleyebilirsiniz.
    
    #### - 1. adım :
    - **CMD(komut istemi) Uygulamasını açın.**
    #### - 2. adım 
    - **Aşşağıdaki kodu yapıştırın :**
    ####
      curl "https://raw.githubusercontent.com/Berkwe/Valorant-instalocker-TUI/refs/heads/main/agents.json" > %LOCALAPPDATA%\VALORANT\agents.json
---
### 🪲 Log Sistemi Açıklaması

* **Instalocker, hata ayıklama ve yönetimi kolaylaştırmak için sürekli olarak log (kayıt) tutar. Logları ayrıntılı hale getirmek için, mod seçimi ekranındayken konsola ‘debug’ yazabilirsiniz. Bu sayede log dosyasını geliştiriciye gönderdiğinizde hatanın anlaşılması daha kolay olacaktır.**

* **Instalocker.log dosyasını bulmak için Windows+R tuş kombinasyonu ile açılan ‘Çalıştır’ penceresine aşağıdaki komutu girebilirsiniz.**

* ```
  %LOCALAPPDATA%/VALORANT
  ```


---


## ⓘ Performans ve Geri Bildirim

* **Performans sorunları veya önerileriniz için** [Issues](https://github.com/Berkwe/Valorant-instalocker-TUI/issues) **sayfasını kullanabilirsiniz.**

---

## 🖤 Ayrıca Teşekkürler
- **Projeye direkt katkısı olmasada valorant apisini [dokümanlaştıran](https://github.com/techchrism/valorant-api-docs) [techchrism'e](https://github.com/techchrism) ve bu apiyi modülleştiren [colinhartigan'a](https://github.com/colinhartigan) teşekkürler.**

---

## 🌟 Diğer Projelerim

* [ADB Brute-Force](https://github.com/Berkwe/ADB-bruteforce)
* [Audio Converter](https://github.com/Berkwe/Audio-converter)

---

## 📞 İletişim

<a href="https://discord.gg/Xagnh5aYSy" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/discord.svg" alt="Berkwe" height="30" width="40" /></a>

---

## 📝 Lisans

Bu proje [MIT Lisansı](https://github.com/Berkwe/Valorant-instalocker-TUI/blob/main/LICENSE) altında lisanslanmıştır.

---

## ⚠️ Sorumluluk Reddi

Bu yazılım tamamen **eğitim ve kişisel kullanım** amacıyla geliştirilmiştir. Yazılımın kullanımından doğabilecek her türlü risk (oyun içi yasaklamalar, hesap kısıtlamaları, veri kaybı vb.) tamamen **kullanıcının sorumluluğundadır.** Geliştirici, bu yazılımın üçüncü taraf hizmet şartlarını (Riot Games vb.) ihlal etmesi durumunda veya kullanım sonucunda oluşabilecek hiçbir zarardan **sorumlu tutulamaz.** Bu aracı kullanarak bu şartları kabul etmiş sayılırsınız.

---

### 🔑 Anahtar kelimeler
valorant instalocker, valorant auto lock, valorant agent locker, valorant instalock script, valorant agent picker, valorant instalocker tui











