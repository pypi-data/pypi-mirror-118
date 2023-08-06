from durations import Duration


class Interval(Duration):

    def __init__(self, repr: str, *args, **kwargs):
        super().__init__(repr, *args, **kwargs)

    @staticmethod
    def of_seconds(seconds: int):
        return Interval(str(seconds) + 's')

    @staticmethod
    def of_minutes(minutes: int):
        return Interval.of_seconds(minutes * 60)

    @staticmethod
    def of_hours(hours: int):
        return Interval.of_seconds(hours * 60 * 60)

    @staticmethod
    def of_days(days: int):
        return Interval.of_seconds(days * 60 * 60 * 24)
