import random
from datetime import datetime

#DummySensor 클래스 생성
class DummySensor:      
    
    # 객체의 초기값 설정
    # __init__ : 인스턴스를 생성 시 자동으로 호출, 초기화 작업 수행
    # self : 클래스를 정의 할 때 첫 매개변수로 사용되는 변수 (파이선에서 권장하는 관례)
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature' : 0,
            'mars_base_external_temperature' : 0,
            'mars_base_internal_humidity' : 0,
            'mars_base_external_illuminance' : 0,
            'mars_base_internal_co2' : 0,
            'mars_base_interanl_oxygen' : 0
        }

    # 제시된 범위 내에서 랜덤하게 환경 값을 생성하여 저장
    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = random.randint(18, 30)
        self.env_values['mars_base_external_temperature'] = random.randint(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.randint(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.randint(500, 715)
        # 이산화탄소 농도 (0.02~0.1) 이므로 소수점 둘 째자리 까지 표현
        # random.uniform : 주어진 범위 내에서 실수 난수 반환
        # round : 소수점 자리에 맞춰 반올림
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 2)
        self.env_values['mars_base_internal_oxygen'] = random.randint(4, 7)

    # env_values 반환
    # 보너스과제 : 출력할 내용을 날짜와 시간, env_values 와 같이 log를 남기는 부분 추가
    def get_env(self):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 로그 문자열 구성
        log_data = (
            f"{current_time}, "
            f"{self.env_values['mars_base_internal_temperature']}°C, "
            f"{self.env_values['mars_base_external_temperature']}°C, "
            f"{self.env_values['mars_base_internal_humidity']}%, "
            f"{self.env_values['mars_base_external_illuminance']} W/m2, "
            f"{self.env_values['mars_base_internal_co2']}%, "
            f"{self.env_values['mars_base_internal_oxygen']}%"
        )

        # mission_log.txt 파일에 기록
        with open('mission_log.txt', 'a', encoding='utf-8') as f:
            f.write(log_data + '\n')

        return self.env_values
    
if __name__ == '__main__':
    # DummySensor 인스턴스 생성
    ds = DummySensor()

    # 환경 값 설정 (set_env 호출)
    ds.set_env()

    # 환경 값 읽기 및 출력 (get_env 호출)
    current_env = ds.get_env()
    
    print('--- 화성 기지 환경 모니터링 시스템 ---')
    for key, value in current_env.items():
        print(f'{key}: {value}')
    print('------------------------------------')
    print('시스템 메시지: 환경 데이터가 mission_log.txt에 기록되었습니다.')

    
