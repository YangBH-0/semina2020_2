#include <SoftwareSerial.h>
#include "DHT.h"
#define DHTPIN 2     // 디지털 2번핀 사용
#define DHTTYPE DHT11   // DHT 11 모델사용 
DHT dht(DHTPIN, DHTTYPE);
int cds=0;
String arduino_num = "01";

SoftwareSerial BTSerial(4,5); //  Rx, Tx

void setup() {  
  Serial.begin(9600); // 시리얼 모니터
  BTSerial.begin(9600); // 블루투스 시리얼 개방
  dht.begin();
}

void loop() {
  int h = dht.readHumidity(); // 습도 측정
  int t = dht.readTemperature(); // 섭씨 온도 측정
  cds = analogRead(A0);

  //블루투스 시리얼 출력
  BTSerial.print(arduino_num);
  BTSerial.print(":");
  BTSerial.print(h);
  BTSerial.print(" ");
  BTSerial.print(t);
  BTSerial.print(" ");
  BTSerial.print(cds);
  BTSerial.print("!");

  // 시리얼 모니터 출력
  Serial.print(arduino_num);
  Serial.print(":");
  Serial.print(h);
  Serial.print(" ");
  Serial.print(t);
  Serial.print(" ");
  Serial.print(cds);
  Serial.println();
  
  delay(5000);  
}
