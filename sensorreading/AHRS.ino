#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_HMC5883_U.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_AHRS.h> // Madgwick veya Mahony filtreleri burada

Adafruit_MPU6050 mpu;
Adafruit_HMC5883_Unified mag = Adafruit_HMC5883_Unified(12345);

// Madgwick algoritmasını başlatalım
Adafruit_Madgwick filter;

// Filtre frekansı (örnekleme hızı)
float sampleFreq = 50.0f; // 50 Hz

void setup() {
  Serial.begin(115200);
  while (!Serial);

  Serial.println("MPU6050 + HMC5883L (Adafruit AHRS) başlatılıyor...");

  if (!mpu.begin()) {
    Serial.println("MPU6050 bulunamadı!");
    while (1);
  }

  if (!mag.begin()) {
    Serial.println("HMC5883L bulunamadı! (GY-271 modülünü kontrol et)");
    while (1);
  }

  // MPU6050 ayarları
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  // Filtreyi başlat
  filter.begin(sampleFreq);

  Serial.println("Sensörler hazır!");
  delay(100);
}

void loop() {
  sensors_event_t accel, gyro, temp;
  sensors_event_t magEvent;

  mpu.getEvent(&accel, &gyro, &temp);
  mag.getEvent(&magEvent);

  // Zaman adımı
  static unsigned long lastUpdate = 0;
  unsigned long now = millis();
  float dt = (now - lastUpdate) / 1000.0;
  lastUpdate = now;

  // Madgwick algoritmasını güncelle (gyro rad/s, accel m/s², mag µT)
  filter.update(gyro.gyro.x, gyro.gyro.y, gyro.gyro.z,
                accel.acceleration.x, accel.acceleration.y, accel.acceleration.z,
                magEvent.magnetic.x, magEvent.magnetic.y, magEvent.magnetic.z);

  // Euler açılarını (yaw, pitch, roll) al
  float roll  = filter.getRoll();
  float pitch = filter.getPitch();
  float yaw   = filter.getYaw();

  // Ekrana yazdır
  Serial.print("Pitch: ");
  Serial.print(pitch, 2);
  Serial.print("° | Roll: ");
  Serial.print(roll, 2);
  Serial.print("° | Yaw: ");
  Serial.print(yaw, 2);
  Serial.print("° | Sicaklik: ");
  Serial.print(temp.temperature);
  Serial.println(" °C");

  delay(20); // 50 Hz frekans için 20 ms gecikme
}
