#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_MPU6050.h>

Adafruit_MPU6050 mpu;

void setup() {
  Serial.begin(115200);
  while (!Serial)
    delay(10); // Seri bağlantı açılana kadar bekle

  Serial.println("MPU6050 başlatılıyor...");

  if (!mpu.begin()) {
    Serial.println("MPU6050 bulunamadı! Bağlantıyı kontrol et.");
    while (1) {
      delay(10);
    }
  }
  Serial.println("MPU6050 bulundu!");

  // Sensör aralıklarını ayarla (isteğe bağlı)
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  delay(100);
}

void loop() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  Serial.print("Ivme (m/s^2): X=");
  Serial.print(a.acceleration.x);
  Serial.print(" | Y=");
  Serial.print(a.acceleration.y);
  Serial.print(" | Z=");
  Serial.print(a.acceleration.z);

  Serial.print(" || Jiroskop (rad/s): X=");
  Serial.print(g.gyro.x);
  Serial.print(" | Y=");
  Serial.print(g.gyro.y);
  Serial.print(" | Z=");
  Serial.print(g.gyro.z);

  Serial.print(" || Sicaklik: ");
  Serial.print(temp.temperature);
  Serial.println(" °C");

  delay(500);
}
