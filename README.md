# teleconomy

## 소개
실시간 경제지표 발표를 자동으로 크롤링하고, 새로운 발표가 감지되면 텔레그램으로 알림을 보내주는 Python 자동화 시스템입니다.

## 주요 기능
- TradingEconomics 캘린더에서 경제지표를 주기적으로 크롤링
- 발표치가 새로 등록된 지표만 감지하여 알림
- 발표 1분 전 ~ 2분 후까지 30초 간격으로 집중 크롤링/알림
- 텔레그램 봇을 통한 실시간 알림 전송

## 폴더/파일 구조

```
├── CalendarCrawler.py   # 경제지표 캘린더 크롤러
├── EconomicCalendar.py  # 데이터 비교 및 신규 발표 감지
├── Timer.py             # 타겟 시간 기반 타이머/스케줄러
├── message.py           # 알림 메시지 포맷 변환
├── telegram.py          # 텔레그램 메시지 전송
├── main.py              # 전체 자동화 진입점
├── ec.py                # 예시/테스트 스크립트
├── Test/                # 테스트 코드
└── README.md
```

## 사용법
1. Python 3.10 이상 환경에서 필요한 패키지 설치
   ```bash
   pip install -r requirements.txt
   ```
2. 텔레그램 봇 토큰과 채팅 ID를 환경변수로 지정하거나 main.py에 직접 입력
   - `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`
3. main.py 실행
   ```bash
   python main.py
   ```
4. CLI에서 다음 타겟 발표시간, 대기 시간, 알림 구간이 출력됨

## 환경 변수 예시
```
export TELEGRAM_BOT_TOKEN=여러분의_텔레그램_봇_토큰
export TELEGRAM_CHAT_ID=여러분의_채팅_ID
```

## 동작 원리
- 최초 실행 시, 앞으로 발표될 경제지표 중 가장 빠른 KST_DATETIME을 타겟으로 설정
- 해당 시간 1분 전~2분 후까지 30초 간격으로 크롤링 및 알림
- 알림 루프가 끝나면 다음 타겟 발표시간을 자동 추적하여 반복

## 참고/문의
- TradingEconomics 캘린더: https://tradingeconomics.com/calendar
- 문의: 깃허브 이슈 또는 개발자에게 직접 연락