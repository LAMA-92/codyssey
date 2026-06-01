import csv
import os
from datetime import datetime

import pyaudio
import speech_recognition as sr
import wave

class VoiceRecorder:
    def __init__(self):
        # 녹음 설정 및 초기화
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.record_folder = 'records'
        
        # STT 음성 인식기 초기화
        self.recognizer = sr.Recognizer()

        # records 폴더가 없으면 생성
        if not os.path.exists(self.record_folder):
            os.makedirs(self.record_folder)

    def record_audio(self, duration=5):
        audio = pyaudio.PyAudio()
        
        stream = audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )

        print('녹음을 시작합니다...')
        frames = []

        for _ in range(0, int(self.rate / self.chunk * duration)):
            data = stream.read(self.chunk)
            frames.append(data)

        print('녹음이 완료되었습니다.')

        stream.stop_stream()
        stream.close()
        audio.terminate()

        # 파일명 생성: 년월일-시간분초
        now = datetime.now()
        file_name = now.strftime('%Y%m%d-%H%M%S') + '.wav'
        file_path = os.path.join(self.record_folder, file_name)

        wf = wave.open(file_path, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(audio.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()

        print('저장 완료: ' + file_path)
        return file_path

    def speech_to_text(self, file_path):
        # 음성 파일에서 텍스트를 추출하고 CSV로 기록하는 함수
        # [수행과제 2] 음성파일을 가져오면 음성 파일에서 텍스트를 추출하는 STT(Speech to Text) 기능을 구현하고 음성이 텍스트로 잘 인식되는지 확인
        if not os.path.exists(file_path):
            print('지정된 음성 파일이 존재하지 않습니다.')
            return

        print('음성 분석 중: ' + os.path.basename(file_path))
        
        # [수행과제 4] 파일의 이름은 음성 파일의 이름과 같은 이름으로 저장하되 확장자는 .CSV로 저장한다.
        csv_file_path = os.path.splitext(file_path)[0] + '.csv'
        current_timestamp = datetime.now().strftime('%H:%M:%S')

        with sr.AudioFile(file_path) as source:
            audio_data = self.recognizer.record(source)
            try:
                text = self.recognizer.recognize_google(audio_data, language='ko-KR')
                print('인식 결과: ' + text)
            except sr.UnknownValueError:
                print('음성을 인식하지 못했습니다.')
                text = '[인식 불가]'
            except sr.RequestError:
                print('STT 서비스에 접근할 수 없습니다.')
                text = '[에러 발생]'

        # 추출된 텍스트를 요구 조건에 맞는 CSV 파일로 저장
        # [수행과제 3] STT로 구현된 텍스트 인식 정보를 다음과 같은 CSV 파일로 저장한다
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            # 파일 포맷: 음성 파일내에서의 시간, 인식된 텍스트
            writer.writerow([current_timestamp, text])
            
        print('CSV 변환 완료: ' + csv_file_path)

    def process_all_records(self):
        # records 폴더 안의 모든 .wav 파일을 찾아 STT 작업을 수행
        # [수행과제 1] 문제 7에서 녹음된 음성파일들의 목록을 불러온다
        if not os.path.exists(self.record_folder):
            print('녹음 폴더가 존재하지 않습니다.')
            return

        files = os.listdir(self.record_folder)
        wav_files = [f for f in files if f.endswith('.wav')]

        if not wav_files:
            print('처리할 음성 파일이 없습니다.')
            return

        for wav_file in wav_files:
            full_path = os.path.join(self.record_folder, wav_file)
            csv_path = os.path.splitext(full_path)[0] + '.csv'
            
            # 이미 변환된 CSV가 없다면 STT 처리를 실행합니다.
            if not os.path.exists(csv_path):
                self.speech_to_text(full_path)

    def search_keyword_in_records(self, keyword):
        # 특정 키워드가 포함된 CSV 기록 검색 함수
        # [보너스 과제] 특정 키워드를 입력하면 저장된 CSV 파일 안에서 내용을 찾아서 출력해 준다.
        if not os.path.exists(self.record_folder):
            print('기록 폴더가 존재하지 않습니다.')
            return

        print('\n[키워드 \'' + keyword + '\' 검색 결과]')
        files = os.listdir(self.record_folder)
        csv_files = [f for f in files if f.endswith('.csv')]
        found = False

        for file in csv_files:
            full_path = os.path.join(self.record_folder, file)
            with open(full_path, 'r', encoding='utf-8') as csv_file:
                reader = csv.reader(csv_file)
                for row in reader:
                    if len(row) >= 2 and keyword in row[1]:
                        print('파일: ' + file + ' | 시간: ' + row[0] + ' | 내용: ' + row[1])
                        found = True

        if not found:
            print('\'' + keyword + '\'가 포함된 기록을 찾지 못했습니다.')


if __name__ == '__main__':
    recorder = VoiceRecorder()
    
    # 1. 테스트용 녹음 진행 및 파일 경로 획득
    new_file = recorder.record_audio(5)
    
    # 2. 방금 녹음한 파일 또는 폴더 내 모든 미처리 파일 STT 변환 및 CSV 저장
    recorder.process_all_records()
    
    # 특정 단어 포함 문장 검색 시뮬레이션
    recorder.search_keyword_in_records('테스트')