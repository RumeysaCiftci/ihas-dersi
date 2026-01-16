import serial
import time
import struct
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# --- 1. Arduino Ayarları (Arduino Koduyla Eşleşmeli) ---
SERIAL_PORT = 'COM8'  # Lütfen burayı kendi alıcı cihazınızın (915MHz modülün bağlı olduğu) portu ile değiştirin
BAUD_RATE = 57600
START_BYTE = 0xAA
AES_KEY_SIZE = 16  # 16 byte = 128 bit
BLOCK_SIZE = 16    # AES blok boyutu

# --- 2. Şifreleme Parametreleri (Arduino Koduyla BİREBİR AYNI olmalı!) ---
KEY = bytes([
    0x2B, 0x7E, 0x15, 0x16, 0x28, 0xAE, 0xD2, 0xA6,
    0xAB, 0xF7, 0x15, 0x88, 0x09, 0xCF, 0x4F, 0x3C
])
IV = bytes([
    0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
    0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F
])

# --- 3. Veri Yapısı Tanımı (MPUData) ---
# Arduino'daki struct MpuData'nın Python karşılığı
# 6 adet float (her biri 4 bayt) = 24 bayt
# Format: < (Little-endian), f (float)
MPU_STRUCT_FORMAT = '<6f'
MPU_DATA_LENGTH = struct.calcsize(MPU_STRUCT_FORMAT) # 24 byte

def decrypt_cbc_data(cipher_text: bytes, key: bytes, iv: bytes) -> bytes:
    """AES-128 CBC ile şifre çözer ve PKCS#7 dolgusunu kaldırır."""
    try:
        # CBC modunda AES şifreleyici oluştur
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        # Şifreyi çöz
        decrypted_padded_data = cipher.decrypt(cipher_text)
        
        # PKCS#7 dolgusunu kaldır (Arduino'daki pkcs7_padding ile uyumlu)
        # unpad fonksiyonu dolguyu otomatik olarak temizler.
        plain_data = unpad(decrypted_padded_data, BLOCK_SIZE, 'pkcs7')
        
        return plain_data
    except ValueError as e:
        print(f"Şifre Çözme/Dolgu Hatası: {e}. Anahtar/IV/Dolgu uyumsuz olabilir.")
        return b''
    except Exception as e:
        print(f"Beklenmedik Şifre Çözme Hatası: {e}")
        return b''

def unpack_mpu_data(binary_data: bytes):
    """24 baytlık ikili veriyi MPUData yapısına (6 float) dönüştürür."""
    if len(binary_data) != MPU_DATA_LENGTH:
        print(f"Hata: Çözülecek veri boyutu yanlış. Beklenen: {MPU_DATA_LENGTH}, Gelen: {len(binary_data)}")
        return None
        
    try:
        # <6f formatına göre baytları 6 float değere çöz
        unpacked = struct.unpack(MPU_STRUCT_FORMAT, binary_data)
        
        data = {
            'AccelX': unpacked[0],
            'AccelY': unpacked[1],
            'AccelZ': unpacked[2],
            'GyroX': unpacked[3],
            'GyroY': unpacked[4],
            'GyroZ': unpacked[5]
        }
        return data
    except struct.error as e:
        print(f"Veri Çözme Hatası: {e}")
        return None

def read_arduino_stream():
    """Seri portu dinler, Arduino paketlerini ayrıştırır ve işler."""
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=5)
        print(f"Seri Port {SERIAL_PORT} {BAUD_RATE} baud hızında açıldı. Dinleniyor...")
        time.sleep(2)
        
        while True:
            # 1. Başlangıç baytını ara (Paket Senkronizasyonu)
            if ser.in_waiting > 0:
                # Tek bir bayt oku ve START_BYTE olup olmadığını kontrol et
                byte_read = ser.read(1)
                
                if not byte_read: # Timeout oluşursa atla
                    continue
                    
                if ord(byte_read) == START_BYTE:
                    
                    # 2. Başlık okuma (Bayrak ve Boyut)
                    header = ser.read(2) # [1 Byte Bayrak] + [1 Byte Veri Boyutu]
                    
                    if len(header) == 2:
                        encryption_flag = header[0]
                        data_size = header[1]
                        
                        # 3. Veri bloğunu oku (Şifreli veya Şifresiz)
                        data_payload = ser.read(data_size)
                        
                        if len(data_payload) == data_size:
                            
                            processed_data = b''
                            
                            if encryption_flag == 1:
                                # Şifreli veri (Dolgu dahil boyutu data_size)
                                print("\n[ŞİFRELİ PAKET] Alınıyor...")
                                # CBC şifre çözme ve dolgu kaldırma
                                processed_data = decrypt_cbc_data(data_payload, KEY, IV)
                                
                            else:
                                # Şifresiz veri (Ham boyutu data_size)
                                print("\n[ŞİFRESİZ PAKET] Alınıyor...")
                                processed_data = data_payload
                            
                            # 4. Çözülmüş (Decrypted) veya Ham veriyi MPU yapısına dönüştür
                            unpacked_mpu = unpack_mpu_data(processed_data)
                            
                            if unpacked_mpu:
                                print("--> Durum: BAŞARILI. Veri Yapısı Çözüldü:")
                                print(f"    Accel X/Y/Z: {unpacked_mpu['AccelX']:.4f}, {unpacked_mpu['AccelY']:.4f}, {unpacked_mpu['AccelZ']:.4f}")
                                print(f"    Gyro X/Y/Z:  {unpacked_mpu['GyroX']:.4f}, {unpacked_mpu['GyroY']:.4f}, {unpacked_mpu['GyroZ']:.4f}")
                            else:
                                print(f"--> Durum: HATA. Veri çözme başarısız (Boyut/Format). Ham Veri Boyutu: {len(processed_data)}")
                        
                        else:
                            print(f"Hata: Eksik veri bloğu alındı. Beklenen: {data_size}, Gelen: {len(data_payload)}")
                    else:
                        print("Hata: Başlık tam okunamadı.")
                
            time.sleep(0.005) # Kısa bekleme

    except serial.SerialException as e:
        print(f"\n[KRİTİK HATA] Seri Port Hatası: {e}")
        print(f"Lütfen {SERIAL_PORT} portunun takılı ve boşta olduğundan emin olun.")
    
    except KeyboardInterrupt:
        print("\nProgram kullanıcı tarafından sonlandırıldı.")
    
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Seri Port kapatıldı.")

if __name__ == "__main__":
    read_arduino_stream()