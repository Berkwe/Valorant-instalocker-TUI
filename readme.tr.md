<p align="center">
      🌐 <a href=https://github.com/Berkwe/Valorant-instalocker/blob/main/README.md>English</a>  |  Türkçe
</p>

# ❗ÖNEMLİ
**Bu sürüm hala deneme aşamasındadır hatalarınız  [sorunlar](https://github.com/Berkwe/Valorant-instalocker/issues) kısmından iletin lütfen.**

# 🛠️ Valorant Instalocker

Valorant Instalocker, Riot Games’in Valorant oyunu için hızlı ve güvenilir bir otomatik ajan kilitleme aracıdır. Genellikle Valorant instalock aracı veya ajan seçici olarak adlandırılır. Seçtiğiniz ajanı resmi Valorant API’sini kullanarak otomatik olarak seçer ve kilitler. Program Python ile yazılmıştır, basit bir CLI (konsol arayüzü) içerir ve ajan seçme aşamasını önemli ölçüde hızlandıran hafif bir instalocker betiği olarak çalışır. (ve evet bu yazı ai ile yazıldı)

---

## 🆕 Yeni Özellikler v1.7

* **Masaüstü Kısayol Oluşturma:** Belirli ajanlar ve modlar için masaüstüne kısayol oluşturabilirsiniz. Kısayolu çalıştırarak hızlıca instalock atabilirsiniz.
* **Dil Desteği:** Instalocker artık birden fazla dil destekliyor, yalnız deneysel bir özellik bu sebeple hataları [Issues](https://github.com/Berkwe/Valorant-instalocker/issues) kısmından bildirebilirsiniz.
* **Otomatik Dil Algılama:** Dil desteği için otomatik dili algılar, valorant ayarlarına göre değişebilir. Yine de belirli komutlarla değiştirebilirsiniz.
---

## 🚀 Öne Çıkan Özellikler

* **Ajan Kilitleme Modu:** Seçilen ajanı kilitler, klasik instalock.
* **Sadece Seçme Modu:** Ajanı seçer fakat kilitlemez. Maç sırasında bilgisayar başında olmanıza gerek yok.
* **Bozma Mekaniği:** Ajan kitlendikten sonra tek tuşla maç bozabilir, ana menüye dönülür.
* **Ajan İsim Kısaltma:** Uzun isimlere sahip ajanların isimlerini kısaltarak hızlı seçim yapabilirsiniz.
* **Otomatik Ajan Güncellemesi:** Yeni ajanlar eklendiğinde otomatik olarak eklenir.
* **Log Sistemi:** Hataları kaydeder ve geliştiriciye bildirme kolaylığı sağlar.

---

## 📦 Kurulum

### 💾 Exe ile:

1. **Exe'yi İndirin:**
   [Instalocker.exe](https://github.com/Berkwe/Valorant-instalocker/releases/latest/download/Instalocker.exe)
2. **Çalıştırın:** İki kez tıkla ve çalıştır?

### 🐍 Python ile:

#### Gereksinimler

* Python 3.9+
* Ek modüller (requirements.txt)
* **_Not : Bazı özellikler çalışmayabilir_**
#### Adımlar

1. **Projeyi İndirin:**

   - **[Zip Dosyasını İndirin](https://github.com/Berkwe/Valorant-instalocker/archive/refs/heads/main.zip)**  

   **VEYA**  

   - **Git ile Klonlayın:**
   ```
   git clone https://github.com/Berkwe/Valorant-instalocker
   cd Valorant-instalocker
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

### Ajan Seçimi ve Modlar

- **Ajan Kitleme Modu:** Ajanı kilitler, klasik instalock.
- **Sadece Seçme Modu:** Ajanı seçer fakat kitlemez. Bu şekilde maç aranırken bilgisayarda olmanıza gerek yok.

### ⏩ Kısayol Kullanımı

* Masaüstüne kısayol oluşturmak için ajan seçim ekranında E/H yazın.
* Masaüstünde ajan isminize ve kullanım modunuza göre bir kısayol belirir.

### 🚫 **Instalocker üzerinden maç bozmak :**
- Ajan kitlendikden sonra konsola e veya y yazmanız yeterlidir. Bozarsanız Instalocker tekrardan başlar, cezalar yine de verilir.

### ✂️ Ajan İsim Kısaltmaları
- Ajanların hızlı seçilebilinmesi için eklenen basit bir mekanik. artık 5 karakter üstü isimlere sahip olan ajanların isimlerini kısaltsanız bile seçebileceksiniz, fakat yazılan isim en az 4 karakter olmak zorunda. 

### Kafan mı karıştı? işte bir örnek : 


  ```text
  ✅ brim → geçerli
  ❌ reyn → geçersiz
  ```

### 🔄 Sunucu algılama

* Sunucu otomatik algılanır, manuel giriş olağanüstü durumlarda etkinleşir.(ne olduğunu anlamadıysan bak geç)

### Otomatik ajan güncellemesi:
- #### İnstalocker Artık ajan listesini otomatik olarak sürekli güncelliyor. Fakat bir insan evladı olduğumdan ben de hata yapabilirim, bu yüzden manuel olarak güncellemek gerekebilir. Böyle bir durum olursa aşşağıdaki adımları uygulayın : 
    #### - 1. adım :
    - **CMD(komut istemi) Uygulamasını açın.**
    #### - 2. adım 
    - **Aşşağıdaki kodu yapıştırın :**
    ####
      curl "https://raw.githubusercontent.com/Berkwe/Valorant-instalocker/refs/heads/main/agents.json" > %LOCALAPPDATA%\VALORANT\agents.json

---


## ⓘ Performans ve Geri Bildirim

* **Performans sorunları veya önerileriniz için** [Issues](https://github.com/Berkwe/Valorant-instalocker/issues) **sayfasını kullanabilirsiniz.**

---

## 🖤 Ayrıca Teşekkürler
- **Projeye direkt katkısı olmasada valorant apisini [dökümanlaştıran](https://github.com/techchrism/valorant-api-docs) [techchrism'e](https://github.com/techchrism) ve bu apiyi modülleştiren [colinhartigan'a](https://github.com/colinhartigan) teşekkürler.**

---

## 🌟 Diğer Projelerim

* [ADB Brute-Force](https://github.com/Berkwe/ADB-bruteforce)
* [Audio Converter](https://github.com/Berkwe/Audio-converter)

---

## 📞 İletişim

<a href="https://discord.gg/Xagnh5aYSy" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/discord.svg" alt="Berkwe" height="30" width="40" /></a>

---

## 📝 Lisans

Bu proje [MIT Lisansı](https://github.com/Berkwe/Valorant-instalocker/blob/main/LICENSE) altında lisanslanmıştır.

### 🔑 Anahtar kelimeler
valorant instalocker, valorant auto lock, valorant agent locker, valorant instalock script, valorant agent picker, valorant instalocker gui





