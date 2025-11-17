#include <AESLib.h>

AESLib aesLib;

// ---- AES-256 KEY (Base64 → 32 Byte HEX) ----
// fz5PQLfxzU6La2JxyFnSsyXwT+BTStrSZx30BK1RUMA=
byte aes_key[32] = {
  0x7F,0x3E,0x4F,0x40,0xB7,0xF1,0xCD,0x4E,
  0x8B,0x6B,0x62,0x71,0xC8,0x59,0xD2,0xB3,
  0x25,0xF0,0x4F,0xE0,0x53,0x4A,0xDA,0xD2,
  0x67,0x1D,0xF4,0x04,0xAD,0x51,0x50,0xC0
};

// ---- CBC IV (16 Byte) ----
byte aes_iv[16] = {
  0xA1, 0xB2, 0xC3, 0xD4,
  0xE5, 0xF6, 0xA7, 0xB8,
  0xC9, 0xDA, 0xEB, 0xFC,
  0x1A, 0x2B, 0x3C, 0x4D
};

String plaintext = "Hello-World?";


void printHex(byte *buf, int len) {
  for (int i = 0; i < len; i++) {
    if (buf[i] < 16) Serial.print("0");
    Serial.print(buf[i], HEX);
  }
  Serial.println();
}


void setup() {
  Serial.begin(9600);
  delay(1000);

  Serial.println("AES-256-CBC Encrypt + Decrypt");

  // ----- PLAINTEXT -----
  int plaintextLen = plaintext.length() + 1;
  char plainBuf[plaintextLen];
  plaintext.toCharArray(plainBuf, plaintextLen);

  // ----- ENCRYPT -----
  byte encrypted[128];

  byte iv_enc[16];
  memcpy(iv_enc, aes_iv, 16);

  int cipherLen = aesLib.encrypt(
                    (byte*)plainBuf,
                    plaintextLen,
                    encrypted,
                    aes_key,
                    256,        // AES-256
                    iv_enc
                  );

  Serial.print("Encrypted (HEX): ");
  printHex(encrypted, cipherLen);

  // ----- DECRYPT -----
  byte decrypted[128];

  byte iv_dec[16];
  memcpy(iv_dec, aes_iv, 16);   // decrypt için IV resetlenmeli

  int decryptedLen = aesLib.decrypt(
                       encrypted,
                       cipherLen,
                       decrypted,
                       aes_key,
                       256,
                       iv_dec
                     );

  Serial.print("Decrypted Text: ");
  Serial.println((char*)decrypted);
}


void loop() {

}
