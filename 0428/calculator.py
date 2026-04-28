import sys

try:
    from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QLineEdit, QPushButton
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QFontMetrics, QFont
# [제약조건] UI를 다루는 PyQt는 사용 가능
except ImportError:
    print('[ERROR] PyQt5 라이브러리가 설치되어 있지 않습니다.')
    print('터미널(또는 명령 프롬프트)에서 다음 명령어를 실행해주세요: pip install PyQt5')
    sys.exit(1)

# [수행과제 1] Calculator 클래스를 만든다.
class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        # 계산기의 상태를 추적하기 위한 변수 (eval()을 쓰지 않고 직접 구현하기 위함)
        self.current_num = '0'       # 화면에 표시되는 현재 숫자
        self.previous_num = None     # 연산자가 눌리기 전의 숫자
        self.operator = None         # 현재 선택된 연산자
        self.waiting_for_new = False # 새로운 숫자 입력 대기 상태
        
        try:
            self.init_ui()
        except Exception as e:
            print(f'[GRAPHIC ERROR] 화면을 그리는 중 문제가 발생했습니다: {e}')
            sys.exit(1)

    def init_ui(self):
        self.setWindowTitle('Calculator')
        self.setFixedSize(300, 450)

        main_widget = QWidget()    
        self.setCentralWidget(main_widget)
        vbox = QVBoxLayout()
        main_widget.setLayout(vbox)

        # 텍스트 출력창 (Display)
        self.display = QLineEdit('0')
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFixedHeight(80) 
        self.display.setStyleSheet('font-size: 40px;') 
        vbox.addWidget(self.display)

        grid = QGridLayout()
        vbox.addLayout(grid)

        # 계산기 배열
        buttons = [
            ('AC', 0, 0), ('+/-', 0, 1), ('%', 0, 2), ('/', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('*', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
            ('0', 4, 0, 1, 2), ('.', 4, 2), ('=', 4, 3)
        ]

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

                # [수행과제 7] UI의 각 버튼과 Calculator 클래스를 연결해서 완전한 동작을 구현한다.
                button.clicked.connect(self.button_clicked)
        except Exception as e:
            print(f'[GRAPHIC ERROR] 버튼을 배치하는 중 문제가 발생했습니다: {e}')

    # ---------------------------------------------------------
    # [수행과제 2] 사칙 연산을 담당할 메소드인 add(), subtract(), multiply(), divide() 를 추가하고 기능 구현
    # ---------------------------------------------------------
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        # [제약조건] 수학에서 발생할 수 있는 예외 적용 - 0을 나누면 안된다.
        if b == 0:
            raise ZeroDivisionError('0으로 나눌 수 없습니다.')
        return a / b


    # ---------------------------------------------------------
    # [수행과제 3] 초기화, 음수양수, 퍼센트를 담당할 reset(), negative_positive(), percent() 메소드 추가 및 기능 구현
    # ---------------------------------------------------------
    def reset(self):
        # 화면과 내부 상태를 모두 초기 상태로 돌림
        self.current_num = '0'
        self.previous_num = None
        self.operator = None
        self.waiting_for_new = False
        self.update_display()

    def negative_positive(self):
        if self.current_num == '0' or self.current_num == 'Error':
            return
        
        # 음수면 양수로, 양수면 음수로 기호 전환
        if self.current_num.startswith('-'):
            self.current_num = self.current_num[1:]
        else:
            self.current_num = '-' + self.current_num
        self.update_display()

    def percent(self):
        if self.current_num == 'Error':
            return
        try:
            # 현재 숫자를 100으로 나눔
            val = float(self.current_num)
            # [보너스과제 2] 소수점 6자리 이하 반올림
            result = round(val / 100, 6)

            if result.is_integer():
                self.current_num = str(int(result))
            else:
                self.current_num = str(result)
            self.update_display()
        except Exception:
            self.current_num = 'Error'
            self.update_display()


    # ---------------------------------------------------------
    # [수행과제 6] 결과를 출력할 equal() 메소드를 추가하고 기능을 구현한다.
    # ---------------------------------------------------------
    def equal(self):
        if not self.operator or self.previous_num is None:
            return
        
        try:
            a = float(self.previous_num)
            b = float(self.current_num)
            result = 0

            # 저장된 연산자에 따라 알맞은 사칙연산 메소드 호출
            if self.operator == '+':
                result = self.add(a, b)
            elif self.operator == '-':
                result = self.subtract(a, b)
            elif self.operator == '*':
                result = self.multiply(a, b)
            elif self.operator == '/':
                result = self.divide(a, b)

            # [제약조건] 처리 할 수 있는 숫자의 범위가 넘어가면 예외 처리 적용
            if result > 1e100 or result < -1e100:
                raise OverflowError('범위 초과')

            # [보너스 과제 2] 소수점 6자리 이하의 경우 반올림한 결과로 줄여서 출력한다.
            result = round(result, 6)

            # 파이썬 특성상 정수라도 1.0 처럼 표시될 수 있으므로, 정수일 경우 소수점 제거
            if result.is_integer():
                self.current_num = str(int(result))
            else:
                self.current_num = str(result)
            
            # 계산 완료 후 상태 초기화 (결과는 화면에 남김)
            self.operator = None
            self.previous_num = None
            self.waiting_for_new = True
            self.update_display()

        except ZeroDivisionError:
            self.current_num = 'Error'
            self.operator = None
            self.previous_num = None
            self.waiting_for_new = True
            self.update_display()
        except OverflowError:
            self.current_num = 'Error'
            self.operator = None
            self.previous_num = None
            self.waiting_for_new = True
            self.update_display()
        except Exception:
            self.current_num = 'Error'
            self.update_display()

    def update_display(self):
        # [보너스 과제 1] 출력되는 값의 길이에 따라서 폰트의 크기를 동적으로 조정
        text = self.current_num
        
        # 1. 폰트 최대/최소 크기 설정
        max_font_size = 40
        min_font_size = 15
        font_size = max_font_size
        
        # 2. 너비 계산을 위한 임시 폰트 객체 생성
        font = self.display.font()
        font.setPixelSize(font_size)
        
        # 3. 텍스트가 표시될 위젯(QLineEdit)의 실제 가용 너비 (좌우 여백 20px 정도 뺌)
        available_width = self.display.width() - 20
        
        # 프로그램이 처음 실행되어 화면이 렌더링되기 전에는 width가 0일 수 있으므로 예외 처리
        if available_width <= 0:
            available_width = 260 
            
        fm = QFontMetrics(font)
        
        # 4. 글자의 실제 픽셀 너비가 가용 너비보다 크다면, 폰트를 1px씩 줄이면서 반복 계산
        while fm.boundingRect(text).width() > available_width and font_size > min_font_size:
            font_size -= 1
            font.setPixelSize(font_size)
            fm = QFontMetrics(font)
            
        # 5. 최종 결정된 폰트 크기를 반영하고 텍스트 출력
        self.display.setStyleSheet(f'font-size: {font_size}px;')
        self.display.setText(text)

    # 버튼 클릭 이벤트를 각 기능으로 분기해주는 라우터 역할
    def button_clicked(self):
        try:
            button = self.sender()
            text = button.text()
        except AttributeError:
            return

        if text == 'AC':
            self.reset()
        elif text == '+/-':
            self.negative_positive()
        elif text == '%':
            self.percent()
        elif text == '=':
            self.equal()
        elif text in ['+', '-', '*', '/']:
            # 연속해서 연산자를 누를 경우 (=을 누르지 않아도) 중간 계산 처리
            if self.operator and not self.waiting_for_new:
                self.equal()
            self.operator = text
            self.previous_num = self.current_num
            self.waiting_for_new = True
        else:
            if self.current_num == 'Error':
                self.current_num = '0'

            # [수행과제 5] 소수점 키를 누르면 소수점이 입력된다. 단 이미 소수점이 입력되어 있는 상태에서는 추가로 입력되지 않는다.
            if text == '.':
                if self.waiting_for_new:
                    self.current_num = '0.'
                    self.waiting_for_new = False
                elif '.' not in self.current_num:  # 이미 소수점이 있는지 검사
                    self.current_num += '.'
            # [수행과제 4] 숫자키를 누를 때 마다 화면에 숫자가 누적된다.
            else:
                if self.waiting_for_new or self.current_num == '0':
                    self.current_num = text
                    self.waiting_for_new = False
                else:
                    self.current_num += text # 문자열 더하기를 통해 숫자 누적
            
            self.update_display()

if __name__ == '__main__':
    # 경고 메시지 없이 모든 코드는 실행 되어야 함
    try:
        app = QApplication(sys.argv)
        calc = Calculator()             
        calc.show()                     
        sys.exit(app.exec_())           
    except Exception as e:
        print(f'[RUNNING ERROR] 프로그램을 실행하거나 유지하는 중 문제가 발생했습니다: {e}')
