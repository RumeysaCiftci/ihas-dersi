#include <SoftwareSerial.h>

#include <TinyGPS++.h>

 

// Define the RX and TX pins for SoftwareSerial

#define GPS_RX_PIN 4

#define GPS_TX_PIN 3

 

// Create a SoftwareSerial object to communicate with the GPS module

SoftwareSerial gpsSerial(GPS_RX_PIN, GPS_TX_PIN);

 

// Create a TinyGPS++ object to parse GPS data

TinyGPSPlus gps;

 

void setup() {

  // Start the Arduino's hardware serial for debugging

 Serial.begin(9600);

 

  // Start the SoftwareSerial for GPS communication

  gpsSerial.begin(9600);

 

  Serial.println("GPS Module Test - NEO-7M");

  Serial.println("Waiting for GPS data...");

}

 

void loop() {

  // Check if data is available from the GPS module

  while (gpsSerial.available() > 0) {

    // Feed the GPS data to the TinyGPS++ object

    if (gps.encode(gpsSerial.read())) {

      // Check if we have valid GPS data

      if (gps.location.isValid()) {

        Serial.print("Latitude: ");

        Serial.println(gps.location.lat(), 6); // Print latitude with 6 decimal places

        Serial.print("Longitude: ");

        Serial.println(gps.location.lng(), 6); // Print longitude with 6 decimal places

        Serial.print("Altitude: ");

        Serial.print(gps.altitude.meters()); // Print altitude in meters

        Serial.println(" m");

        Serial.print("Speed: ");

        Serial.print(gps.speed.kmph()); // Print speed in km/h

        Serial.println(" km/h");

        Serial.print("Satellites: ");

        Serial.println(gps.satellites.value()); // Number of satellites in view

        Serial.print("Date: ");

        printDateTime(); // Print date and time

      } else {

        Serial.println("Waiting for GPS fix...");

      }

    }

  }

 

  // If no data is received for 5 seconds, print a message

  if (millis() > 5000 && gps.charsProcessed() < 10) {

    Serial.println("No GPS data received: check wiring");

    while (true); // Halt execution

  }

 

  delay(1000); // Update every second

}

 

// Function to print date and time in a readable format

void printDateTime() {

  if (gps.date.isValid() && gps.time.isValid()) {

    // Print date (YYYY/MM/DD)

    Serial.print(gps.date.year());

    Serial.print("/");

    if (gps.date.month() < 10) Serial.print("0");

    Serial.print(gps.date.month());

    Serial.print("/");

    if (gps.date.day() < 10) Serial.print("0");

    Serial.print(gps.date.day());

    Serial.print(" ");

 

    // Print time (HH:MM:SS)

    if (gps.time.hour() < 10) Serial.print("0");

    Serial.print(gps.time.hour());

    Serial.print(":");

    if (gps.time.minute() < 10) Serial.print("0");

    Serial.print(gps.time.minute());

    Serial.print(":");

    if (gps.time.second() < 10) Serial.print("0");

    Serial.println(gps.time.second());

  } else {

    Serial.println("Invalid date/time");

  }

}