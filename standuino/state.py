import datetime
import pytz


def now():
    return datetime.datetime.now(pytz.UTC)


class State:
    def __init__(self, standing, at_desk,
                 id=None, start_time=None, end_time=None):
        self.id = id
        self.standing = standing
        self.at_desk = at_desk
        self.start_time = start_time
        self.end_time = end_time

    def start(self):
        self.start_time = now()

    def end(self):
        self.end_time = now()

    @property
    def description(self):
        if not self.at_desk:
            return "away_from_desk"
        if self.standing:
            return "standing_at_desk"
        return "sitting_at_desk"

    @property
    def duration_secs(self):
        return (self.end_time - self.start_time).seconds

    def json(self):
        """Will format datetimes like: "2015-07-10 14:44:23.088524+00:00"
        """
        return {
            "id": self.id,
            "standing": self.standing,
            "at_desk": self.at_desk,
            "description": self.description,
            "start_time": str(self.start_time),
            "end_time": str(self.end_time),
            "duration_secs": self.duration_secs,
        }
