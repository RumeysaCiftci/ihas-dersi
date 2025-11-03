#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_HMC5883_U.h>
#include <Adafruit_Sensor.h>
#include <math.h>

Adafruit_MPU6050 mpu;
Adafruit_HMC5883_Unified mag = Adafruit_HMC5883_Unified(12345);

float pitch = 0.0;
float roll = 0.0;
float yaw = 0.0;

unsigned long prevTime = 0;

void setup() {
  Serial.begin(115200);
  while (!Serial);

  Serial.println("MPU6050 + HMC5883L başlatılıyor...");

  if (!mpu.begin()) {
    Serial.println("MPU6050 bulunamadı! Bağlantıyı kontrol et.");
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

  delay(100);
  prevTime = millis();
}

void loop() {
  sensors_event_t a, g, temp;
  sensors_event_t event;

  mpu.getEvent(&a, &g, &temp);
  mag.getEvent(&event);

  unsigned long currentTime = millis();
  float dt = (currentTime - prevTime) / 1000.0;
  prevTime = currentTime;

  // 🔹 1. Pitch & Roll (ivmeölçer)
  float accPitch = atan2(a.acceleration.y, sqrt(a.acceleration.x * a.acceleration.x + a.acceleration.z * a.acceleration.z)) * 180 / PI;
  float accRoll  = atan2(-a.acceleration.x, a.acceleration.z) * 180 / PI;

  // 🔹 2. Jiroskop (deg/s)
  float gyroPitchRate = g.gyro.x * 180 / PI;
  float gyroRollRate  = g.gyro.y * 180 / PI;

  // 🔹 3. Komplemanter filtre ile Pitch & Roll füzyonu
  float alpha = 0.96;
  pitch = alpha * (pitch + gyroPitchRate * dt) + (1 - alpha) * accPitch;
  roll  = alpha * (roll + gyroRollRate * dt) + (1 - alpha) * accRoll;

  // 🔹 4. Manyetometre (GY-271) ile Yaw hesaplama
  float magX = event.magnetic.x;
  float magY = event.magnetic.y;
  float magZ = event.magnetic.z;

  // Pitch & Roll etkisini düzelt (tilt compensation)
  float magX_comp = magX * cos(pitch * PI / 180) + magZ * sin(pitch * PI / 180);
  float magY_comp = magX * sin(roll * PI / 180) * sin(pitch * PI / 180) + magY * cos(roll * PI / 180) - magZ * sin(roll * PI / 180) * cos(pitch * PI / 180);

  float heading = atan2(magY_comp, magX_comp);
  if (heading < 0)
    heading += 2 * PI;

  yaw = heading * 180 / PI;

  // 🔹 5. Verileri yazdır
  Serial.print("Pitch: ");
  Serial.print(pitch, 2);
  Serial.print("° | Roll: ");
  Serial.print(roll, 2);
  Serial.print("° | Yaw: ");
  Serial.print(yaw, 2);
  Serial.print("° | Sicaklik: ");
  Serial.print(temp.temperature);
  Serial.println(" °C");

  delay(100);
}
