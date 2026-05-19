# [수행과제 2] 카이사르의 암호를 풀 수 있는 함수를 caesar_cipher_decode() 라는 이름으로 만든다.
def caesar_cipher_decode(target_text):
    # 보너스 과제: 텍스트 사전 구성
    dictionary = ['mars', 'base', 'emergency', 'door', 'open', 'system']
    
    # 자리수(shift)를 1부터 25까지(알파벳 수만큼) 변경하며 반복
    # [수행과제 4] caesar_cipher_decode() 에서 자리수에 따라 암호표가 바뀌게 한다. 자리수는 알파벳 수만큼 반복한다.
    for shift in range(1, 26):
        decoded_text = ''
        
        for char in target_text:
            if 'a' <= char <= 'z':
                shifted = ord(char) - shift
                if shifted < ord('a'):
                    shifted += 26
                decoded_text += chr(shifted)
            elif 'A' <= char <= 'Z':
                shifted = ord(char) - shift
                if shifted < ord('A'):
                    shifted += 26
                decoded_text += chr(shifted)
            else:
                # 알파벳 이외의 문자(공백, 기호 등)는 그대로 둠
                decoded_text += char
                
        # [수행과제 5] 자리수에 따라서 해독된 결과를 출력한다.
        print(f'Shift {shift:2d}: {decoded_text}')
        
        # 보너스 과제: 사전에 있는 단어와 일치하는 키워드 발견 시 반복 중단
        lower_decoded = decoded_text.lower()
        for word in dictionary:
            if word in lower_decoded:
                print(f'\n[알림] 사전에 등록된 키워드 \'{word}\'가 발견되었습니다!')
                print('의미 있는 문장으로 판단하여 반복을 멈춥니다.')
                return  # 함수 종료를 통해 반복문을 빠져나감

def main():
    target_text = ''
    
    # [수행과제 1] password.txt 파일을 읽어온다.
    try:
        with open('password.txt', 'r', encoding='utf-8') as file:
            target_text = file.read().strip()
    except FileNotFoundError:
        print('오류: \'password.txt\' 파일을 찾을 수 없습니다.')
        return
    except Exception as e:
        print(f'파일을 읽어오는 중 오류가 발생했습니다: {e}')
        return

    if not target_text:
        print('오류: 파일에 해독할 내용이 없습니다.')
        return

    print('--- 카이사르 암호 해독 시작 ---\n')
    
    # [수행과제 3] caesar_cipher_decode() 함수는 풀어야 하는 문자열을 파라메터로 추가한다. 이때 파라메터의 이름은 target_text으로 한다.
    caesar_cipher_decode(target_text)
    
    # [수행과제 6] 몇 번째 자리수로 암호가 해독되는지 찾아낸다. 눈으로 식별이 가능하면 해당 번호를 입력하면 그 결과를 result.txt로 저장을 한다.
    print('\n눈으로 확인하여 암호가 해독된 번호(Shift)를 입력해 주세요.')
    try:
        user_input = input('해독된 번호 입력: ')
        choice_shift = int(user_input)
        
        # 입력한 번호로 다시 한 번 정확히 해독하여 저장할 텍스트 생성
        final_text = ''
        for char in target_text:
            if 'a' <= char <= 'z':
                shifted = ord(char) - choice_shift
                if shifted < ord('a'):
                    shifted += 26
                final_text += chr(shifted)
            elif 'A' <= char <= 'Z':
                shifted = ord(char) - choice_shift
                if shifted < ord('A'):
                    shifted += 26
                final_text += chr(shifted)
            else:
                final_text += char
                
        # 결과를 result.txt로 저장 (파일 예외처리 포함)
        with open('result.txt', 'w', encoding='utf-8') as file:
            file.write(final_text)
            
        print(f'성공: 해독된 문장이 \'result.txt\' 파일로 저장되었습니다. (해독 번호: {choice_shift})')
        
    except ValueError:
        print('오류: 숫자만 입력해야 합니다.')
    except Exception as e:
        print(f'파일을 저장하는 중 오류가 발생했습니다: {e}')

# 프로그램 실행 시작점
if __name__ == '__main__':
    main()