# DB Requests package

from backend.app.data.db_requests.users import user_requests
from backend.app.data.db_requests.students import student_requests
from backend.app.data.db_requests.teachers import teacher_requests
from backend.app.data.db_requests.instruments import instrument_requests
from backend.app.data.db_requests.schedule import schedule_requests

__all__ = [
    "user_requests",
    "student_requests",
    "teacher_requests",
    "instrument_requests",
    "schedule_requests",
]
