def inventory_danger(file_path):
    try:
        # [수행과제 1] 파일 읽기 및 출력
        print('---[정보] 원본 재고 리스트 출력 ---')
        with open(file_path, 'r', encoding='utf-8') as input_file:
            content = input_file.read()
            print(content)
            
        # [수행과제 2] 파일 리스트 객체로 변환
        inven_list = []
        lines = content.strip().split('\n')     # 공백 제거 및 줄바꿈
        header = lines[0]                       # 제목 부분 분리

        for line in lines[1:]:
            parts = line.split(',')             # ',' 를 기준으로 라인 나누기
            if len(parts) == 5:
                name = parts[0]
                try:
                    flame_val = float(parts[4])
                    inven_list.append([name, flame_val])
                except ValueError:              # 숫자로 변환 불가능한 데이터는 제외           
                    continue

        # [수행과제 3] 인화성 높은 순 정렬
        inven_list.sort(key=lambda x: x[1], reverse=True)

        # [수행과제 4] 인화성 지수 0.7 이상 출력
        print('\n---[정보] 위험 물질 리스트 (인화성 0.7 이상) ---')
        danger_list = []
        for item in inven_list:
            if item[1] >= 0.7:
                danger_list.append(item)
                print(f'위험 물질: {item[0]}, 지수: {item[1]}')

        # [수행과제 5] 위험 목록 CSV 저장
        with open('Mars_Base_Inventory_danger.csv', 'w', encoding='utf-8') as csv_output:
            csv_output.write('위험 물질,지수\n')
            for item in danger_list:
                csv_output.write(f'{item[0]},{item[1]}\n')

        # [보너스 1] 이진 파일(.bin)로 저장
        with open('Mars_Base_Inventory_List.bin', 'wb') as binary_file:         # 파일을 이진 파일 형태로 생성
            for item in inven_list:
                data_line = f'{item[0]}:{item[1]}\n'.encode('utf-8')            # 데이터를 '이름:지수\n' 형태의 바이트로 변환
                binary_file.write(data_line)
        print('\n[정보] Mars_Base_Inventory_List.bin 저장 완료.')

        # [보너스 2] 이진 파일 내용을 다시 읽어 들여서 화면에 출력
        print('\n--- [정보] 이진 파일 로드 결과 ---')
        with open('Mars_Base_Inventory_List.bin', 'rb') as binary_output:
            binary_data = binary_output.read()                                    
            decoded_text = binary_data.decode('utf-8')                          # 바이트를 다시 문자열로 디코딩
            print(decoded_text)

    except FileNotFoundError:
        print('[에러] Code 404: Mars_Base_Inventory_List.csv 파일이 없습니다.')
    except PermissionError:
        print('[에러] Code 403: 파일 접근 권한이 없습니다.')
    except UnicodeDecodeError:
        print('[에러] Code 500: 파일 인코딩 형식이 맞지 않습니다.')
    except Exception as e:
        print(f'[에러] 치명적 시스템 오류 발생: {e}')

if __name__ == '__main__':
    file = 'Mars_Base_Inventory_List.csv'
    inventory_danger(file)
