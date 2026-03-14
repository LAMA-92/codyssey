def log_analyze(file_path):
    error_word = 'explosion'
    problem_log = 'problem_logs.txt'

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # 출력 결과를 시간의 역순으로 정렬해서 출력한다.
        for line in reversed(lines):
            print(line.rstrip())
        
        # 출력 결과 중 문제가 되는 부분만 따로 파일로 저장한다.
        problem_lines = []
        for line in lines:
            if error_word in line.lower():
                problem_lines.append(line)

        if problem_lines:
            with open(problem_log, 'w', encoding='utf-8') as out_file:
                out_file.writelines(problem_lines)
        else:
            print('로그 내에서 폭발 관련 기록을 찾을 수 없습니다.')
        
    except FileNotFoundError:
        print(f"오류 : '{file_path}' 파일을 찾을 수 없습니다.")
    except Exception as e:
        print('시스템 분석 중 예기치 못한 오류 발생 : {e}')

if __name__ == '__main__':
    print('Hello Mars')
    log = 'mission_computer_main.log'
    log_analyze(log)