#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

void setup() {
  Serial.begin(9600);
  Wire.begin();

  Serial.println("MPU6050 baslatiliyor...");

  mpu.initialize();  // Sensörü başlat
  if (mpu.testConnection()) {
    Serial.println("MPU6050 baglantisi basarili!");
  } else {
    Serial.println("MPU6050 baglantisi basarisiz!");
    while (1); // Bağlantı yoksa durur
  }

  delay(1000);
}

void loop() {
  int16_t ax, ay, az; // ivmeölçer verileri
  int16_t gx, gy, gz; // jiroskop verileri

  // Sensörden verileri oku
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

  // Ham ivme verileri
  Serial.print("Ivme -> X: "); Serial.print(ax);
  Serial.print(" | Y: "); Serial.print(ay);
  Serial.print(" | Z: "); Serial.println(az);

  // Ham jiroskop verileri
  Serial.print("Gyro -> X: "); Serial.print(gx);
  Serial.print(" | Y: "); Serial.print(gy);
  Serial.print(" | Z: "); Serial.println(gz);

  Serial.println("-----------------------------");
  delay(500);
}
