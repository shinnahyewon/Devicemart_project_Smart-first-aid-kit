'''
Microphone Client : 음성인식 기술 처리
작성일 : 2024.03.30
'''
import speech_recognition as sr
import socket
import threading
import sys
import time
import re
import pygame

pygame.init()

HOST = "10.10.14.70"
PORT = 5000
ADDR = (HOST,PORT)

recvId = "MIC"
recvFlag = False
rsplit = []
lock=threading.Lock()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class SoundManager:
    def __init__(self):
        self.current_sound = None

    def play_sound(self, file_path):
        try:
            if self.current_sound is not None:
                self.current_sound.stop()
            self.current_sound = pygame.mixer.Sound(file_path)
            self.current_sound.play()
        except FileNotFoundError:
            print(f"File not found: {file_path}. Skipping sound playback.")

# 사운드 매니저 인스턴스 생성
sound_manager = SoundManager()

# 음성 인식기 및 마이크 초기화
recognizer = sr.Recognizer()

intro_sound_path = '인트로.wav'
retry_sound_path = '다시.wav'

sound_to_words_mapping = {
    '화상.wav': ['데었', '화상', '뜨거워', '뜨겁'],
    '베임.wav': ['출혈', '피', '베었', '찔렸'],
    '벌레.wav': ['물렸', '가렵', '모기'],
    '두통.wav': ['두통', '머리', '열', '어지러워', '어지럼증'],
    '감기.wav': ['감기', '기침', '콧물', '몸살', '목', '재채기', '칼칼']
}


try:
	s.connect((HOST, PORT)) 
	def sendingMsg(): 
		s.send('[MIC:PASSWD]'.encode()) 
		time.sleep(0.5)
		while True: 
			data = input() 
			data = bytes(data+'\n', "utf-8") 
			s.send(data) 
			s.close() 
	def gettingMsg(): 
		global rsplit
		global recvFlag
		while True: 
			data = s.recv(1024) 
			rstr = data.decode("utf-8")
			rsplit = re.split('[\]|\[@]|\n',rstr)  #'[',']','@' 분리
			recvFlag = True

		s.close() 
	threading._start_new_thread(sendingMsg,()) 
	threading._start_new_thread(gettingMsg,()) 
except Exception as e:
	print('%s:%s'%ADDR)
	sys.exit()
print('connect is success')
ledFlag = False


def find_sound_path(text):
    for sound_path, keywords in sound_to_words_mapping.items():
        if any(keyword in text for keyword in keywords):
            return sound_path
    return None

# 음성 입력 처리 함수
def process_speech_input():
    with sr.Microphone() as source:
        print("주변 소음 조정 중...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("아파!를 말하면 음성 인식이 시작됩니다.")

        while True:
            try:
                print("듣고 있습니다...\n")
                audio_data = recognizer.listen(source, timeout=10, phrase_time_limit=5)
                text = recognizer.recognize_google(audio_data, language='ko-KR')
                print(f"인식된 명령: {text}")
  
                # 특정 키워드에 따른 명령 전송
                if "열어" in text :
                    s.send(b'[BT]SERVO@ON\n')
                    print("문이 열렸습니다.\n")
                elif "닫아" in text:
                    s.send(b'[BT]SERVO@OFF\n')
                    print("문이 닫혔습니다.\n")


                if "아파" in text:
                    sound_manager.play_sound(intro_sound_path)
                    print("추가 명령을 말하세요.\n")

                    # 추가 명령 대기
                    audio_data = recognizer.listen(source, timeout=10, phrase_time_limit=5)
                    text = recognizer.recognize_google(audio_data, language='ko-KR')
                    print(f"인식된 추가 명령: {text}")

                    sound_path = find_sound_path(text)

                    if sound_path:
                        sound_manager.play_sound(sound_path)
                        print(f"재생: {sound_path}")

                        # 특정 키워드에 따른 명령 전송
                        if any(keyword in text for keyword in ['두통', '머리', '열', '어지러워', '어지럼증']):
                            s.send(b'[BT]MOTOR3@ON\n')
                            print("motor3 work\n")
                        elif any(keyword in text for keyword in ['데었', '화상', '뜨거워', '뜨겁']):
                            s.send(b'[BT]MOTOR1@ON\n')
                            print("motor1 work\n")
                            s.send(b'[BT]MOTOR2@ON\n')
                            print("motor2 work\n")
                        elif any(keyword in text for keyword in ['물렸', '가렵', '모기']):
                            s.send(b'[BT]SERVO@ON\n')
                            print("servo work\n")
                        elif any(keyword in text for keyword in ['출혈', '피', '베었', '찔렸']):
                            s.send(b'[BT]MOTOR1@ON\n') 
                            print("motor1 work\n")

                    else:
                        sound_manager.play_sound(retry_sound_path)
                        print("알아듣지 못했습니다. 다시 말해주세요.\n")

                    

            except sr.UnknownValueError:
                print("불분명한 음성입니다. 다시 말해주세요.\n")
            except sr.WaitTimeoutError:
                print("시간 초과입니다. 다시 시도해주세요.\n")
            except sr.RequestError as e:
                print(f"음성 인식 서비스 요청 중 문제 발생: {e}")


threading.Thread(target=process_speech_input).start()

while True:
    time.sleep(1)
