2024 ICT 융합프로젝트 공모전 최우수상작
Devicemart_project_Smart-first-aid-kit

수행기간 : 2024.02.24.~2024.03.31

담당역할 : 
- (아두이노 모듈 제어) 영상처리 결과에 맞는 명령어를 수신 받아 IR 센서를 이용하여 레일 모터 제어와 서보 모터 제어
- 라즈베리파이 서버와 소켓 통신을 통해 아두이노에서 수신된 값에 따라 제어 시스템 활성화
- 상처 모델링 작업

수행목표 :
- 상처 인식 AI 컴퓨터 비전 영상처리
- 음성 인식 및 대처 방법 출력
- 컴퓨터 비전과 음성 인식 기술을 활용한 응급 처치 및 시간 단축
- 특정 명령을 통한 약품함 개폐 시스템

사용 기술 : C, C++, Python, 아두이노, 라즈베리파이, 젯슨나노, Ubuntu, Yolo, OpenCV, TCP/IP, GUI 

세부수행내용 :

■ 프로젝트 개요
1) 개발 배경
  스마트 구급상자는 기존 구급상자를 재설계하여 사용자가 필요한 상황에 맞는 항목을 신속하고 정확하게 찾고 제공받을 수 있도록 하였다. 구급상자라는 단순한 보관 도구를 넘어서는 것을 목표로 구현하였으며 사용자에게 다양한 의료 지원을 제공하고 사람들의 건강과 안전을 효과적으로 보호하는 방안을 마련하였다.

2) 개발 목표
 스마트 구급상자는 실시간 영상 인식 및 음성 인식 기술을 활용하여 사용자의 의료적 필요를 정확히 파악하고 적시에 맞춤형 의료 지원을 제공하는 구급상자이다. 이 작품의 주요 목표는 즉각적인 의료 지원을 제공받을 수 없는 상황에서 의료 서비스에 대한 접근성을 향상하는 것이다. 사용자가 상처를 입었을 때, 상처 식별을 위한 영상 인식과 음성 인식 기술을 통합해 상처의 종류를 영상으로 판단하거나, 사용자의 음성 지시를 통해 필요한 의료용품을 자동으로 제공한다.

■ 시스템 구성
 1) 전체 시스템 구성

![image](https://github.com/shinnahyewon/Devicemart_project_Smart-first-aid-kit/assets/161293023/03433d0b-b716-4c60-86d3-a88406efb447)

  2)세부 시스템 구성
 1. Raspberry pi (Server, Master)

