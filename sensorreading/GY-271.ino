#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_HMC5883_U.h>

Adafruit_HMC5883_Unified mag = Adafruit_HMC5883_Unified(12345);

void setup(void) {
  Serial.begin(115200);
  Serial.println("HMC5883L başlatılıyor...");

  if(!mag.begin()) {
    Serial.println("HMC5883L bulunamadı! Bağlantıyı kontrol et.");
    while(1);
  }
}

void loop(void) {
  sensors_event_t event; 
  mag.getEvent(&event);

  // Manyetik alan değerleri (mikroTesla)
  float x = event.magnetic.x;
  float y = event.magnetic.y;
  float z = event.magnetic.z;

  // Yön (heading) hesabı - derece cinsinden
  float heading = atan2(y, x);
  if(heading < 0)
    heading += 2 * PI;

  float headingDegrees = heading * 180 / PI;

  Serial.print("X: "); Serial.print(x);
  Serial.print("  Y: "); Serial.print(y);
  Serial.print("  Z: "); Serial.print(z);
  Serial.print("  | Yaw (Heading): ");
  Serial.print(headingDegrees);
  Serial.println("°");

  delay(500);
}
