#include <TinyGPS++.h>  // TinyGPS++ kütüphanesini dahil et

// GPS modülünün baud hızı (genellikle 9600)
static const uint32_t GPSBaud = 9600;

// TinyGPS++ nesnesi oluştur
TinyGPSPlus gps;

void setup() {
  // Bilgisayar ile iletişim
  Serial.begin(9600);
  // GPS modülü ile iletişim (Arduino Mega üzerinde Serial1)
  Serial1.begin(GPSBaud);

  Serial.println(F("=== GY-NEO6MV2 GPS Veri Okuma (Arduino Mega) ==="));
  Serial.println(F("GPS sinyali aranıyor..."));
}

void loop() {
  // GPS'ten gelen verileri TinyGPS++'a gönder
  while (Serial1.available() > 0) {
    gps.encode(Serial1.read());

    // Eğer yeni konum verisi varsa ekrana yaz
    if (gps.location.isUpdated()) {
      Serial.println(F("-----------------------------"));
      Serial.print(F("Enlem: "));
      Serial.println(gps.location.lat(), 6);

      Serial.print(F("Boylam: "));
      Serial.println(gps.location.lng(), 6);

      Serial.print(F("Uydu Sayısı: "));
      Serial.println(gps.satellites.value());

      Serial.print(F("Yükseklik: "));
      Serial.print(gps.altitude.meters());
      Serial.println(F(" m"));

      Serial.print(F("Tarih: "));
      Serial.print(gps.date.day());
      Serial.print(F("/"));
      Serial.print(gps.date.month());
      Serial.print(F("/"));
      Serial.println(gps.date.year());

      Serial.print(F("Saat (UTC): "));
      Serial.print(gps.time.hour());
      Serial.print(F(":"));
      Serial.print(gps.time.minute());
      Serial.print(F(":"));
      Serial.println(gps.time.second());
      Serial.println(F("-----------------------------\n"));
    }
  }
}
