#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_HMC5883_U.h>
#include <Adafruit_Sensor.h>
#include "Kalman.h"  // Kristian Lauszus kütüphanesi

Adafruit_MPU6050 mpu;
Adafruit_HMC5883_Unified mag = Adafruit_HMC5883_Unified(12345);

// Her eksen için Kalman filtreleri
Kalman kalmanX;
Kalman kalmanY;
Kalman kalmanZ;

float accX, accY, accZ;
float gyroX, gyroY, gyroZ;
float magX, magY, magZ;

float roll, pitch, yaw;
float gyroXangle, gyroYangle;
float compAngleX, compAngleY;
float kalAngleX, kalAngleY;

unsigned long timer;

void setup() {
  Serial.begin(115200);
  Wire.begin();

  if (!mpu.begin()) {
    Serial.println("MPU6050 bulunamadı!");
    while (1);
  }

  if (!mag.begin()) {
    Serial.println("HMC5883L bulunamadı!");
    while (1);
  }

  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  sensors_event_t accel, gyro, temp;
  mpu.getEvent(&accel, &gyro, &temp);

  accX = accel.acceleration.x;
  accY = accel.acceleration.y;
  accZ = accel.acceleration.z;

  roll  = atan2(accY, accZ) * RAD_TO_DEG;
  pitch = atan(-accX / sqrt(accY * accY + accZ * accZ)) * RAD_TO_DEG;

  kalmanX.setAngle(roll);
  kalmanY.setAngle(pitch);
  timer = micros();

  Serial.println("Kalman IMU başlatıldı!");
  delay(100);
}

void loop() {
  sensors_event_t accel, gyro, temp;
  sensors_event_t magEvent;

  mpu.getEvent(&accel, &gyro, &temp);
  mag.getEvent(&magEvent);

  // Zaman adımı (dt)
  double dt = (double)(micros() - timer) / 1000000;
  timer = micros();

  // Ham sensör verileri
  accX = accel.acceleration.x;
  accY = accel.acceleration.y;
  accZ = accel.acceleration.z;

  gyroX = gyro.gyro.x * RAD_TO_DEG;
  gyroY = gyro.gyro.y * RAD_TO_DEG;
  gyroZ = gyro.gyro.z * RAD_TO_DEG;

  magX = magEvent.magnetic.x;
  magY = magEvent.magnetic.y;
  magZ = magEvent.magnetic.z;

  // Pitch ve Roll hesapla (ivmeden)
  double rollAcc  = atan2(accY, accZ) * RAD_TO_DEG;
  double pitchAcc = atan(-accX / sqrt(accY * accY + accZ * accZ)) * RAD_TO_DEG;

  // Kalman filtreleriyle açıları güncelle
  kalAngleX = kalmanX.getAngle(rollAcc, gyroX, dt);
  kalAngleY = kalmanY.getAngle(pitchAcc, gyroY, dt);

  // Manyetometre ile Yaw hesapla (pusula yönü)
  double heading = atan2(magY, magX) * RAD_TO_DEG;
  if (heading < 0) heading += 360;
  yaw = heading;

  Serial.print("Roll: ");
  Serial.print(kalAngleX, 2);
  Serial.print(" | Pitch: ");
  Serial.print(kalAngleY, 2);
  Serial.print(" | Yaw: ");
  Serial.print(yaw, 2);
  Serial.print(" | Temp: ");
  Serial.print(temp.temperature);
  Serial.println(" °C");

  delay(20); // ~50Hz
}