![image](https://github.com/shinnahyewon/Devicemart_project_Smart-first-aid-kit/assets/161293023/ab672dbc-66f9-4170-8a40-d16203520094)

클라이언트 간의 데이터 송수신을 위해 서버 소켓을 생성한다. 클라이언트가 접속하기 전까지 대기 상태를 유지하다가 클라이언트로부터 연결 요청이 들어오면 서버는 연결을 수락한다. 이 부분에서 보안을 위해 idpasswd.txt 파일을 만들어 인증된 클라이언트만 접속할 수 있도록 하였다. 인증된 클라이언트는 메시지를 서버에 전송할 수 있으므로 클라이언트 간의 송수신을 통해 다양한 접속기기로 Arduino를 제어하도록 했다.

2. Jetson Nano (Client)

![image](https://github.com/shinnahyewon/Devicemart_project_Smart-first-aid-kit/assets/161293023/2bfa7c9e-a592-48a9-8f7a-64554801135e)

Jetson Nano는 머신 러닝을 이용해 객체를 감지하는 역할을 담당한다. 웹캠으로 객체를 인식하고 인식된 결과를 문자열로 값을 바꾸어 Raspberry Pi Server와의 소켓 통신을 통해 문자열 값을 Arduino에 송신한다. 송신된 결괏값을 받으면 Arduino 제어가 가능하게 했다.

3.Raspberry Pi (Client)

![image](https://github.com/shinnahyewon/Devicemart_project_Smart-first-aid-kit/assets/161293023/e422e80c-1254-4c46-a2fe-4f93997fa704)

Raspberry Pi에 마이크와 스피커를 연결하여 핫 워드를 인식시키면 Raspberry Pi Server와의 소켓 통신을 통해 문자열 값을 Arduino에 송신한다. 송신된 결괏값을 받으면 Arduino 제어가 가능하게 했다.

4.Arduino (Slave)

![image](https://github.com/shinnahyewon/Devicemart_project_Smart-first-aid-kit/assets/161293023/5fe85b8e-5755-4156-bdc4-e594b6c71eae)

Raspberry Pi Server와의 소켓 통신을 통해 Arduino에 데이터를 송신하면 Arduino에 수신된 값에 따라 설정된 제어시스템이 활성화된다. 만약 수신된 정보가 문 열림을 필요로 한다면 시스템은 먼저 적외선 센서로 약품의 존재 여부를 감지한다. 감지 되는 경우 서보모터가 작동하여 문을 열고 약품을 꺼낸 후 다시 넣으면 센서가 이를 감지하고 7초 뒤에 문을 자동으로 닫는다. 만약 수신된 데이터가 레일 작업을 요구한다면, 해당 작업은 레일 모터 시스템으로 전달된다. 이때, 레일 모터는 특정 조합에 따라 작동하여 물체를 이동시킨다. 만약 레일이 작동하여 물체가 아래로 떨어져 적외선센서에 물체가 인식되지 않으면 레일이 정지하게 된다.

■ 주 시스템
1) Raspberry Pi Server
 Raspberry Pi Server는 음성을 인식하는 Raspberry Pi 모듈과 영상을 인식하는 Jetson Nano 모듈로부터 클라이언트 연결을 받아들여 명령어를 수신하는 중추적 역할을 한다. 이와 동시에, Arduino와의 통신에서는 마스터-슬레이브 관계를 형성하여 스마트 구급상자의 모터 제어를 담당한다. Arduino는 블루투스를 통해 Raspberry Pi로부터 명령어를 수신한다.
2) Ai Modeling
 스마트 구급상자에 쓰인 ai 모델은 주변에서 흔히 볼 수 있는 상처를 인식하도록 생성했다. 모델은 Roboflow를 이용하여 약 7300장의 상처 이미지 데이터를 수집하고 라벨링을 시행했다. 모델 유형은 실시간 상처 인식을 위해 객체 감지 유형으로 선택했다. 구현한 모델은 베임, 화상, 벌레 물림 상처를 구분하여 인식한다. 본 프로젝트에서는 Ultralytics YOLOv8을 이용하여 모델링을 진행하였다. 데이터 클래스는 bites, burns, cuts 세 개의 클래스로 구성했다. 데이터 셋 버전을 생성한 뒤 트레이닝을 위해 데이터 셋 형식을 다운 받아 코랩에서 학습 시켰다. 학습의 정확도를 높이기 위해 Epoch는 100으로 지정하고 batch 사이즈는 일반적으로 많이 사용하는 16으로 지정하였다.

![image](https://github.com/shinnahyewon/Devicemart_project_Smart-first-aid-kit/assets/161293023/d59f2a46-0b7e-497b-9212-d753982eea40)
<Training Graphs>
Training Graphs를 보면 50에서 100 사이의 Loss 값이 안정되는 것을 볼 수 있다.

![image](https://github.com/shinnahyewon/Devicemart_project_Smart-first-aid-kit/assets/161293023/04a7f42f-0d54-4af1-999b-87b300ae31f0)
<Roboflow에서 제공하는 상처 인식 데이터셋의 Training Graphs>

![image](https://github.com/shinnahyewon/Devicemart_project_Smart-first-aid-kit/assets/161293023/09136449-abfa-4488-a1e9-e1f082039a86)
<학습된 모델의 train_batch0.jpg 이미지>

머신러닝은 batch=16의 크기만큼 데이터를 활용해 모델의 예측값과 실제 정답 간의 오차를 계산하여 파라미터를 업데이트한다. 학습 후 생성된 best.pt 파일로 모델을 생성했다.

3. Jetson Nano 영상처리

   ![image](https://github.com/shinnahyewon/Devicemart_project_Smart-first-aid-kit/assets/161293023/01c3c7e0-9931-47b9-9488-c904cb32d601)
<실행 초기화면 GUI>

 스마트 구급상자는 실시간 상처 인식 기능을 통해 상처에 적합한 약품을 자동으로 제공한다. 이를 위해 NVIDIA에서 개발한 Jetson Nano 단일 보드 AI 키트를 사용했다. 상처 인식 과정에서는 카메라와 마우스가 입력 장치로 사용된다. 카메라는 사용자의 상처를 실시간으로 캡처하여 LCD 화면을 통해 GUI와 함께 보여준다. 사용자는 마우스를 사용하여 LCD의 GUI 버튼을 조작할 수 있다.

  진단 버튼을 누르면 Jetson Nano는 연결된 Raspberry Pi 서버로 모터 구동 명령어를 전송한다. 이 명령어는 Raspberry Pi를 통해 Arduino에 연결되며, Arduino는 명령에 따라 모터를 구동하여 적절한 약품을 스마트 구급상자에서 출력하도록 한다. 이 과정을 통해 사용자는 자신의 상처에 가장 적합한 치료를 신속하게 받을 수 있다.

![image](https://github.com/shinnahyewon/Devicemart_project_Smart-first-aid-kit/assets/161293023/0463f625-0f2b-4753-a484-368561dbadeb)

4. Raspberry Pi 음성인식 처리

![image](https://github.com/shinnahyewon/Devicemart_project_Smart-first-aid-kit/assets/161293023/cb726322-0a23-4a3d-b386-3c7f22418f06)

음성 인식용 Raspberry Pi 보드는 사용자의 증상에 따른 해결책과 약품 제공을 위해 음성 인식 기술을 활용한다. 사용자가 ‘아파’라는 핫워드를 통해 증상을 말하면, 모듈은 증상을 인식하고 해당 정보를 바탕으로 Arduino에 명령어를 전송합니다. 이 명령에 따라, 스피커는 증상에 맞는 해결책을 포함한 음성 파일을 재생하며, 스마트 구급상자는 필요한 약품을 제공한다.

5. Arduino 모듈 제어
  영상처리 결과에 맞는 명령어를 Arduino 보드에서 블루투스 모듈로 받고, 이 명령어로 선택된 모터가 구동되고, IR 센서를 통해 감지된 물체의 상태 변화를 통해 모터 구동 제어를 하는 것을 Arduino 개발의 시나리오로 설정했다. 

  우선 블루투스 모듈을 통해 MOTOR1@ON, MOTOR2@ON, MOTOR3@ON, SERVO@ON 명령어를 받고, 그에 맞는 모터를 구동하는 기능을 bluetoothEvent 함수로 구현하였다. 레일과 연결된 서보형 DC모터는 디지털 출력을 HIGH로 설정해 위에 올려진 물건을 나오는 방향으로 옮기도록 하였고, 여닫이문에 연결된 일반 서보모터는 110°만큼 회전해 문이 열리도록 설정했다.

![image](https://github.com/shinnahyewon/Devicemart_project_Smart-first-aid-kit/assets/161293023/723b157b-1029-4b47-9fce-2da67d1078fa)

이후의 모터 구동은 레일과 여닫이문 두 가지 경우로 나누어 IR 센서의 출력값을 통해 제어한다. 레일의 이동 방향 끝에 달린 IR 센서의 출력값이 변하면 서보형 DC모터가 구동을 멈춘다. 레일 위에는 여러 개의 약품이 간격을 둔 상태로 올려져 있으며, 한 개의 약품만을 떨어뜨릴 것이다.

![image](https://github.com/shinnahyewon/Devicemart_project_Smart-first-aid-kit/assets/161293023/6b5e092d-ec54-4510-af25-5da9ff1337d7)

여닫이문은 레일과는 반대로 수납공간에 위치한 IR 센서의 출력값이 1->0->1로 변하면 110° 회전(명령어를 받고 문이 열려있는 상태)해 있던 서보모터가 다시 원위치(문이 닫혀있는 상태)로 돌아오도록 구성하였다. 

  여닫이문의 기본값은 IR 센서값이 1이면 서보모터가 원위치에 있고, 0인 순간에는 서보모터가 110°에 위치한 상태를 기본으로 설정했다. 문이 닫혀있는 상태에는 안의 물건을 꺼낼 수 없고, 문이 열려있는 상태에서만 물건을 빼고 다시 수납하는 것이 가능하다. 또한 약품을 다시 수납하고 바로 문이 닫히지 않도록(손 끼임 방지) 7초의 delay를 추가했다.

■ 기대 목표
- 응급조치
  위급상황 시 음성으로 신속한 응급 요청과 응급구조가 오기 전의 최소한의 응급처치로 상황이 악화함을 방지하여 상황 호전을 기대할 수 있다.
- 공공장소 및 직장 등에서의 의료지원
  자연재해나 긴급 상황 시에 필요한 의약품을 먼저 제공하는 기능을 추가해 공공장소, 직장 등의 장소에서 활용함으로써 사회적인 기여를 기대할 수 있다.
- 개인화된 의료서비스
  병원이나 클리닉의 헬스케어 시스템과 연동하여 처방받은 약을 자동으로 제공하거나, 사용자의 건강 상태에 맞는 맞춤형 정보를 제공하는 방향으로 발전시킬 수 있다.
- 사용자의 의료 서비스 접근성 향상
  시각 장애가 있는 사용자나 의료 지식이 부족한 사용자도 음성 명령을 통해 쉽게 구급상자를 사용할 수 있다.



