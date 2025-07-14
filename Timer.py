import threading
import time
import datetime
import pytz


def timer_loop(interval_sec, target_func, *args, **kwargs):
    """
    interval_sec(초)마다 target_func를 별도 스레드로 반복 실행

    예시: timer_loop(60, my_function, arg1, arg2)
    """
    def loop():
        while True:
            try:
                target_func(*args, **kwargs)
            except Exception as e:
                print(f"[ERROR] timer_loop: 함수 실행 중 예외 발생: {e}")
            time.sleep(interval_sec)

    t = threading.Thread(target=loop, daemon=True)
    t.start()


def timer_until_window(target_dt, target_func, *args, **kwargs):
    """
    지정된 타겟 시간의 -1분 ~ +2분 동안 30초 간격으로 target_func를 동기적으로 실행

    Args:
        target_dt (datetime.datetime): Asia/Seoul 타임존의 tz-aware datetime
        target_func (callable): 실행할 함수
        *args, **kwargs: 함수 인자
    """

    # ==== 유효성 검사 ====
    if not isinstance(target_dt, datetime.datetime):
        raise TypeError("target_dt는 datetime.datetime 타입이어야 합니다.")
    if target_dt.tzinfo is None or target_dt.tzinfo.zone != 'Asia/Seoul':
        raise ValueError("target_dt는 Asia/Seoul 타임존이 적용된 tz-aware datetime이어야 합니다.")

    # ==== 현재 시간 함수 ====
    def now_kst():
        return datetime.datetime.now(pytz.timezone('Asia/Seoul'))

    # ==== 타이머 범위 설정 ====
    start_time = target_dt - datetime.timedelta(minutes=1)
    end_time = target_dt + datetime.timedelta(minutes=2)

    print(f"[TIMER] 대기 시작: 타겟 시간 {target_dt} 기준, {start_time} ~ {end_time} 구간 모니터링 예정")

    # ==== 시작 전 대기 ====
    while now_kst() < start_time:
        remain = int((start_time - now_kst()).total_seconds())
        if remain % 10 == 0:
            print(f"[TIMER] 타겟 시간까지 {remain}초 남음")
        time.sleep(min(5, remain))

    print(f"[TIMER] 타겟 1분 전 도달: 집중 실행 시작")

    # ==== 집중 실행 구간 ====
    while now_kst() <= end_time:
        try:
            print(f"[TIMER] {now_kst()} - 함수 실행 시작")
            target_func(*args, **kwargs)
        except Exception as e:
            print(f"[ERROR] timer_until_window: 함수 실행 중 예외 발생: {e}")
        time.sleep(30)

    print(f"[TIMER] 타겟 2분 후 도달: 집중 실행 종료")
