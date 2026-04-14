import random
import time
import json
import platform
import os
from datetime import datetime

# 시스템 정보를 가져오는 부분은 별도의 라이브러리를 사용 할 수 있다.
try:
    import psutil
except ImportError:
# 설치 되어 있지 않을 때의 예외 처리
    psutil : None

# 3주차 - DummySensor 클래스 생성
class DummySensor:      
    
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature' : 0,
            'mars_base_external_temperature' : 0,
            'mars_base_internal_humidity' : 0,
            'mars_base_external_illuminance' : 0,
            'mars_base_internal_co2' : 0,
            'mars_base_internal_oxygen' : 0
        }
        self.log_file()

    def log_file(self):
        # 파일이 없을 경우에만 데이터 헤더를 작성
        header = (
            'Timestamp, Internal_Temp, External_Temp, '
            'Humidity, Illuminance, CO2, Oxygen'
        )

        try:
            # 파일이 이미 있는지 확인
            with open('mission_log.txt', 'r', encoding='utf-8') as f:
                pass
        except FileNotFoundError:
            with open('mission_log.txt', 'w', encoding='utf-8') as f:
                f.write(header + '\n')
    
    def set_env(self):
        try:
            self.env_values['mars_base_internal_temperature'] = round(random.uniform(18, 30), 2)
            self.env_values['mars_base_external_temperature'] = round(random.uniform(0, 21), 2)
            self.env_values['mars_base_internal_humidity'] = round(random.uniform(50, 60), 2)
            self.env_values['mars_base_external_illuminance'] = round(random.uniform(500, 715), 2)
            self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 2)
            self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4, 7), 2)
        except Exception as e:
            print(f'[SENSOR ERROR] 수치 생성 실패: {e}')

    def get_env(self):
        self.set_env()
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        log_data = (
            f"{current_time}, "
            f"{self.env_values['mars_base_internal_temperature']}°C, "
            f"{self.env_values['mars_base_external_temperature']}°C, "
            f"{self.env_values['mars_base_internal_humidity']}%, "
            f"{self.env_values['mars_base_external_illuminance']} W/m2, "
            f"{self.env_values['mars_base_internal_co2']}%, "
            f"{self.env_values['mars_base_internal_oxygen']}%"
        )

        try:
            with open('mission_log.txt', 'a', encoding='utf-8') as f:
                f.write(log_data + '\n')
        except OSError as e:
            print(f'[FILE ERROR] 로그 기록 실패 (저장 장치 확인 필요): {e}')

        return self.env_values

# MissionComputer 클래스 생성
class MissionComputer:
    def __init__(self):
        # 초기화
        self.env_values = {}
        self.ds = DummySensor()
        self.history = []
        self.last_avg_time = time.time()
        self.settings = self.load_settings()

    def calculate_average(self):
        ### 5분 평균값
        try:
            if not self.history:
                print('[SYSTEM NOTICE] 계산할 누적 데이터가 없습니다.')
                return
            
            count = len(self.history)
            averages = {}

            for key in self.history[0].keys():
                # 기록 중 숫자만 골라낸 후 평균을 내서 저장
                total = sum(data[key] for data in self.history if isinstance(data[key], (int, float)))
                averages[key] = round(total / count, 2)

            print('\n' + '=' * 50)
            print(f'[REPORT] 5분간의 환경 평균 데이터 (샘플 수 : {count})')
            # Dict 데이터를 Json 형태로 변환, indent=4 : 4칸 들여쓰기, 가시성 확보
            print(json.dumps(averages, indent=4))
            print('=' * 50 + '\n')

            self.history = []

        except (ZeroDivisionError, IndexError, KeyError) as e:
            print(f'[CALC ERROR] 통계 데이터 생성 중 오류: {e}')
        except Exception as e:
            print(f'[SYSTEM ERROR] 예기치 못한 연산 오류: {e}')

    def get_sensor_data(self):
        try:
            while True:
                try:
                    # 센서의 값을 가져와서 env_value에 담기
                    data = self.ds.get_env()
                    if not data:
                        raise ValueError('센서로부터 데이터를 수신하지 못했습니다.')
                    
                    self.env_values = data
                    self.history.append(self.env_values.copy())

                    # env_values 값 json 형태로 출력
                    print(f'[{datetime.now().strftime("%H:%M:%S")}] 실시간 모니터링 중...')
                    print(json.dumps(self.env_values, indent=4))

                    if time.time() - self.last_avg_time >= 300:
                        self.calculate_average()
                        self.last_avg_time = time.time()

                except ValueError as ve:
                    print(f'[WARNING] {ve}')
                except Exception as e:
                    print(f'[RUNTIME ERROR] 루프 내 오류 발생: {e}')

                # 5초에 한번 씩 반복
                time.sleep(5)
            
        except KeyboardInterrupt:
            # Ctrl + C 눌렀을 때 실행 됨
            print('\nSystem stopped....')
        except Exception as e:
            print(f'\n[FATAL ERROR] 시스템이 치명적 오류로 중단되었습니다: {e}')

