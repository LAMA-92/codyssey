import zipfile
import time
import itertools
import string
from datetime import datetime

def unlock_zip(zip_filepath='emergency_storage_key.zip'):
    
    # [수행과제 2] 단 암호는 특수 문자 없이 숫자와 소문자 알파벳으로 구성된다.
    # string 모듈의 ascii_lowercase와 digits 상수를 병합하여 탐색할 문자열 풀 생성
    chars = string.ascii_lowercase + string.digits
    
    # [수행과제 4 - 파트 A] 암호를 푸는 과정을 출력하는데 시작 시간을 출력한다.
    # datetime.now()로 현재 시각 포맷팅 및 time.time()으로 소요 시간 측정을 위한 기준점 기록
    start_time = time.time()
    start_dt = datetime.now()
    print(f'시작 시간: {start_dt.strftime("%Y-%m-%d %H:%M:%S")}')
    print('암호 해독을 시작합니다...\n')
    
    try:
        zip_file = zipfile.ZipFile(zip_filepath)
    except FileNotFoundError:
        print(f'오류: {zip_filepath} 파일을 찾을 수 없습니다.')
        return None
    except zipfile.BadZipFile:
        print(f'오류: 파일이 손상되었습니다.')
        return None
        
    attempts = 0
    password_found = None
    
    # [수행과제 1 & 2] zip 파일의 암호를 풀 수 있는 코드를 작성한다. (6자리 문자)
    # itertools.product()를 사용해 chars의 중복 순열(데카르트 곱)을 생성하여 6자리 모든 경우의 수 탐색
    for pwd_tuple in itertools.product(chars, repeat=6):
        attempts += 1
        pwd = ''.join(pwd_tuple)
        
        # [수행과제 4 - 파트 B] 반복 횟수 그리고 진행 시간 등을 출력한다.
        # 모듈로 연산(%)을 이용해 100만 회마다 time.time()을 재측정하여 경과 시간과 횟수 출력 (I/O 병목 방지)
        if attempts % 1000000 == 0:
            current_elapsed = time.time() - start_time
            print(f'진행 중... 반복 횟수: {attempts}번, 진행 시간: {current_elapsed:.2f}초')
            
        try:
            # zipfile.extractall() : 비밀번호가 맞는지 검증. 문자열을 바이트로 변환하여 압축 해제 시도
            # 파이썬 문자열을 바이트 객체로 변환하기 위해 .encode('utf-8') 사용
            zip_file.extractall(pwd=pwd.encode('utf-8'))
            password_found = pwd
            break
        except RuntimeError as e:
            # 비밀번호가 틀렸을 때 발생하는 에러를 캐치하고 계속 진행
            if 'Bad password' in str(e) or 'password required' in str(e):
                continue
        except Exception:
            continue

    zip_file.close()
    
    # 해독 종료 후 최종 결과 요약 출력
    if password_found:
        total_elapsed = time.time() - start_time
        print(f'\n해독 성공! 암호: [{password_found}]')
        print(f'총 반복 횟수: {attempts}번')
        print(f'총 진행 시간: {total_elapsed:.2f}초')
        
        # [수행과제 5] 암호를 푸는 데 성공하면 암호는 password.txt로 저장한다.
        # with open() 컨텍스트 매니저를 사용하여 파일 스트림을 안전하게 열고 쓰기('w') 모드로 저장
        try:
            with open('password.txt', 'w', encoding='utf-8') as f:
                f.write(password_found)
            print('암호를 password.txt 파일에 저장했습니다.')
        except IOError:
            print('파일 저장 중 오류가 발생했습니다.')
    else:
        print('\n암호 해독 실패.')
        
    return password_found

# [수행과제 6] 암호를 풀 수 있는 전체 코드는 door_hacking.py로 저장한다.
# 위 코드를 door_hacking.py 파일로 저장한 뒤 아래 조건문으로 스크립트 실행
if __name__ == '__main__':
    unlock_zip()
