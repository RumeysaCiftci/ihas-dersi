#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <math.h>

Adafruit_MPU6050 mpu;

// Açı değişkenleri
float yaw = 0.0;
float pitch = 0.0;
float roll = 0.0;

// Zaman hesaplama için
unsigned long prevTime = 0;

void setup() {
  Serial.begin(115200);
  while (!Serial);

  Serial.println("MPU6050 başlatılıyor...");

  if (!mpu.begin()) {
    Serial.println("MPU6050 bulunamadı! Bağlantıyı kontrol et.");
    while (1) delay(10);
  }

  Serial.println("MPU6050 bulundu!");

  // Aralıkları ayarlayalım
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  delay(100);
  prevTime = millis();
}

void loop() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  unsigned long currentTime = millis();
  float dt = (currentTime - prevTime) / 1000.0; // saniyeye çevir
  prevTime = currentTime;

  // İvmeölçer ile pitch ve roll hesaplama (radyan → derece)
  float accPitch = atan2(a.acceleration.y, sqrt(a.acceleration.x * a.acceleration.x + a.acceleration.z * a.acceleration.z)) * 180 / PI;
  float accRoll  = atan2(-a.acceleration.x, a.acceleration.z) * 180 / PI;

  // Jiroskop verisini derece/saniye cinsine çevir
  float gyroPitchRate = g.gyro.x * 180 / PI;
  float gyroRollRate  = g.gyro.y * 180 / PI;
  float gyroYawRate   = g.gyro.z * 180 / PI;

  // Komplemanter filtre (ivme + jiroskop birleşimi)
  float alpha = 0.96; // filtre katsayısı (denge için)
  pitch = alpha * (pitch + gyroPitchRate * dt) + (1 - alpha) * accPitch;
  roll  = alpha * (roll + gyroRollRate * dt) + (1 - alpha) * accRoll;
  yaw   += gyroYawRate * dt; // sadece jiroskopla (drift yapabilir)

  // Ekrana yazdır
  Serial.print("Pitch: ");
  Serial.print(pitch, 2);
  Serial.print(" | Roll: ");
  Serial.print(roll, 2);
  Serial.print(" | Yaw: ");
  Serial.print(yaw, 2);
  Serial.print(" | Sicaklik: ");
  Serial.print(temp.temperature);
  Serial.println(" °C");

  delay(50);
}
