#include <SoftwareSerial.h>
#include <TinyGPS++.h>


SoftwareSerial gpsSerial(3,4); 
TinyGPSPlus gps;

void setup() {
  Serial.begin(9600);      // Bilgisayar ile iletişim
  gpsSerial.begin(9600);   // NEO-7M varsayılan baud rate: 9600

  Serial.println(F("GPS Başlatılıyor..."));
  Serial.println(F("Enlem, Boylam, Saat, Uydu Sayısı"));
}

void loop() {
  while (gpsSerial.available() > 0) {
    if (gps.encode(gpsSerial.read())) {
      if (gps.location.isValid()) {
        Serial.print(F("Enlem: "));
        Serial.print(gps.location.lat(), 6);
        Serial.print(F(" | Boylam: "));
        Serial.print(gps.location.lng(), 6);
      } else {
        Serial.print(F("Konum: BULUNAMADI"));
      }

      Serial.print(F(" | Saat: "));
      if (gps.time.isValid()) {
        if (gps.time.hour() < 10) Serial.print(F("0"));
        Serial.print(gps.time.hour());
        Serial.print(F(":"));
        if (gps.time.minute() < 10) Serial.print(F("0"));
        Serial.print(gps.time.minute());
        Serial.print(F(":"));
        if (gps.time.second() < 10) Serial.print(F("0"));
        Serial.print(gps.time.second());
      } else {
        Serial.print(F("GEÇERSİZ"));
      }

      Serial.print(F(" | Uydular: "));
      Serial.println(gps.satellites.value());

      delay(1000); // 1 saniyede bir güncelle
    }
  }

  // GPS verisi gelmiyorsa uyarı
  if (millis() > 5000 && gps.charsProcessed() < 10) {
    Serial.println(F("GPS sinyali alınamıyor! Bağlantıyı kontrol et."));
  }
}