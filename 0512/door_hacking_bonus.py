import zipfile
import time
import itertools
import string
import multiprocessing as mp
from datetime import datetime

def check_password_chunk(args):
    """
    할당된 첫 번째 문자를 기준으로 나머지 5자리 조합을 검사하는 독립 워커 함수
    """
    start_char, zip_filepath = args
    chars = string.ascii_lowercase + string.digits
    
    try:
        z_file = zipfile.ZipFile(zip_filepath)
    except Exception:
        return None
        
    attempts = 0
    # 나머지 5자리에 대해서만 조합 생성
    for pwd_tuple in itertools.product(chars, repeat=5):
        attempts += 1
        pwd = start_char + ''.join(pwd_tuple)
        
        try:
            z_file.extractall(pwd=pwd.encode('utf-8'))
            # 정답을 찾으면 (비밀번호, 해당 워커의 시도 횟수)를 반환
            return (pwd, attempts)
        except RuntimeError as e:
            if 'Bad password' in str(e) or 'password required' in str(e):
                continue
        except Exception:
            continue
            
    return None

def unlock_zip(zip_filepath='emergency_storage_key.zip'):
    chars = string.ascii_lowercase + string.digits
    start_time = time.time()
    start_dt = datetime.now()
    
    print(f'시작 시간: {start_dt.strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'고속 해독 알고리즘(멀티프로세싱)을 가동합니다. (가용 코어 수: {mp.cpu_count()})')
    
    # 첫 번째 자리를 기준으로 36개의 분할된 작업(Task) 생성
    tasks = [(char, zip_filepath) for char in chars]
    
    password_found = None
    total_attempts = 0
    
    # CPU 코어 수만큼 프로세스 풀(Pool) 생성
    pool = mp.Pool(processes=mp.cpu_count())
    
    try:
        # imap_unordered를 사용하여 결과를 비동기적으로 빠르게 확인
        for result in pool.imap_unordered(check_password_chunk, tasks):
            if result is not None:
                password_found, chunk_attempts = result
                total_attempts = chunk_attempts
                
                # 정답을 찾았으므로 나머지 병렬 프로세스 즉각 종료
                pool.terminate()
                break
    finally:
        pool.close()
        pool.join()
        
    total_elapsed = time.time() - start_time
    
    if password_found:
        print(f'\n해독 성공! 암호: [{password_found}]')
        # 병렬 처리 특성상 전체 정확한 시도 횟수 합산은 오버헤드가 발생하므로 정답을 찾은 워커의 횟수만 출력
        print(f'해당 분할 작업에서의 반복 횟수: {total_attempts}번') 
        print(f'총 진행 시간: {total_elapsed:.2f}초')
        
        try:
            with open('password.txt', 'w', encoding='utf-8') as f:
                f.write(password_found)
            print('암호를 password.txt 파일에 저장했습니다.')
        except IOError:
            print('파일 저장 중 오류가 발생했습니다.')
    else:
        print('\n암호 해독 실패.')
        
    return password_found

if __name__ == '__main__':
    # Windows 환경에서 multiprocessing 모듈을 안전하게 실행하기 위한 필수 구문
    mp.freeze_support()
    unlock_zip()