# 5주차====================================================================

    def load_settings(self):
        # 보너스과제 : setting.txt 파일을 읽어 출력할 항목 리스트 반환
        settings = []
        try:
            if os.path.exists('setting.txt'):
                with open('setting.txt', 'r', encoding='utf-8') as f:
                    for line in f:
                        item = line.strip()
                        if item:  # 빈 줄 제외
                            settings.append(item)
            else:
                print('[SYSTEM NOTICE] setting.txt 파일이 없어 모든 항목을 출력합니다.')
        except Exception as e:
            print(f'[SYSTEM ERROR] 설정 파일을 읽는 중 오류 발생: {e}')
        return settings

    def _filter_data(self, data):
        # 설정된 항목만 남기고 데이터를 필터링
        if not self.settings:
            return data
        return {k: v for k, v in data.items() if k in self.settings}
        # 딕셔너리 컴프리헨션 (Dictionary Comprehension)
        # 간결하게 딕셔너리를 생성하는 방법         
        # 키_표현식: 값_표현식 for 항목 in 반복 가능한 객체 if 조건
        # 설정 파일에 있는 키값만 포함된 새로운 딕셔너리 생성

    def get_mission_computer_info(self):
        # 미션 컴퓨터의 시스템 정보를 가져와 JSON 형식으로 출력
        try:
            if psutil is None:
                raise ImportError('psutil 라이브러리가 로드되지 않았습니다')
            
            info = {
                'operating_system' : platform.system(),
                'os_version' : platform.version(),
                'cpu_type' : platform.processor(),
                'cpu_cores' : psutil.cpu_count(logical=True),
                'memory_size' : f'{round(psutil.virtual_memory().total / (1024**3), 2)} GB'
                # psutil.cpu_count(logical=True) : 논리적 코어(쓰레드) 개수 까지 합친 CPU 코어 수
                # psutil.virtual_memory().total : 전체 메모리 용량 (기본 단위 Byte) 
                # 이를 GB 단위로 바꿈            
            }

            # 설정에 맞춰 필터링
            display_info = self._filter_data(info)

            print('\n' + '=' * 50)
            print('[SYSTEM INFO] 미션 컴퓨터 제원 정보')
            print(json.dumps(display_info, indent=4))
            # json.dumps : 딕셔너리를 JSON 문자열 형태로 변환
            print('=' * 50 + '\n')

            return display_info
        except Exception as e:
            print(f'[SYSTEM ERROR] 시스템 정보 수집 중 예기치 못한 오류 발생: {e}')
            return None

    def get_mission_computer_load(self):
        # 미션 컴퓨터의 실시간 부하 정보를 가져와 JSON으로 출력
        try:
            if psutil is None:
                raise ImportError('psutil 라이브러리가 로드되지 않았습니다.')

            load = {
                'cpu_usage_percent': f'{psutil.cpu_percent(interval=1)}%',
                'memory_usage_percent': f'{psutil.virtual_memory().percent}%'
                # psutil.cpu_percent(interval=1) : 1초 동안의 CPU 사용량
                # psutil.virtual_memory().percent : 현재 메모리 사용량
            }

            # 설정에 맞춰 필터링
            display_load = self._filter_data(load)

            print('\n' + '=' * 50)
            print('[SYSTEM LOAD] 미션 컴퓨터 실시간 리소스 부하 상태')
            print(json.dumps(display_load, indent=4))
            print('=' * 50 + '\n')

            return display_load
        except Exception as e:
            print(f'[SYSTEM ERROR] 시스템 부하 수집 중 예기치 못한 오류 발생: {e}')
            return None
            
# =======================================================================

if __name__ == '__main__':
    # MissionComputer 인스턴스 생성
    runComputer = MissionComputer()
    
    # get_sensor_data() 메소드 호출
    # RunComputer.get_sensor_data()

    # 정보 출력 확인
    runComputer.get_mission_computer_info()
    runComputer.get_mission_computer_load()
