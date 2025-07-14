import pandas as pd

class EconomicCalendarData:
    def __init__(self, df: pd.DataFrame):
        # 초기화 시 발표치가 비어있지 않은 행만 저장
        self.df = self._filter_non_empty_actual(df)

    @staticmethod
    def _filter_non_empty_actual(df: pd.DataFrame) -> pd.DataFrame:
        return df[df['발표치'].notna() & (df['발표치'].str.strip() != "")].reset_index(drop=True)

    def compare_and_alert(self, new_df: pd.DataFrame) -> pd.DataFrame:
        # 새로 받은 데이터에서 발표치가 비어있지 않은 행만 필터링
        new_filtered = self._filter_non_empty_actual(new_df)

        # 기존 데이터와 새로운 데이터를 병합해서 기존에 없던 항목만 찾기
        combined = pd.merge(
            new_filtered,
            self.df,
            on=["시간", "국가", "국가코드", "지표명", "레퍼런스"],
            how="left",
            indicator=True
        )

        # 새롭게 추가된 항목만 필터링
        new_alerts = combined[combined["_merge"] == "left_only"]
        return new_alerts.drop(columns=["_merge"]).reset_index(drop=True)

# 사용 예시:
# 기존 데이터와 새 데이터가 있다고 가정하고, 클래스 생성 및 비교
# ec = EconomicCalendarData(old_df)
# new_alerts = ec.compare_and_alert(new_df)
