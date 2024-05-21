#include <SoftwareSerial.h>
#include <Wire.h>
#include <Servo.h> // 서보모터 라이브러리 추가

#define DEBUG
#define IRSENSOR1_PIN 2 // 적외선 센서 핀
#define IRSENSOR2_PIN 3
#define IRSENSOR3_PIN 4
#define IRSENSOR4_PIN 5

#define MOTOR1_PIN 7
#define MOTOR2_PIN 8
#define MOTOR3_PIN 9

#define ARR_CNT 5
#define CMD_SIZE 60

char sendBuf[CMD_SIZE];
char recvId[10] = "SQL"; // SQL 저장 클라이언트 ID

bool Flag = false;
SoftwareSerial BTSerial(10, 11); 

// 상승, 하강엣지 탐지를 위한 previous, currnet value 변수 지정
int previousIrValue1 = 0;
int currentIrValue1 = 0;
int previousIrValue2 = 0;
int currentIrValue2 = 0;
int previousIrValue3 = 0;
int currentIrValue3 = 0;
int previousIrValue4 = 0;
int currentIrValue4 = 0;

int doorstate = 0;


Servo myServo1; // 서보모터 객체 생성

void setup() {
#ifdef DEBUG

  Serial.begin(115200);
  Serial.println("setup() start!");

#endif

  pinMode(IRSENSOR1_PIN, INPUT);
  pinMode(IRSENSOR2_PIN, INPUT);
  pinMode(IRSENSOR3_PIN, INPUT);
  pinMode(IRSENSOR4_PIN, INPUT);

  pinMode(MOTOR1_PIN, OUTPUT);
  pinMode(MOTOR2_PIN, OUTPUT);
  pinMode(MOTOR3_PIN, OUTPUT);

  
  digitalWrite(MOTOR1_PIN, LOW);
  digitalWrite(MOTOR2_PIN, LOW);
  digitalWrite(MOTOR3_PIN, LOW);

  BTSerial.begin(9600); // 블루투스 시리얼 통신 설정

  myServo1.attach(12); // 서보모터 핀 설정
  myServo1.write(0); 

}

void loop() {
  if (BTSerial.available())
    bluetoothEvent();

  previousIrValue1 = currentIrValue1; 
  previousIrValue2 = currentIrValue2;
  previousIrValue3 = currentIrValue3;
  previousIrValue4 = currentIrValue4;

  currentIrValue1 = digitalRead(IRSENSOR1_PIN); 
  currentIrValue2 = digitalRead(IRSENSOR2_PIN); 
  currentIrValue3 = digitalRead(IRSENSOR3_PIN); 
  currentIrValue4 = digitalRead(IRSENSOR4_PIN); 

  if (Flag) {

    // 각 적외선 센서의 출력값의 상승, 하강엣지를 감지해 모터를 제어

    if (digitalRead(IRSENSOR1_PIN) == LOW) {
      digitalWrite(MOTOR1_PIN, LOW);
    } else {
      digitalWrite(MOTOR1_PIN, HIGH);
    }

    if (digitalRead(IRSENSOR2_PIN) == LOW) {
      digitalWrite(MOTOR2_PIN, LOW);
    } else {
      digitalWrite(MOTOR2_PIN, HIGH);
    }

    if (digitalRead(IRSENSOR3_PIN) == LOW) {
      digitalWrite(MOTOR3_PIN, LOW);
    } else {
      digitalWrite(MOTOR3_PIN, HIGH);
    }

    if (digitalRead(IRSENSOR4_PIN) == HIGH) {
      myServo1.write(0);
    } else {
      myServo1.write(110);
    }

  }

  // 적외선 센서의 출력값에 따른 해당 모터의 기본 상태를 설정
  
  if (previousIrValue1 == LOW && currentIrValue1 == HIGH) { 
    digitalWrite(MOTOR1_PIN, LOW); 
  }

  if (previousIrValue2 == LOW && currentIrValue2 == HIGH) {
    digitalWrite(MOTOR2_PIN, LOW); 
  }

  if (previousIrValue3 == LOW && currentIrValue3 == HIGH) {
    digitalWrite(MOTOR3_PIN, LOW); 
  }

  if (doorstate == 1 && previousIrValue4 == HIGH && currentIrValue4 == LOW) {
     delay(7000); 
     doorstate = 1; 
   }
   
   
  if (doorstate == 1 && previousIrValue4 == LOW && currentIrValue4 == HIGH) {
    delay(7000); 
    doorstate = 0; 
    myServo1.write(0);
  }

#ifdef DEBUG
  if (Serial.available())
    BTSerial.write(Serial.read());
#endif
}

//블루투스 모듈을 통한 명령어 송신, 선택된 모터 제어
void bluetoothEvent() { 
  int i = 0;
  char *pToken;
  char *pArray[ARR_CNT] = {0};
  char recvBuf[CMD_SIZE] = {0};
  int len = BTSerial.readBytesUntil('\n', recvBuf, sizeof(recvBuf) - 1);

#ifdef DEBUG
  Serial.print("Recv : ");
  Serial.println(recvBuf);
#endif

  pToken = strtok(recvBuf, "[@]");
  while (pToken != NULL) {
    pArray[i] = pToken;
    if (++i >= ARR_CNT)
      break;
    pToken = strtok(NULL, "[@]");
  }

  // 디버그를 위한 off 명령어 추가

 if (!strcmp(pArray[1], "MOTOR1")) { // 모터1 제어 명령
    if (!strcmp(pArray[2], "ON")) {
      digitalWrite(MOTOR1_PIN, HIGH);
    } else if (!strcmp(pArray[2], "OFF")) {
      digitalWrite(MOTOR1_PIN, LOW);
    }
    sprintf(sendBuf, "[%s]%s@%s\n", pArray[0], pArray[1], pArray[2]);
  } else if (!strcmp(pArray[1], "MOTOR2")) { // 모터2 제어 명령
    if (!strcmp(pArray[2], "ON")) {
      digitalWrite(MOTOR2_PIN, HIGH);
    } else if (!strcmp(pArray[2], "OFF")) {
      digitalWrite(MOTOR2_PIN, LOW);
    }
    sprintf(sendBuf, "[%s]%s@%s\n", pArray[0], pArray[1], pArray[2]);
  } else if (!strcmp(pArray[1], "MOTOR3")) { // 모터3 제어 명령
    if (!strcmp(pArray[2], "ON")) {
      digitalWrite(MOTOR3_PIN, HIGH);
    } else if (!strcmp(pArray[2], "OFF")) {
      digitalWrite(MOTOR3_PIN, LOW);
    }
    sprintf(sendBuf, "[%s]%s@%s\n", pArray[0], pArray[1], pArray[2]);
  } else if (!strcmp(pArray[1], "SERVO")) { // 서보모터 제어 명령
    if (!strcmp(pArray[2], "ON")) {
      doorstate = 1;
      myServo1.write(110); // 110도 회전
    } 
    else if (!strcmp(pArray[2], "OFF")) { 
      doorstate = 0;
      myServo1.write(0); // 원위치로 회전
    }
    sprintf(sendBuf, "[%s]%s@%s\n", pArray[0], pArray[1], pArray[2]);
  }

#ifdef DEBUG
  Serial.print("Send : ");
  Serial.print(sendBuf);
#endif
  BTSerial.write(sendBuf);
}