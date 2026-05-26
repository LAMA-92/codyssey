import os
import wave
import warnings
from datetime import datetime

# [수행과제 2] 시스템의 마이크를 인식하고 음성을 녹음하는 부분은 외부 라이브러리를 사용하는 것이 가능하다.
import pyaudio

# 불필요한 시스템 경고 메시지 출력을 방지합니다.
warnings.filterwarnings('ignore')

class VoiceRecorder:
    def __init__(self):
        # 녹음 설정 및 초기화
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.record_folder = 'records'

        # chunk            한 번에 읽을 오디오 프레임 수
        # format           데이터 타입
        # channels         오디오 채널 수
        # rate             초당 샘플 수
        # record_folder    저장될 폴더 이름

        # records 폴더가 없으면 생성합니다.
        if not os.path.exists(self.record_folder):
            os.makedirs(self.record_folder)

    # [수행과제 1] 시스템의 마이크를 인식하고 음성을 녹음하는 부분을 완성한다.
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

        # 지정된 시간(초) 만큼 마이크 입력을 읽어옵니다.
        for _ in range(0, int(self.rate / self.chunk * duration)):
            data = stream.read(self.chunk)
            frames.append(data)

        print('녹음이 완료되었습니다.')

        # 스트림을 종료하고 리소스를 반환합니다.
        stream.stop_stream()
        stream.close()
        audio.terminate()

        # 파일명 생성: 년월일-시간분초
        # [수행과제 4] 파일의 이름은 녹음 날짜와 시간을 참조해서 ‘년월일-시간분초’와 같은 형태로 저장한다.
        now = datetime.now()
        file_name = now.strftime('%Y%m%d-%H%M%S') + '.wav'
        file_path = os.path.join(self.record_folder, file_name)

        # wave 모듈을 사용하여 wav 파일로 저장합니다.
        wf = wave.open(file_path, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(audio.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()

        # [수행과제 3] 파일들은 파이썬 앱이 실행되고 있는 하위에 records 폴더에 모두 저장된다
        print('저장 완료: ' + file_path)

    # [보너스 과제] 특정 범위의 날짜의 녹음 파일을 보여주는 기능을 추가한다.
    def show_records_by_date(self, start_date_str, end_date_str):
        if not os.path.exists(self.record_folder):
            print('녹음 폴더가 존재하지 않습니다.')
            return

        try:
            start_date = datetime.strptime(start_date_str, '%Y%m%d')
            end_date = datetime.strptime(end_date_str, '%Y%m%d')
        except ValueError:
            print('날짜 형식이 잘못되었습니다. YYYYMMDD 형태로 입력해주세요.')
            return

        print(start_date_str + ' 부터 ' + end_date_str + ' 까지의 파일 목록:')
        
        files = os.listdir(self.record_folder)
        found = False
        
        for file in files:
            if file.endswith('.wav'):
                date_part = file.split('-')[0]
                try:
                    file_date = datetime.strptime(date_part, '%Y%m%d')
                    if start_date <= file_date <= end_date:
                        print('- ' + file)
                        found = True
                except ValueError:
                    continue
                    
        if not found:
            print('해당 기간에 기록된 녹음 파일이 없습니다.')


if __name__ == '__main__':
    recorder = VoiceRecorder()
    
    # 5초간 음성을 녹음합니다.
    recorder.record_audio(5)
    
    # 보너스 기능 테스트 (예시: 2026년 5월 전체 기록 확인)
    print('\n[기록 검색 테스트]')
    recorder.show_records_by_date('20260501', '20260531')