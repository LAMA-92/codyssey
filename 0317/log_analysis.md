# 화성 기지 사고 원인 분석 보고서

## 1. 분석 상황

- **기록자:** 한송이 박사
- **분석 데이터:** mission_computer_main.log
- **도구:** 미션 컴퓨터 Python 인터프리터

## 2. 사고 발생 타임라인

- 2023-08-27 **12:00:00**,INFO,Center and mission control systems powered down.
- 2023-08-27 **11:40:00**,INFO,Oxygen tank explosion.
- 2023-08-27 **11:35:00**,INFO,Oxygen tank unstable.
- 2023-08-27 **11:30:00**,INFO,Mission completed successfully. Recovery team dispatched.
- 2023-08-27 **11:28:00**,INFO,Touchdown confirmed. Rocket safely landed.

## 3. 로그 분석

로그의 타임라인상 폭발은 **착륙 완료(11:28) 및 미션 성공 선언(11:30)** 이후 10분 이내에 발생하였다. 로켓은 아무 문제 없이 안전하게 착륙했다. 하지만 착륙 직후에 **산소탱크가 불안정(11:35)** 해지기 시작했고, 5분 후 폭발했다.

## 4. 사고 발생 원인 결론

결론적으로 해당 사고는 비행 과정에서의 결함이 아닌, 착륙 후 발생한 지상 사고이다.
