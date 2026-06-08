"""
Description:
    제공된 화성 날씨 CSV 데이터(mars_weathers_data.csv)를 파싱하여 
    로컬 MySQL 데이터베이스의 `mars_weather` 테이블에 적재(Insert)하는 스크립트.

Requirements Compliance:
    - [수행과제] Python 기본 제공 모듈(csv) 및 외부 라이브러리(pymysql) 사용
    - [수행과제] CSV 파싱 및 INSERT 쿼리 반복 실행
    - [보너스과제] MySQLHelper 클래스를 통한 데이터베이스 로직 캡슐화
"""

import csv
import pymysql
import getpass


class MySQLHelper:
    """
    [보너스 과제] MySQLHelper 클래스를 만들어서 데이터베이스 연결 및 쿼리 등을 쉽게 할 수 있게 구성한다.
     
    데이터베이스 연결 및 쿼리 실행을 전담하는 Helper 클래스.
    """

    def __init__(self, host, user, password, database):
        """클래스 인스턴스화 시 DB 접속 정보 초기화 (생성자)"""
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        """
        MySQL 서버 접속 메서드.
        - pymysql.connect()를 활용하여 세션 객체를 생성하고 저장함.
        """
        self.connection = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            charset='utf8'
        )

    def execute_insert(self, query, params=None):
        """
        INSERT 쿼리 실행 메서드.
        - Context Manager (with 문)를 사용하여 cursor 객체의 안전한 반환을 보장함.
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
        # 트랜잭션 확정 (실제 DB에 데이터 쓰기)
        self.connection.commit()

    def close(self):
        """자원 누수를 막기 위한 DB 세션 종료 메서드"""
        if self.connection:
            self.connection.close()


def read_csv_and_insert(file_path, db_helper):
    """
    [수행 과제] CSV 파일을 읽어 MySQL에 적재하는 메인 비즈니스 로직.
    
    Args:
        file_path (str): 읽어들일 CSV 파일의 상대 경로
        db_helper (MySQLHelper): 쿼리를 실행할 DB 헬퍼 인스턴스
    """
    insert_query = 'INSERT INTO mars_weather (mars_date, temp, storm) VALUES (%s, %s, %s)'
    
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_data = csv.reader(file)
        next(csv_data)  # 첫 번째 행(Header) 스킵
        
        for row in csv_data:
            # CSV 구조(인덱스)에 맞춰 데이터 매핑
            mars_date = row[1]
            
            # [Data Cleansing & Type Casting]
            # 원본 데이터의 소수점(float)을 처리
            # int()와 float()를 체이닝하여 타입 변환 예외 처리
            temp = int(float(row[2]))
            storm = int(float(row[3]))
            
            # 헬퍼 클래스를 호출하여 한 줄씩 데이터 INSERT (반복 실행 요구사항 충족)
            db_helper.execute_insert(insert_query, (mars_date, temp, storm))


def main():
    """
    스크립트 진입점 (Entry Point).
    실행 흐름: DB 접속 정보 획득 -> 연결 -> 데이터 적재 -> 연결 종료
    """
    host = 'localhost'
    user = 'root'
    
    # 보안 강화를 위해 콘솔에서 비밀번호를 마스킹하여 입력받음 (getpass 내장 모듈)
    password = getpass.getpass('MySQL root 계정 비밀번호를 입력하세요: ')
    database = 'mars_db'
    
    # 1. 헬퍼 객체 생성 및 연결
    db_helper = MySQLHelper(host, user, password, database)
    db_helper.connect()
    
    # 2. 데이터 적재 로직 실행
    file_path = 'mars_weathers_data.csv'
    read_csv_and_insert(file_path, db_helper)
    
    # 3. 자원 해제
    db_helper.close()
    
    print('데이터 입력이 완료되었습니다.')

if __name__ == '__main__':
    main()