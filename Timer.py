
import threading
import time


def timer_loop(interval_sec, target_func, *args, **kwargs):
    """
    interval_sec(초)마다 target_func를 반복 실행
    """
    def loop():
        while True:
            target_func(*args, **kwargs)
            time.sleep(interval_sec)
    t = threading.Thread(target=loop, daemon=True)
    t.start()

def timer_until_window(target_dt, target_func, *args, **kwargs):
    """
    target_dt(타겟 datetime) 기준, 1분 전~2분 후까지 30초 간격으로 target_func 실행
    """
    def loop():
        now = time.time()
        start = target_dt.timestamp() - 60  # 1분 전
        end = target_dt.timestamp() + 120  # 2분 후
        last_debug = 0
        while time.time() < start:
            remain = int(start - time.time())
            # 10초마다 남은 시간 출력
            if remain // 10 != last_debug:
                print(f"[TIMER] 타겟 시간 1분 전까지 {remain}초 남음 (타겟: {target_dt})")
                last_debug = remain // 10
            time.sleep(min(5, start - time.time()))  # 대기(짧게 polling)
        print(f"[TIMER] 타겟 시간 1분 전 도달! 집중 크롤링 시작 (타겟: {target_dt})")
        while time.time() <= end:
            target_func(*args, **kwargs)
            time.sleep(30)
    t = threading.Thread(target=loop, daemon=True)
    t.start()
