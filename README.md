# PhotoMod

![PhotoMod Logo](https://wearetheartmakers.com/us/images/2024/08/19/photomodLOGO.png)

**PhotoMod**, Raspberry Pi 4B üzerinde çalışan bir fotoğraf kabini (photobooth) uygulamasıdır. Bu uygulama ile kullanıcılar, çeşitli fotoğraf seçeneklerinden birini seçip fotoğraf çekebilir ve bu fotoğrafları yazdırabilirler. Uygulama, Flask, Pygame ve Pillow gibi kütüphaneler kullanılarak geliştirilmiştir ve fotoğraf işleme, ses efektleri gibi özellikleri destekler.

## Gereksinimler

- Raspberry Pi 4B (diğer modeller de desteklenir)
- 7 inç DSI LCD 800x480 Kapasitif Dokunmatik Ekran
- Raspberry Pi Kamera (libcamera destekli)
- Python 3
- Flask
- Pygame
- Pillow
- libcamera
- CUPS (yazıcı desteği için)


## Kurulum

### 1. Gerekli Kütüphaneleri Yükleme

Gerekli Python kütüphanelerini yüklemek için aşağıdaki komutu çalıştırın:

bash 
pip install -r requirements.txt

### 2. CUPS Kurulumu

CUPS yazıcı hizmetini yükleyin ve yapılandırın:

bash
sudo apt-get install cups
sudo usermod -aG lpadmin pi
sudo systemctl restart cups

### 3. Raspberry Pi Kamera Ayarları

Raspberry Pi üzerindeki kamerayı etkinleştirmek için `raspi-config` aracını kullanın. Kamera modülünü etkinleştirdikten sonra, `picamera2` kütüphanesini kullanarak fotoğraf çekimi sağlayabilirsiniz. Bunun için:

bash
sudo raspi-config

### 5. Uygulamayı Başlatma

Flask uygulamasını başlatmak için aşağıdaki komutu kullanın:

bash
python3 app.py

### 6. Otomatik Başlatma Ayarı

PhotoMod uygulamasını Raspberry Pi açılışında otomatik olarak çalışacak şekilde ayarlamak için, aşağıdaki adımları izleyin:

bash
sudo nano /etc/systemd/system/photomod.service

[Unit]
Description=PhotoMod Flask Uygulaması
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/photomod/app.py
WorkingDirectory=/home/pi/photomod
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi
Environment=FLASK_ENV=production

[Install]
WantedBy=multi-user.target

Daha sonra, hizmeti etkinleştirin ve başlatın:

bash
Kodu kopyala
sudo systemctl enable photomod.service
sudo systemctl start photomod.service


![ARAYUZ ](https://wearetheartmakers.com/us/images/2024/08/19/photomod.jpg)

## Kullanım

Raspberry Pi açıldığında, uygulama otomatik olarak başlar ve bir arayüz sunar. 

- Kullanıcı, tek veya dört fotoğraf seçeneğinden birini seçer.
- Seçilen fotoğraf sayısına göre fotoğraf çekimi yapılır ve birleştirilmiş bir fotoğraf oluşturulur.
- Çekilen fotoğraf, yazıcıya gönderilerek basılır.

### Özellikler

- **Kullanıcı dostu arayüz:** Fotoğraf seçeneklerini kolayca seçin ve fotoğraflarınızı çekin.
- **Ses efektleri:** Fotoğraf çekimi sırasında sesli geri bildirim alın.
- **Fotoğraf baskısı:** Çekilen fotoğrafları kolayca yazdırın.
- **Fotoğraf birleştirme:** Birden fazla fotoğrafı tek bir görüntüde birleştirin.

### Sorun Giderme

Eğer ekran veya kamera çalışmıyorsa, Raspberry Pi OS üzerinde gerekli ayarların yapıldığından emin olun ve `config.txt` dosyasını kontrol edin. CUPS üzerinden yazıcı bağlantılarınızı kontrol edin ve yazıcının doğru şekilde tanımlandığından emin olun.

## Katkıda Bulunma

Bu projeye katkıda bulunmak isterseniz, lütfen bir pull request gönderin veya bir sorun bildirimi açın.
