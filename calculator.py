import sys
# 라이브러리 임포트 에러 방지
try:
    from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QLineEdit, QPushButton
    from PyQt5.QtCore import Qt
except ImportError:
    print('[ERROR] PyQt5 라이브러리가 설치되어 있지 않습니다.')
    print('터미널(또는 명령 프롬프트)에서 다음 명령어를 실행해주세요: pip install PyQt5')
    sys.exit(1)    # 프로그램 안전 종료

class Calculator(QMainWindow):
    # 메인 창 (QMainWindow) 의 기능을 물려받아 계산기 클래스 만들기
    def __init__(self):
        super().__init__()
        try:
            self.init_ui()
        except Exception as e:
            print(f'[GRAPHIC ERROR] 화면을 그리는 중 문제가 발생했습니다: {e}')
            sys.exit(1)

    def init_ui(self):
        self.setWindowTitle('Calculator')
        # 창 크기 설정
        self.setFixedSize(300, 450)

        # 메인 위젯 및 레이아웃 설정
        main_widget = QWidget()    
        self.setCentralWidget(main_widget)
        vbox = QVBoxLayout()        # 수직으로 요소 배치하는 레이아웃
        main_widget.setLayout(vbox) # 사용자가 타이핑 하는 것이 아닌 버튼으로 입력되게 설정

        # 텍스트 출력창 (Display)
        self.display = QLineEdit('0')
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight) # 숫자 우측 정렬
        self.display.setFixedHeight(80) 
        self.display.setStyleSheet('font-size: 40px;') 
        vbox.addWidget(self.display)

        # 버튼 배치를 위한 그리드 레이아웃
        grid = QGridLayout()
        vbox.addLayout(grid)

        # 아이폰 계산기 배열과 동일한 버튼 구성 (텍스트, 행, 열, [행 병합, 열 병합])
        buttons = [
            ('AC', 0, 0), ('+/-', 0, 1), ('%', 0, 2), ('/', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('*', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
            ('0', 4, 0, 1, 2), ('.', 4, 2), ('=', 4, 3)
        ]

        # 버튼 생성 및 그리드에 추가
        try:
            for btn_data in buttons:
                text = btn_data[0]
                button = QPushButton(text)
                button.setMinimumHeight(60)
                button.setStyleSheet('font-size: 20px;')

                if len(btn_data) == 3:
                    grid.addWidget(button, btn_data[1], btn_data[2])
                else:
                    grid.addWidget(button, btn_data[1], btn_data[2], btn_data[3], btn_data[4])

                button.clicked.connect(self.button_clicked)
        except Exception as e:
            print(f'[GRAPHIC ERROR] 버튼을 배치하는 중 문제가 발생했습니다: {e}')

    def button_clicked(self):
        try:
            button = self.sender()  # 방금 클릭 된 버튼의 정보 확인
            text = button.text()    # 버튼의 텍스트 가져옴
            current_text = self.display.text() # 출력창 표시 텍스트 가져옴
        except AttributeError:
            # sender()가 버튼 객체가 아닐 경우 발생하는 사소한 오류 방지
            return

        # 초기화 버튼
        if text == 'AC':
            self.display.setText('0')
            
        # 보너스 과제: 결과 출력 버튼 (4칙 연산 실행)
        elif text == '=':
            try:
                # 파이썬 내장 eval()을 활용하여 문자열 수식을 계산
                result = str(eval(current_text))
                self.display.setText(result)
            except ZeroDivisionError:
                self.display.setText('Error')
            except SyntaxError:
                # '1++' 등 수식 문법이 틀렸을 때
                self.display.setText('Error')
            except Exception:
                self.display.setText('Error')
                print(f'[ERROR] {e}')
                
        # 양수/음수 전환 버튼
        elif text == '+/-':
            try:
                if current_text != '0' and current_text != 'Error':
                    if current_text[0] == '-':
                        self.display.setText(current_text[1:])
                    else:
                        self.display.setText('-' + current_text)
            except IndexError:
                # 문자열 인덱스 접근 시 발생할 수 있는 에러 방지
                pass
                    
        # 백분율 버튼
        elif text == '%':
            if current_text != 'Error':
                try:
                    result = str(eval(current_text) / 100)
                    self.display.setText(result)
                except Exception as e:
                    self.display.setText('Error')
                    print(f'[ERROR] {e}')
                    
        # 일반 숫자 및 연산자 입력
        else:
            try:
                if current_text == '0' or current_text == 'Error':
                    self.display.setText(text)
                else:
                    self.display.setText(current_text + text)
            except Exception as e:
                print(f'[ERROR] {e}')


if __name__ == '__main__':
    # 5. 애플리케이션 실행 에러 방지
    try:
        app = QApplication(sys.argv)    # PyQt 프로그램을 실행하기 위한 핵심 애플리케이션 객체 만들기
        calc = Calculator()             
        calc.show()                     # 계산기 객체를 메모리에 올리고 화면에 보여줌
        sys.exit(app.exec_())           
    except Exception as e:
        print(f'[RUNNING ERROR] 프로그램을 실행하거나 유지하는 중 문제가 발생했습니다: {e}')