import pandas as pd
import pytz
from datetime import datetime


class EconomicCalendarData:
    def __init__(self, df: pd.DataFrame):
        """
        발표치가 비어있지 않고, 현재 시각 이전(KST)인 지표만 필터링하여 저장
        """
        self.df = self._filter_valid_entries(df)

    @staticmethod
    def _filter_valid_entries(df: pd.DataFrame) -> pd.DataFrame:
        # 발표치 비어있지 않음
        df = df[df['발표치'].notna() & (df['발표치'].str.strip() != "")]

        # 시점 필터링: 현재 시각 이전(KST)
        now_kst = pd.Timestamp.now(tz='Asia/Seoul')
        kst_col = pd.to_datetime(df['KST_DATETIME'], errors='coerce')
        kst_col = kst_col.dt.tz_localize('Asia/Seoul', nonexistent='NaT', ambiguous='NaT')
        df = df[kst_col <= now_kst]

        return df.reset_index(drop=True)

    def compare_and_alert(self, new_df: pd.DataFrame) -> pd.DataFrame:
        """
        새로운 데이터 중 기존에 없던 발표치가 채워진 항목만 반환
        """
        new_filtered = self._filter_valid_entries(new_df)

        combined = pd.merge(
            new_filtered,
            self.df,
            on=["시간", "국가", "국가코드", "지표명", "레퍼런스"],
            how="left",
            indicator=True
        )

        new_alerts = combined[combined["_merge"] == "left_only"]
        return new_alerts.drop(columns=["_merge"]).reset_index(drop=True)
