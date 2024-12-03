from fastapi import FastAPI, Query
from datetime import datetime, timedelta

app = FastAPI()

class DateInfo:
    def __init__(self, year: int, month: int, day: int):
        self.date = datetime(year, month, day)
        self.year = year
        self.month = month
        self.day = day

    def get_quarter(self) -> int:
        """获取季度"""
        return (self.month - 1) // 3 + 1

    def get_day_of_year(self) -> int:
        """获取在年的第几天"""
        return (self.date - datetime(self.year, 1, 1)).days + 1

    def get_week_of_year(self) -> int:
        """获取在年的第几周"""
        return self.date.isocalendar()[1]

    def get_week_of_month(self) -> int:
        """获取在月的第几周"""
        first_day_of_month = datetime(self.year, self.month, 1)
        return ((self.date - first_day_of_month).days // 7) + 1

    def get_year_progress(self) -> float:
        """获取当前日期过了年的多少（小数）"""
        year_start = datetime(self.year, 1, 1)
        next_year_start = datetime(self.year + 1, 1, 1)
        year_length = (next_year_start - year_start).total_seconds()
        elapsed = (self.date - year_start).total_seconds()
        return elapsed / year_length

    def get_day_of_week(self) -> str:
        """获取星期几"""
        weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        return self.date.weekday()
        return weekdays[self.date.weekday()]

    def calculate(self) -> dict:
        """计算所有日期相关信息"""
        quarter = self.get_quarter()
        day_of_year = self.get_day_of_year()
        week_of_year = self.get_week_of_year()
        week_of_month = self.get_week_of_month()
        year_progress = self.get_year_progress()
        day_of_week = self.get_day_of_week()

        return {
            "year": self.year,
            "month": self.month,
            "day": self.day,
            "quarter": quarter,
            "day_of_year": day_of_year,
            "week_of_year": week_of_year,
            "week_of_month": week_of_month,
            "year_progress": round(year_progress, 4),  # 保留四位小数
            "day_of_week_index": day_of_week
        }

@app.get("/date_info")
def date_info(
    year: int = Query(None),
    month: int = Query(None),
    day: int = Query(None)
):
    # 如果参数缺失，使用当前日期
    if not year or not month or not day:
        now = datetime.now()
        year, month, day = now.year, now.month, now.day

    date_info = DateInfo(year, month, day)
    return date_info.calculate()
